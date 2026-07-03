# R053 Stack Boundary Appendix

Date: 2026-07-03

## Verdict

R053 strengthens robotics breadth as boundary evidence, not as a positive
transfer result.

The cleaned Stack evidence says that adding online interventions is not
automatically beneficial under the current mechanism. In the registered R018
multiseed Stack comparison, the no-online matched behavioral-cloning baseline
is stronger than both online-intervention variants:

| Strategy | Evidence | Interpretation |
|---|---:|---|
| No-online matched BC | `131/180 = 72.8%`, cost `0.0` | Strong zero-online-human reference. |
| Random matched BC | `107/180 = 59.4%`, cost `478.0` | Negative online-intervention boundary evidence. |
| Stack-tuned LV-VoI | `107/180 = 59.4%`, cost `433.3` | Negative trigger-transfer boundary evidence. |

R019 remains a seed-0 mechanism probe rather than multiseed paper-core
evidence. Its update-safe and phase-guard variants stayed below the seed-0
no-online matched reference, so it supports the conservative interpretation but
should not be promoted to a broad method claim.

## Generated Assets

| Artifact | Purpose |
|---|---|
| `results/r053_stack_boundary_appendix/stack_boundary_claims.md` | Registry-generated Markdown table for Stack boundary evidence. |
| `figures/TABLE_stack_boundary_appendix_r053.tex` | Ready-to-include LaTeX appendix table. |
| `scripts/generate_stack_boundary_appendix.py` | Reproducible table-generation entry point. |

## Allowed Use

Use R053 to say:

- Stack is retained as robotics breadth and boundary evidence.
- The current online-intervention mechanism does not transfer as a positive
  Stack result.
- Strong no-online/BC baselines should be included before claiming that HIL-RL
  interventions help on a harder manipulation task.

Do not use R053 to claim:

- broad robotics generalization;
- LV-VoI superiority;
- real-human or real-robot validation;
- a new trigger method.
