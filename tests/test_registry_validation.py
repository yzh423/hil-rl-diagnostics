import csv
import tempfile
import unittest
from pathlib import Path

from foresight_hil.evaluation.registry_validation import (
    format_registry_report,
    validate_evidence_registry,
)


REGISTRY_HEADER = [
    "run_id", "artifact_type", "task", "configuration", "seeds",
    "successes", "episodes", "success_rate", "ci_low", "ci_high",
    "mean_best_human_steps", "primary_source", "claim_supported",
    "registry_note",
]


def write_registry(path, rows):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=REGISTRY_HEADER)
        writer.writeheader()
        writer.writerows(rows)


def registry_row(run_id, source):
    return {
        "run_id": run_id,
        "artifact_type": "test",
        "task": "Lift",
        "configuration": "cfg",
        "seeds": "0",
        "successes": "",
        "episodes": "",
        "success_rate": "",
        "ci_low": "",
        "ci_high": "",
        "mean_best_human_steps": "",
        "primary_source": source,
        "claim_supported": "test",
        "registry_note": "note",
    }


class RegistryValidationTest(unittest.TestCase):
    def test_validates_existing_sources_and_parses_csv_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "results" / "r001").mkdir(parents=True)
            (root / "results" / "r001" / "source.csv").write_text(
                "metric,value\nsuccess,0.8\n")
            (root / "results" / "r001" / "note.md").write_text("# note\n")
            registry = root / "results" / "registry.csv"
            write_registry(registry, [
                registry_row("R001", "results/r001/source.csv"),
                registry_row("R002", "results/r001/note.md"),
            ])

            report = validate_evidence_registry(registry, root=root)

        self.assertTrue(report.ok)
        self.assertEqual(report.rows_checked, 2)
        self.assertEqual(report.sources_checked, 2)
        self.assertEqual(report.csv_sources_checked, 1)
        self.assertEqual(report.issues, ())

    def test_reports_missing_sources_and_blank_primary_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "results").mkdir()
            registry = root / "results" / "registry.csv"
            write_registry(registry, [
                registry_row("R001", "results/missing.csv"),
                registry_row("R002", ""),
            ])

            report = validate_evidence_registry(registry, root=root)

        self.assertFalse(report.ok)
        self.assertEqual(len(report.issues), 2)
        self.assertIn("missing", report.issues[0].message)
        self.assertIn("blank primary_source", report.issues[1].message)

    def test_reports_malformed_csv_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "results").mkdir()
            bad = root / "results" / "bad.csv"
            bad.write_text("a,b\n1,2,3\n")
            registry = root / "results" / "registry.csv"
            write_registry(registry, [registry_row("R001", "results/bad.csv")])

            report = validate_evidence_registry(registry, root=root)

        self.assertFalse(report.ok)
        self.assertEqual(report.csv_sources_checked, 1)
        self.assertIn("extra unnamed columns", report.issues[0].message)

    def test_reports_registry_rows_with_extra_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "results").mkdir()
            source = root / "results" / "source.csv"
            source.write_text("metric,value\nsuccess,1\n")
            registry = root / "results" / "registry.csv"
            registry.write_text(
                ",".join(REGISTRY_HEADER)
                + "\nR001,test,Lift,cfg,0,,,,,,,results/source.csv,test,note,extra\n"
            )

            report = validate_evidence_registry(registry, root=root)

        self.assertFalse(report.ok)
        self.assertIn("registry row has extra unnamed columns", report.issues[0].message)

    def test_formats_report_summary_and_issues(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "results").mkdir()
            registry = root / "results" / "registry.csv"
            write_registry(registry, [registry_row("R001", "results/missing.csv")])
            report = validate_evidence_registry(registry, root=root)

            text = format_registry_report(report)

        self.assertIn("rows=1", text)
        self.assertIn("issues=1", text)
        self.assertIn("R001", text)


if __name__ == "__main__":
    unittest.main()
