"""B-4 secondary metric: local LLM judge for c9 (talking-to-passenger)
descriptions. Text-only judging against the known ground-truth label —
NO paid APIs, judge = local Qwen2.5-VL-32B-4bit (text-only prompt).

Judge sees the description only (not the image); the question is whether the
description asserts the driver is interacting with / turned toward a passenger.
Deterministic keyword metrics in analyze_openvocab.py remain the primary
metric; this is a robustness check on paraphrases the keyword list misses.
"""
import json
from pathlib import Path

from mlx_vlm import generate, load
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config

RUNS = Path("runs")
JUDGE = "mlx-community/Qwen2.5-VL-32B-Instruct-4bit"
RUN_IDS = ["qwen3b-4bit-base_desc", "qwen3b-4bit-ftfull_desc",
           "qwen3b-4bit-ftholdout_desc"]

PROMPT = """Ground truth: the driver in the image is TALKING TO A PASSENGER \
(head turned toward the passenger seat, engaged in conversation).

A model described the image as:
"{desc}"

Does the description correctly convey that the driver is talking to / \
interacting with a passenger (or at least turned toward another person)?
Answer with ONLY JSON: {{"match": true}} or {{"match": false}}"""


def main():
    model, proc = load(JUDGE)
    cfg = load_config(JUDGE)
    out = {}
    for rid in RUN_IDS:
        p = RUNS / rid / "predictions.jsonl"
        rows = [json.loads(l) for l in p.open() if json.loads(l)["true"] == "c9"]
        verdicts = []
        for r in rows:
            desc = r["raw"].strip().replace('"', "'")[:300]
            prompt = apply_chat_template(proc, cfg, PROMPT.format(desc=desc),
                                         num_images=0)
            res = generate(model, proc, prompt, image=[], max_tokens=16,
                           temperature=0.0, verbose=False)
            verdicts.append("true" in res.text.lower())
        out[rid] = {"n": len(verdicts), "judge_match_rate":
                    round(sum(verdicts) / len(verdicts), 4)}
        print(rid, out[rid])
    Path("results/c9_judge.json").write_text(json.dumps(
        {"judge_model": JUDGE, "note": "text-only judging vs known label; "
         "secondary to deterministic keyword metric", **out}, indent=2))


if __name__ == "__main__":
    main()
