"""Audit evidence registry numeric fields against primary CSV sources."""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from foresight_hil.evaluation.registry_numeric_audit import (
    audit_registry_numbers,
    format_numeric_audit_report,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--registry",
        default="results/EXPERIMENT_EVIDENCE_REGISTRY.csv",
        help="path to the evidence registry CSV",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="project root used to resolve relative primary_source paths",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=5e-4,
        help="absolute tolerance for numeric comparisons",
    )
    args = parser.parse_args()

    report = audit_registry_numbers(
        args.registry, root=args.root, tolerance=args.tolerance)
    print(format_numeric_audit_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
