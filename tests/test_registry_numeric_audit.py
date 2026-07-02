import csv
import tempfile
import unittest
from pathlib import Path

from foresight_hil.evaluation.registry_numeric_audit import (
    audit_registry_numbers,
    format_numeric_audit_report,
)


REGISTRY_HEADER = [
    "run_id", "artifact_type", "task", "configuration", "seeds",
    "successes", "episodes", "success_rate", "ci_low", "ci_high",
    "mean_best_human_steps", "primary_source", "claim_supported",
    "registry_note",
]


def write_csv(path, fieldnames, rows):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def registry_row(run_id, config, source, **numbers):
    row = {
        "run_id": run_id,
        "artifact_type": "eval",
        "task": "Lift",
        "configuration": config,
        "seeds": "0;1",
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
    row.update(numbers)
    return row


class RegistryNumericAuditTest(unittest.TestCase):
    def test_audits_numeric_fields_against_matching_strategy_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "results").mkdir()
            source = root / "results" / "source.csv"
            write_csv(source, [
                "strategy", "total_successes", "total_episodes",
                "repeated_success", "success_ci_low", "success_ci_high",
                "mean_best_human_steps",
            ], [{
                "strategy": "random_b350",
                "total_successes": "87",
                "total_episodes": "100",
                "repeated_success": "0.8700",
                "success_ci_low": "0.7900",
                "success_ci_high": "0.9200",
                "mean_best_human_steps": "177.0000",
            }])
            registry = root / "results" / "registry.csv"
            write_csv(registry, REGISTRY_HEADER, [
                registry_row(
                    "R001", "random_b350", "results/source.csv",
                    successes="87", episodes="100", success_rate="0.8700",
                    ci_low="0.7900", ci_high="0.9200",
                    mean_best_human_steps="177.0",
                )
            ])

            report = audit_registry_numbers(registry, root=root)

        self.assertTrue(report.ok)
        self.assertEqual(report.rows_checked, 1)
        self.assertEqual(report.numeric_checks, 6)
        self.assertEqual(report.issues, ())

    def test_uses_explicit_alias_for_r020_lv_voi_scale3(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "results").mkdir()
            source = root / "results" / "source.csv"
            write_csv(source, [
                "strategy", "total_successes", "total_episodes",
                "repeated_success", "mean_best_human_steps",
            ], [{
                "strategy": "method",
                "total_successes": "416",
                "total_episodes": "500",
                "repeated_success": "0.8320",
                "mean_best_human_steps": "202.0",
            }])
            registry = root / "results" / "registry.csv"
            write_csv(registry, REGISTRY_HEADER, [
                registry_row(
                    "R020", "lv_voi_scale3", "results/source.csv",
                    successes="416", episodes="500", success_rate="0.8320",
                    mean_best_human_steps="202.0",
                )
            ])

            report = audit_registry_numbers(registry, root=root)

        self.assertTrue(report.ok)
        self.assertEqual(report.numeric_checks, 4)

    def test_reports_number_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "results").mkdir()
            source = root / "results" / "source.csv"
            write_csv(source, ["strategy", "total_successes"], [
                {"strategy": "random", "total_successes": "10"}
            ])
            registry = root / "results" / "registry.csv"
            write_csv(registry, REGISTRY_HEADER, [
                registry_row(
                    "R001", "random", "results/source.csv",
                    successes="11",
                )
            ])

            report = audit_registry_numbers(registry, root=root)

        self.assertFalse(report.ok)
        self.assertEqual(report.numeric_checks, 1)
        self.assertIn("successes", report.issues[0].field)
        self.assertIn("11", report.issues[0].registry_value)
        self.assertIn("10", report.issues[0].source_value)

    def test_skips_rows_without_csv_primary_source_or_numeric_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "results").mkdir()
            note = root / "results" / "note.md"
            note.write_text("# note\n")
            registry = root / "results" / "registry.csv"
            write_csv(registry, REGISTRY_HEADER, [
                registry_row("R001", "artifact", "results/note.md"),
            ])

            report = audit_registry_numbers(registry, root=root)

        self.assertTrue(report.ok)
        self.assertEqual(report.rows_checked, 1)
        self.assertEqual(report.rows_skipped, 1)
        self.assertIn("issues=0", format_numeric_audit_report(report))


if __name__ == "__main__":
    unittest.main()
