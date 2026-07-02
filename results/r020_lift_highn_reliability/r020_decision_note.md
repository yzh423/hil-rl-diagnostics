# R020 Decision Note: Lift High-N Checkpoint Reliability

## Raw Data Table

Each checkpoint was evaluated with `5 x 20` autonomous Lift episodes. The five seeds therefore contribute `500` evaluation episodes per strategy.

| Strategy | Successes / Episodes | Repeated Success | Wilson CI | Mean Best Human Steps |
|---|---:|---:|---:|---:|
| No online human | 400 / 500 | 80.0% | 76.3-83.3% | 0.0 |
| Random human | 426 / 500 | 85.2% | 81.8-88.0% | 269.2 |
| LV-VoI scale3 | 416 / 500 | 83.2% | 79.7-86.2% | 202.0 |

Per-seed repeated success:

| Strategy | Seed 0 | Seed 1 | Seed 2 | Seed 3 | Seed 4 |
|---|---:|---:|---:|---:|---:|
| No online human | 74/100 | 78/100 | 80/100 | 82/100 | 86/100 |
| Random human | 69/100 | 99/100 | 61/100 | 98/100 | 99/100 |
| LV-VoI scale3 | 75/100 | 85/100 | 82/100 | 88/100 | 86/100 |

## Key Findings

1. Observation: The LV-VoI scale3 result remains stable under higher-N evaluation: `416/500` (83.2%) versus the earlier `256/300` (85.3%).
2. Observation: Random human is the highest-success point at `426/500` (85.2%), but it uses more mean best-step human cost (`269.2`) than LV-VoI (`202.0`).
3. Observation: LV-VoI improves over no-online by 3.2 percentage points while using 202.0 mean best-step human steps.
4. Interpretation: The defensible main claim is not success dominance over random. The defensible claim is a success-cost tradeoff: LV-VoI reaches near-random success with lower human cost and more stable per-seed behavior than random.

## Decision

Use R020 as the current paper-grade Lift reliability table. Wording should emphasize human-efficiency at near-matched success, not unconditional superiority. The next experimental gap is a budget-matched random comparison around the LV-VoI cost range, so reviewers cannot argue that random would match the method at the same human cost.

Artifacts:

- `results/r020_lift_highn_reliability/r020_lift_highn_seed_table.csv`
- `results/r020_lift_highn_reliability/r020_lift_highn_aggregate.csv`
- `results/r020_lift_highn_reliability/r020_lift_highn_success_cost.png`
