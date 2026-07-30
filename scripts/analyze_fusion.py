"""Stage 7 analysis — does SYNTHETIC heart-rate text context change outputs?

Compares fusion runs (same frozen images, same model, only the injected HR
band differs). Heart rates are synthetic test values, NOT measurements; the
question is whether the fusion path works (text context reaches the output),
not whether accuracy improves.
"""
import json
from collections import Counter
from pathlib import Path

RUNS = Path("runs")
CONDS = ["low", "normal", "high"]


def load(run_id):
    p = RUNS / run_id / "predictions.jsonl"
    if not p.exists():
        return None
    return {r["img"]: r for r in map(json.loads, p.open())}


def main():
    data = {c: load(f"qwen7b-4bit_fusion_{c}") for c in CONDS}
    missing = [c for c, d in data.items() if d is None]
    if missing:
        print(f"missing runs: {missing}")
        return
    imgs = sorted(set(data["normal"]) & set(data["low"]) & set(data["high"]))
    out = {"n": len(imgs), "note": "HR values are SYNTHETIC context, not measurements"}

    # 1) arousal output distribution per HR condition (fusion path works if
    #    the distribution tracks the injected band)
    out["arousal_by_condition"] = {
        c: dict(Counter(data[c][i].get("arousal") for i in imgs)) for c in CONDS}

    # 2) visual class stability: does injected HR perturb class_id?
    base = data["normal"]
    for c in ["low", "high"]:
        same = sum(data[c][i]["pred"] == base[i]["pred"] for i in imgs)
        out[f"class_agreement_normal_vs_{c}"] = round(same / len(imgs), 4)

    # 3) accuracy per condition (should be ~flat if vision judgment is robust)
    for c in CONDS:
        out[f"accuracy_{c}"] = round(
            sum(data[c][i]["pred"] == data[c][i]["true"] for i in imgs) / len(imgs), 4)

    Path("results").mkdir(exist_ok=True)
    Path("results/fusion_analysis.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
