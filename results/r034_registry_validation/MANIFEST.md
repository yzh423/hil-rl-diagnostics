# R034 Registry Validation Manifest

Date: 2026-07-02

Purpose: record the evidence-registry source validation helper and the R023
registry correction.

| File | Purpose |
|---|---|
| `REGISTRY_VALIDATION.md` | Rationale, validation rules, issue found, fix, and next target. |

Repo-level files added or updated in this step:

| File | Purpose |
|---|---|
| `foresight_hil/evaluation/registry_validation.py` | Registry source validation module. |
| `foresight_hil/evaluation/__init__.py` | Exports registry validation interface. |
| `scripts/validate_evidence_registry.py` | CLI validator for `EXPERIMENT_EVIDENCE_REGISTRY.csv`. |
| `tests/test_registry_validation.py` | Tests for source existence, CSV parsing, blank source, and extra-column detection. |
| `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` | Fixes malformed R023 rows and adds R034 row. |
| `results/EXPERIMENT_EVIDENCE_REGISTRY.md` | Updates registry description through R034. |
| `CONTEXT.md` | Updates current module-deepening state. |
| `PROJECT_STRUCTURE.md` | Adds R034 and validation command. |
| `results/RESULTS_INDEX.md` | Adds R034 to project-structure support artifacts. |
| `refine-logs/EXPERIMENT_TRACKER.md` | Adds R034 milestone row. |
