# R024 Decision Note: Score-Floor LV-VoI

## Purpose

R024 tested the R023 diagnosis that current LV-VoI wastes budget on low-score
mid/late starts. The tested repair was a default-off score floor:

- original LV-VoI scale3
- budget 600
- `--voi_score_floor_after_step 4000`
- `--voi_score_floor_after_value 0.05`
- Lift seeds 0-2
- repeated checkpoint evaluation: `5 x 20` episodes per seed

## Result

| Strategy | Successes / Episodes | Repeated Success | Wilson CI | Mean Best-Step Human Cost | Delta vs random_b350 |
|---|---:|---:|---:|---:|---:|
| random_b350 | 259 / 300 | 86.3% | 82.0-89.8% | 95.0 | reference |
| R024 score-floor LV-VoI | 233 / 300 | 77.7% | 72.6-82.0% | 253.3 | -8.7 pp, +158.3 steps |
| R022 min-disagree LV-VoI | 226 / 300 | 75.3% | 70.2-79.9% | 211.7 | -11.0 pp, +116.7 steps |

Seed-level R024 repeated success:

| Seed | Repeated Success | Successes / Episodes | Best Step | Best Human Steps |
|---:|---:|---:|---:|---:|
| 0 | 61.0% | 61 / 100 | 2000 | 80 |
| 1 | 94.0% | 94 / 100 | 10000 | 600 |
| 2 | 78.0% | 78 / 100 | 4000 | 80 |

## Trace Diagnosis

R024 did enforce the floor mechanically: after step 4000, there were zero
intervention starts with score below 0.05. However, it did not solve the budget
problem:

- R023 original LV-VoI scale3: 96 starts across seeds 0-2.
- R024 score-floor LV-VoI: 94 starts across seeds 0-2.
- random_b350: 55 starts across seeds 0-2.

The score floor shifted which mid/late starts were accepted, but the accepted
starts still passed the low threshold often enough to consume nearly the full
budget on seeds 1 and 2. The median R024 start score is only about 0.067, so a
0.05 floor is too weak to create random-level selectivity. More importantly,
the result suggests that raw VoI score magnitude is not calibrated well enough
to be a reliable standalone budget controller.

## Decision

Do not expand R024 to five seeds. R024 is dominated by `random_b350` on the
same seed subset: lower repeated success and much higher best-step human cost.

This strengthens the pivot recommended after R023: the paper should no longer
center on "VoI trigger superiority" unless a substantially different mechanism
is introduced. The stronger near-term paper direction is:

1. cost-matched HIL-RL diagnostic benchmark,
2. negative findings for intuitive VoI/disagreement/score-floor triggers,
3. intervention-timing and evaluation-protocol analysis,
4. redesigned protocol showing why random baselines and repeated checkpoint
   evaluation are necessary.

## Artifacts

- `r024_score_floor_seed_table.csv`
- `r024_score_floor_aggregate.csv`
- `r024_trace_strategy_compare.csv`
- `r024_trace_seed_diagnostics.csv`
- `r024_trace_time_bins_compare.csv`
- `r024_success_cost_compare.png`
- `r024_intervention_timing_bins_compare.png`
- `r024_score_over_time.png`
