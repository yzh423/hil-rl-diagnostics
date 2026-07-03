"""Generate the R053 Stack boundary-evidence appendix table."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from foresight_hil.evaluation.claim_tables import (
    build_stack_boundary_claims,
    read_registry_rows,
    render_claims_latex_table,
    render_claims_markdown_table,
)


def write_stack_boundary_appendix(registry_csv, output_dir, figure_dir):
    rows = read_registry_rows(registry_csv)
    claims = build_stack_boundary_claims(rows)

    output_path = Path(output_dir)
    figure_path = Path(figure_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    figure_path.mkdir(parents=True, exist_ok=True)

    md_path = output_path / "stack_boundary_claims.md"
    md_path.write_text(
        render_claims_markdown_table(
            "R053 Stack Boundary Evidence",
            claims,
        ),
        encoding="utf-8",
    )

    tex_path = figure_path / "TABLE_stack_boundary_appendix_r053.tex"
    tex_path.write_text(
        render_claims_latex_table(
            claims,
            caption=(
                "Registry-generated Stack boundary evidence. The no-online "
                "matched behavioral-cloning baseline is retained as a strong "
                "zero-online-human-cost reference; the online intervention "
                "variants are negative boundary evidence, not positive "
                "robotics-transfer results."
            ),
            label="tab:stack_boundary_appendix",
            highlight_configurations={"none_matched_bc"},
            table_environment="table*",
        ),
        encoding="utf-8",
    )
    return (md_path, tex_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--registry",
        default="results/EXPERIMENT_EVIDENCE_REGISTRY.csv",
        help="path to the evidence registry CSV",
    )
    parser.add_argument(
        "--output-dir",
        default="results/r053_stack_boundary_appendix",
        help="directory for the R053 Markdown table",
    )
    parser.add_argument(
        "--figure-dir",
        default="figures",
        help="directory for the LaTeX table asset",
    )
    args = parser.parse_args()

    files = write_stack_boundary_appendix(
        args.registry,
        output_dir=args.output_dir,
        figure_dir=args.figure_dir,
    )
    print(f"[stack-boundary] wrote {len(files)} files")
    for path in files:
        print(f"[stack-boundary] {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
