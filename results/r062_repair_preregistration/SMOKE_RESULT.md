# R062 Candidate-Logging Smoke Result

Date: 2026-07-03

## Verdict

R062-S0 passed the logging-readiness gate. The tiny Lift VoI smoke wrote
nonempty candidate-state traces with both accepted and rejected gate-evaluation
rows. This result verifies logging plumbing only; it is not paper performance
evidence and must not be used to change the protected R021/R022/R024 empirical
boundary.

## Command

```powershell
python scripts\train_robosuite_hil.py --task Lift --strategy voi --budget 40 --total_steps 300 --n_demos 3 --learning_starts 50 --batch_size 32 --gradient_steps 1 --dyn_epochs 1 --dyn_refit_every 50 --eval_every 300 --eval_episodes 2 --takeover_len 5 --seed 0 --trace_candidates --trace_interventions --out_dir results\r062_repair_preregistration\smoke_local --run_label r062_candidate_trace_smoke --no_save_best_model
```

Console output was archived at
`results/r062_repair_preregistration/smoke_local/r062_candidate_trace_smoke_console.log`.
PowerShell reported a `NativeCommandError` because Gym/robosuite warnings were
written to stderr, but the log contains a `[done]` line and no Python traceback
or exception.

## Artifacts

| Artifact | Result |
|---|---|
| `smoke_local/candidate_trace_Lift_voi_b40_seed0_r062_candidate_trace_smoke.csv` | 14 gate-evaluated rows. |
| `smoke_local/trace_Lift_voi_b40_seed0_r062_candidate_trace_smoke.csv` | 8 intervention-start rows. |
| `smoke_local/run_Lift_voi_b40_seed0_r062_candidate_trace_smoke.csv` | One smoke evaluation row at step 300. |
| `smoke_local/robosuite_hil_summary.csv` | Summary row for the smoke run. |
| `smoke_local/r062_candidate_trace_smoke_console.log` | Captured warnings, command progress, and final `[done]` line. |

## Gate Checks

| Check | Observation | Status |
|---|---|---|
| Candidate trace exists and is CSV-readable | File exists and imports with 14 rows. | PASS |
| Candidate trace has nonempty gate-evaluation rows | 14 rows. | PASS |
| Required fields exist | `accepted`, `candidate`, `score`, `p_fail`, and `rejection_reason` are present. | PASS |
| Accepted rows are represented | 8 rows have `accepted=1`. | PASS |
| Rejected rows are represented | 6 rows have `rejection_reason=gate_not_candidate`. | PASS |
| Intervention trace exists | 8 accepted starts were written to the intervention trace. | PASS |
| Smoke metrics are excluded from paper claims | No registry success-rate row was added for the smoke. | PASS |

## Boundary

The optional score-floor rejection-coverage smoke is not needed because R062-S0
already exercised rejected-state logging. R063-P0 later records no-go for
formal online repair before the current submission. A future R064+ formal repair
still requires a separately frozen trigger rule, exact command logs, repeated
evaluation, candidate-state traces, intervention traces, cost-matched random
comparison, registry row, and paper-claim audit before manuscript claims can
change.
