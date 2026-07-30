"""Minimal reproduction: Qwen2.5-VL degenerates whenever chunked prefill engages
(prompt_tokens > prefill_step_size, default 2048).

Self-contained — generates its own synthetic images, no external data.

Observed on: mlx-vlm 0.6.7 (PyPI) AND git main @ 2026-07-26 (0.6.8-dev),
mlx 0.32.0, macOS 26.5 (Darwin 25.5), Apple M4 Max 128GB.
Models: mlx-community/Qwen2.5-VL-3B-Instruct-4bit, 7B-4bit, and 3B **bf16**
(so not a quantization artifact).

Symptom: any prompt longer than prefill_step_size — many images OR text-only —
generates degenerate output at temperature 0: immediate EOS (empty string) or
endless `<|im_start|>` / `addCriterion` repetition.

Decisive toggles (also exercised by this script):
- prompt 2,165 tok (11 images), prefill_step_size=8192 (no chunking)  -> OK
- prompt 1,195 tok (6 images, normally fine), prefill_step_size=512   -> DEGENERATE
- text-only 4,338 tok, default chunking -> DEGENERATE; chunking off   -> OK
- same 4,348-token text-only prompt through mlx-lm 0.31.3 (pure-LLM
  Qwen2.5-3B-Instruct-4bit, same default chunked prefill)             -> OK

Usage:
  python repro_multiimage_collapse.py [--model mlx-community/Qwen2.5-VL-3B-Instruct-4bit]
  # writes repro_log.txt next to this file
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

from mlx_vlm import generate, load
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config

HERE = Path(__file__).parent
PROMPT = "How many images were provided? Answer with just the number."


def make_image(idx: int, size=(448, 336)) -> str:
    """Deterministic synthetic image (colored background + a few shapes)."""
    img = Image.new("RGB", size, ((37 * idx) % 255, (91 * idx) % 255, (53 * idx) % 255))
    d = ImageDraw.Draw(img)
    for k in range(4):
        x = (idx * 61 + k * 97) % (size[0] - 60)
        y = (idx * 43 + k * 71) % (size[1] - 60)
        d.rectangle([x, y, x + 50, y + 50],
                    fill=((k * 80) % 255, (idx * 30) % 255, 200))
    p = HERE / f"_synth_{idx}.jpg"
    img.save(p, quality=90)
    return str(p)


def classify(text: str) -> str:
    t = text.strip()
    if not t:
        return "DEGENERATE(empty)"
    if "<|im_start|>" in t or "addCriterion" in t:
        return "DEGENERATE(repetition)"
    # normal outputs here are a short number-ish answer
    return "OK"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="mlx-community/Qwen2.5-VL-3B-Instruct-4bit")
    ap.add_argument("--counts", default="1,2,4,6,8,10,11,12,14")
    ap.add_argument("--with-mlx-lm-control", action="store_true")
    args = ap.parse_args()

    log = open(HERE / "repro_log.txt", "a")

    def emit(s):
        print(s, flush=True)
        log.write(s + "\n")
        log.flush()

    import mlx.core as mx
    import mlx_vlm
    import platform
    emit(f"=== model={args.model} mlx={mx.__version__} mlx-vlm={mlx_vlm.__version__} "
         f"platform={platform.platform()} ===")

    model, processor = load(args.model)
    config = load_config(args.model)

    # --- control 1: text-only prompt of comparable token length (~3k tokens)
    long_text = ("The quick brown fox jumps over the lazy dog. " * 430
                 + "\nAfter all that text: what is 2+2? Answer with just the number.")
    prompt = apply_chat_template(processor, config, long_text, num_images=0)
    r = generate(model, processor, prompt, image=[], max_tokens=24, temperature=0.0,
                 verbose=False)
    emit(f"[control text-only ~{r.prompt_tokens} tok] -> {classify(r.text):24s} "
         f"out={r.text[:60]!r}")

    # --- sweep: K images, identical trivial question (default prefill 2048)
    for k in [int(x) for x in args.counts.split(",")]:
        images = [make_image(i) for i in range(k)]
        prompt = apply_chat_template(processor, config, PROMPT, num_images=k)
        r = generate(model, processor, prompt, image=images, max_tokens=24,
                     temperature=0.0, verbose=False)
        emit(f"[k={k:2d} images, {r.prompt_tokens:5d} prompt tok] -> "
             f"{classify(r.text):24s} out={r.text[:60]!r}")

    # --- decisive toggles: the ONLY variable is prefill_step_size
    for k, prefill, note in [(11, 8192, "long prompt, chunking OFF -> expect OK"),
                             (6, 512, "short prompt, chunking FORCED -> expect DEGENERATE")]:
        images = [make_image(i) for i in range(k)]
        prompt = apply_chat_template(processor, config, PROMPT, num_images=k)
        r = generate(model, processor, prompt, image=images, max_tokens=24,
                     temperature=0.0, verbose=False, prefill_step_size=prefill)
        emit(f"[k={k:2d} images, {r.prompt_tokens:5d} tok, prefill={prefill}] -> "
             f"{classify(r.text):24s} out={r.text[:40]!r} ({note})")
    prompt = apply_chat_template(processor, config, long_text, num_images=0)
    r = generate(model, processor, prompt, image=[], max_tokens=24,
                 temperature=0.0, verbose=False, prefill_step_size=8192)
    emit(f"[text-only ~4.3k tok, prefill=8192] -> {classify(r.text):24s} "
         f"out={r.text[:40]!r} (text-only, chunking OFF -> expect OK)")

    if args.with_mlx_lm_control:
        # control 2: same text through mlx-lm's pure-LLM path (default chunked
        # prefill there too) — isolates the bug to mlx-vlm's implementation
        try:
            import mlx_lm
            lm, tok = mlx_lm.load("mlx-community/Qwen2.5-3B-Instruct-4bit")
            p = tok.apply_chat_template([{"role": "user", "content": long_text}],
                                        add_generation_prompt=True)
            out = mlx_lm.generate(lm, tok, prompt=p, max_tokens=24, verbose=False)
            emit(f"[control mlx-lm {mlx_lm.__version__} text-only {len(p)} tok, "
                 f"default chunking] -> {classify(out):24s} out={out[:40]!r}")
        except ImportError:
            emit("[control mlx-lm] skipped (mlx-lm not installed)")
    emit("")
    log.close()


if __name__ == "__main__":
    sys.exit(main())
