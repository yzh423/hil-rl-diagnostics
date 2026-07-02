"""Generate paper claim tables from the evidence registry."""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from foresight_hil.evaluation.claim_tables import write_claim_table_assets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--registry",
        default="results/EXPERIMENT_EVIDENCE_REGISTRY.csv",
        help="path to the evidence registry CSV",
    )
    parser.add_argument(
        "--output-dir",
        default="results/r036_claim_tables",
        help="directory for Markdown claim tables",
    )
    parser.add_argument(
        "--figure-dir",
        default="figures",
        help="directory for LaTeX table assets",
    )
    args = parser.parse_args()

    manifest = write_claim_table_assets(
        args.registry,
        output_dir=args.output_dir,
        figure_dir=args.figure_dir,
    )
    print(
        f"[claim-tables] wrote {len(manifest.files)} files "
        f"to {manifest.output_dir} and {manifest.figure_dir}"
    )
    for path in manifest.files:
        print(f"[claim-tables] {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
