"""Validation helpers for source and evidence provenance packages."""

from __future__ import annotations

import csv
import hashlib
import json
import zipfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProvenanceIssue:
    check: str
    path: str
    message: str


@dataclass(frozen=True)
class ProvenanceValidationReport:
    root: Path
    checks_run: int
    files_checked: int
    issues: tuple[ProvenanceIssue, ...]

    @property
    def ok(self):
        return not self.issues


def _resolve(root, path):
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return Path(root) / candidate


def _sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_csv(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def validate_hash_ledger(
        ledger_csv, root=".", check_name="hash-ledger", path_column="path",
        bytes_column="bytes", hash_column="sha256", compare_hashes=True):
    """Validate a CSV hash ledger against files on disk."""
    issues = []
    rows = _read_csv(ledger_csv)
    files_checked = 0
    for row_number, row in enumerate(rows, start=2):
        path_text = (row.get(path_column, "") or "").strip()
        if not path_text:
            issues.append(ProvenanceIssue(
                check_name, str(ledger_csv),
                f"row {row_number} has blank {path_column}",
            ))
            continue
        path = _resolve(root, path_text)
        if not path.exists():
            issues.append(ProvenanceIssue(
                check_name, path_text, "file listed in hash ledger is missing",
            ))
            continue
        if not path.is_file():
            issues.append(ProvenanceIssue(
                check_name, path_text, "hash ledger target is not a file",
            ))
            continue

        files_checked += 1
        if not compare_hashes:
            continue
        actual_bytes = path.stat().st_size
        expected_bytes = str(row.get(bytes_column, "")).strip()
        if expected_bytes and str(actual_bytes) != expected_bytes:
            issues.append(ProvenanceIssue(
                check_name, path_text,
                f"byte size mismatch: expected {expected_bytes}, "
                f"actual {actual_bytes}",
            ))
        expected_hash = str(row.get(hash_column, "")).strip()
        if expected_hash and _sha256(path) != expected_hash:
            issues.append(ProvenanceIssue(
                check_name, path_text, "sha256 mismatch",
            ))
    return files_checked, issues


def validate_registry_source_inventory(inventory_csv, root=".", compare_hashes=True):
    """Validate an R047 registry-source inventory CSV."""
    issues = []
    rows = _read_csv(inventory_csv)
    files_checked = 0
    for row_number, row in enumerate(rows, start=2):
        source = (row.get("primary_source", "") or "").strip()
        if not source:
            issues.append(ProvenanceIssue(
                "registry-source-inventory", str(inventory_csv),
                f"row {row_number} has blank primary_source",
            ))
            continue
        path = _resolve(root, source)
        expected_exists = str(row.get("exists", "")).strip()
        if expected_exists != "True":
            issues.append(ProvenanceIssue(
                "registry-source-inventory", source,
                f"inventory marks source as not present: {expected_exists}",
            ))
        if not path.exists():
            issues.append(ProvenanceIssue(
                "registry-source-inventory", source,
                "registered source is missing on disk",
            ))
            continue
        files_checked += 1
        if not compare_hashes:
            continue
        expected_bytes = str(row.get("bytes", "")).strip()
        if expected_bytes and str(path.stat().st_size) != expected_bytes:
            issues.append(ProvenanceIssue(
                "registry-source-inventory", source,
                f"byte size mismatch: expected {expected_bytes}, "
                f"actual {path.stat().st_size}",
            ))
        expected_hash = str(row.get("sha256", "")).strip()
        if expected_hash and _sha256(path) != expected_hash:
            issues.append(ProvenanceIssue(
                "registry-source-inventory", source, "sha256 mismatch",
            ))
    return files_checked, issues


def validate_source_snapshot(summary_json, root=".", compare_disk=False):
    """Validate an R048 deterministic source snapshot archive."""
    issues = []
    summary_path = Path(summary_json)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    archive_path = _resolve(root, summary["archive"])
    manifest_path = _resolve(root, summary["manifest"])
    files_checked = 0

    if not archive_path.exists():
        issues.append(ProvenanceIssue(
            "source-snapshot", str(archive_path), "archive is missing",
        ))
        return files_checked, issues
    archive_bytes = archive_path.stat().st_size
    if archive_bytes != int(summary.get("archive_bytes", -1)):
        issues.append(ProvenanceIssue(
            "source-snapshot", str(archive_path),
            f"archive byte size mismatch: expected {summary.get('archive_bytes')}, "
            f"actual {archive_bytes}",
        ))
    if _sha256(archive_path) != summary.get("archive_sha256"):
        issues.append(ProvenanceIssue(
            "source-snapshot", str(archive_path), "archive sha256 mismatch",
        ))

    if not manifest_path.exists():
        issues.append(ProvenanceIssue(
            "source-snapshot", str(manifest_path), "manifest is missing",
        ))
        return files_checked, issues
    manifest_rows = _read_csv(manifest_path)
    manifest_by_path = {row["path"]: row for row in manifest_rows}
    if len(manifest_rows) != int(summary.get("file_count", -1)):
        issues.append(ProvenanceIssue(
            "source-snapshot", str(manifest_path),
            f"manifest row count mismatch: expected {summary.get('file_count')}, "
            f"actual {len(manifest_rows)}",
        ))

    with zipfile.ZipFile(archive_path, "r") as zf:
        zip_names = set(zf.namelist())
        manifest_names = set(manifest_by_path)
        for name in sorted(zip_names - manifest_names):
            issues.append(ProvenanceIssue(
                "source-snapshot", name,
                "zip entry is not listed in manifest",
            ))
        for name in sorted(manifest_names - zip_names):
            issues.append(ProvenanceIssue(
                "source-snapshot", name,
                "manifest entry is missing from zip archive",
            ))
        for name in sorted(zip_names & manifest_names):
            data = zf.read(name)
            expected = manifest_by_path[name].get("sha256")
            if hashlib.sha256(data).hexdigest() != expected:
                issues.append(ProvenanceIssue(
                    "source-snapshot", name, "zip entry sha256 mismatch",
                ))
            else:
                files_checked += 1

    if compare_disk:
        for row in manifest_rows:
            target = _resolve(root, row["path"])
            if not target.exists():
                issues.append(ProvenanceIssue(
                    "source-snapshot", row["path"],
                    "manifest file is missing on disk",
                ))
                continue
            if str(target.stat().st_size) != str(row.get("bytes", "")):
                issues.append(ProvenanceIssue(
                    "source-snapshot", row["path"], "disk byte size mismatch",
                ))
            if _sha256(target) != row.get("sha256"):
                issues.append(ProvenanceIssue(
                    "source-snapshot", row["path"], "disk sha256 mismatch",
                ))
    return files_checked, issues


def validate_checkpoint_inventory(
        inventory_csv, root=".", path_column="checkpoint_path",
        exists_column="checkpoint_exists", bytes_column="checkpoint_bytes",
        hash_column="checkpoint_sha256", check_name="checkpoint-inventory"):
    """Validate checkpoint paths and hashes from an inventory CSV."""
    issues = []
    rows = _read_csv(inventory_csv)
    files_checked = 0
    for row_number, row in enumerate(rows, start=2):
        path_text = (row.get(path_column, "") or "").strip()
        if not path_text:
            continue
        path = _resolve(root, path_text)
        expected_exists = str(row.get(exists_column, "")).strip()
        if expected_exists and expected_exists != "True":
            issues.append(ProvenanceIssue(
                check_name, path_text,
                f"inventory marks checkpoint as not present: {expected_exists}",
            ))
        if not path.exists():
            issues.append(ProvenanceIssue(
                check_name, path_text,
                f"row {row_number} checkpoint is missing on disk",
            ))
            continue
        files_checked += 1
        expected_bytes = str(row.get(bytes_column, "")).strip()
        if expected_bytes and str(path.stat().st_size) != expected_bytes:
            issues.append(ProvenanceIssue(
                check_name, path_text, "checkpoint byte size mismatch",
            ))
        expected_hash = str(row.get(hash_column, "")).strip()
        if expected_hash and _sha256(path) != expected_hash:
            issues.append(ProvenanceIssue(
                check_name, path_text, "checkpoint sha256 mismatch",
            ))
    return files_checked, issues


def validate_current_provenance(root=".", compare_current_files=False):
    """Validate the current R047/R048 provenance packages."""
    root_path = Path(root)
    checks = []
    r047 = root_path / "results" / "r047_evidence_provenance_package"
    r048 = root_path / "results" / "r048_version_command_provenance"
    checks.append(validate_registry_source_inventory(
        r047 / "registry_source_inventory.csv", root=root_path,
        compare_hashes=compare_current_files))
    checks.append(validate_hash_ledger(
        r047 / "artifact_hashes.csv", root=root_path,
        check_name="r047-artifact-hashes",
        compare_hashes=compare_current_files))
    checks.append(validate_source_snapshot(
        r048 / "source_snapshot_summary.json", root=root_path,
        compare_disk=compare_current_files))
    checks.append(validate_hash_ledger(
        r048 / "r048_artifact_hashes.csv", root=root_path,
        check_name="r048-artifact-hashes"))
    checks.append(validate_checkpoint_inventory(
        r048 / "r020_r021_checkpoint_inventory.csv", root=root_path,
        check_name="r020-r021-checkpoints"))
    checks.append(validate_checkpoint_inventory(
        r048 / "r021_raw_run_inventory.csv", root=root_path,
        path_column="best_checkpoint_path",
        check_name="r021-raw-run-checkpoints"))

    files_checked = sum(item[0] for item in checks)
    issues = tuple(issue for _, item_issues in checks for issue in item_issues)
    return ProvenanceValidationReport(
        root=root_path,
        checks_run=len(checks),
        files_checked=files_checked,
        issues=issues,
    )


def format_provenance_report(report):
    status = "OK" if report.ok else "FAIL"
    lines = [
        f"[provenance] {status} checks={report.checks_run} "
        f"files={report.files_checked} issues={len(report.issues)}",
        f"[provenance] root={report.root}",
    ]
    for issue in report.issues:
        lines.append(
            f"[issue] check={issue.check} path={issue.path} :: {issue.message}"
        )
    return "\n".join(lines)
