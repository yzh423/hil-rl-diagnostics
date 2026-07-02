from __future__ import annotations

import csv
import glob
from pathlib import Path
from textwrap import shorten

import numpy as np
import matplotlib.pyplot as plt

from paper_plot_style import COLORS, FIG_DIR, save_fig


ROOT = Path(__file__).resolve().parents[1]
R021 = ROOT / "results" / "r021_random_costmatch"
R024 = ROOT / "results" / "r024_score_floor_seed0_2"
R025 = ROOT / "results" / "r025_paper_pivot"


LABELS = {
    "none": "No intervention",
    "random_b350": "Random b350",
    "random_b450": "Random b450",
    "random_b600": "Random b600",
    "lv_voi_scale3": "LV-VoI scale3",
    "score_floor_vlv3_after4000_floor0p05": "Score-floor LV-VoI",
    "min_disagree_vlv0p25": "Min-disagree LV-VoI",
}

SHORT_LABELS = {
    "random_b350": "Random\nb350",
    "lv_voi_scale3": "LV-VoI\nscale3",
    "score_floor_vlv3_after4000_floor0p05": "Score-floor\nLV-VoI",
}


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pct(x):
    return float(x) * 100.0


def ci_yerr(row):
    y = pct(row["repeated_success"])
    return [[y - pct(row["success_ci_low"])], [pct(row["success_ci_high"]) - y]]


def strategy_color(name):
    if name == "none":
        return COLORS["none"]
    if name.startswith("random"):
        return COLORS["random"]
    if "min_disagree" in name or "score_floor" in name:
        return COLORS["repair"]
    return COLORS["method"]


def add_panel_label(ax, label):
    ax.text(-0.12, 1.04, label, transform=ax.transAxes, fontsize=11,
            fontweight="bold", va="bottom", ha="left")


def fig1_hero():
    cost_rows = read_csv(R021 / "r021_costmatch_aggregate.csv")
    trace_rows = read_csv(R024 / "r024_trace_strategy_compare.csv")
    fig = plt.figure(figsize=(7.2, 2.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.1, 1.15, 1.05], wspace=0.58)

    ax0 = fig.add_subplot(gs[0, 0])
    ax0.axis("off")
    boxes = [
        ("Train SAC+BC", 0.78),
        ("Trigger intervention", 0.53),
        ("Cost-match random", 0.28),
        ("Repeat checkpoint eval", 0.03),
    ]
    for text, y in boxes:
        ax0.text(0.5, y, text, ha="center", va="bottom",
                 bbox=dict(boxstyle="round,pad=0.28", fc="white", ec="#555555", lw=0.8),
                 fontsize=8)
        if y > 0.03:
            ax0.annotate("", xy=(0.5, y - 0.07), xytext=(0.5, y - 0.16),
                         arrowprops=dict(arrowstyle="->", lw=0.8, color="#555555"))
    add_panel_label(ax0, "A")

    ax1 = fig.add_subplot(gs[0, 1])
    for row in cost_rows:
        name = row["strategy"]
        if name not in ("none", "random_b350", "lv_voi_scale3"):
            continue
        x = float(row["mean_best_human_steps"])
        y = pct(row["repeated_success"])
        ax1.errorbar(x, y, yerr=ci_yerr(row), fmt="o", ms=5,
                     color=strategy_color(name), capsize=2)
        offset = {
            "none": (4, 2),
            "random_b350": (4, 5),
            "lv_voi_scale3": (4, -10),
        }[name]
        ax1.annotate(LABELS[name], (x, y), xytext=offset,
                     textcoords="offset points", fontsize=7)
    ax1.set_xlabel("Human steps")
    ax1.set_ylabel("Success (%)")
    ax1.set_xlim(-15, 230)
    ax1.set_ylim(74, 92)
    add_panel_label(ax1, "B")

    ax2 = fig.add_subplot(gs[0, 2])
    wanted = ["random_b350", "lv_voi_scale3", "score_floor_vlv3_after4000_floor0p05"]
    values = []
    labels = []
    colors = []
    for name in wanted:
        row = next(r for r in trace_rows if r["strategy"] == name)
        values.append(float(row["trace_starts"]))
        labels.append(SHORT_LABELS.get(name, LABELS[name]))
        colors.append(strategy_color(name))
    ax2.bar(range(len(values)), values, color=colors)
    ax2.set_xticks(range(len(values)), labels, rotation=0)
    ax2.tick_params(axis="x", labelsize=7)
    ax2.text(0.03, 0.96, "Starts", transform=ax2.transAxes,
             ha="left", va="top", fontsize=8)
    add_panel_label(ax2, "C")
    save_fig(fig, "fig1_hero_diagnostic_summary")


def fig2_cost_matched_frontier():
    rows = read_csv(R021 / "r021_costmatch_aggregate.csv")
    fig, ax = plt.subplots(figsize=(3.55, 2.65))
    order = ["none", "random_b350", "lv_voi_scale3", "random_b450", "random_b600"]
    for name in order:
        row = next(r for r in rows if r["strategy"] == name)
        x = float(row["mean_best_human_steps"])
        y = pct(row["repeated_success"])
        ax.errorbar(x, y, yerr=ci_yerr(row), fmt="o", ms=5,
                    color=strategy_color(name), capsize=2)
        offsets = {
            "none": (4, 0),
            "random_b350": (4, 5),
            "lv_voi_scale3": (4, -13),
            "random_b450": (-42, -13),
            "random_b600": (7, 8),
        }
        ax.annotate(LABELS[name], (x, y), xytext=offsets[name],
                    textcoords="offset points", fontsize=6.8)
    ax.set_xlabel("Mean best-step human steps")
    ax.set_ylabel("Repeated success (%)")
    ax.set_xlim(-20, 290)
    ax.set_ylim(75, 92)
    save_fig(fig, "fig2_cost_matched_frontier")


def fig3_trigger_repairs():
    rows = read_csv(R024 / "r024_score_floor_aggregate.csv")
    order = ["random_b350", "min_disagree_vlv0p25", "score_floor_vlv3_after4000_floor0p05"]
    fig, ax = plt.subplots(figsize=(3.55, 2.65))
    for name in order:
        row = next(r for r in rows if r["strategy"] == name)
        x = float(row["mean_best_human_steps"])
        y = pct(row["repeated_success"])
        ax.errorbar(x, y, yerr=ci_yerr(row), fmt="o", ms=5,
                    color=strategy_color(name), capsize=2)
        ax.annotate(LABELS[name], (x, y), xytext=(4, 3),
                    textcoords="offset points", fontsize=7)
    ax.set_xlabel("Mean best-step human steps")
    ax.set_ylabel("Repeated success (%)")
    ax.set_xlim(60, 280)
    ax.set_ylim(68, 91)
    save_fig(fig, "fig3_trigger_repairs")


def fig4_intervention_timing():
    rows = read_csv(R024 / "r024_trace_time_bins_compare.csv")
    labels = ["0-2000", "2000-4000", "4000-6000", "6000-8000", "8000-10000"]
    order = ["random_b350", "lv_voi_scale3", "score_floor_vlv3_after4000_floor0p05"]
    x = np.arange(len(labels))
    width = 0.25
    fig, ax = plt.subplots(figsize=(4.9, 2.75))
    for i, name in enumerate(order):
        vals = []
        for label in labels:
            row = next(r for r in rows if r["strategy"] == name and r["bin"] == label)
            vals.append(pct(row["fraction"]))
        ax.bar(x + (i - 1) * width, vals, width, label=LABELS[name],
               color=strategy_color(name), alpha=0.92)
    ax.set_xlabel("Training step window")
    ax.set_ylabel("Starts (%)")
    ax.set_xticks(x, labels, rotation=20)
    ax.legend(frameon=False, ncols=1, loc="upper right")
    save_fig(fig, "fig4_intervention_timing")


def fig5_score_over_time():
    trace_rows = []
    for path in glob.glob(str(R024 / "trace_Lift_voi_b600_seed*.csv")):
        trace_rows.extend(read_csv(Path(path)))

    fig, ax = plt.subplots(figsize=(4.9, 2.75))
    for seed in sorted({r["seed"] for r in trace_rows}, key=int):
        rows = [r for r in trace_rows if r["seed"] == seed]
        ax.scatter([float(r["env_step"]) for r in rows],
                   [float(r["score"]) for r in rows],
                   s=16, alpha=0.75, label=f"seed {seed}")
    ax.axvline(4000, color="#333333", linestyle="--", lw=0.9)
    ax.axhline(0.05, color=COLORS["warning"], linestyle=":", lw=1.1)
    ax.text(4050, 0.065, "floor active", fontsize=7, color="#333333")
    ax.set_yscale("log")
    ax.set_ylim(0.03, 20.0)
    ax.set_xlabel("Training step")
    ax.set_ylabel("VoI score at start")
    ax.legend(frameon=False, ncols=3, loc="upper center", bbox_to_anchor=(0.5, 1.15))
    save_fig(fig, "fig5_score_over_time")


def latex_escape(text):
    return str(text).replace("_", "\\_").replace("%", "\\%")


def table_main_results():
    rows = read_csv(R021 / "r021_costmatch_aggregate.csv")
    order = ["none", "random_b350", "lv_voi_scale3", "random_b450", "random_b600"]
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Cost-matched Lift results with repeated checkpoint evaluation. Success is aggregated over five seeds with $5\times20$ episodes per seed.}",
        r"\label{tab:cost_matched_lift}",
        r"\begin{tabular}{lcccc}",
        r"\toprule",
        r"Strategy & Success & 95\% CI & Human steps & $\Delta$ vs. LV-VoI \\",
        r"\midrule",
    ]
    for name in order:
        row = next(r for r in rows if r["strategy"] == name)
        success = f"{pct(row['repeated_success']):.1f}\\%"
        ci = f"[{pct(row['success_ci_low']):.1f}, {pct(row['success_ci_high']):.1f}]"
        cost = f"{float(row['mean_best_human_steps']):.1f}"
        delta = row.get("delta_success_vs_lvvoi_pp", "")
        delta = "--" if delta == "" else f"{float(delta):+.1f} pp"
        label = r"\textbf{" + LABELS[name] + "}" if name == "random_b350" else LABELS[name]
        lines.append(f"{label} & {success} & {ci} & {cost} & {delta} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    (FIG_DIR / "TABLE_main_costmatched_results.tex").write_text("\n".join(lines), encoding="utf-8")


def table_negative_findings():
    rows = read_csv(R025 / "negative_findings_table.csv")
    lines = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Negative trigger findings. Each hypothesis was stopped once it remained dominated by cost-matched baselines or failed the diagnostic test.}",
        r"\label{tab:negative_findings}",
        r"\begin{tabular}{p{0.10\textwidth}p{0.31\textwidth}p{0.34\textwidth}p{0.17\textwidth}}",
        r"\toprule",
        r"ID & Hypothesis & Observed result & Decision \\",
        r"\midrule",
    ]
    for row in rows:
        hypothesis = latex_escape(shorten(row["hypothesis"], width=95, placeholder="..."))
        observed = latex_escape(shorten(row["observed_result"], width=105, placeholder="..."))
        decision = latex_escape(row["decision"])
        lines.append(f"{latex_escape(row['finding_id'])} & {hypothesis} & {observed} & {decision} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    (FIG_DIR / "TABLE_negative_findings.tex").write_text("\n".join(lines), encoding="utf-8")


def table_trace_diagnostics():
    rows = read_csv(R024 / "r024_trace_strategy_compare.csv")
    order = ["random_b350", "lv_voi_scale3", "score_floor_vlv3_after4000_floor0p05"]
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Intervention-start diagnostics on Lift seeds 0--2.}",
        r"\label{tab:trace_diagnostics}",
        r"\begin{tabular}{lcccc}",
        r"\toprule",
        r"Strategy & Starts & Early & Mid & Mean $d_{g,c}$ \\",
        r"\midrule",
    ]
    for name in order:
        row = next(r for r in rows if r["strategy"] == name)
        starts = int(float(row["trace_starts"]))
        early = f"{pct(row['early_0_2k_frac']):.1f}\\%"
        mid = f"{pct(row['mid_2_6k_frac']):.1f}\\%"
        dist = f"{float(row['mean_g2c_norm']):.3f}"
        lines.append(f"{LABELS[name]} & {starts} & {early} & {mid} & {dist} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    (FIG_DIR / "TABLE_trace_diagnostics.tex").write_text("\n".join(lines), encoding="utf-8")


def latex_includes():
    text = r"""
% === Fig. 1: Diagnostic Summary ===
\begin{figure*}[t]
    \centering
    \includegraphics[width=0.95\textwidth]{figures/fig1_hero_diagnostic_summary.pdf}
    \caption{Diagnostic evaluation pipeline and main failure pattern. Cost matching reverses the initially promising LV-VoI result, and trace diagnostics reveal over-triggering rather than simple far-from-object intervention.}
    \label{fig:diagnostic_summary}
\end{figure*}

% === Fig. 2: Cost-Matched Frontier ===
\begin{figure}[t]
    \centering
    \includegraphics[width=0.48\textwidth]{figures/fig2_cost_matched_frontier.pdf}
    \caption{Cost-matched Lift frontier over five seeds. The lower-budget random baseline dominates LV-VoI scale3 in both repeated success and best-step human cost.}
    \label{fig:cost_matched_frontier}
\end{figure}

% === Fig. 3: Trigger Repairs ===
\begin{figure}[t]
    \centering
    \includegraphics[width=0.48\textwidth]{figures/fig3_trigger_repairs.pdf}
    \caption{Two intuitive trigger repairs remain dominated by same-seed random intervention.}
    \label{fig:trigger_repairs}
\end{figure}

% === Fig. 4: Intervention Timing ===
\begin{figure}[t]
    \centering
    \includegraphics[width=0.95\textwidth]{figures/fig4_intervention_timing.pdf}
    \caption{Intervention-start timing distribution. LV-VoI variants concentrate starts in the mid-run window and use more starts than random.}
    \label{fig:intervention_timing}
\end{figure}

% === Fig. 5: Score Over Time ===
\begin{figure}[t]
    \centering
    \includegraphics[width=0.95\textwidth]{figures/fig5_score_over_time.pdf}
    \caption{R024 score-floor diagnostics. The floor blocks sub-threshold starts after step 4000, but accepted scores remain frequent enough to consume nearly the full budget.}
    \label{fig:score_over_time}
\end{figure}
"""
    (FIG_DIR / "latex_includes.tex").write_text(text.strip() + "\n", encoding="utf-8")


def manifest():
    files = [
        "fig1_hero_diagnostic_summary.pdf",
        "fig2_cost_matched_frontier.pdf",
        "fig3_trigger_repairs.pdf",
        "fig4_intervention_timing.pdf",
        "fig5_score_over_time.pdf",
        "TABLE_main_costmatched_results.tex",
        "TABLE_negative_findings.tex",
        "TABLE_trace_diagnostics.tex",
        "latex_includes.tex",
        "gen_r026_paper_figures.py",
        "paper_plot_style.py",
    ]
    lines = ["# R026 Figure/Table Manifest", "", "| File | Purpose |", "|---|---|"]
    purposes = {
        "fig1_hero_diagnostic_summary.pdf": "Draft hero diagnostic summary.",
        "fig2_cost_matched_frontier.pdf": "Five-seed cost-matched success-cost frontier.",
        "fig3_trigger_repairs.pdf": "R022/R024 trigger repair comparison.",
        "fig4_intervention_timing.pdf": "Intervention timing distribution.",
        "fig5_score_over_time.pdf": "R024 score-over-time diagnostic.",
        "TABLE_main_costmatched_results.tex": "Main Lift cost-matched result table.",
        "TABLE_negative_findings.tex": "Negative findings table.",
        "TABLE_trace_diagnostics.tex": "Trace diagnostic table.",
        "latex_includes.tex": "LaTeX figure include snippets.",
        "gen_r026_paper_figures.py": "Reproducible generation script.",
        "paper_plot_style.py": "Shared publication style.",
    }
    for file in files:
        lines.append(f"| `{file}` | {purposes[file]} |")
    (FIG_DIR / "R026_MANIFEST.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    fig1_hero()
    fig2_cost_matched_frontier()
    fig3_trigger_repairs()
    fig4_intervention_timing()
    fig5_score_over_time()
    table_main_results()
    table_negative_findings()
    table_trace_diagnostics()
    latex_includes()
    manifest()


if __name__ == "__main__":
    main()
