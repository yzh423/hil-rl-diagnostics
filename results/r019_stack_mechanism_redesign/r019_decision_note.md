# R019 Decision Note: Stack Mechanism Redesign Diagnostics

## Raw Data Table

All rows are Stack seed 0 with 50 demos, 10000 BC pretraining steps, SAC online training, restore-best checkpointing, and repeated best-checkpoint evaluation with `3 x 20` episodes.

| Variant | Successes / Episodes | Repeated Success | Wilson CI | Best Human Steps | Interpretation |
|---|---:|---:|---:|---:|---|
| No online human, matched BC | 47 / 60 | 78.3% | 66.4-86.9% | 0 | Strong baseline |
| R017 tau0 LV-VoI | 47 / 60 | 78.3% | 66.4-86.9% | 600 | Matches no-online but spends full budget |
| R019 starts-only demo replay | 38 / 60 | 63.3% | 50.7-74.4% | 0 | Lower than no-online; best checkpoint is pre-online |
| R019 Stack phase guard, budget 600 | 35 / 60 | 58.3% | 45.7-69.9% | 252 | Single-eval spike did not survive repeated eval |
| R019 Stack phase guard, budget 300 | 34 / 60 | 56.7% | 44.1-68.4% | 0 | Budget clamp did not rescue the variant |

## Code Changes Tested

- `--intervention_demo_mode all|starts|none`: controls whether intervention transitions enter the demo replay used by actor BC regularization.
- `--voi_phase_guard none|stack_pick_place`: masks Stack VoI starts outside contact-sensitive pick/place windows.

Both default to the original behavior (`all`, `none`), so prior runs remain comparable.

## Key Findings

1. Update-safe replay alone does not explain the Stack failure. Restricting demo replay to engagement starts lowered repeated success to `38/60`.
2. The Stack phase guard reduced early spending and produced a single training eval of 75% at step 4000, but repeated evaluation fell to `35/60`.
3. Reducing the phase-guard budget to 300 did not help; the best checkpoint was again the pre-online actor.
4. R017's positive seed-0 result is not enough to justify scaling this Stack online-intervention direction because the matched no-online actor gets the same repeated success with zero online human cost.

## Decision

Do not expand these R019 Stack variants to more seeds. Treat Stack as a failure-analysis case showing that strong demo-regularized SAC can dominate naive online intervention. The next productive step is to return to the Lift main claim and run paper-grade reliability checks, or pick a different second task only after defining a stronger task-aware intervention mechanism.

Artifacts:

- `results/r019_stack_mechanism_redesign/r019_stack_seed0_mechanism_summary.csv`
- `results/r019_stack_mechanism_redesign/r019_stack_seed0_mechanism_summary.png`
