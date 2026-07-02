"""Validate current source/evidence provenance packages."""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from foresight_hil.evaluation.provenance_validation import (
    format_provenance_report,
    validate_current_provenance,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default=".",
        help="project root used to resolve provenance paths",
    )
    parser.add_argument(
        "--compare-current-files",
        action="store_true",
        help=(
            "also compare historical source/hash ledgers against the current "
            "working tree; useful for drift diagnosis but expected to fail "
            "after new R0xx packages change project-control files"
        ),
    )
    args = parser.parse_args()

    report = validate_current_provenance(
        root=args.root, compare_current_files=args.compare_current_files)
    print(format_provenance_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
