# R034 Registry Source Validation

Date: 2026-07-02

Purpose: add a reusable validation helper for paper-facing evidence registry
sources and run it on the current registry.

## Change

R034 adds:

- `foresight_hil/evaluation/registry_validation.py`
- `scripts/validate_evidence_registry.py`
- `tests/test_registry_validation.py`

The validation interface is:

- `validate_evidence_registry(registry_csv, root=None)`
- `format_registry_report(report)`

The CLI command is:

```bash
python scripts/validate_evidence_registry.py
```

## Rules Checked

- The registry CSV must contain required columns.
- Every row must have a non-blank `primary_source`.
- Every `primary_source` must exist relative to the project root.
- CSV primary sources must parse with `csv.DictReader`.
- Registry rows and CSV sources must not contain extra unnamed columns.

## Issue Found and Fixed

The first validation pass found that both R023 rows were malformed: the
`primary_source` field was shifted to `95.0` and `276.0` because the row had too
many blank numeric fields before the source path.

R034 corrected the two R023 rows so that:

- `success_rate` stores the trace CSV's `mean_final_success`;
- `mean_best_human_steps` stores `95.0` and `276.0`;
- `primary_source` points to
  `results/r023_real_trace_seed0_2/r023_trace_strategy_diagnostics.csv`.

After the correction, validation reports:

```text
[registry] OK rows=22 sources=22 csv_sources=14 issues=0
```

## Why This Matters

The registry is the interface between raw experiment artifacts and paper claims.
This validator catches source drift before a number enters a draft, table,
caption, or rebuttal.

## Next Candidate

R035 should add a paper-claim audit helper that checks registry numeric fields
against their primary CSV rows for the main R020-R024 claims. That is a stricter
step than source validation and should stay separate.
