# R035 Registry Numeric Audit

Date: 2026-07-02

Purpose: add a reusable audit helper that checks paper-facing numeric registry
fields against the matching rows in their primary CSV sources.

## Change

R035 adds:

- `foresight_hil/evaluation/registry_numeric_audit.py`
- `scripts/audit_registry_numbers.py`
- `tests/test_registry_numeric_audit.py`

The audit interface is:

- `audit_registry_numbers(registry_csv, root=None, tolerance=5e-4)`
- `format_numeric_audit_report(report)`

The CLI command is:

```bash
python scripts/audit_registry_numbers.py
```

## Numeric Fields Checked

The audit compares these registry fields to source CSV columns:

| Registry field | Source CSV column |
|---|---|
| `successes` | `total_successes` |
| `episodes` | `total_episodes` |
| `success_rate` | `repeated_success` or `mean_final_success` |
| `ci_low` | `success_ci_low` |
| `ci_high` | `success_ci_high` |
| `mean_best_human_steps` | `mean_best_human_steps` |

Rows without numeric fields, or rows whose primary source is not a CSV, are
skipped. This keeps paper-preparation artifact rows in the registry without
forcing fake numeric checks.

## Source Row Matching

The audit matches registry `configuration` to the source CSV `strategy` or
`configuration` column. R020 uses an explicit alias because the registry names
the method as `lv_voi_scale3`, while the original source CSV stores it as
`method`.

## Current Result

After adding the R035 row, the current registry audit reports:

```text
[numeric-audit] OK rows=24 skipped=10 checks=76 issues=0
[numeric-audit] path=results\EXPERIMENT_EVIDENCE_REGISTRY.csv
```

The numeric paper-facing registry rows are therefore consistent with their
primary CSV sources at the current tolerance.

## Scope Limit

This is not a full manuscript claim audit. It does not read arbitrary prose,
captions, or LaTeX tables. It only verifies the curated numeric fields already
entered in `results/EXPERIMENT_EVIDENCE_REGISTRY.csv`.

## Next Candidate

R036 should build a paper-claim table generator or claim matrix that consumes
the registry and emits manuscript-ready numbers. That would reduce manual
copying before the first full draft.
