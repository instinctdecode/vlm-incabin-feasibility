"""B-4 open-vocabulary retention analysis.

Compares free-form 'describe' runs (base vs ft-full vs ft-holdout) with
deterministic metrics defined BEFORE looking at outputs:

1. core-content hit: description mentions >=1 keyword of the image's true
   class (per-class keyword sets below) — proxy for "still describes what
   actually happens".
2. json_leak: model answers the free-form question with its fine-tuned
   classification format ('{"class_id": ...}' or similar) — catastrophic
   format collapse signature.
3. degenerate: empty / token-repetition output.
4. length: mean words per description (collapse to terse outputs).

Also breaks out class c9 (held out from ft_holdout training) separately.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

RUNS = Path("runs")

KEYWORDS = {
    "c0": ["steering", "wheel", "driving", "road", "both hands"],
    "c1": ["phone", "texting", "cell", "mobile", "device", "screen"],
    "c2": ["phone", "call", "ear", "talking on"],
    "c3": ["phone", "texting", "cell", "mobile", "device", "screen"],
    "c4": ["phone", "call", "ear", "talking on"],
    "c5": ["radio", "console", "dashboard", "control", "button", "panel", "screen"],
    "c6": ["drink", "bottle", "cup", "beverage", "sipping", "water", "coffee"],
    "c7": ["reaching", "behind", "back seat", "backseat", "rear", "turning around"],
    "c8": ["hair", "makeup", "mirror", "grooming", "touching", "face"],
    "c9": ["passenger", "talking", "convers", "speaking", "another person",
           "someone", "looking to the side", "chatting"],
}


def analyze(run_id):
    p = RUNS / run_id / "predictions.jsonl"
    if not p.exists():
        return None
    rows = [json.loads(l) for l in p.open()]
    out = {"run_id": run_id, "n": len(rows)}
    per_class_hit = defaultdict(list)
    leaks = degen = 0
    lengths = []
    for r in rows:
        text = r["raw"].strip()
        tl = text.lower()
        leak = bool(re.match(r'^\s*[{\["]', text)) or "class_id" in tl
        degenerate = (not text) or "<|im_start|>" in text or len(set(text.split())) <= 2
        hit = any(k in tl for k in KEYWORDS[r["true"]]) and not leak and not degenerate
        per_class_hit[r["true"]].append(hit)
        leaks += leak
        degen += degenerate
        lengths.append(len(text.split()))
    out["core_content_hit_rate"] = round(
        sum(sum(v) for v in per_class_hit.values()) / len(rows), 4)
    out["per_class_hit"] = {c: round(sum(v) / len(v), 3)
                            for c, v in sorted(per_class_hit.items())}
    out["json_leak_rate"] = round(leaks / len(rows), 4)
    out["degenerate_rate"] = round(degen / len(rows), 4)
    out["mean_words"] = round(sum(lengths) / len(lengths), 1)
    out["c9_hit"] = out["per_class_hit"].get("c9")
    return out


def main():
    results = []
    for rid in ["qwen3b-4bit-base_desc", "qwen3b-4bit-ftfull_desc",
                "qwen3b-4bit-ftholdout_desc"]:
        r = analyze(rid)
        if r:
            results.append(r)
            print(json.dumps(r, indent=1))
    Path("results").mkdir(exist_ok=True)
    Path("results/openvocab_analysis.json").write_text(json.dumps(results, indent=2))

    # sample outputs for the report (first 2 c9 descriptions per run)
    samples = {}
    for rid in ["qwen3b-4bit-base_desc", "qwen3b-4bit-ftfull_desc",
                "qwen3b-4bit-ftholdout_desc"]:
        p = RUNS / rid / "predictions.jsonl"
        if p.exists():
            rows = [json.loads(l) for l in p.open() if json.loads(l)["true"] == "c9"]
            samples[rid] = [r["raw"][:200] for r in rows[:3]]
    Path("results/openvocab_samples.json").write_text(
        json.dumps(samples, indent=2, ensure_ascii=False))
    print("saved results/openvocab_analysis.json, openvocab_samples.json")


if __name__ == "__main__":
    main()
