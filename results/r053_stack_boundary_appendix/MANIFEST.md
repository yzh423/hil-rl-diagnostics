# R053 Stack Boundary Appendix Manifest

Date: 2026-07-03

## Purpose

R053 packages Stack as a clean appendix-ready boundary-evidence module. It uses
existing R018/R019 results and does not add new experiments or edit historical
raw CSVs.

## Inputs

| Source | Role |
|---|---|
| `results/r018_stack_multiseed_alignment/r018_stack_multiseed_aggregate.csv` | Registered multiseed Stack boundary comparison. |
| `results/r018_stack_multiseed_alignment/r018_stack_multiseed_seed_table.csv` | Per-seed traceability for the R018 aggregate. |
| `results/r019_stack_mechanism_redesign/r019_stack_seed0_mechanism_summary.csv` | Seed-0 mechanism probe used only as supporting context. |

## Outputs

| File | Purpose |
|---|---|
| `results/r053_stack_boundary_appendix/STACK_BOUNDARY_APPENDIX.md` | R053 interpretation and claim boundaries. |
| `results/r053_stack_boundary_appendix/stack_boundary_claims.md` | Markdown table generated from registered R018 rows. |
| `figures/TABLE_stack_boundary_appendix_r053.tex` | LaTeX appendix table generated from registered R018 rows. |
| `scripts/generate_stack_boundary_appendix.py` | Reproducible generation script. |

## Regeneration

```powershell
python scripts\generate_stack_boundary_appendix.py
```

## Boundary

R053 is robotics breadth evidence, not a positive method result. It should be
used to keep the paper honest about task transfer limits.
