from __future__ import annotations

import csv
from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from paper_plot_style import COLORS, FIG_DIR

plt.rcParams.update({
    "font.size": 8,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
})


ROOT = Path(__file__).resolve().parents[1]
R021 = ROOT / "results" / "r021_random_costmatch"
R023 = ROOT / "results" / "r023_real_trace_seed0_2"
R029 = ROOT / "results" / "r029_protocol_hero"

LABELS = {
    "random_b350": "Random b350",
    "lv_voi_scale3": "LV-VoI scale3",
}


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pct(value):
    return float(value) * 100.0


def yerr(row):
    y = pct(row["repeated_success"])
    return [[y - pct(row["success_ci_low"])], [pct(row["success_ci_high"]) - y]]


def strategy_color(name):
    if name.startswith("random"):
        return COLORS["random"]
    return COLORS["method"]


def panel_label(ax, label):
    ax.text(-0.08, 1.03, label, transform=ax.transAxes,
            fontsize=11, fontweight="bold", ha="left", va="bottom")


def wrap(text, width):
    return "\n".join(textwrap.wrap(text, width=width))


def save_both(fig, stem):
    pdf = FIG_DIR / f"{stem}.pdf"
    png = FIG_DIR / f"{stem}.png"
    fig.savefig(pdf)
    fig.savefig(png, dpi=300)
    plt.close(fig)
    print(f"saved {pdf}")
    print(f"saved {png}")


def draw_protocol_panel(ax, checklist):
    ax.axis("off")
    y = 0.90
    dy = 0.185
    for row in checklist:
        gate = row["gate_id"]
        title = row["protocol_gate"]
        hero_text = row["hero_text"]
        color = COLORS["random"] if gate in ("G1", "G2") else COLORS["none"]
        box = FancyBboxPatch(
            (0.045, y - 0.125), 0.87, 0.125,
            boxstyle="round,pad=0.010,rounding_size=0.018",
            linewidth=0.8, edgecolor=color, facecolor="white",
            transform=ax.transAxes, clip_on=False,
        )
        ax.add_patch(box)
        ax.text(0.075, y - 0.043, gate, transform=ax.transAxes,
                color=color, fontsize=7.2, fontweight="bold",
                ha="left", va="center")
        ax.text(0.195, y - 0.043, title, transform=ax.transAxes,
                fontsize=6.8, fontweight="bold", ha="left", va="center")
        ax.text(0.195, y - 0.086, hero_text, transform=ax.transAxes,
                fontsize=6.1, color="#444444", ha="left", va="center")
        y -= dy
    panel_label(ax, "A")


def draw_cost_panel(ax):
    rows = read_csv(R021 / "r021_costmatch_aggregate.csv")
    wanted = ["random_b350", "lv_voi_scale3"]
    for name in wanted:
        row = next(r for r in rows if r["strategy"] == name)
        x = float(row["mean_best_human_steps"])
        y = pct(row["repeated_success"])
        ax.errorbar(x, y, yerr=yerr(row), fmt="o", markersize=6,
                    color=strategy_color(name), capsize=2.5, lw=1.2)
        if name == "random_b350":
            xytext = (151.5, 87.45)
            textcoords = "data"
            va = "top"
        else:
            xytext = (8, -16)
            textcoords = "offset points"
            va = "center"
        ax.annotate(
            f"{LABELS[name]}\n{y:.1f}%\n{x:.0f} steps",
            (x, y), xytext=xytext, textcoords=textcoords,
            fontsize=7, ha="left", va=va
        )
    ax.annotate(
        "higher success\nlower cost",
        xy=(177, 87.8), xytext=(205, 90.5),
        arrowprops=dict(arrowstyle="->", lw=0.9, color="#333333"),
        fontsize=7, ha="center", va="center",
    )
    ax.set_xlabel("Best-step human steps")
    ax.set_ylabel("Repeated success (%)")
    ax.set_xlim(150, 220)
    ax.set_ylim(78, 92)
    panel_label(ax, "B")


def draw_trace_panel(ax):
    rows = read_csv(R023 / "r023_trace_strategy_diagnostics.csv")
    wanted = ["random_b350", "lv_voi_scale3"]
    starts = [float(next(r for r in rows if r["strategy"] == name)["trace_starts"])
              for name in wanted]
    dists = [float(next(r for r in rows if r["strategy"] == name)["mean_g2c_norm"])
             for name in wanted]
    colors = [strategy_color(name) for name in wanted]
    x = [0, 1]
    bars = ax.bar(x, starts, width=0.55, color=colors, alpha=0.93)
    ax.set_xticks(x, ["Random\nb350", "LV-VoI\nscale3"])
    ax.set_ylabel("Intervention starts")
    ax.set_ylim(0, 110)
    for bar, val in zip(bars, starts):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 3,
                f"{int(val)}", ha="center", va="bottom", fontsize=7)

    ax2 = ax.twinx()
    ax2.plot(x, dists, color="#333333", marker="s", lw=1.2, ms=4)
    ax2.set_ylabel("Mean gripper-cube distance")
    ax2.set_ylim(0.16, 0.32)
    ax2.tick_params(axis="y", labelsize=8)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(True)
    ax.text(0.03, 0.08, "More starts,\ncloser to cube",
            transform=ax.transAxes, fontsize=7,
            bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="#777777", lw=0.6))
    panel_label(ax, "C")


def fig1_protocol_hero():
    checklist = read_csv(R029 / "protocol_checklist.csv")
    fig = plt.figure(figsize=(7.15, 5.15))
    gs = fig.add_gridspec(
        2, 2, height_ratios=[1.0, 1.08], hspace=0.42, wspace=0.36)
    draw_protocol_panel(fig.add_subplot(gs[0, :]), checklist)
    draw_cost_panel(fig.add_subplot(gs[1, 0]))
    draw_trace_panel(fig.add_subplot(gs[1, 1]))
    save_both(fig, "fig1_protocol_hero_r029")


def latex_escape(text):
    return str(text).replace("_", "\\_").replace("%", "\\%").replace("&", "\\&")


def table_protocol_checklist():
    rows = read_csv(R029 / "protocol_checklist.csv")
    lines = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Diagnostic protocol checklist for HIL-RL intervention-trigger claims. Each gate is motivated by a failure mode surfaced in the Lift/Stack case study.}",
        r"\label{tab:protocol_checklist}",
        r"\begin{tabular}{p{0.07\textwidth}p{0.19\textwidth}p{0.32\textwidth}p{0.33\textwidth}}",
        r"\toprule",
        r"Gate & Requirement & What to report & Why it matters \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(
            f"{latex_escape(row['gate_id'])} & "
            f"{latex_escape(row['protocol_gate'])} & "
            f"{latex_escape(row['required_report'])} & "
            f"{latex_escape(row['why_it_matters'])} \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    path = FIG_DIR / "TABLE_protocol_checklist.tex"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"saved {path}")


def latex_includes():
    text = r"""
% === R029 Fig. 1: Protocol-Centered Hero ===
\begin{figure*}[t]
    \centering
    \includegraphics[width=0.95\textwidth]{figures/fig1_protocol_hero_r029.pdf}
    \caption{Diagnostic protocol for HIL-RL intervention-trigger claims. The protocol requires cost-matched random families, repeated checkpoint evaluation, best/final policy accounting, trace-level intervention diagnostics, and a same-seed stop gate before expansion. Applied to robosuite Lift, it reverses an initially plausible LV-VoI conclusion: \texttt{random\_b350} achieves higher repeated success at lower best-step human cost than LV-VoI scale3. Trace diagnostics show that LV-VoI starts more interventions while starting closer to the cube, rejecting a simple far-from-object explanation.}
    \label{fig:protocol_hero}
\end{figure*}

% === R029 Table: Protocol Checklist ===
\input{figures/TABLE_protocol_checklist.tex}
"""
    path = FIG_DIR / "latex_includes_r029.tex"
    path.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"saved {path}")


def main():
    fig1_protocol_hero()
    table_protocol_checklist()
    latex_includes()


if __name__ == "__main__":
    main()
