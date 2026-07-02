# R036 Claim Tables Manifest

Date: 2026-07-02

Purpose: record registry-driven claim table generation and its paper-facing
outputs.

| File | Purpose |
|---|---|
| `CLAIM_TABLE_GENERATOR.md` | Rationale, generated assets, claim logic, verification, and next target. |
| `main_costmatched_claims.md` | Markdown main cost-matched claims with source paths. |
| `trigger_repair_claims.md` | Markdown negative trigger-repair claims with source paths. |

Repo-level files added or updated in this step:

| File | Purpose |
|---|---|
| `foresight_hil/evaluation/claim_tables.py` | Registry-driven claim table module. |
| `foresight_hil/evaluation/__init__.py` | Exports claim table interfaces. |
| `scripts/generate_claim_tables.py` | CLI generator for R036 claim table assets. |
| `tests/test_claim_tables.py` | Tests for claim row construction, delta calculation, rendering, and file output. |
| `figures/TABLE_registry_costmatched_results_r036.tex` | Registry-generated main cost-matched LaTeX table. |
| `figures/TABLE_registry_trigger_repairs_r036.tex` | Registry-generated trigger-repair LaTeX table. |
| `figures/latex_includes_r036.tex` | Include snippets for R036 tables. |
| `figures/FIGURE_ASSET_INDEX.md` | Adds R036 table assets. |
| `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` | Adds R036 registry row. |
| `results/EXPERIMENT_EVIDENCE_REGISTRY.md` | Updates registry description through R036. |
| `PAPER_PLAN.md` | Points Table 1/Table 2 to registry-generated table assets. |
| `CONTEXT.md` | Updates current evidence-discipline state. |
| `PROJECT_STRUCTURE.md` | Adds R036 and generation command. |
| `results/RESULTS_INDEX.md` | Adds R036 to paper-facing artifacts. |
| `refine-logs/EXPERIMENT_TRACKER.md` | Adds R036 milestone row. |
