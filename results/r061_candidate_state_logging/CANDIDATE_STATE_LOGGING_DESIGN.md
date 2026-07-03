# R061 Candidate-State Logging Design

Date: 2026-07-03

## Verdict

R061 adds the missing logging layer required before a new online trigger repair:
future VoI runs can now write one row per gate-evaluated state, not only one row
per accepted intervention start.

This directly addresses the R060 limitation. R060 showed that post-hoc filters
over accepted starts can look selective even though the actual score-floor
online follow-up still spent nearly as many starts. Candidate-state traces give
future audits the rejected states needed to distinguish score/gate selectivity
from replacement dynamics.

## Interface

Enable candidate-state traces with:

```powershell
python scripts\train_robosuite_hil.py ... --trace_candidates
```

Optionally choose the output path with:

```powershell
--candidate_trace_path results\r062_example\candidate_trace.csv
```

If no explicit path is provided, the training script writes:

```text
candidate_trace_<run_tag>.csv
```

under the run output directory.

## Row Semantics

The candidate trace writes a row only when the VoI gate is actually evaluated.
Each row records:

| Field family | Meaning |
|---|---|
| Step context | `env_step`, `episode`, `episode_step`, task, strategy, seed. |
| Budget context | cumulative `human_steps`, `budget_used_frac`, and `engagements` after the decision. |
| Decision context | `gate_evaluated`, `intervened`, `accepted`, `candidate`, `score`, `p_fail`, `score_floor_blocked`, `rejection_reason`. |
| Privileged geometry | Lift/Stack diagnostic geometry copied from the existing intervention trace schema. |

`accepted=1` means the gate evaluation started a new intervention. Rejected rows
use `rejection_reason`, currently including `gate_not_candidate` and
`score_floor`. Ongoing takeover steps, pacing blocks, and exhausted-budget
steps are not candidate rows because the VoI gate is not evaluated there.

## Use In Future Experiments

For any R064+ online repair after the R062 smoke/pre-registration gate and a
reversal of the R063 no-go decision:

1. Pre-register the trigger rule and expected stop gate.
2. Run with `--trace_candidates` and `--trace_interventions`.
3. Archive exact command, stdout/stderr, Git commit, environment summary, raw
   run CSV, candidate trace, intervention trace, and repeated-evaluation CSVs.
4. Compare against the cost-matched random family before writing any positive
   method prose.
5. Register the result row and rerun claim/numeric audits before manuscript use.

## Boundary

R061 does not run a new experiment and does not change any historical result.
It only makes future experiments auditable enough to test trace-derived repairs.
