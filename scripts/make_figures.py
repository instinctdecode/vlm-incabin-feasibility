"""Report figures from runs/*/metrics.json -> results/figs/*.png.

Palette: validated 3-slot categorical (blue #2a78d6 / orange #eb6834 /
aqua #1baf7a, light mode), sequential blue ramp for heatmap. <=3 series per
chart (all-pairs validated); direct labels; one axis per chart.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e5e4e0", "#fcfcfb"
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#1c5cab", "#104281"]

plt.rcParams.update({
    "font.family": "Apple SD Gothic Neo", "axes.unicode_minus": False,
    "figure.facecolor": SURF, "axes.facecolor": SURF,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.size": 10,
})

RUNS = Path("runs")
FIGS = Path("results/figs")
FIGS.mkdir(parents=True, exist_ok=True)


def m(run_id):
    p = RUNS / run_id / "metrics.json"
    return json.loads(p.read_text()) if p.exists() else None


def save(fig, name):
    fig.tight_layout()
    fig.savefig(FIGS / name, dpi=180)
    plt.close(fig)
    print("saved", FIGS / name)


# ---------------------------------------------------------------- fig 1
def fig_size_accuracy(edge_budget_gb=(1, 4)):
    pts_4bit = [("SmolVLM2-2.2B", "smolvlm2-4bit_zs_p1"),
                ("Qwen2.5-VL-3B", "qwen3b-4bit_zs_p1"),
                ("Qwen2.5-VL-7B", "qwen7b-4bit_zs_p1"),
                ("Qwen2.5-VL-32B", "qwen32b-4bit_zs_p1"),
                ("Qwen2.5-VL-72B", "qwen72b-4bit_zs_p1")]
    pts_bf16 = [("SmolVLM2-2.2B", "smolvlm2-bf16_zs_p1"),
                ("Qwen2.5-VL-3B", "qwen3b-bf16_zs_p1"),
                ("Qwen2.5-VL-7B", "qwen7b-bf16_zs_p1")]
    cnn = [("MobileNetV3-S", "cnn_mobilenet_v3_small"),
           ("ResNet18", "cnn_resnet18")]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axvspan(*edge_budget_gb, color="#f0efec", zorder=0)
    ax.text(edge_budget_gb[1] * 0.92, 0.02, "차량 DMS 메모리 예산대(공개자료 기반, §6)",
            fontsize=8, color=INK2, ha="right")
    for label, series, color, marker, annotate in [
            ("4bit", pts_4bit, BLUE, "o", True),
            ("bf16", pts_bf16, ORANGE, "s", False)]:
        xs, ys, names = [], [], []
        for name, rid in series:
            mm = m(rid)
            if mm:
                xs.append(mm["weights_resident_gb"])
                ys.append(mm["accuracy"])
                names.append(name)
        ax.plot(xs, ys, marker=marker, color=color, label=f"VLM 제로샷 ({label})",
                linewidth=2, markersize=7)
        if annotate:
            for x, y, name in zip(xs, ys, names):
                ax.annotate(name.replace("Qwen2.5-VL", "Qwen"), (x, y),
                            textcoords="offset points", xytext=(0, 9),
                            fontsize=8, color=INK, ha="center")
    for name, rid in cnn:
        mm = m(rid)
        if mm:
            x = max(mm["model_disk_gb"], 0.01)
            ax.plot([x], [mm["accuracy"]], marker="*", color=AQUA, markersize=14,
                    linestyle="none",
                    label="전용 CNN(전이학습, 디스크 GB)" if name == cnn[0][0] else None)
            ax.annotate(name, (x, mm["accuracy"]), textcoords="offset points",
                        xytext=(8, -3), fontsize=8, color=INK)
    ft = m("qwen3b-4bit-ftfull_zs_p1")
    if ft:
        ax.plot([ft["weights_resident_gb"]], [ft["accuracy"]], marker="D",
                color=BLUE, markersize=9, linestyle="none",
                label="VLM QLoRA 미세조정 (3B-4bit)")
        ax.annotate("Qwen-3B FT", (ft["weights_resident_gb"], ft["accuracy"]),
                    textcoords="offset points", xytext=(0, 9), fontsize=8,
                    color=INK, ha="center")
    ax.set_xscale("log")
    ax.set_xticks([0.01, 0.1, 1, 10, 100])
    ax.set_xticklabels(["0.01", "0.1", "1", "10", "100"])
    ax.minorticks_off()
    ax.set_xlabel("모델 상주 메모리 (GB, log)")
    ax.set_ylabel("동결 세트 정확도 (n=250)")
    ax.set_ylim(0, 1.0)
    ax.set_title("모델 크기 vs 판정 정확도 — 10클래스 운전자 상태 (State Farm)", color=INK)
    ax.legend(frameon=False, loc="center left")
    save(fig, "fig1_size_accuracy.png")


# ---------------------------------------------------------------- fig 2
def fig_latency():
    series = [("SmolVLM2-2.2B", "smolvlm2"), ("Qwen2.5-VL-3B", "qwen3b"),
              ("Qwen2.5-VL-7B", "qwen7b"), ("Qwen2.5-VL-32B", "qwen32b"),
              ("Qwen2.5-VL-72B", "qwen72b")]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for qi, (quant, color, marker) in enumerate([("4bit", BLUE, "o"), ("bf16", ORANGE, "s")]):
        xs, ys, names = [], [], []
        for name, pre in series:
            mm = m(f"{pre}-{quant}_zs_p1")
            if mm:
                xs.append(mm["weights_resident_gb"])
                ys.append(mm["latency_p50_s"])
                names.append(name)
        ax.plot(xs, ys, marker=marker, color=color, linewidth=2, markersize=7,
                label=f"VLM ({quant})")
        if quant == "4bit":
            for x, y, name in zip(xs, ys, names):
                ax.annotate(name.replace("Qwen2.5-VL", "Qwen"), (x, y),
                            textcoords="offset points", xytext=(0, 9),
                            fontsize=8, color=INK, ha="center")
    for name, rid in [("MobileNetV3-S", "cnn_mobilenet_v3_small"),
                      ("ResNet18", "cnn_resnet18")]:
        mm = m(rid)
        if mm:
            ax.plot([max(mm["model_disk_gb"], 0.01)], [mm["latency_p50_s"]],
                    marker="*", color=AQUA, markersize=14, linestyle="none",
                    label="전용 CNN (디스크 GB)" if "Mobile" in name else None)
            ax.annotate(name, (max(mm["model_disk_gb"], 0.01), mm["latency_p50_s"]),
                        textcoords="offset points", xytext=(8, -3), fontsize=8, color=INK)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([0.01, 0.1, 1, 10, 100])
    ax.set_xticklabels(["0.01", "0.1", "1", "10", "100"])
    ax.set_yticks([0.01, 0.1, 1, 10])
    ax.set_yticklabels(["0.01", "0.1", "1", "10"])
    ax.minorticks_off()
    ax.set_xlabel("모델 상주 메모리 (GB, log)")
    ax.set_ylabel("프레임당 지연 p50 (초, log)")
    ax.set_title("모델 크기 vs 지연 — Apple M4 Max 측정, 상대 비교 전용(차량 SoC 아님)", color=INK)
    ax.legend(frameon=False, loc="upper left")
    save(fig, "fig2_latency.png")


# ---------------------------------------------------------------- fig 3
def fig_multiframe():
    rows = [("1", "qwen7b-4bit_zs_p1"), ("2", "qwen7b-4bit_mf2"),
            ("4", "qwen7b-4bit_mf4"), ("8", "qwen7b-4bit_mf8")]
    xs, acc, lat, mem = [], [], [], []
    for n, rid in rows:
        mm = m(rid)
        if mm:
            xs.append(n)
            acc.append(mm["accuracy"])
            lat.append(mm["latency_p50_s"])
            mem.append(mm["peak_memory_gb"])
    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(11, 3.6))
    for ax_, ys, fmt, ylab, off in [(a1, acc, "{:.2f}", "정확도", 8),
                                    (a2, lat, "{:.1f}s", "지연 p50 (초)", 8),
                                    (a3, mem, "{:.1f}GB", "피크 메모리 (GB)", 8)]:
        ax_.plot(xs, ys, marker="o", color=BLUE, linewidth=2)
        for x, y in zip(xs, ys):
            ax_.annotate(fmt.format(y), (x, y), textcoords="offset points",
                         xytext=(0, off), fontsize=8, color=INK, ha="center")
        ax_.set_xlabel("입력 프레임 수")
        ax_.set_ylabel(ylab)
        ax_.set_ylim(0, max(ys) * 1.35)
    a1.set_ylim(0, 1)
    fig.suptitle("다중 프레임 입력 — Qwen2.5-VL-7B 4bit, 프레임 max-side 448 통일 "
                 "(M4 Max, 상대 비교 전용)", color=INK, fontsize=10)
    save(fig, "fig3_multiframe.png")


# ---------------------------------------------------------------- fig 4
def fig_confusion(run_id="qwen7b-4bit_zs_p1"):
    from common import CLASS_IDS, SHORT
    mm = m(run_id)
    if not mm:
        return
    conf = mm["confusion"]
    n = len(CLASS_IDS)
    grid = [[conf.get(f"{t}->{p}", 0) for p in CLASS_IDS] for t in CLASS_IDS]
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("seqblue", ["#ffffff"] + SEQ)
    im = ax.imshow(grid, cmap=cmap, vmin=0, vmax=25)
    ax.set_xticks(range(n), [SHORT[c] for c in CLASS_IDS], rotation=45, ha="right")
    ax.set_yticks(range(n), [SHORT[c] for c in CLASS_IDS])
    for i in range(n):
        for j in range(n):
            v = grid[i][j]
            if v:
                ax.text(j, i, str(v), ha="center", va="center", fontsize=8,
                        color="#ffffff" if v > 12 else INK)
    ax.set_xlabel("예측")
    ax.set_ylabel("정답")
    ax.set_title(f"혼동 행렬 — {run_id} (acc={mm['accuracy']:.3f})", color=INK, fontsize=10)
    ax.grid(False)
    fig.colorbar(im, ax=ax, shrink=0.8)
    save(fig, f"fig4_confusion_{run_id}.png")


# ---------------------------------------------------------------- fig 5
def fig_quant_delta():
    models = [("SmolVLM2-2.2B", "smolvlm2"), ("Qwen2.5-VL-3B", "qwen3b"),
              ("Qwen2.5-VL-7B", "qwen7b")]
    labels, bf16s, fourbits = [], [], []
    for name, pre in models:
        a, b = m(f"{pre}-bf16_zs_p1"), m(f"{pre}-4bit_zs_p1")
        if a and b:
            labels.append(name)
            bf16s.append(a["accuracy"])
            fourbits.append(b["accuracy"])
    x = range(len(labels))
    w = 0.36
    fig, ax = plt.subplots(figsize=(7, 4))
    b1 = ax.bar([i - w / 2 for i in x], bf16s, w * 0.94, color=ORANGE, label="bf16")
    b2 = ax.bar([i + w / 2 for i in x], fourbits, w * 0.94, color=BLUE, label="4bit")
    for bars in (b1, b2):
        for r in bars:
            ax.annotate(f"{r.get_height():.3f}", (r.get_x() + r.get_width() / 2,
                        r.get_height()), textcoords="offset points", xytext=(0, 3),
                        fontsize=8, color=INK, ha="center")
    ax.set_xticks(list(x), labels)
    ax.set_ylabel("동결 세트 정확도")
    ax.set_ylim(0, 1)
    ax.set_title("양자화(bf16→4bit)에 따른 정확도 변화 — 제로샷 p1", color=INK, fontsize=10)
    ax.legend(frameon=False)
    save(fig, "fig5_quant_delta.png")


if __name__ == "__main__":
    fig_size_accuracy()
    fig_latency()
    fig_multiframe()
    fig_confusion()
    fig_quant_delta()
