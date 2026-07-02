"""Numeric consistency audit for the evidence registry."""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path


REGISTRY_TO_SOURCE_FIELDS = {
    "successes": ("total_successes",),
    "episodes": ("total_episodes",),
    "success_rate": ("repeated_success", "mean_final_success"),
    "ci_low": ("success_ci_low",),
    "ci_high": ("success_ci_high",),
    "mean_best_human_steps": ("mean_best_human_steps",),
}

SOURCE_KEY_COLUMNS = ("strategy", "configuration")
CONFIG_ALIASES = {
    ("R020", "lv_voi_scale3"): "method",
}


@dataclass(frozen=True)
class NumericAuditIssue:
    row_number: int
    run_id: str
    configuration: str
    field: str
    registry_value: str
    source_value: str
    message: str


@dataclass(frozen=True)
class NumericAuditReport:
    registry_path: Path
    rows_checked: int
    rows_skipped: int
    numeric_checks: int
    issues: tuple[NumericAuditIssue, ...]

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


def _numeric_fields_present(row):
    return [field for field in REGISTRY_TO_SOURCE_FIELDS if str(row.get(field, "")).strip()]


def _parse_float(value):
    text = str(value).strip()
    if text == "":
        return None
    try:
        value_float = float(text)
    except ValueError:
        return None
    if not math.isfinite(value_float):
        return None
    return value_float


def _numbers_match(registry_value, source_value, tolerance):
    registry_float = _parse_float(registry_value)
    source_float = _parse_float(source_value)
    if registry_float is None or source_float is None:
        return str(registry_value).strip() == str(source_value).strip()
    return abs(registry_float - source_float) <= tolerance


def _source_match_key(row):
    for key in SOURCE_KEY_COLUMNS:
        if key in row:
            return key
    return None


def _expected_source_config(registry_row):
    run_id = registry_row.get("run_id", "")
    configuration = registry_row.get("configuration", "")
    return CONFIG_ALIASES.get((run_id, configuration), configuration)


def _load_source_rows(source_path):
    with source_path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _find_source_row(registry_row, source_rows):
    if not source_rows:
        return None
    key = _source_match_key(source_rows[0])
    if key is None:
        return None
    expected = _expected_source_config(registry_row)
    for row in source_rows:
        if row.get(key) == expected:
            return row
    return None


def _source_value_for(source_row, registry_field):
    for source_field in REGISTRY_TO_SOURCE_FIELDS[registry_field]:
        if source_field in source_row and str(source_row.get(source_field, "")).strip() != "":
            return source_field, source_row[source_field]
    return None, ""


def audit_registry_numbers(registry_csv, root=None, tolerance=5e-4):
    """Audit numeric registry fields against their primary CSV source rows."""
    registry_path = Path(registry_csv)
    root_path = Path(root) if root is not None else _default_root_for(registry_path)
    issues = []
    rows_checked = 0
    rows_skipped = 0
    numeric_checks = 0

    with registry_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row_number, registry_row in enumerate(reader, start=2):
            rows_checked += 1
            numeric_fields = _numeric_fields_present(registry_row)
            primary_source = (registry_row.get("primary_source", "") or "").strip()
            source_path = _source_path(root_path, primary_source) if primary_source else None
            if not numeric_fields or source_path is None or source_path.suffix.lower() != ".csv":
                rows_skipped += 1
                continue

            source_rows = _load_source_rows(source_path)
            source_row = _find_source_row(registry_row, source_rows)
            if source_row is None:
                issues.append(NumericAuditIssue(
                    row_number=row_number,
                    run_id=registry_row.get("run_id", ""),
                    configuration=registry_row.get("configuration", ""),
                    field="configuration",
                    registry_value=registry_row.get("configuration", ""),
                    source_value="",
                    message=f"no matching source row in {primary_source}",
                ))
                continue

            for field in numeric_fields:
                source_field, source_value = _source_value_for(source_row, field)
                numeric_checks += 1
                if source_field is None:
                    issues.append(NumericAuditIssue(
                        row_number=row_number,
                        run_id=registry_row.get("run_id", ""),
                        configuration=registry_row.get("configuration", ""),
                        field=field,
                        registry_value=registry_row.get(field, ""),
                        source_value="",
                        message="source row lacks mapped numeric field",
                    ))
                    continue
                registry_value = registry_row.get(field, "")
                if not _numbers_match(registry_value, source_value, tolerance):
                    issues.append(NumericAuditIssue(
                        row_number=row_number,
                        run_id=registry_row.get("run_id", ""),
                        configuration=registry_row.get("configuration", ""),
                        field=field,
                        registry_value=str(registry_value),
                        source_value=str(source_value),
                        message=f"number mismatch vs source field {source_field}",
                    ))

    return NumericAuditReport(
        registry_path=registry_path,
        rows_checked=rows_checked,
        rows_skipped=rows_skipped,
        numeric_checks=numeric_checks,
        issues=tuple(issues),
    )


def format_numeric_audit_report(report):
    status = "OK" if report.ok else "FAIL"
    lines = [
        f"[numeric-audit] {status} rows={report.rows_checked} "
        f"skipped={report.rows_skipped} checks={report.numeric_checks} "
        f"issues={len(report.issues)}",
        f"[numeric-audit] path={report.registry_path}",
    ]
    for issue in report.issues:
        lines.append(
            f"[issue] row={issue.row_number} run_id={issue.run_id} "
            f"config={issue.configuration} field={issue.field} "
            f"registry={issue.registry_value} source={issue.source_value} :: "
            f"{issue.message}"
        )
    return "\n".join(lines)
