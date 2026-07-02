# R023 Diagnostic Note: Real Intervention Traces

## Purpose

R023 reran the real Lift seeds 0-2 comparison with intervention-start tracing enabled, without adding a new method. The goal was to explain why cost-matched random beats current LV-VoI variants before designing R024.

## Compared Configurations

- `random_b350`: random intervention starts, budget 350, seeds 0-2
- `lv_voi_scale3`: original LV-VoI scale3, budget 600, seeds 0-2
- Shared training setup: 10k steps, 20 demos, BC pretrain 5000, BC actor regularization 50.0, takeover length 20, eval every 2000, eval episodes 20, restore best checkpoint
- Trace row: one row per intervention start with step, budget fraction, score/p_fail when available, and privileged Lift geometry

These are trace reruns for diagnosis. The paper-grade success claims should still use the repeated-evaluation R020-R022 tables.

## Key Trace Results

| Strategy | Starts | Mean starts / seed | Median start step | Early 0-2k | Mid 2-6k | Late 6-10k | Mean g2c norm | Mean g2c xy | Mean final success | Mean best cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| random_b350 | 55 | 18.3 | 4451 | 27.3% | 34.5% | 38.2% | 0.285 | 0.235 | 83.3% | 95.0 |
| lv_voi_scale3 | 96 | 32.0 | 4624 | 12.5% | 50.0% | 37.5% | 0.217 | 0.152 | 81.7% | 276.0 |

## Interpretation

The trace does not support the simple hypothesis that LV-VoI fails because it intervenes far from the object. In fact, LV-VoI starts are closer to the cube than random starts on both 3D and XY gripper-to-cube distance.

The stronger failure pattern is score/timing mismatch:

- LV-VoI starts more interventions than random: 96 vs 55 starts across seeds 0-2.
- LV-VoI has a hard discontinuity in timing: 12 starts in 0-2k, zero starts in 2-4k, then 48 starts in 4-6k.
- The 0-2k LV-VoI starts are all saturated (`score=10`, `p_fail=1`), suggesting early model/value calibration artifacts.
- The 4-10k LV-VoI starts are mostly very low score / low p_fail but still pass the low `tau=0.01` threshold.
- LV-VoI can reach high single-eval success, but it often keeps spending after a strong checkpoint and does not convert the extra starts into a robust cost advantage.

## R024 Decision

Do not make R024 a phase-aware/contact-aware trigger yet. The traces show LV-VoI already tends to intervene closer to the cube than random, so a contact-window heuristic is not the first repair.

R024 should test score-calibrated LV-VoI:

1. Keep the same geometry/task setup.
2. Suppress low-confidence mid/late starts, e.g. by increasing the effective threshold after warm-up or using a quantile/score-floor gate.
3. Preserve the ability to intervene early, but treat saturated `score=10, p_fail=1` events as a calibration warning and log them separately.
4. Gate expansion by the same cost-matched criterion: seeds 0-2 first, then only expand if the variant is not dominated by `random_b350`.

If score-calibrated LV-VoI still fails, the paper should pivot from trigger superiority to a cost-matched HIL-RL diagnostic benchmark with negative findings and a redesigned evaluation protocol.
