"""VLM evaluation harness (stages 2, 4, 5, 7).

One process = one model load = one run directory under runs/<run-id>/ with:
  config.json        — full measurement conditions (model, quant, prompt, n, warmup, resolution, host)
  predictions.jsonl  — per-image raw output, parsed label, latency
  metrics.json       — accuracy, per-class, confusion, parse-fail, latency p50/p95, memory

All accuracy numbers are computed on the frozen eval set only (data/frozen_eval).
Latency caveat: measured on Apple M4 Max — NOT representative of automotive
SoC latency. Relative comparisons between sizes/quantizations are the point.

Modes:
  zeroshot   — single frame, prompt p1/p2/p3
  fewshot    — 10 or 20 class-labeled example images (from non-eval subjects) + query
  multiframe — N consecutive frames from the same subject/class window
  fusion     — single frame + SYNTHETIC heart-rate text context (NOT real data)
"""
import argparse
import csv
import json
import platform
import random
import statistics
import time
from collections import defaultdict
from pathlib import Path

import mlx.core as mx
from mlx_vlm import generate, load
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config

from common import CLASS_IDS, PROMPTS, parse_prediction, prompt_fusion, prompt_multiframe

WARMUP = 3


def model_disk_bytes(model_id: str) -> int:
    if Path(model_id).is_dir():
        p = Path(model_id)
    else:
        from huggingface_hub import snapshot_download
        p = Path(snapshot_download(model_id, local_files_only=True))
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file())


def load_manifest(eval_dir: Path):
    with open(eval_dir / "manifest.csv") as f:
        return list(csv.DictReader(f))


def prep_fewshot_images(eval_dir: Path, data_root: Path, per_class: int, scratch: Path,
                        max_side: int = 224):
    """Return (paths, class order). Examples resized to max side 224: with
    ~2.5k+ prompt tokens of image content the MLX stack degenerates (see
    runs/logs/multiimage_collapse_repro.md), so example token cost is bounded."""
    from PIL import Image
    with open(eval_dir / "fewshot_manifest.csv") as f:
        rows = list(csv.DictReader(f))
    scratch.mkdir(parents=True, exist_ok=True)
    paths, order = [], []
    by_cls = defaultdict(list)
    for r in rows:
        by_cls[r["classname"]].append(r)
    for cls in CLASS_IDS:
        for r in by_cls[cls][:per_class]:
            src = data_root / r["relpath"]
            dst = scratch / f"{cls}_{r['img']}"
            if not dst.exists():
                im = Image.open(src)
                im.thumbnail((max_side, max_side))
                im.save(dst, quality=90)
            paths.append(str(dst))
            order.append(cls)
    return paths, order


def build_fewshot_messages(order, base_prompt: str):
    """Interleaved image-label few-shot as a single user turn (native
    processor chat template; one {"type":"image"} slot per image)."""
    content = [{"type": "text", "text": "Labeled examples of driver states:"}]
    for cid in order:
        content.append({"type": "image"})
        content.append({"type": "text", "text": f"class_id={cid}"})
    content.append({"type": "text", "text": "\nNow classify this query image:"})
    content.append({"type": "image"})
    content.append({"type": "text", "text": base_prompt})
    return [{"role": "user", "content": content}]


def resize_frames(paths, scratch: Path, max_side: int = 448):
    """Uniformly downsize multiframe inputs (all of mf2/4/8) to max side 448 —
    8 native-res frames exceed the MLX stack's stable multi-image budget."""
    from PIL import Image
    scratch.mkdir(parents=True, exist_ok=True)
    out = []
    for p in paths:
        p = Path(p)
        dst = scratch / f"{p.parent.name}_{p.name}"
        if not dst.exists():
            im = Image.open(p)
            im.thumbnail((max_side, max_side))
            im.save(dst, quality=90)
        out.append(str(dst))
    return out


def synth_hr(img: str, mode: str, seed: int = 20260725) -> int:
    """SYNTHETIC heart rate for fusion experiments — not a real measurement."""
    rng = random.Random(f"{seed}:{img}:{mode}")
    lo, hi = {"low": (48, 60), "normal": (65, 85), "high": (98, 128)}[mode]
    return rng.randint(lo, hi)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--adapter-path", default=None,
                    help="LoRA adapter dir (task B fine-tuning)")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--mode", default="zeroshot",
                    choices=["zeroshot", "fewshot", "multiframe", "fusion", "describe"])
    ap.add_argument("--prompt", default="p1", choices=["p1", "p2", "p3"])
    ap.add_argument("--frames", type=int, default=1)
    ap.add_argument("--fewshot-per-class", type=int, default=1)
    ap.add_argument("--fusion-hr", default="normal", choices=["low", "normal", "high"])
    ap.add_argument("--limit", type=int, default=0, help="0 = full frozen set")
    ap.add_argument("--eval-dir", default="data/frozen_eval")
    ap.add_argument("--max-tokens", type=int, default=96)
    ap.add_argument("--runs-dir", default="runs")
    args = ap.parse_args()

    eval_dir = Path(args.eval_dir)
    split = json.loads((eval_dir / "split.json").read_text())
    data_root = Path(split["data_root"])
    manifest = load_manifest(eval_dir)
    if args.limit:
        manifest = manifest[: args.limit]

    run_dir = Path(args.runs_dir) / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"[{args.run_id}] loading {args.model} adapter={args.adapter_path}", flush=True)
    t0 = time.perf_counter()
    model, processor = load(args.model, adapter_path=args.adapter_path)
    config = load_config(args.model)
    load_s = time.perf_counter() - t0
    mx.reset_peak_memory()
    weights_gb = mx.get_active_memory() / 1e9
    print(f"loaded in {load_s:.1f}s, weights resident {weights_gb:.2f} GB", flush=True)

    fewshot_paths, fewshot_order = [], []
    if args.mode == "fewshot":
        fewshot_paths, fewshot_order = prep_fewshot_images(
            eval_dir, data_root, args.fewshot_per_class,
            Path(args.runs_dir) / "_fewshot_224")

    frames_map = None
    if args.mode == "multiframe":
        frames_map = json.loads((eval_dir / "frames_map.json").read_text())

    cfg = {
        "run_id": args.run_id, "model": args.model,
        "adapter_path": args.adapter_path, "mode": args.mode,
        "prompt": args.prompt, "frames": args.frames,
        "fewshot_per_class": args.fewshot_per_class if args.mode == "fewshot" else 0,
        "fusion_hr": args.fusion_hr if args.mode == "fusion" else None,
        "n_eval": len(manifest), "warmup": WARMUP,
        "max_tokens": args.max_tokens, "temperature": 0.0,
        "image_resolution": {
            "zeroshot": "query native 640x480",
            "fewshot": "examples max-side 224 (interleaved labels), query native",
            "multiframe": "all frames max-side 448 (uniform across mf2/4/8)",
            "fusion": "query native 640x480",
            "describe": "query native 640x480",
        }[args.mode],
        "host": {"machine": "Apple M4 Max 128GB", "platform": platform.platform(),
                 "mlx": mx.__version__},
        "manifest_sha256": split["manifest_sha256"],
        "load_seconds": round(load_s, 2),
        "weights_resident_gb": round(weights_gb, 3),
        "model_disk_gb": round(model_disk_bytes(args.model) / 1e9, 3),
        "latency_note": "Measured on Apple M4 Max; NOT automotive-SoC latency. "
                        "Use only for relative comparison.",
    }
    (run_dir / "config.json").write_text(json.dumps(cfg, indent=2))

    preds_f = open(run_dir / "predictions.jsonl", "w")
    latencies, records = [], []

    for i, row in enumerate(manifest):
        img_path = str(data_root / row["relpath"])

        if args.mode == "zeroshot":
            images = [img_path]
            text = PROMPTS[args.prompt]
        elif args.mode == "describe":
            # open-vocabulary retention probe (B-4): free-form description,
            # no class list, no JSON constraint
            images = [img_path]
            text = ("What is the driver in this in-cabin image doing? "
                    "Describe in one or two sentences.")
        elif args.mode == "fewshot":
            images = fewshot_paths + [img_path]
            text = None  # interleaved messages below
        elif args.mode == "multiframe":
            fm = frames_map[row["img"]]
            native = [str(data_root / p) for p in fm["frames"][: args.frames]]
            images = resize_frames(native, Path(args.runs_dir) / "_frames_448")
            text = prompt_multiframe(len(images))
        elif args.mode == "fusion":
            hr = synth_hr(row["img"], args.fusion_hr)
            images = [img_path]
            text = prompt_fusion(hr)

        if args.mode == "fewshot":
            messages = build_fewshot_messages(fewshot_order, PROMPTS[args.prompt])
            prompt = processor.apply_chat_template(
                messages, add_generation_prompt=True, tokenize=False)
        else:
            prompt = apply_chat_template(processor, config, text, num_images=len(images))
        t1 = time.perf_counter()
        res = generate(model, processor, prompt, image=images,
                       max_tokens=args.max_tokens, temperature=0.0, verbose=False)
        dt = time.perf_counter() - t1

        out_text = res.text if hasattr(res, "text") else str(res)
        cid, pmode, extra = parse_prediction(out_text)
        warm = i < WARMUP
        if not warm:
            latencies.append(dt)
        rec = {
            "img": row["img"], "true": row["classname"], "subject": row["subject"],
            "pred": cid, "parse": pmode, "latency_s": round(dt, 3), "warmup": warm,
            "prompt_tokens": getattr(res, "prompt_tokens", None),
            "gen_tokens": getattr(res, "generation_tokens", None),
            "raw": out_text[:500],
        }
        if args.mode == "fusion":
            rec["hr_bpm"] = hr
            rec["arousal"] = extra.get("arousal")
        records.append(rec)
        preds_f.write(json.dumps(rec) + "\n")
        preds_f.flush()
        if (i + 1) % 25 == 0:
            acc = sum(r["pred"] == r["true"] for r in records) / len(records)
            print(f"  {i + 1}/{len(manifest)} acc so far {acc:.3f} "
                  f"p50 {statistics.median(latencies):.2f}s", flush=True)
    preds_f.close()

    peak_gb = mx.get_peak_memory() / 1e9
    scored = records[:]  # warmup rows still carry valid predictions (temp=0)
    n = len(scored)
    correct = sum(r["pred"] == r["true"] for r in scored)
    per_class = {}
    conf = defaultdict(int)
    for cid in CLASS_IDS:
        rows_c = [r for r in scored if r["true"] == cid]
        per_class[cid] = round(
            sum(r["pred"] == r["true"] for r in rows_c) / max(1, len(rows_c)), 4)
    for r in scored:
        conf[f"{r['true']}->{r['pred']}"] += 1
    lat_sorted = sorted(latencies)
    metrics = {
        "run_id": args.run_id, "model": args.model, "mode": args.mode,
        "prompt": args.prompt, "n": n,
        "accuracy": round(correct / n, 4),
        "per_class_accuracy": per_class,
        "confusion": dict(sorted(conf.items())),
        "parse_strict_rate": round(sum(r["parse"] == "strict" for r in scored) / n, 4),
        "parse_fallback_rate": round(sum(r["parse"] == "fallback" for r in scored) / n, 4),
        "parse_fail_rate": round(sum(r["parse"] == "fail" for r in scored) / n, 4),
        "latency_p50_s": round(lat_sorted[len(lat_sorted) // 2], 3),
        "latency_p95_s": round(lat_sorted[int(len(lat_sorted) * 0.95)], 3),
        "latency_mean_s": round(statistics.mean(latencies), 3),
        "load_seconds": cfg["load_seconds"],
        "weights_resident_gb": cfg["weights_resident_gb"],
        "peak_memory_gb": round(peak_gb, 3),
        "peak_inference_overhead_gb": round(peak_gb - cfg["weights_resident_gb"], 3),
        "model_disk_gb": cfg["model_disk_gb"],
        "mean_prompt_tokens": round(statistics.mean(
            [r["prompt_tokens"] for r in scored if r["prompt_tokens"]]), 1),
        "mean_gen_tokens": round(statistics.mean(
            [r["gen_tokens"] for r in scored if r["gen_tokens"]]), 1),
    }
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))
    with open(Path(args.runs_dir) / "index.jsonl", "a") as f:
        f.write(json.dumps(metrics) + "\n")
    print(json.dumps({k: metrics[k] for k in
                      ["accuracy", "parse_fail_rate", "latency_p50_s",
                       "latency_p95_s", "peak_memory_gb"]}, indent=2))
    print(f"[{args.run_id}] DONE", flush=True)


if __name__ == "__main__":
    main()
