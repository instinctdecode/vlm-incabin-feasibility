"""Aggregate runs/*/metrics.json into report tables (results/)."""
import json
from pathlib import Path

from common import CLASS_IDS, SHORT

RUNS = Path("runs")
OUT = Path("results")
OUT.mkdir(exist_ok=True)


def load_all():
    metrics = []
    for p in sorted(RUNS.glob("*/metrics.json")):
        m = json.loads(p.read_text())
        metrics.append(m)
    return metrics


def fmt(v, nd=3):
    if v is None:
        return "-"
    if isinstance(v, float):
        return f"{v:.{nd}f}"
    return str(v)


def main_table(ms):
    cols = ["run_id", "model", "mode", "prompt", "accuracy", "parse_fail_rate",
            "parse_fallback_rate", "latency_p50_s", "latency_p95_s",
            "peak_memory_gb", "model_disk_gb", "n"]
    lines = ["| " + " | ".join(cols) + " |",
             "|" + "---|" * len(cols)]
    for m in ms:
        lines.append("| " + " | ".join(fmt(m.get(c)) for c in cols) + " |")
    return "\n".join(lines)


def per_class_table(ms):
    header = ["run_id"] + [SHORT[c] for c in CLASS_IDS]
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for m in ms:
        pc = m.get("per_class_accuracy", {})
        lines.append("| " + m["run_id"] + " | " +
                     " | ".join(fmt(pc.get(c), 2) for c in CLASS_IDS) + " |")
    return "\n".join(lines)


def confusion_md(m):
    conf = m.get("confusion", {})
    header = ["true\\pred"] + [SHORT[c] for c in CLASS_IDS] + ["FAIL"]
    lines = [f"**{m['run_id']}** (acc={m['accuracy']})", "",
             "| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for t in CLASS_IDS:
        row = [SHORT[t]]
        for p in CLASS_IDS:
            row.append(str(conf.get(f"{t}->{p}", 0)))
        row.append(str(conf.get(f"{t}->None", 0)))
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def main():
    ms = load_all()
    md = ["# Run summary (frozen eval set, n=250, Apple M4 Max)", "",
          "Latency measured on Apple M4 Max — relative comparison only, "
          "NOT automotive-SoC performance.", "",
          "## All runs", "", main_table(ms), "",
          "## Per-class accuracy", "", per_class_table(ms), "",
          "## Confusion matrices", ""]
    for m in ms:
        md.append(confusion_md(m))
        md.append("")
    (OUT / "summary.md").write_text("\n".join(md))
    (OUT / "summary.json").write_text(json.dumps(ms, indent=1))
    print(f"{len(ms)} runs -> results/summary.md")


if __name__ == "__main__":
    main()
