# R022 Decision Note: Minimum Reference-Disagreement Gate

## Purpose

R022 tested whether the R021 random-dominance failure could be repaired by making learning-value VoI more selective. The added filter, `--voi_learning_value_min_disagreement 0.25`, only allows a reference-policy VoI intervention when the actor action differs sufficiently from the nearest demonstration action.

## Setup

- Task: robosuite Lift
- Seeds: 0-2
- Strategy: LV-VoI scale3 + demo-nearest reference + minimum disagreement 0.25
- Budget: 600 human-control steps
- Training: 10k steps, 20 demos, BC pretrain 5000, BC actor regularization 50.0
- Checkpoint selection: restored best checkpoint
- Repeated evaluation: 5 repeats x 20 autonomous episodes per seed
- Comparator: R021 `random_b350` on the same seeds, same repeated-eval protocol

## Seed Results

| Strategy | Seed | Repeated Success | Successes / Episodes | Best-Step Human Cost |
|---|---:|---:|---:|---:|
| random_b350 | 0 | 74.0% | 74 / 100 | 100 |
| random_b350 | 1 | 98.0% | 98 / 100 | 85 |
| random_b350 | 2 | 87.0% | 87 / 100 | 100 |
| min-disagree LV-VoI | 0 | 61.0% | 61 / 100 | 487 |
| min-disagree LV-VoI | 1 | 93.0% | 93 / 100 | 68 |
| min-disagree LV-VoI | 2 | 72.0% | 72 / 100 | 80 |

## Aggregate

| Strategy | Successes / Episodes | Repeated Success | Wilson CI | Mean Best-Step Human Cost | Delta vs random_b350 |
|---|---:|---:|---:|---:|---:|
| random_b350 | 259 / 300 | 86.3% | 82.0-89.8% | 95.0 | reference |
| min-disagree LV-VoI | 226 / 300 | 75.3% | 70.2-79.9% | 211.7 | -11.0 pp, +116.7 steps |

## Interpretation

The minimum-disagreement filter does not repair the R021 failure. It improves selectivity on seed 1, where the best checkpoint uses only 68 human steps and reaches 93/100 repeated success, but the effect is not robust: seed 0 spends 487 best-step human steps and reaches only 61/100, while seed 2 reaches 72/100. Aggregated over seeds 0-2, the variant is worse than random_b350 in both success and cost.

The failure suggests that action disagreement with the demo-nearest reference is not a sufficient proxy for intervention learning value. The gate still appears to trigger in states where takeover data does not translate into stable autonomous policy quality.

## Decision

- Do not expand `--voi_learning_value_min_disagreement 0.25` to five seeds.
- Do not present this variant as a positive method result.
- Keep R022 as a negative mechanism-ablation result.
- Next work should diagnose where successful random_b350 interventions occur versus where LV-VoI variants spend budget, before adding another trigger heuristic.
