# R036 Registry-Driven Claim Tables

Date: 2026-07-02

Purpose: generate manuscript-ready claim tables directly from
`results/EXPERIMENT_EVIDENCE_REGISTRY.csv` after source validation and numeric
audit have passed.

## Change

R036 adds:

- `foresight_hil/evaluation/claim_tables.py`
- `scripts/generate_claim_tables.py`
- `tests/test_claim_tables.py`

The generation interface is:

- `read_registry_rows(registry_csv)`
- `build_main_costmatched_claims(registry_rows)`
- `build_trigger_repair_claims(registry_rows)`
- `render_claims_markdown_table(title, rows)`
- `render_claims_latex_table(rows, caption, label, highlight_configurations=None)`
- `write_claim_table_assets(registry_csv, output_dir, figure_dir)`

The CLI command is:

```bash
python scripts/generate_claim_tables.py
```

## Generated Assets

| File | Purpose |
|---|---|
| `main_costmatched_claims.md` | Traceable Markdown table for the main R020/R021 cost-matched claim. |
| `trigger_repair_claims.md` | Traceable Markdown table for R022/R024 negative trigger-repair claims. |
| `figures/TABLE_registry_costmatched_results_r036.tex` | LaTeX table for the registry-generated main cost-matched result. |
| `figures/TABLE_registry_trigger_repairs_r036.tex` | LaTeX table for registry-generated trigger-repair results. |
| `figures/latex_includes_r036.tex` | LaTeX include snippet for both generated tables. |

## Claim Logic

The main table uses:

- R020 `none` as the no-intervention reference row;
- R021 `random_b350`, `lv_voi_scale3`, `random_b450`, and `random_b600`;
- R021 `lv_voi_scale3` as the delta reference.

The trigger-repair table uses:

- R024 `random_b350` as the same-seed baseline and delta reference;
- R022 `min_disagree_vlv0p25`;
- R024 `score_floor_vlv3_after4000_floor0p05`.

This preserves the current paper route: the tables support the diagnostic
protocol and negative trigger-repair claims, not LV-VoI superiority.

## Verification

The generated tables were checked after R035 numeric audit:

```text
python scripts\validate_evidence_registry.py
[registry] OK rows=25 sources=25 csv_sources=14 issues=0

python scripts\audit_registry_numbers.py
[numeric-audit] OK rows=25 skipped=11 checks=76 issues=0

python -m unittest discover -s tests
Ran 72 tests
OK
```

## Next Candidate

R037 should either finish the R027 citation metadata/context audit or build a
minimal manuscript skeleton that imports R029/R036 assets and keeps claims
tethered to the registry.
