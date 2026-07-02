# R021 Decision Note: Cost-Matched Random Check

## Purpose

R020 showed that LV-VoI scale3 reached near-random Lift success with lower mean best-checkpoint human cost than the original random budget-600 baseline. R021 tests the reviewer-critical alternative explanation: random querying at a budget closer to the LV-VoI cost range may match or beat the method.

## Setup

- Task: robosuite Lift
- Seeds: 0-4
- Training horizon: 10k steps
- Checkpoint selection: restored best checkpoint
- Repeated evaluation: 5 repeats x 20 autonomous episodes per seed
- Shared training settings: 20 demos, BC pretrain 5000, BC actor regularization 50.0, learning starts 500, batch size 256, gradient steps 1

## Aggregate Results

| Strategy | Successes / Episodes | Repeated Success | Wilson CI | Mean Best-Step Human Cost | Delta vs LV-VoI |
|---|---:|---:|---:|---:|---:|
| No online | 400 / 500 | 80.0% | 76.3-83.3% | 0.0 | -3.2 pp, -202.0 steps |
| Random b350 | 439 / 500 | 87.8% | 84.6-90.4% | 177.0 | +4.6 pp, -25.0 steps |
| LV-VoI scale3 | 416 / 500 | 83.2% | 79.7-86.2% | 202.0 | reference |
| Random b450 | 426 / 500 | 85.2% | 81.8-88.0% | 250.0 | +2.0 pp, +48.0 steps |
| Random b600 | 426 / 500 | 85.2% | 81.8-88.0% | 269.2 | +2.0 pp, +67.2 steps |

## Interpretation

The cost-matched random check overturns the current LV-VoI Pareto claim. Random b350 is the decisive point: it achieves higher repeated success than LV-VoI scale3 while using fewer mean best-checkpoint human steps. This means the current method cannot be framed as a Pareto-superior human-efficiency result on Lift.

The R020 statement that LV-VoI is near-random at lower cost is no longer sufficient for a main claim, because a lower-budget random baseline dominates it. The result is valuable because it identifies a real scientific failure mode: the current learning-value trigger does not yet allocate human interventions better than a cheaper random budget once random is properly cost-matched.

## Decision

- Do not use current LV-VoI scale3 as the main positive method claim.
- Keep R021 as a mandatory reviewer-defense result and a pivot point.
- Start R022 as a trigger redesign/diagnosis run, not as another scale-up of the dominated variant.

## R022 Direction

The next run should test whether the trigger can beat random b350 by improving selectivity rather than increasing budget. Candidate directions:

1. Add a budget-pacing term so early interventions do not consume useful budget before the policy reaches contact-sensitive states.
2. Calibrate the learning-value trigger against random b350 cost, targeting roughly 175-200 human steps.
3. Log intervention state features and compare where random b350 succeeds against where LV-VoI spends budget.

Minimum R022 gate: on Lift seeds 0-2 first, a redesigned trigger must beat random b350 on success-cost Pareto before expanding to seeds 0-4.
