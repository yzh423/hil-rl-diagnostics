"""Validation helpers for paper-facing evidence registry sources."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


REQUIRED_REGISTRY_COLUMNS = (
    "run_id",
    "artifact_type",
    "task",
    "configuration",
    "primary_source",
    "claim_supported",
)


@dataclass(frozen=True)
class RegistryIssue:
    row_number: int
    run_id: str
    primary_source: str
    message: str


@dataclass(frozen=True)
class RegistryValidationReport:
    registry_path: Path
    rows_checked: int
    sources_checked: int
    csv_sources_checked: int
    issues: tuple[RegistryIssue, ...]

    @property
    def ok(self):
        return not self.issues


def _default_root_for(registry_path):
    if registry_path.parent.name == "results":
        return registry_path.parent.parent
    return Path.cwd()


def _source_path(root, primary_source):
    source = Path(primary_source)
    if source.is_absolute():
        return source
    return Path(root) / source


def _csv_parse_issues(path):
    issues = []
    try:
        with path.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                return ["CSV source has no header"]
            for row_idx, row in enumerate(reader, start=2):
                if None in row:
                    issues.append(
                        f"CSV source has extra unnamed columns at line {row_idx}")
    except UnicodeDecodeError as exc:
        return [f"CSV source could not be decoded as UTF-8: {exc}"]
    except csv.Error as exc:
        return [f"CSV source could not be parsed: {exc}"]
    return issues


def validate_evidence_registry(registry_csv, root=None):
    """Validate registry rows and their primary source files."""
    registry_path = Path(registry_csv)
    root_path = Path(root) if root is not None else _default_root_for(registry_path)
    issues = []
    rows_checked = 0
    sources_checked = 0
    csv_sources_checked = 0

    try:
        with registry_path.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            fieldnames = tuple(reader.fieldnames or ())
            missing_columns = [
                col for col in REQUIRED_REGISTRY_COLUMNS if col not in fieldnames
            ]
            if missing_columns:
                issues.append(RegistryIssue(
                    row_number=1,
                    run_id="",
                    primary_source="",
                    message="registry missing required columns: "
                    + ", ".join(missing_columns),
                ))
                return RegistryValidationReport(
                    registry_path=registry_path,
                    rows_checked=0,
                    sources_checked=0,
                    csv_sources_checked=0,
                    issues=tuple(issues),
                )

            for row_number, row in enumerate(reader, start=2):
                rows_checked += 1
                run_id = row.get("run_id", "")
                primary_source = (row.get("primary_source", "") or "").strip()
                if None in row:
                    issues.append(RegistryIssue(
                        row_number=row_number,
                        run_id=run_id,
                        primary_source=primary_source,
                        message="registry row has extra unnamed columns",
                    ))
                if not primary_source:
                    issues.append(RegistryIssue(
                        row_number=row_number,
                        run_id=run_id,
                        primary_source=primary_source,
                        message="blank primary_source",
                    ))
                    continue

                sources_checked += 1
                source_path = _source_path(root_path, primary_source)
                if not source_path.exists():
                    issues.append(RegistryIssue(
                        row_number=row_number,
                        run_id=run_id,
                        primary_source=primary_source,
                        message=f"missing primary_source: {source_path}",
                    ))
                    continue

                if source_path.suffix.lower() == ".csv":
                    csv_sources_checked += 1
                    for message in _csv_parse_issues(source_path):
                        issues.append(RegistryIssue(
                            row_number=row_number,
                            run_id=run_id,
                            primary_source=primary_source,
                            message=message,
                        ))
    except FileNotFoundError:
        issues.append(RegistryIssue(
            row_number=0,
            run_id="",
            primary_source="",
            message=f"registry file not found: {registry_path}",
        ))

    return RegistryValidationReport(
        registry_path=registry_path,
        rows_checked=rows_checked,
        sources_checked=sources_checked,
        csv_sources_checked=csv_sources_checked,
        issues=tuple(issues),
    )


def format_registry_report(report):
    """Format a registry validation report for CLI output."""
    status = "OK" if report.ok else "FAIL"
    lines = [
        f"[registry] {status} rows={report.rows_checked} "
        f"sources={report.sources_checked} csv_sources={report.csv_sources_checked} "
        f"issues={len(report.issues)}",
        f"[registry] path={report.registry_path}",
    ]
    for issue in report.issues:
        lines.append(
            f"[issue] row={issue.row_number} run_id={issue.run_id} "
            f"source={issue.primary_source} :: {issue.message}"
        )
    return "\n".join(lines)
