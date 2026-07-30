"""Stage 3 — dedicated small CNN baseline via transfer learning.

Fair-comparison rules:
- Trains ONLY on cnn_train_subjects from split.json (17 subjects); early-stops
  on cnn_val_subjects (3 subjects). The 6 frozen-eval subjects are never seen.
- Evaluated on the same frozen 250-image set as every VLM run.
- No horizontal flip augmentation: left/right distinction is label-bearing
  (texting-left vs texting-right).

Outputs runs/<run-id>/{config.json,predictions.jsonl,metrics.json} in the same
schema as eval_vlm.py, plus model checkpoint under runs/<run-id>/model.pt.

Latency caveat: Apple M4 Max measurements are for relative comparison only,
not automotive-SoC performance.
"""
import argparse
import csv
import json
import platform
import statistics
import time
from collections import defaultdict
from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchvision import models, transforms

from common import CLASS_IDS

DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"


class DriverDataset(Dataset):
    def __init__(self, items, tf):
        self.items = items  # (path, class_idx)
        self.tf = tf

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i):
        p, y = self.items[i]
        img = Image.open(p).convert("RGB")
        return self.tf(img), y


def build_model(arch: str):
    if arch == "mobilenet_v3_small":
        m = models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.IMAGENET1K_V1)
        m.classifier[3] = nn.Linear(m.classifier[3].in_features, 10)
    elif arch == "resnet18":
        m = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        m.fc = nn.Linear(m.fc.in_features, 10)
    elif arch == "efficientnet_b0":
        m = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
        m.classifier[1] = nn.Linear(m.classifier[1].in_features, 10)
    else:
        raise ValueError(arch)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arch", default="mobilenet_v3_small")
    ap.add_argument("--epochs", type=int, default=8)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--eval-dir", default="data/frozen_eval")
    ap.add_argument("--runs-dir", default="runs")
    ap.add_argument("--run-id", default=None)
    args = ap.parse_args()
    run_id = args.run_id or f"cnn_{args.arch}"

    eval_dir = Path(args.eval_dir)
    split = json.loads((eval_dir / "split.json").read_text())
    data_root = Path(split["data_root"])
    train_dir = Path(split["train_dir"])
    cls_to_idx = {c: i for i, c in enumerate(CLASS_IDS)}

    rows = []
    with open(data_root / "driver_imgs_list.csv") as f:
        for r in csv.DictReader(f):
            rows.append((r["subject"], r["classname"], r["img"]))
    tr_subj = set(split["cnn_train_subjects"])
    va_subj = set(split["cnn_val_subjects"])
    train_items = [(train_dir / c / img, cls_to_idx[c]) for s, c, img in rows if s in tr_subj]
    val_items = [(train_dir / c / img, cls_to_idx[c]) for s, c, img in rows if s in va_subj]

    with open(eval_dir / "manifest.csv") as f:
        eval_rows = list(csv.DictReader(f))
    eval_items = [(data_root / r["relpath"], cls_to_idx[r["classname"]]) for r in eval_rows]

    norm = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    tf_train = transforms.Compose([
        transforms.RandomResizedCrop(224, scale=(0.75, 1.0), ratio=(0.9, 1.1)),
        transforms.ColorJitter(0.2, 0.2, 0.2),
        transforms.ToTensor(), norm,
    ])
    tf_eval = transforms.Compose([
        transforms.Resize(256), transforms.CenterCrop(224),
        transforms.ToTensor(), norm,
    ])

    dl_train = DataLoader(DriverDataset(train_items, tf_train), batch_size=args.batch,
                          shuffle=True, num_workers=6, persistent_workers=True)
    dl_val = DataLoader(DriverDataset(val_items, tf_eval), batch_size=args.batch,
                        num_workers=4)

    model = build_model(args.arch).to(DEVICE)
    nparams = sum(p.numel() for p in model.parameters())
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=args.epochs)
    crit = nn.CrossEntropyLoss(label_smoothing=0.1)

    run_dir = Path(args.runs_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"[{run_id}] arch={args.arch} params={nparams/1e6:.2f}M "
          f"train={len(train_items)} val={len(val_items)} device={DEVICE}", flush=True)

    t_train0 = time.perf_counter()
    best_val, best_state, history = 0.0, None, []
    for ep in range(args.epochs):
        model.train()
        for xb, yb in dl_train:
            xb, yb = xb.to(DEVICE), yb.to(DEVICE)
            opt.zero_grad()
            loss = crit(model(xb), yb)
            loss.backward()
            opt.step()
        sched.step()
        model.eval()
        corr = tot = 0
        with torch.no_grad():
            for xb, yb in dl_val:
                pred = model(xb.to(DEVICE)).argmax(1).cpu()
                corr += (pred == yb).sum().item()
                tot += len(yb)
        va = corr / tot
        history.append({"epoch": ep + 1, "val_acc": round(va, 4)})
        print(f"  epoch {ep+1}/{args.epochs} val_acc={va:.4f}", flush=True)
        if va > best_val:
            best_val = va
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
    train_seconds = time.perf_counter() - t_train0

    model.load_state_dict(best_state)
    ckpt = run_dir / "model.pt"
    torch.save(best_state, ckpt)
    disk_mb = ckpt.stat().st_size / 1e6

    # ---- frozen-set evaluation (batch=1, end-to-end incl. JPEG decode+preprocess,
    # same accounting as the VLM harness) ----
    model.eval()
    records, latencies = [], []
    for i, (r, (p, y)) in enumerate(zip(eval_rows, eval_items)):
        t1 = time.perf_counter()
        img = Image.open(p).convert("RGB")
        x = tf_eval(img).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            out = model(x)
            pred_idx = int(out.argmax(1).item())
        if DEVICE == "mps":
            torch.mps.synchronize()
        dt = time.perf_counter() - t1
        if i >= 3:  # warmup=3, same as VLM harness
            latencies.append(dt)
        records.append({"img": r["img"], "true": r["classname"],
                        "subject": r["subject"], "pred": CLASS_IDS[pred_idx],
                        "parse": "n/a", "latency_s": round(dt, 4), "warmup": i < 3})
    with open(run_dir / "predictions.jsonl", "w") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")

    # pure forward latency (no I/O), batch=1
    x = torch.randn(1, 3, 224, 224).to(DEVICE)
    for _ in range(10):
        with torch.no_grad():
            model(x)
    if DEVICE == "mps":
        torch.mps.synchronize()
    fwd = []
    for _ in range(100):
        t1 = time.perf_counter()
        with torch.no_grad():
            model(x)
        if DEVICE == "mps":
            torch.mps.synchronize()
        fwd.append(time.perf_counter() - t1)
    fwd.sort()

    n = len(records)
    correct = sum(r["pred"] == r["true"] for r in records)
    per_class = {}
    conf = defaultdict(int)
    for cid in CLASS_IDS:
        rc = [r for r in records if r["true"] == cid]
        per_class[cid] = round(sum(r["pred"] == r["true"] for r in rc) / len(rc), 4)
    for r in records:
        conf[f"{r['true']}->{r['pred']}"] += 1
    lat = sorted(latencies)
    metrics = {
        "run_id": run_id, "model": args.arch, "mode": "cnn_baseline", "prompt": None,
        "n": n, "accuracy": round(correct / n, 4),
        "per_class_accuracy": per_class, "confusion": dict(sorted(conf.items())),
        "parse_strict_rate": 1.0, "parse_fallback_rate": 0.0, "parse_fail_rate": 0.0,
        "latency_p50_s": round(lat[len(lat) // 2], 4),
        "latency_p95_s": round(lat[int(len(lat) * 0.95)], 4),
        "latency_mean_s": round(statistics.mean(lat), 4),
        "forward_p50_s": round(fwd[50], 4), "forward_p95_s": round(fwd[95], 4),
        "params_m": round(nparams / 1e6, 3),
        "model_disk_gb": round(disk_mb / 1000, 4),
        "train_seconds": round(train_seconds, 1),
        "train_images": len(train_items), "val_best_acc": round(best_val, 4),
        "history": history,
        "peak_memory_gb": round(torch.mps.driver_allocated_memory() / 1e9, 3)
        if DEVICE == "mps" else None,
    }
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))
    cfg = {
        "run_id": run_id, "arch": args.arch, "epochs": args.epochs,
        "batch": args.batch, "lr": args.lr, "device": DEVICE,
        "train_subjects": sorted(tr_subj), "val_subjects": sorted(va_subj),
        "n_train": len(train_items), "n_val": len(val_items),
        "augment": "RandomResizedCrop(224,0.75-1.0)+ColorJitter(0.2) — no hflip (left/right is label-bearing)",
        "pretrained": "ImageNet1K", "manifest_sha256": split["manifest_sha256"],
        "host": {"machine": "Apple M4 Max 128GB", "platform": platform.platform(),
                 "torch": torch.__version__},
        "latency_note": "Measured on Apple M4 Max; NOT automotive-SoC latency.",
    }
    (run_dir / "config.json").write_text(json.dumps(cfg, indent=2))
    with open(Path(args.runs_dir) / "index.jsonl", "a") as f:
        f.write(json.dumps(metrics) + "\n")
    print(json.dumps({k: metrics[k] for k in
                      ["accuracy", "latency_p50_s", "forward_p50_s", "params_m",
                       "model_disk_gb", "train_seconds", "val_best_acc"]}, indent=2))
    print(f"[{run_id}] DONE", flush=True)


if __name__ == "__main__":
    main()
