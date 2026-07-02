import csv
import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from foresight_hil.evaluation.provenance_validation import (
    format_provenance_report,
    validate_checkpoint_inventory,
    validate_hash_ledger,
    validate_source_snapshot,
)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_csv(path, fieldnames, rows):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class ProvenanceValidationTest(unittest.TestCase):
    def test_hash_ledger_accepts_matching_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.txt"
            source.write_text("stable\n")
            ledger = root / "ledger.csv"
            write_csv(ledger, ["path", "bytes", "sha256"], [{
                "path": "source.txt",
                "bytes": str(source.stat().st_size),
                "sha256": sha256(source),
            }])

            files, issues = validate_hash_ledger(ledger, root=root)

        self.assertEqual(files, 1)
        self.assertEqual(issues, [])

    def test_hash_ledger_reports_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.txt"
            source.write_text("changed\n")
            ledger = root / "ledger.csv"
            write_csv(ledger, ["path", "bytes", "sha256"], [{
                "path": "source.txt",
                "bytes": "999",
                "sha256": "0" * 64,
            }])

            files, issues = validate_hash_ledger(ledger, root=root)

        self.assertEqual(files, 1)
        self.assertEqual(len(issues), 2)

    def test_source_snapshot_validates_archive_manifest_and_disk_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "a.txt"
            source.write_text("alpha\n")
            archive = root / "snapshot.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.write(source, "a.txt")
            manifest = root / "manifest.csv"
            write_csv(manifest, ["path", "bytes", "sha256"], [{
                "path": "a.txt",
                "bytes": str(source.stat().st_size),
                "sha256": sha256(source),
            }])
            summary = root / "summary.json"
            summary.write_text(json.dumps({
                "archive": "snapshot.zip",
                "archive_bytes": archive.stat().st_size,
                "archive_sha256": sha256(archive),
                "manifest": "manifest.csv",
                "file_count": 1,
            }))

            files, issues = validate_source_snapshot(summary, root=root)

        self.assertEqual(files, 1)
        self.assertEqual(issues, [])

    def test_source_snapshot_reports_disk_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "a.txt"
            source.write_text("alpha\n")
            archive = root / "snapshot.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.write(source, "a.txt")
            manifest = root / "manifest.csv"
            write_csv(manifest, ["path", "bytes", "sha256"], [{
                "path": "a.txt",
                "bytes": str(source.stat().st_size),
                "sha256": sha256(source),
            }])
            summary = root / "summary.json"
            summary.write_text(json.dumps({
                "archive": "snapshot.zip",
                "archive_bytes": archive.stat().st_size,
                "archive_sha256": sha256(archive),
                "manifest": "manifest.csv",
                "file_count": 1,
            }))
            source.write_text("beta\n")

            _, issues = validate_source_snapshot(
                summary, root=root, compare_disk=True)

        self.assertTrue(any("disk" in issue.message for issue in issues))

    def test_checkpoint_inventory_validates_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            checkpoint = root / "model.zip"
            checkpoint.write_bytes(b"checkpoint")
            inventory = root / "inventory.csv"
            write_csv(inventory, [
                "checkpoint_path", "checkpoint_exists", "checkpoint_bytes",
                "checkpoint_sha256",
            ], [{
                "checkpoint_path": "model.zip",
                "checkpoint_exists": "True",
                "checkpoint_bytes": str(checkpoint.stat().st_size),
                "checkpoint_sha256": sha256(checkpoint),
            }])

            files, issues = validate_checkpoint_inventory(inventory, root=root)

        self.assertEqual(files, 1)
        self.assertEqual(issues, [])

    def test_formats_report(self):
        class Report:
            ok = True
            checks_run = 2
            files_checked = 3
            issues = ()
            root = Path(".")

        text = format_provenance_report(Report())

        self.assertIn("OK", text)
        self.assertIn("checks=2", text)


if __name__ == "__main__":
    unittest.main()
