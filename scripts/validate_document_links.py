"""Validate local Markdown links in project documentation."""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from foresight_hil.evaluation.document_links import (
    find_local_markdown_link_issues,
    format_document_link_report,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default=".",
        help="project root whose Markdown files should be checked",
    )
    args = parser.parse_args()

    report = find_local_markdown_link_issues(args.root)
    print(format_document_link_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
