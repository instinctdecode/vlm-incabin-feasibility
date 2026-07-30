"""Build the frozen evaluation set (stage 1-2).

Design decisions (recorded for the report):
- Split is BY SUBJECT (driver), not by image. State Farm images are video
  frames; the same driver appears in hundreds of near-duplicate frames, so a
  random image split leaks identity/pose and inflates accuracy. Eval subjects
  never appear in CNN training or few-shot examples.
- Eval subjects are chosen by seeded shuffle (seed fixed below), not manually.
- Per-class sample: 25 images/class (250 total). Rationale: 95% binomial CI
  at 250 is roughly ±6%p overall; per-class CI at n=25 is wide (~±17%p) and is
  reported as a limitation. 25/class keeps the full measurement matrix
  (~5,000 VLM inferences) tractable on one machine.
- Every referenced file is pinned by sha256; the manifest itself is hashed.

Usage: python scripts/freeze_eval_set.py --data-root data/raw_hf/extracted
"""
import argparse
import csv
import hashlib
import json
import random
import re
from collections import defaultdict
from pathlib import Path

SEED = 20260725
PER_CLASS = 25
N_EVAL_SUBJECTS = 6
N_VAL_SUBJECTS = 3          # taken from the non-eval side, for CNN early stop
FEWSHOT_PER_CLASS = 2
FRAME_WINDOW = 8            # multi-frame experiments need up to 8 frames


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def find_layout(root: Path):
    """Locate train/c0..c9 image dir and driver_imgs_list.csv under root."""
    train_dir = None
    for cand in root.rglob("c0"):
        if cand.is_dir() and (cand.parent / "c9").is_dir():
            train_dir = cand.parent
            break
    csv_path = None
    for cand in root.rglob("driver_imgs_list.csv"):
        csv_path = cand
        break
    return train_dir, csv_path


def img_num(name: str) -> int:
    m = re.search(r"(\d+)", name)
    return int(m.group(1)) if m else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", required=True)
    ap.add_argument("--out", default="data/frozen_eval")
    args = ap.parse_args()

    root = Path(args.data_root)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    train_dir, csv_path = find_layout(root)
    if train_dir is None or csv_path is None:
        raise SystemExit(
            f"layout not found under {root}: train_dir={train_dir} csv={csv_path}"
        )
    print(f"train_dir={train_dir}\ncsv={csv_path}")

    # subject,classname,img
    rows = []
    with open(csv_path) as f:
        for r in csv.DictReader(f):
            rows.append((r["subject"], r["classname"], r["img"]))
    subjects = sorted({r[0] for r in rows})
    print(f"{len(rows)} rows, {len(subjects)} subjects")

    rng = random.Random(SEED)
    shuffled = subjects[:]
    rng.shuffle(shuffled)
    eval_subjects = sorted(shuffled[:N_EVAL_SUBJECTS])
    rest = sorted(shuffled[N_EVAL_SUBJECTS:])
    val_subjects = sorted(rest[:N_VAL_SUBJECTS])
    cnn_train_subjects = sorted(rest[N_VAL_SUBJECTS:])
    print(f"eval subjects: {eval_subjects}")
    print(f"cnn val subjects: {val_subjects}")
    print(f"cnn train subjects: {len(cnn_train_subjects)}")

    by_class_eval = defaultdict(list)
    by_class_fewshot_pool = defaultdict(list)
    for subj, cls, img in rows:
        if subj in eval_subjects:
            by_class_eval[cls].append((subj, img))
        elif subj in cnn_train_subjects:
            by_class_fewshot_pool[cls].append((subj, img))

    # frozen eval sample: seeded, class-balanced, spread across subjects
    manifest = []
    for cls in sorted(by_class_eval):
        pool = sorted(by_class_eval[cls])
        rng2 = random.Random(SEED + int(cls[1]))
        picks = rng2.sample(pool, PER_CLASS)
        for subj, img in sorted(picks):
            p = train_dir / cls / img
            manifest.append(
                {"img": img, "classname": cls, "subject": subj,
                 "relpath": str(p.relative_to(root)),
                 "sha256": sha256_file(p)}
            )
    man_path = out / "manifest.csv"
    with open(man_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(manifest[0].keys()))
        w.writeheader()
        w.writerows(manifest)
    man_hash = sha256_file(man_path)
    print(f"frozen eval: {len(manifest)} images -> {man_path}")
    print(f"manifest sha256: {man_hash}")

    # few-shot examples: from CNN-train subjects only (never eval subjects)
    fewshot = []
    for cls in sorted(by_class_fewshot_pool):
        pool = sorted(by_class_fewshot_pool[cls])
        rng3 = random.Random(SEED * 2 + int(cls[1]))
        for subj, img in sorted(rng3.sample(pool, FEWSHOT_PER_CLASS)):
            p = train_dir / cls / img
            fewshot.append(
                {"img": img, "classname": cls, "subject": subj,
                 "relpath": str(p.relative_to(root)),
                 "sha256": sha256_file(p)}
            )
    fs_path = out / "fewshot_manifest.csv"
    with open(fs_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(fewshot[0].keys()))
        w.writeheader()
        w.writerows(fewshot)

    # multi-frame map: for each eval image, a contiguous window of
    # FRAME_WINDOW frames (by numeric filename order within subject+class).
    # Filename order approximates temporal order (frames extracted from
    # video); this assumption is recorded in the report.
    seq_index = defaultdict(list)
    for subj, cls, img in rows:
        seq_index[(subj, cls)].append(img)
    for k in seq_index:
        seq_index[k].sort(key=img_num)

    frames_map = {}
    for m in manifest:
        seq = seq_index[(m["subject"], m["classname"])]
        i = seq.index(m["img"])
        start = min(i, max(0, len(seq) - FRAME_WINDOW))
        window = seq[start:start + FRAME_WINDOW]
        frames_map[m["img"]] = {
            "classname": m["classname"], "subject": m["subject"],
            "anchor": m["img"],
            "frames": [str((train_dir / m["classname"] / w).relative_to(root))
                       for w in window],
        }
    fm_path = out / "frames_map.json"
    fm_path.write_text(json.dumps(frames_map, indent=1))

    split = {
        "seed": SEED,
        "eval_subjects": eval_subjects,
        "cnn_val_subjects": val_subjects,
        "cnn_train_subjects": cnn_train_subjects,
        "per_class": PER_CLASS,
        "n_eval": len(manifest),
        "manifest_sha256": man_hash,
        "fewshot_manifest_sha256": sha256_file(fs_path),
        "frames_map_sha256": sha256_file(fm_path),
        "data_root": str(root),
        "train_dir": str(train_dir),
    }
    (out / "split.json").write_text(json.dumps(split, indent=2))
    print(json.dumps(split, indent=2))


if __name__ == "__main__":
    main()
