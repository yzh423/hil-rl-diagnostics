import csv
import tempfile
import unittest
from pathlib import Path

from foresight_hil.evaluation.claim_tables import (
    build_main_costmatched_claims,
    build_stack_boundary_claims,
    build_trigger_repair_claims,
    read_registry_rows,
    render_claims_latex_table,
    render_claims_markdown_table,
    write_claim_table_assets,
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


def registry_row(run_id, config, successes, episodes, rate, cost, **extra):
    row = {
        "run_id": run_id,
        "artifact_type": "repeated_checkpoint_eval",
        "task": "Lift",
        "configuration": config,
        "seeds": "0;1;2",
        "successes": str(successes),
        "episodes": str(episodes),
        "success_rate": str(rate),
        "ci_low": "0.7000",
        "ci_high": "0.9000",
        "mean_best_human_steps": str(cost),
        "primary_source": "results/source.csv",
        "claim_supported": "test",
        "registry_note": "note",
    }
    row.update(extra)
    return row


class ClaimTablesTest(unittest.TestCase):
    def test_builds_main_costmatched_rows_in_paper_order_with_delta(self):
        rows = [
            registry_row("R021", "lv_voi_scale3", 416, 500, "0.8320", "202.0"),
            registry_row("R021", "random_b350", 439, 500, "0.8780", "177.0"),
            registry_row("R021", "random_b450", 426, 500, "0.8520", "250.0"),
            registry_row("R021", "random_b600", 426, 500, "0.8520", "269.2"),
            registry_row("R020", "none", 400, 500, "0.8000", "0.0"),
        ]

        claims = build_main_costmatched_claims(rows)

        self.assertEqual(
            [row.configuration for row in claims],
            ["none", "random_b350", "lv_voi_scale3", "random_b450", "random_b600"],
        )
        self.assertEqual(claims[1].success_text, "439/500 = 87.8%")
        self.assertEqual(claims[1].cost_text, "177.0")
        self.assertEqual(claims[1].delta_text, "+4.6 pp")
        self.assertEqual(claims[0].delta_text, "-3.2 pp")

    def test_builds_trigger_repair_rows_from_negative_repair_runs(self):
        rows = [
            registry_row("R022", "min_disagree_vlv0p25", 226, 300, "0.7533", "211.6667"),
            registry_row("R024", "random_b350", 259, 300, "0.8633", "95.0"),
            registry_row("R024", "score_floor_vlv3_after4000_floor0p05", 233, 300, "0.7767", "253.3333"),
        ]

        claims = build_trigger_repair_claims(rows)

        self.assertEqual(
            [row.configuration for row in claims],
            ["random_b350", "min_disagree_vlv0p25", "score_floor_vlv3_after4000_floor0p05"],
        )
        self.assertEqual(claims[0].success_text, "259/300 = 86.3%")
        self.assertEqual(claims[1].delta_text, "-11.0 pp")
        self.assertEqual(claims[2].delta_text, "-8.7 pp")

    def test_builds_stack_boundary_rows_from_registered_stack_evidence(self):
        rows = [
            registry_row("R018", "none_matched_bc", 131, 180, "0.7278", "0.0"),
            registry_row("R018", "random_matched_bc", 107, 180, "0.5944", "478.0"),
            registry_row("R018", "voi_stack_tuned", 107, 180, "0.5944", "433.3"),
        ]

        claims = build_stack_boundary_claims(rows)

        self.assertEqual(
            [row.configuration for row in claims],
            ["none_matched_bc", "random_matched_bc", "voi_stack_tuned"],
        )
        self.assertEqual(claims[0].label, "No-online matched BC")
        self.assertEqual(claims[0].success_text, "131/180 = 72.8%")
        self.assertEqual(claims[1].delta_text, "-13.3 pp")
        self.assertEqual(claims[2].cost_text, "433.3")

    def test_renders_markdown_and_latex_with_traceable_sources(self):
        rows = [
            registry_row("R021", "lv_voi_scale3", 416, 500, "0.8320", "202.0"),
            registry_row("R021", "random_b350", 439, 500, "0.8780", "177.0"),
            registry_row("R020", "none", 400, 500, "0.8000", "0.0"),
            registry_row("R021", "random_b450", 426, 500, "0.8520", "250.0"),
            registry_row("R021", "random_b600", 426, 500, "0.8520", "269.2"),
        ]
        claims = build_main_costmatched_claims(rows)

        markdown = render_claims_markdown_table("Main claims", claims)
        latex = render_claims_latex_table(
            claims,
            caption="Cost-matched registry claims.",
            label="tab:registry_costmatched_claims",
            highlight_configurations={"random_b350"},
        )

        self.assertIn("| Random b350 | R021 | 439/500 = 87.8% |", markdown)
        self.assertIn("results/source.csv", markdown)
        self.assertIn(r"\textbf{Random b350}", latex)
        self.assertIn(r"LV-VoI scale3", latex)
        self.assertNotIn("random_b350", latex)

    def test_writes_claim_table_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry.csv"
            write_registry(registry, [
                registry_row("R020", "none", 400, 500, "0.8000", "0.0"),
                registry_row("R021", "random_b350", 439, 500, "0.8780", "177.0"),
                registry_row("R021", "lv_voi_scale3", 416, 500, "0.8320", "202.0"),
                registry_row("R021", "random_b450", 426, 500, "0.8520", "250.0"),
                registry_row("R021", "random_b600", 426, 500, "0.8520", "269.2"),
                registry_row("R022", "min_disagree_vlv0p25", 226, 300, "0.7533", "211.6667"),
                registry_row("R024", "random_b350", 259, 300, "0.8633", "95.0"),
                registry_row("R024", "score_floor_vlv3_after4000_floor0p05", 233, 300, "0.7767", "253.3333"),
            ])
            output_dir = root / "results" / "r036"
            figure_dir = root / "figures"

            manifest = write_claim_table_assets(registry, output_dir, figure_dir)

            self.assertEqual(len(manifest.files), 5)
            for path in manifest.files:
                self.assertTrue(path.exists(), path)
            self.assertIn("Random b350", (output_dir / "main_costmatched_claims.md").read_text())
            self.assertIn(
                r"\label{tab:registry_trigger_repairs}",
                (figure_dir / "TABLE_registry_trigger_repairs_r036.tex").read_text(),
            )

    def test_reads_registry_rows_from_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = Path(tmp) / "registry.csv"
            write_registry(registry, [
                registry_row("R021", "random_b350", 439, 500, "0.8780", "177.0"),
            ])

            rows = read_registry_rows(registry)

        self.assertEqual(rows[0]["configuration"], "random_b350")


if __name__ == "__main__":
    unittest.main()
