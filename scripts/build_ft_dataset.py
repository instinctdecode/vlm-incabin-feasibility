"""Build LoRA fine-tuning datasets for Qwen2.5-VL-3B (task B).

Leakage rules (hard-verified at build time):
- Training images come ONLY from the 17 cnn_train_subjects of split.json.
  The 6 frozen-eval subjects and 3 val subjects never appear.
- Zero filename overlap with the frozen eval manifest (asserted).
- Training prompt == evaluation prompt p1, answer == strict JSON, so the
  fine-tuned model is evaluated by the exact harness used for zero-shot.

Two variants:
- data/ft_full/train.jsonl     : 300/class x 10 classes = 3,000 samples
- data/ft_holdout/train.jsonl  : same but class c9 EXCLUDED from training
  (2,700 samples) — open-vocabulary retention experiment (B-4).

Sample count rationale: 300/class is a deliberate "practical effort" budget
(~2 epochs ≈ 3,000 optimizer steps at batch 2) — NOT the full 14,709 images the
CNN baseline used; recorded as a comparison condition in the report.
"""
import argparse
import csv
import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from common import PROMPT_P1

SEED = 20260725
PER_CLASS = 300


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval-dir", default="data/frozen_eval")
    args = ap.parse_args()

    split = json.loads((Path(args.eval_dir) / "split.json").read_text())
    data_root = Path(split["data_root"]).resolve()
    train_dir = Path(split["train_dir"]).resolve()
    train_subjects = set(split["cnn_train_subjects"])
    eval_subjects = set(split["eval_subjects"])
    val_subjects = set(split["cnn_val_subjects"])

    with open(Path(args.eval_dir) / "manifest.csv") as f:
        frozen_imgs = {r["img"] for r in csv.DictReader(f)}

    rows = []
    with open(data_root / "driver_imgs_list.csv") as f:
        for r in csv.DictReader(f):
            rows.append((r["subject"], r["classname"], r["img"]))

    by_class = defaultdict(list)
    for subj, cls, img in rows:
        if subj in train_subjects:
            by_class[cls].append((subj, img))

    picked = {}
    for cls in sorted(by_class):
        pool = sorted(by_class[cls])
        rng = random.Random(SEED * 3 + int(cls[1]))
        picked[cls] = rng.sample(pool, PER_CLASS)

    # ---- leakage verification (hard asserts) ----
    for cls, items in picked.items():
        for subj, img in items:
            assert subj in train_subjects, f"non-train subject {subj}"
            assert subj not in eval_subjects and subj not in val_subjects
            assert img not in frozen_imgs, f"frozen eval image leaked: {img}"
    n_total = sum(len(v) for v in picked.values())
    print(f"leak check PASSED: {n_total} samples, subjects ⊆ 17 train subjects, "
          f"0 overlap with frozen manifest ({len(frozen_imgs)} files)")

    def write(out_dir: Path, exclude_classes=()):
        out_dir.mkdir(parents=True, exist_ok=True)
        p = out_dir / "train.jsonl"
        n = 0
        h = hashlib.sha256()
        with open(p, "w") as f:
            entries = []
            for cls, items in picked.items():
                if cls in exclude_classes:
                    continue
                for subj, img in items:
                    entries.append((cls, subj, img))
            rng = random.Random(SEED)
            rng.shuffle(entries)
            for cls, subj, img in entries:
                rec = {
                    "images": [str(train_dir / cls / img)],
                    "messages": [
                        {"role": "user", "content": PROMPT_P1},
                        {"role": "assistant", "content": json.dumps({"class_id": cls})},
                    ],
                }
                line = json.dumps(rec)
                h.update(line.encode())
                f.write(line + "\n")
                n += 1
        meta = {"n": n, "per_class": PER_CLASS, "seed": SEED,
                "excluded_classes": list(exclude_classes),
                "subjects": sorted(train_subjects),
                "train_jsonl_sha256": h.hexdigest(),
                "prompt": "p1 (identical to zero-shot evaluation prompt)"}
        (out_dir / "meta.json").write_text(json.dumps(meta, indent=2))
        print(f"{p}: {n} samples, sha256 {h.hexdigest()[:16]}…")

    write(Path("data/ft_full"))
    write(Path("data/ft_holdout"), exclude_classes=("c9",))


if __name__ == "__main__":
    main()
