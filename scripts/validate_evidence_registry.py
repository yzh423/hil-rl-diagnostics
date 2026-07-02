"""Validate paper-facing evidence registry primary sources."""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from foresight_hil.evaluation.registry_validation import (
    format_registry_report,
    validate_evidence_registry,
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
    args = parser.parse_args()

    report = validate_evidence_registry(args.registry, root=args.root)
    print(format_registry_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
