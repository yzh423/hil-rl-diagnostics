"""Build manuscript-ready claim tables from the evidence registry."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


DISPLAY_LABELS = {
    "none": "No intervention",
    "random": "Random",
    "random_b350": "Random b350",
    "random_b450": "Random b450",
    "random_b600": "Random b600",
    "lv_voi_scale3": "LV-VoI scale3",
    "min_disagree_vlv0p25": "Min-disagree LV-VoI",
    "score_floor_vlv3_after4000_floor0p05": "Score-floor LV-VoI",
    "none_matched_bc": "No-online matched BC",
    "random_matched_bc": "Random matched BC",
    "voi_stack_tuned": "Stack-tuned LV-VoI",
}

MAIN_COSTMATCHED_ORDER = (
    ("R020", "none"),
    ("R021", "random_b350"),
    ("R021", "lv_voi_scale3"),
    ("R021", "random_b450"),
    ("R021", "random_b600"),
)

TRIGGER_REPAIR_ORDER = (
    ("R024", "random_b350"),
    ("R022", "min_disagree_vlv0p25"),
    ("R024", "score_floor_vlv3_after4000_floor0p05"),
)

STACK_BOUNDARY_ORDER = (
    ("R018", "none_matched_bc"),
    ("R018", "random_matched_bc"),
    ("R018", "voi_stack_tuned"),
)


@dataclass(frozen=True)
class ClaimTableRow:
    run_id: str
    configuration: str
    label: str
    success_text: str
    ci_text: str
    cost_text: str
    delta_text: str
    primary_source: str
    claim_supported: str


@dataclass(frozen=True)
class ClaimTableManifest:
    output_dir: Path
    figure_dir: Path
    files: tuple[Path, ...]


def read_registry_rows(registry_csv):
    """Read the evidence registry as dictionaries."""
    with Path(registry_csv).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _row_key(row):
    return row.get("run_id", ""), row.get("configuration", "")


def _find_row(rows, run_id, configuration):
    for row in rows:
        if _row_key(row) == (run_id, configuration):
            return row
    raise ValueError(f"missing registry row: {run_id} {configuration}")


def _pct(value):
    return float(value) * 100.0


def _format_success(row):
    successes = row.get("successes", "")
    episodes = row.get("episodes", "")
    rate = row.get("success_rate", "")
    if successes and episodes:
        return f"{successes}/{episodes} = {_pct(rate):.1f}%"
    return f"{_pct(rate):.1f}%"


def _format_ci(row):
    ci_low = row.get("ci_low", "")
    ci_high = row.get("ci_high", "")
    if not ci_low or not ci_high:
        return "--"
    return f"[{_pct(ci_low):.1f}, {_pct(ci_high):.1f}]"


def _format_cost(row):
    return f"{float(row['mean_best_human_steps']):.1f}"


def _format_delta_pp(row, reference_success):
    delta = _pct(row["success_rate"]) - _pct(reference_success)
    return f"{delta:+.1f} pp"


def _claim_row(row, reference_success):
    configuration = row["configuration"]
    return ClaimTableRow(
        run_id=row["run_id"],
        configuration=configuration,
        label=DISPLAY_LABELS.get(configuration, configuration),
        success_text=_format_success(row),
        ci_text=_format_ci(row),
        cost_text=_format_cost(row),
        delta_text=_format_delta_pp(row, reference_success),
        primary_source=row.get("primary_source", ""),
        claim_supported=row.get("claim_supported", ""),
    )


def _build_claims(rows, order, reference):
    reference_row = _find_row(rows, *reference)
    reference_success = reference_row["success_rate"]
    return [_claim_row(_find_row(rows, *key), reference_success) for key in order]


def build_main_costmatched_claims(registry_rows):
    """Return paper-ordered rows for the main cost-matched Lift table."""
    return _build_claims(
        registry_rows,
        MAIN_COSTMATCHED_ORDER,
        reference=("R021", "lv_voi_scale3"),
    )


def build_trigger_repair_claims(registry_rows):
    """Return paper-ordered rows for the negative trigger-repair table."""
    return _build_claims(
        registry_rows,
        TRIGGER_REPAIR_ORDER,
        reference=("R024", "random_b350"),
    )


def build_stack_boundary_claims(registry_rows):
    """Return paper-ordered rows for the Stack boundary-evidence table."""
    return _build_claims(
        registry_rows,
        STACK_BOUNDARY_ORDER,
        reference=("R018", "none_matched_bc"),
    )


def render_claims_markdown_table(title, rows):
    lines = [
        f"# {title}",
        "",
        "| Strategy | Run | Success | 95% CI | Human steps | Delta | Source | Claim status |",
        "|---|---|---:|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.label} | {row.run_id} | {row.success_text} | {row.ci_text} | "
            f"{row.cost_text} | {row.delta_text} | `{row.primary_source}` | "
            f"{row.claim_supported} |"
        )
    return "\n".join(lines) + "\n"


def _latex_escape(text):
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    return "".join(replacements.get(char, char) for char in str(text))


def render_claims_latex_table(
    rows,
    caption,
    label,
    highlight_configurations=None,
    table_environment="table",
):
    highlight_configurations = set(highlight_configurations or ())
    lines = [
        rf"\begin{{{table_environment}}}[t]",
        r"\centering",
        rf"\caption{{{_latex_escape(caption)}}}",
        rf"\label{{{label}}}",
        r"\begin{tabular}{llcccc}",
        r"\toprule",
        r"Strategy & Run & Success & 95\% CI & Human steps & $\Delta$ \\",
        r"\midrule",
    ]
    for row in rows:
        label_text = _latex_escape(row.label)
        if row.configuration in highlight_configurations:
            label_text = r"\textbf{" + label_text + "}"
        lines.append(
            f"{label_text} & {_latex_escape(row.run_id)} & "
            f"{_latex_escape(row.success_text)} & {_latex_escape(row.ci_text)} & "
            f"{_latex_escape(row.cost_text)} & {_latex_escape(row.delta_text)} \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}", rf"\end{{{table_environment}}}", ""]
    return "\n".join(lines)


def _latex_includes():
    return r"""
% === R036 Registry-Generated Main Claim Table ===
\input{figures/TABLE_registry_costmatched_results_r036.tex}

% === R036 Registry-Generated Trigger Repair Claim Table ===
\input{figures/TABLE_registry_trigger_repairs_r036.tex}
""".strip() + "\n"


def write_claim_table_assets(registry_csv, output_dir, figure_dir):
    """Write R036 Markdown and LaTeX claim-table assets."""
    registry_rows = read_registry_rows(registry_csv)
    output_path = Path(output_dir)
    figure_path = Path(figure_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    figure_path.mkdir(parents=True, exist_ok=True)

    main_rows = build_main_costmatched_claims(registry_rows)
    repair_rows = build_trigger_repair_claims(registry_rows)

    files = []
    main_md = output_path / "main_costmatched_claims.md"
    main_md.write_text(
        render_claims_markdown_table("R036 Main Cost-Matched Claims", main_rows),
        encoding="utf-8",
    )
    files.append(main_md)

    repair_md = output_path / "trigger_repair_claims.md"
    repair_md.write_text(
        render_claims_markdown_table("R036 Trigger Repair Claims", repair_rows),
        encoding="utf-8",
    )
    files.append(repair_md)

    main_tex = figure_path / "TABLE_registry_costmatched_results_r036.tex"
    main_tex.write_text(
        render_claims_latex_table(
            main_rows,
            caption=(
                "Registry-generated cost-matched Lift claims. "
                "All numeric entries are drawn from the evidence registry."
            ),
            label="tab:registry_costmatched_claims",
            highlight_configurations={"random_b350"},
        ),
        encoding="utf-8",
    )
    files.append(main_tex)

    repair_tex = figure_path / "TABLE_registry_trigger_repairs_r036.tex"
    repair_tex.write_text(
        render_claims_latex_table(
            repair_rows,
            caption=(
                "Registry-generated negative trigger-repair claims on Lift "
                "seeds 0--2."
            ),
            label="tab:registry_trigger_repairs",
            highlight_configurations={"random_b350"},
        ),
        encoding="utf-8",
    )
    files.append(repair_tex)

    include_tex = figure_path / "latex_includes_r036.tex"
    include_tex.write_text(_latex_includes(), encoding="utf-8")
    files.append(include_tex)

    return ClaimTableManifest(
        output_dir=output_path,
        figure_dir=figure_path,
        files=tuple(files),
    )
