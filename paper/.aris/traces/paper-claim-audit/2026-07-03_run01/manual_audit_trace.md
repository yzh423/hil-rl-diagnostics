# Manual Paper Claim Audit Trace

Date: 2026-07-03

## Procedure

1. Extracted numeric, comparison, and scope claims from `paper/main.tex`,
   `paper/sections/*.tex`, and R036 LaTeX claim tables.
2. Checked core Lift values against the registry and R020-R024 aggregate/trace
   sources.
3. Checked Stack boundary values against R018/R019 sources.
4. Checked reproducibility and provenance language against R047/R048/R049 and
   the current Git state.
5. Repaired one stale provenance wording issue in
   `paper/sections/07_reproducibility_inventory.tex`.

## Commands And Sources

- `rg -n "\\d|dominates|dominated|success|cost|starts|Stack|Lift|95\\%|CI|human|zero|R0|same-seed|lower|higher|repair|trace" paper\main.tex paper\sections`
- `Get-Content results\EXPERIMENT_EVIDENCE_REGISTRY.csv`
- `Get-Content results\r021_random_costmatch\r021_costmatch_aggregate.csv`
- `Get-Content results\r022_lift_min_disagree_seed0_2\r022_min_disagree_aggregate.csv`
- `Get-Content results\r023_real_trace_seed0_2\r023_trace_strategy_diagnostics.csv`
- `Get-Content results\r024_score_floor_seed0_2\r024_score_floor_aggregate.csv`
- `Get-Content results\r024_score_floor_seed0_2\r024_trace_strategy_compare.csv`
- `Get-Content results\r018_stack_multiseed_alignment\r018_stack_multiseed_aggregate.csv`
- `git rev-parse HEAD`
- `git remote -v`
- `git branch --show-current`

## Outcome

The manuscript claim audit passed after repairing the stale provenance wording.
No raw evidence files were edited.
