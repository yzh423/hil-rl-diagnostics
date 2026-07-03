# R062 Candidate-Logging Smoke Plan

Date: 2026-07-03

## Purpose

Verify that the R061 candidate-state trace interface writes auditable rows in a
short Lift VoI run before any formal repair experiment is launched. This smoke
is a plumbing check only.

## Planned Smoke ID

`R062-S0-candidate-trace-smoke`

## Planned Command

```powershell
python scripts\train_robosuite_hil.py --task Lift --strategy voi --budget 40 --total_steps 300 --n_demos 3 --learning_starts 50 --batch_size 32 --gradient_steps 1 --dyn_epochs 1 --dyn_refit_every 50 --eval_every 300 --eval_episodes 2 --takeover_len 5 --seed 0 --trace_candidates --trace_interventions --out_dir results\r062_repair_preregistration\smoke_local --run_label r062_candidate_trace_smoke --no_save_best_model
```

This command intentionally uses tiny training and evaluation settings. It is
not designed to estimate success rate.

## Required Artifacts If Executed

| Artifact | Required check |
|---|---|
| `candidate_trace_*.csv` | Exists, has the R061 candidate schema, and contains at least one gate-evaluated row. |
| `trace_*.csv` | Exists when `--trace_interventions` is enabled; may be empty if no intervention starts in the tiny smoke. |
| `run_*.csv` | Exists and records the smoke evaluation rows. |
| stdout/stderr log | Captures command line, warnings, and any simulator/runtime issue. |
| manifest note | Records whether the smoke passed, failed, or was not run. |

## Pass Criteria

The smoke passes only if:

1. the command completes without a Python exception;
2. the candidate trace file is present and CSV-readable;
3. the candidate trace contains nonempty gate-evaluation rows;
4. the fields `accepted`, `candidate`, `score`, `p_fail`, and
   `rejection_reason` are present;
5. any observed rejected rows have interpretable reasons such as
   `gate_not_candidate` or `score_floor`;
6. no smoke metric is promoted to a paper result.

If the smoke has accepted rows but no rejected rows, it can confirm trace
writing but should not be treated as sufficient diagnostic coverage for a
formal repair. Run a second smoke with a stricter existing score floor only if
rejected-state coverage is needed.

## Optional Rejection-Coverage Smoke

Use only if `R062-S0` produces no rejected candidate rows:

```powershell
python scripts\train_robosuite_hil.py --task Lift --strategy voi --budget 40 --total_steps 300 --n_demos 3 --learning_starts 50 --batch_size 32 --gradient_steps 1 --dyn_epochs 1 --dyn_refit_every 50 --eval_every 300 --eval_episodes 2 --takeover_len 5 --seed 0 --trace_candidates --trace_interventions --voi_score_floor_after_step 50 --voi_score_floor_after_value 0.05 --out_dir results\r062_repair_preregistration\smoke_local_score_floor --run_label r062_candidate_trace_score_floor_smoke --no_save_best_model
```

This optional run is still a logging smoke, not a repair experiment.

## Failure Actions

| Failure | Action |
|---|---|
| Command fails before writing headers | Debug runtime/import issue before any formal experiment. |
| Candidate trace exists but has zero gate-evaluated rows | Adjust smoke length/refit settings; do not launch a formal repair. |
| Candidate trace lacks required fields | Repair R061 logging/tests before any formal experiment. |
| Candidate trace has only accepted rows | Run the optional stricter smoke before claiming rejected-state logging coverage. |
| Smoke succeeds | Use a separate go/no-go decision before freezing any future formal trigger rule and comparison plan. |

## Boundary

Smoke output should remain local plumbing evidence. It should not receive a
success-rate registry row, should not enter manuscript tables, and should not
be used to update the protected R021/R022/R024 result boundary.

## Execution Status

R062-S0 was executed on 2026-07-03. See `SMOKE_RESULT.md` for the artifact
inventory and gate checks. The optional score-floor smoke is not needed because
the first smoke already produced rejected candidate rows.
