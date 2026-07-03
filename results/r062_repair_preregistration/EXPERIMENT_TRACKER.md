# R062 Experiment Tracker

Date: 2026-07-03

| Run ID | Milestone | Purpose | Priority | Status | Decision Gate |
|---|---|---|---|---|---|
| R062-S0 | Candidate logging smoke | Verify `--trace_candidates` writes nonempty gate-evaluation rows in a tiny Lift VoI run. | MUST | Planned, not run in this package | Required before any R063+ online repair. |
| R062-S0b | Optional rejection-coverage smoke | Use an existing score-floor setting only if S0 has no rejected rows. | CONDITIONAL | Planned, not run | Required only when S0 does not exercise rejected-state logging. |
| R063-P0 | Formal repair pre-registration | Freeze the exact trigger rule, baseline comparison, repeated-eval plan, and stop rule. | MUST BEFORE TRAINING | Blocked on R062 smoke | Needed before launching new online repair compute. |
| R063+ | Formal online repair | Test a pre-registered trace-derived repair against cost-matched random-family evidence. | OPTIONAL | Not eligible yet | Eligible only after smoke pass and tested implementation if new code is needed. |

## Current Status

No R062 smoke or formal experiment has been executed in this package. R062 only
records the readiness plan and the required evidence boundary.
