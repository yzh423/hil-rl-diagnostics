# R062 Experiment Tracker

Date: 2026-07-03

| Run ID | Milestone | Purpose | Priority | Status | Decision Gate |
|---|---|---|---|---|---|
| R062-S0 | Candidate logging smoke | Verify `--trace_candidates` writes nonempty gate-evaluation rows in a tiny Lift VoI run. | MUST | PASS: 14 candidate rows, 8 accepted, 6 rejected | Satisfies logging smoke prerequisite for a future R063-P0 design step. |
| R062-S0b | Optional rejection-coverage smoke | Use an existing score-floor setting only if S0 has no rejected rows. | CONDITIONAL | Not needed | S0 already exercised rejected-state logging. |
| R063-P0 | Formal repair pre-registration | Freeze the exact trigger rule, baseline comparison, repeated-eval plan, and stop rule. | MUST BEFORE TRAINING | Not started | Needed before launching new online repair compute. |
| R063+ | Formal online repair | Test a pre-registered trace-derived repair against cost-matched random-family evidence. | OPTIONAL | Not eligible yet | Eligible only after a frozen R063-P0 design and tested implementation if new code is needed. |

## Current Status

R062-S0 has been executed as a smoke only. It confirms candidate-state logging
coverage for accepted and rejected gate-evaluated rows, but it does not support
any method-performance claim.
