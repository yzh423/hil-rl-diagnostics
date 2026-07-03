from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

from paper_plot_style import COLORS, FIG_DIR


ROOT = Path(__file__).resolve().parents[1]
R021 = ROOT / "results" / "r021_random_costmatch"
R023 = ROOT / "results" / "r023_real_trace_seed0_2"
R024 = ROOT / "results" / "r024_score_floor_seed0_2"
R054 = ROOT / "results" / "r054_attention_allocation_figure_optimization"

FIG_STEM = "fig_attention_allocation_diagnostics_r054"

STRATEGY_LABELS = {
    "none": "No intervention",
    "random_b350": "Random b350",
    "random_b450": "Random b450",
    "random_b600": "Random b600",
    "lv_voi_scale3": "LV-VoI scale3",
    "min_disagree_vlv0p25": "Min-disagree LV-VoI",
    "score_floor_vlv3_after4000_floor0p05": "Score-floor LV-VoI",
}

SHORT_LABELS = {
    "random_b350": "Random\nb350",
    "lv_voi_scale3": "LV-VoI\nscale3",
    "score_floor_vlv3_after4000_floor0p05": "Score-floor\nLV-VoI",
}

TRACE_SPECS = (
    (
        "random_b350",
        R023,
        "trace_Lift_random_b350_seed*.csv",
        "R023 random_b350 traces",
    ),
    (
        "lv_voi_scale3",
        R023,
        "trace_Lift_voi_b600_seed*.csv",
        "R023 LV-VoI scale3 traces",
    ),
    (
        "score_floor_vlv3_after4000_floor0p05",
        R024,
        "trace_Lift_voi_b600_seed*.csv",
        "R024 score-floor LV-VoI traces",
    ),
)

ORDER_TRACE = [
    "random_b350",
    "lv_voi_scale3",
    "score_floor_vlv3_after4000_floor0p05",
]


def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, rows):
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def as_float(value):
    text = str(value).strip()
    if text == "" or text.lower() == "nan":
        return math.nan
    try:
        return float(text)
    except ValueError:
        return math.nan


def finite(values):
    return np.asarray([v for v in values if np.isfinite(v)], dtype=float)


def pct(value):
    return float(value) * 100.0


def strategy_color(strategy):
    if strategy == "none":
        return COLORS["none"]
    if strategy.startswith("random"):
        return COLORS["random"]
    if "floor" in strategy or "disagree" in strategy:
        return COLORS["repair"]
    return COLORS["method"]


def lighten(hex_color, amount=0.58):
    color = hex_color.lstrip("#")
    rgb = np.asarray([int(color[i:i + 2], 16) for i in (0, 2, 4)], dtype=float)
    mixed = rgb + (255 - rgb) * amount
    return "#" + "".join(f"{int(round(x)):02x}" for x in mixed)


def panel_label(ax, label):
    ax.text(
        -0.12,
        1.07,
        f"({label})",
        transform=ax.transAxes,
        fontsize=9,
        fontweight="bold",
        ha="left",
        va="bottom",
    )


def collect_trace_rows():
    traces = []
    for strategy, root, pattern, source_label in TRACE_SPECS:
        files = sorted(root.glob(pattern))
        if not files:
            raise FileNotFoundError(f"no trace files for {strategy}: {root / pattern}")
        for path in files:
            for row in read_csv(path):
                trace_row = dict(row)
                trace_row["diagnostic_strategy"] = strategy
                trace_row["source_label"] = source_label
                traces.append(trace_row)
    return traces


def rows_for(traces, strategy):
    return [row for row in traces if row["diagnostic_strategy"] == strategy]


def values(rows, column):
    return finite(as_float(row.get(column, "")) for row in rows)


def quantile_text(vals):
    if len(vals) == 0:
        return ""
    q1, med, q3 = np.percentile(vals, [25, 50, 75])
    return f"{med:.4f} [{q1:.4f}, {q3:.4f}]"


def trace_profile_rows(traces):
    profile_rows = []
    for strategy in ORDER_TRACE:
        group = rows_for(traces, strategy)
        steps = values(group, "env_step")
        budgets = values(group, "budget_used_frac")
        norm = values(group, "gripper_to_cube_norm")
        xy = values(group, "gripper_to_cube_xy")
        eef_z = values(group, "eef_z")
        cube_z = values(group, "cube_z")
        score = values(group, "score")
        p_fail = values(group, "p_fail")
        eef_gap = eef_z - cube_z if len(eef_z) == len(cube_z) else np.asarray([])

        n = len(group)
        early = float(np.mean(steps < 2000)) if len(steps) else math.nan
        mid = float(np.mean((steps >= 2000) & (steps < 6000))) if len(steps) else math.nan
        late = float(np.mean(steps >= 6000)) if len(steps) else math.nan

        profile_rows.append({
            "strategy": strategy,
            "display_label": STRATEGY_LABELS[strategy],
            "n_trace_starts": n,
            "mean_start_step": f"{np.mean(steps):.3f}" if len(steps) else "",
            "median_start_step": f"{np.median(steps):.3f}" if len(steps) else "",
            "early_0_2k_frac": f"{early:.6f}" if np.isfinite(early) else "",
            "mid_2_6k_frac": f"{mid:.6f}" if np.isfinite(mid) else "",
            "late_6_10k_frac": f"{late:.6f}" if np.isfinite(late) else "",
            "budget_used_frac_median_iqr": quantile_text(budgets),
            "g2c_norm_median_iqr": quantile_text(norm),
            "g2c_xy_median_iqr": quantile_text(xy),
            "eef_z_median_iqr": quantile_text(eef_z),
            "cube_z_median_iqr": quantile_text(cube_z),
            "eef_minus_cube_z_median_iqr": quantile_text(eef_gap),
            "score_median_iqr": quantile_text(score),
            "score_ge_9p9_frac": (
                f"{float(np.mean(score >= 9.9)):.6f}" if len(score) else ""
            ),
            "p_fail_median_iqr": quantile_text(p_fail),
            "p_fail_ge_0p99_frac": (
                f"{float(np.mean(p_fail >= 0.99)):.6f}" if len(p_fail) else ""
            ),
        })
    return profile_rows


def plot_relative_costmatch(ax):
    rows = read_csv(R021 / "r021_costmatch_aggregate.csv")
    lv = next(row for row in rows if row["strategy"] == "lv_voi_scale3")
    lv_success = pct(lv["repeated_success"])
    lv_cost = float(lv["mean_best_human_steps"])
    order = ["none", "random_b350", "lv_voi_scale3", "random_b450", "random_b600"]

    ax.axhline(0, color="#777777", lw=0.8, zorder=1)
    ax.axvline(0, color="#777777", lw=0.8, zorder=1)
    ax.fill_between(
        [-230, 0],
        [0, 0],
        [6.2, 6.2],
        color=lighten(COLORS["random"], 0.78),
        alpha=0.8,
        zorder=0,
    )
    ax.text(
        -210,
        5.25,
        "dominates\nLV-VoI",
        fontsize=7,
        color="#244a61",
        ha="left",
        va="top",
    )
    offsets = {
        "none": (5, -10),
        "random_b350": (7, 6),
        "lv_voi_scale3": (7, -12),
        "random_b450": (-50, 6),
        "random_b600": (5, -13),
    }
    for strategy in order:
        row = next(r for r in rows if r["strategy"] == strategy)
        x = float(row["mean_best_human_steps"]) - lv_cost
        y = pct(row["repeated_success"]) - lv_success
        size = 48 if strategy == "random_b350" else 34
        ax.scatter(
            x,
            y,
            s=size,
            marker="o" if strategy != "lv_voi_scale3" else "D",
            color=strategy_color(strategy),
            edgecolor="white",
            linewidth=0.6,
            zorder=3,
        )
        ax.annotate(
            STRATEGY_LABELS[strategy].replace(" ", "\n", 1),
            (x, y),
            xytext=offsets[strategy],
            textcoords="offset points",
            fontsize=6.5,
            ha="left",
        )
    ax.set_xlim(-230, 85)
    ax.set_ylim(-4.5, 6.2)
    ax.set_xlabel("Human-step change vs LV-VoI")
    ax.set_ylabel("Success change vs LV-VoI (pp)")
    ax.set_title("Cost matching flips the allocation claim", pad=6)
    panel_label(ax, "a")


def plot_repair_stop_gate(ax):
    rows = read_csv(R024 / "r024_score_floor_aggregate.csv")
    baseline = next(row for row in rows if row["strategy"] == "random_b350")
    base_success = pct(baseline["repeated_success"])
    base_cost = float(baseline["mean_best_human_steps"])
    order = [
        "random_b350",
        "min_disagree_vlv0p25",
        "score_floor_vlv3_after4000_floor0p05",
    ]

    ax.axhline(0, color="#777777", lw=0.8, zorder=1)
    ax.axvline(0, color="#777777", lw=0.8, zorder=1)
    ax.fill_between(
        [0, 175],
        [-13, -13],
        [0, 0],
        color=lighten(COLORS["method"], 0.82),
        alpha=0.8,
        zorder=0,
    )
    ax.text(
        78,
        -3.0,
        "dominated by\nsame-seed random",
        fontsize=7,
        color="#7b3a00",
        ha="left",
        va="top",
    )
    offsets = {
        "random_b350": (7, 6),
        "min_disagree_vlv0p25": (-92, -12),
        "score_floor_vlv3_after4000_floor0p05": (-70, 8),
    }
    for strategy in order:
        row = next(r for r in rows if r["strategy"] == strategy)
        x = float(row["mean_best_human_steps"]) - base_cost
        y = pct(row["repeated_success"]) - base_success
        ax.scatter(
            x,
            y,
            s=44 if strategy == "random_b350" else 36,
            color=strategy_color(strategy),
            edgecolor="white",
            linewidth=0.6,
            zorder=3,
        )
        label = {
            "random_b350": "Random b350",
            "min_disagree_vlv0p25": "Min-disagree\nLV-VoI",
            "score_floor_vlv3_after4000_floor0p05": "Score-floor\nLV-VoI",
        }[strategy]
        ax.annotate(
            label,
            (x, y),
            xytext=offsets[strategy],
            textcoords="offset points",
            fontsize=6.5,
            ha="left",
        )
    ax.set_xlim(-12, 175)
    ax.set_ylim(-13, 2.5)
    ax.set_xlabel("Human-step change vs random b350")
    ax.set_ylabel("Success change vs random b350 (pp)")
    ax.set_title("Lightweight repairs remain dominated", pad=6)
    panel_label(ax, "b")


def plot_timing_raster(ax, traces):
    y_positions = {
        "random_b350": 2,
        "lv_voi_scale3": 1,
        "score_floor_vlv3_after4000_floor0p05": 0,
    }
    seed_jitter = {"0": -0.13, "1": 0.0, "2": 0.13}
    for strategy in ORDER_TRACE:
        group = rows_for(traces, strategy)
        x = [as_float(row["env_step"]) for row in group]
        y = [
            y_positions[strategy] + seed_jitter.get(str(row["seed"]).strip(), 0.0)
            for row in group
        ]
        ax.scatter(
            x,
            y,
            marker="|",
            s=95,
            linewidth=1.0,
            color=strategy_color(strategy),
            alpha=0.72,
        )
        ax.text(
            10180,
            y_positions[strategy],
            f"n={len(group)}",
            fontsize=7,
            ha="left",
            va="center",
        )
    ax.axvline(4000, color="#777777", lw=0.8, ls="--")
    ax.text(4100, -0.42, "score floor active", fontsize=6.5, ha="left")
    ax.set_xlim(-250, 10800)
    ax.set_ylim(-0.55, 2.55)
    ax.set_yticks(
        [0, 1, 2],
        [
            SHORT_LABELS["score_floor_vlv3_after4000_floor0p05"],
            SHORT_LABELS["lv_voi_scale3"],
            SHORT_LABELS["random_b350"],
        ],
    )
    ax.set_xlabel("Training step at intervention start")
    ax.set_ylabel("Strategy")
    ax.set_title("Starts concentrate after the gate opens", pad=6)
    panel_label(ax, "c")


def plot_budget_distribution(ax, traces):
    positions = np.arange(len(ORDER_TRACE))
    data = [values(rows_for(traces, strategy), "budget_used_frac") for strategy in ORDER_TRACE]
    box = ax.boxplot(
        data,
        positions=positions,
        widths=0.48,
        showfliers=False,
        patch_artist=True,
        medianprops={"color": "#222222", "lw": 1.1},
        whiskerprops={"color": "#555555", "lw": 0.8},
        capprops={"color": "#555555", "lw": 0.8},
    )
    for patch, strategy in zip(box["boxes"], ORDER_TRACE):
        patch.set_facecolor(lighten(strategy_color(strategy), 0.72))
        patch.set_edgecolor(strategy_color(strategy))
        patch.set_linewidth(0.9)
    rng = np.random.default_rng(54)
    for pos, strategy, vals in zip(positions, ORDER_TRACE, data):
        jitter = rng.uniform(-0.14, 0.14, size=len(vals))
        ax.scatter(
            np.full(len(vals), pos) + jitter,
            vals,
            s=8,
            color=strategy_color(strategy),
            alpha=0.32,
            edgecolors="none",
        )
    ax.set_xticks(positions, [SHORT_LABELS[s] for s in ORDER_TRACE])
    ax.set_ylim(-0.03, 1.03)
    ax.set_ylabel("Budget used at start")
    ax.set_title("Budget fraction distribution", pad=6)
    panel_label(ax, "d")


def iqr_error(values_array):
    if len(values_array) == 0:
        return math.nan, [[0], [0]]
    q1, med, q3 = np.percentile(values_array, [25, 50, 75])
    return med, [[med - q1], [q3 - med]]


def plot_geometry_summary(ax, traces):
    positions = np.arange(len(ORDER_TRACE))
    norm_offset = -0.08
    xy_offset = 0.08
    for pos, strategy in zip(positions, ORDER_TRACE):
        color = strategy_color(strategy)
        group = rows_for(traces, strategy)
        norm = values(group, "gripper_to_cube_norm")
        xy = values(group, "gripper_to_cube_xy")
        norm_med, norm_err = iqr_error(norm)
        xy_med, xy_err = iqr_error(xy)
        ax.errorbar(
            pos + norm_offset,
            norm_med,
            yerr=norm_err,
            fmt="o",
            ms=5,
            color=color,
            capsize=2,
            lw=1.0,
        )
        ax.errorbar(
            pos + xy_offset,
            xy_med,
            yerr=xy_err,
            fmt="^",
            ms=5,
            color=color,
            mfc="white",
            capsize=2,
            lw=1.0,
        )
    ax.set_xticks(positions, [SHORT_LABELS[s] for s in ORDER_TRACE])
    ax.set_ylim(0.0, 0.36)
    ax.set_ylabel("Gripper-cube distance")
    legend_handles = [
        Line2D([0], [0], marker="o", color="#444444", lw=0, label="3D norm"),
        Line2D([0], [0], marker="^", color="#444444", lw=0, mfc="white",
               label="XY distance"),
    ]
    ax.legend(handles=legend_handles, frameon=False, loc="upper right", fontsize=7)
    ax.set_title("Geometry rejects a far-from-cube story", pad=6)
    panel_label(ax, "e")


def plot_score_pfail(ax, traces):
    for strategy, marker in [
        ("lv_voi_scale3", "o"),
        ("score_floor_vlv3_after4000_floor0p05", "^"),
    ]:
        group = rows_for(traces, strategy)
        score = values(group, "score")
        p_fail = values(group, "p_fail")
        keep = np.isfinite(score) & np.isfinite(p_fail) & (score > 0)
        ax.scatter(
            score[keep],
            p_fail[keep],
            s=16,
            marker=marker,
            color=strategy_color(strategy),
            alpha=0.62,
            edgecolors="white",
            linewidths=0.25,
            label=STRATEGY_LABELS[strategy],
        )
    ax.axvline(0.05, color=COLORS["warning"], lw=0.9, ls=":", label="score floor")
    ax.axvline(9.9, color="#555555", lw=0.8, ls="--")
    ax.axhline(0.99, color="#555555", lw=0.8, ls="--")
    ax.text(10.15, 0.93, "clip region", fontsize=6.5, ha="left", va="top")
    ax.set_xscale("log")
    ax.set_xlim(0.035, 13)
    ax.set_ylim(-0.04, 1.05)
    ax.set_xlabel("LV-VoI score at start (log scale)")
    ax.set_ylabel("Predicted failure probability")
    ax.legend(frameon=False, loc="lower right", fontsize=6.6)
    ax.set_title("Scores expose calibration stress", pad=6)
    panel_label(ax, "f")


def save_grayscale(png_path, gray_path):
    try:
        from PIL import Image
    except ImportError:
        return False
    image = Image.open(png_path).convert("L")
    image.save(gray_path)
    return True


def build_figure(traces):
    plt.rcParams.update({
        "font.size": 8,
        "axes.labelsize": 8,
        "axes.titlesize": 8.5,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
    })
    fig, axes = plt.subplots(
        3,
        2,
        figsize=(7.2, 6.9),
        constrained_layout=True,
    )
    plot_relative_costmatch(axes[0, 0])
    plot_repair_stop_gate(axes[0, 1])
    plot_timing_raster(axes[1, 0], traces)
    plot_budget_distribution(axes[1, 1], traces)
    plot_geometry_summary(axes[2, 0], traces)
    plot_score_pfail(axes[2, 1], traces)
    return fig


def main():
    R054.mkdir(parents=True, exist_ok=True)
    traces = collect_trace_rows()

    profile_path = R054 / "attention_allocation_trace_profile.csv"
    profile_rows = trace_profile_rows(traces)
    write_csv(profile_path, list(profile_rows[0].keys()), profile_rows)
    print(f"saved {profile_path}")

    fig = build_figure(traces)
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
