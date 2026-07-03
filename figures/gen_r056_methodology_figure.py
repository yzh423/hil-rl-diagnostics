from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

from paper_plot_style import COLORS, FIG_DIR


ROOT = Path(__file__).resolve().parents[1]
R056 = ROOT / "results" / "r056_methodology_extension"
FIG_STEM = "fig1_methodology_protocol_r056"

GATE_COLORS = {
    "G1": COLORS["random"],
    "G2": "#5A5A5A",
    "G3": COLORS["method"],
    "G4": COLORS["repair"],
}

VERDICT_LABELS = {
    "reject_trigger_superiority": "Reject claim",
    "ranking_auditable": "Audit ranking",
    "diagnose_budget_spending": "Diagnose spending",
    "stop_repair_expansion": "Stop repair",
}

GATE_EVIDENCE_LABELS = {
    "G1": "random_b350: +4.6 pp,\n25 fewer human steps",
    "G2": "500 evaluation episodes\nwith Wilson intervals",
    "G3": "96 vs 55 starts;\ncloser cube geometry",
    "G4": "score-floor: -8.7 pp,\n+158.3 human steps",
}

GATE_NAME_LABELS = {
    "G1": "Cost-matched\nrandom frontier",
    "G2": "Repeated checkpoint\nevaluation",
    "G3": "Trace-level attention\ndiagnosis",
    "G4": "Same-seed repair\nstop gate",
}

METRIC_LABELS = {
    "random_b350_success_margin_vs_lv_voi_pp": "Random success\nmargin (pp)",
    "random_b350_human_step_saving_vs_lv_voi": "Random human-step\nsaving",
    "lv_voi_start_inflation_vs_random": "LV-VoI start\ninflation",
    "score_floor_gap_closure_vs_random": "Score-floor gap\nclosure",
    "score_floor_success_gap_vs_random_pp": "Score-floor success\ngap (pp)",
}


def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def panel_label(ax, label):
    ax.text(
        0.0,
        1.04,
        f"({label})",
        transform=ax.transAxes,
        fontsize=9,
        fontweight="bold",
        ha="left",
        va="bottom",
    )


def rounded_box(ax, xy, width, height, title, subtitle, color, face="#FFFFFF"):
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.012,rounding_size=0.025",
        linewidth=1.0,
        edgecolor=color,
        facecolor=face,
        transform=ax.transAxes,
        clip_on=False,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height * 0.64,
        title,
        transform=ax.transAxes,
        fontsize=8.0,
        fontweight="bold",
        ha="center",
        va="center",
        color="#1F1F1F",
    )
    ax.text(
        xy[0] + width / 2,
        xy[1] + height * 0.30,
        subtitle,
        transform=ax.transAxes,
        fontsize=6.6,
        ha="center",
        va="center",
        color="#444444",
    )


def arrow(ax, start, end):
    patch = FancyArrowPatch(
        start,
        end,
        transform=ax.transAxes,
        arrowstyle="-|>",
        mutation_scale=9,
        linewidth=0.8,
        color="#555555",
        shrinkA=4,
        shrinkB=4,
    )
    ax.add_patch(patch)


def plot_protocol_flow(ax):
    ax.axis("off")
    ax.set_title("A diagnostic protocol for human-attention allocation claims", pad=5)
    y = 0.56
    w = 0.145
    h = 0.24
    xs = [0.03, 0.235, 0.44, 0.645, 0.835]
    boxes = [
        ("Claim + logs", "strategy, cost,\ntraces", "#555555"),
        ("G1 cost match", "random family\naround cost", GATE_COLORS["G1"]),
        ("G2 repeat eval", "success counts\n+ intervals", GATE_COLORS["G2"]),
        ("G3 trace diagnosis", "timing, budget,\ngeometry, score", GATE_COLORS["G3"]),
        ("Decision", "accept, stop,\nor redesign", GATE_COLORS["G4"]),
    ]
    for x, (title, subtitle, color) in zip(xs, boxes):
        rounded_box(ax, (x, y), w, h, title, subtitle, color)
    for i in range(len(xs) - 1):
        arrow(ax, (xs[i] + w, y + h / 2), (xs[i + 1], y + h / 2))

    ax.text(
        0.50,
        0.28,
        "Protocol rule: a trigger claim is supported only if it survives cost matching,\n"
        "repeated checkpoint evaluation, and trace-level budget diagnosis.",
        transform=ax.transAxes,
        fontsize=7.2,
        ha="center",
        va="center",
        color="#333333",
    )
    panel_label(ax, "a")


def plot_gate_outcomes(ax, gate_rows):
    ax.axis("off")
    ax.set_title("Case-study gate outcomes", pad=5)
    ax.text(0.04, 0.91, "Gate", transform=ax.transAxes, fontsize=6.6, color="#666666")
    ax.text(0.22, 0.91, "Protocol check", transform=ax.transAxes, fontsize=6.6, color="#666666", ha="center")
    ax.text(0.51, 0.91, "Evidence readout", transform=ax.transAxes, fontsize=6.6, color="#666666", ha="center")
    ax.text(0.80, 0.91, "Protocol verdict", transform=ax.transAxes, fontsize=6.6, color="#666666")
    y0 = 0.80
    row_h = 0.20
    for idx, row in enumerate(gate_rows):
        y = y0 - idx * row_h
        gate = row["gate_id"]
        color = GATE_COLORS.get(gate, "#555555")
        ax.add_patch(
            FancyBboxPatch(
                (0.02, y - 0.105),
                0.95,
                0.145,
                boxstyle="round,pad=0.008,rounding_size=0.015",
                linewidth=0.7,
                edgecolor="#B8B8B8",
                facecolor="#FFFFFF",
                transform=ax.transAxes,
            )
        )
        ax.text(
            0.055,
            y - 0.045,
            gate,
            transform=ax.transAxes,
            fontsize=7.8,
            fontweight="bold",
            color=color,
            ha="left",
            va="center",
        )
        ax.text(
            0.22,
            y - 0.045,
            GATE_NAME_LABELS.get(gate, row["gate"]),
            transform=ax.transAxes,
            fontsize=6.2,
            fontweight="bold",
            ha="center",
            va="center",
        )
        ax.text(
            0.51,
            y - 0.045,
            GATE_EVIDENCE_LABELS.get(gate, row["case_result"]),
            transform=ax.transAxes,
            fontsize=6.1,
            ha="center",
            va="center",
            color="#222222",
        )
        ax.text(
            0.80,
            y - 0.045,
            VERDICT_LABELS.get(row["verdict"], row["verdict"]),
            transform=ax.transAxes,
            fontsize=6.6,
            fontweight="bold",
            ha="center",
            va="center",
            color=color,
        )
    panel_label(ax, "b")


def metric_value(rows, metric):
    for row in rows:
        if row["metric"] == metric:
            return float(row["value"])
    raise ValueError(f"missing metric: {metric}")


def plot_derived_metrics(ax, metric_rows):
    metrics = [
        ("random_b350_success_margin_vs_lv_voi_pp", 4.6, "pp", COLORS["random"]),
        ("random_b350_human_step_saving_vs_lv_voi", 25.0, "steps", COLORS["random"]),
        ("lv_voi_start_inflation_vs_random", 1.745, "x", COLORS["method"]),
        ("score_floor_gap_closure_vs_random", 0.049, "fraction", COLORS["repair"]),
        ("score_floor_success_gap_vs_random_pp", -8.66, "pp", COLORS["repair"]),
    ]
    labels = [METRIC_LABELS[name] for name, _, _, _ in metrics]
    values = [metric_value(metric_rows, name) for name, _, _, _ in metrics]
    colors = [color for _, _, _, color in metrics]
    y = np.arange(len(metrics))

    ax.axvline(0, color="#777777", lw=0.8)
    for yi, value, color in zip(y, values, colors):
        ax.plot([0, value], [yi, yi], color=color, lw=1.4, alpha=0.75)
        ax.scatter(value, yi, s=34, color=color, edgecolor="white", linewidth=0.6, zorder=3)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlabel("Derived diagnostic value")
    ax.set_title("Derived stop-rule metrics", pad=5)
    ax.set_xlim(-12, 30)
    for yi, (name, _, unit, _), value in zip(y, metrics, values):
        if unit == "fraction":
            text = f"{value:.1%}"
        elif unit == "x":
            text = f"{value:.2f}x"
        elif unit == "steps":
            text = f"{value:.1f} steps"
        else:
            text = f"{value:+.1f} pp"
        ha = "left"
        offset = 0.8 if value >= 0 else 0.7
        ax.text(value + offset, yi, text, fontsize=6.8, va="center", ha=ha)
    panel_label(ax, "c")


def save_grayscale(png_path, gray_path):
    try:
        from PIL import Image
    except ImportError:
        return False
    Image.open(png_path).convert("L").save(gray_path)
    return True


def build_figure():
    plt.rcParams.update({
        "font.size": 8,
        "axes.labelsize": 8,
        "axes.titlesize": 8.5,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
    })
    gate_rows = read_csv(R056 / "protocol_gate_matrix.csv")
    metric_rows = read_csv(R056 / "derived_attention_metrics.csv")
    fig = plt.figure(figsize=(7.2, 5.65), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, height_ratios=[0.92, 1.45], width_ratios=[1.32, 1.0])
    plot_protocol_flow(fig.add_subplot(gs[0, :]))
    plot_gate_outcomes(fig.add_subplot(gs[1, 0]), gate_rows)
    plot_derived_metrics(fig.add_subplot(gs[1, 1]), metric_rows)
    return fig


def main():
    fig = build_figure()
    pdf_path = FIG_DIR / f"{FIG_STEM}.pdf"
    png_path = FIG_DIR / f"{FIG_STEM}.png"
    gray_path = FIG_DIR / f"{FIG_STEM}_grayscale.png"
    fig.savefig(pdf_path)
    fig.savefig(png_path, dpi=300)
    plt.close(fig)
    print(f"saved {pdf_path}")
    print(f"saved {png_path}")
    if save_grayscale(png_path, gray_path):
        print(f"saved {gray_path}")


if __name__ == "__main__":
    main()
