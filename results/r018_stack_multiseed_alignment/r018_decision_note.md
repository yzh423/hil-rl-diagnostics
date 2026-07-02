# R018 Decision Note: Stack Matched Multi-Seed Alignment

## Raw Data Table

All rows use robosuite `Stack`, 50 demos, 10000 BC pretraining steps, SAC online training, restore-best checkpointing, and repeated checkpoint evaluation with `3 x 20` episodes per seed.

| Strategy | Seeds | Successes / Episodes | Repeated Success | Wilson CI | Mean Best Human Steps |
|---|---:|---:|---:|---:|---:|
| No online human, matched BC | 0,1,2 | 131 / 180 | 72.8% | 65.9-78.8% | 0.0 |
| Random human, matched BC | 0,1,2 | 107 / 180 | 59.4% | 52.2-66.4% | 478.0 |
| Stack-tuned LV-VoI | 0,1,2 | 107 / 180 | 59.4% | 52.2-66.4% | 433.3 |

Per-seed repeated success:

| Strategy | Seed 0 | Seed 1 | Seed 2 |
|---|---:|---:|---:|
| No online human, matched BC | 47/60 | 39/60 | 45/60 |
| Random human, matched BC | 40/60 | 42/60 | 25/60 |
| Stack-tuned LV-VoI | 47/60 | 33/60 | 27/60 |

## Key Findings

1. Observation: The Stack-tuned LV-VoI candidate matches random human intervention in aggregate (`107/180`) but is clearly below the matched no-online baseline (`131/180`).
2. Interpretation: The R017 seed-0 recovery was not stable across seeds. With a strong 50-demo / 10000-step BC initialization, Stack does not currently benefit from extra online human replay.
3. Implication: Stack cannot be used as a positive robotics breadth claim for the current FORESIGHT-HIL method. The honest paper claim should remain Lift-centered, with Stack used as a failure-analysis and motivation case.
4. Next step: Redesign the Stack intervention mechanism around task phase and online-update safety, rather than applying the Lift LV-VoI trigger more aggressively.

## Decision

Do not expand this exact Stack-tuned LV-VoI configuration to more seeds. Start R019 as a mechanism-redesign run: compare the strong no-online Stack actor against variants that limit online interventions to phase-aware, high-risk states and reduce destructive updates after good BC behavior.

Artifacts:

- `results/r018_stack_multiseed_alignment/r018_stack_multiseed_seed_table.csv`
- `results/r018_stack_multiseed_alignment/r018_stack_multiseed_aggregate.csv`
- `results/r018_stack_multiseed_alignment/r018_stack_multiseed_success_cost.png`
