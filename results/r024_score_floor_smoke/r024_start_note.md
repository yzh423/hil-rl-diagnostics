# R024 Start Note: Score-Calibrated LV-VoI

## Purpose

R024 follows the R023 trace diagnosis. R023 did not support a simple
"LV-VoI intervenes too far from the cube" explanation. The stronger pattern was
score/timing mismatch: early saturated starts and many low-score mid-run starts.

## Implemented Change

Added an optional, default-off VoI score floor on new intervention starts:

- `--voi_score_floor_after_step`
- `--voi_score_floor_after_value`

When `--voi_score_floor_after_value > 0`, a VoI candidate at or after the
configured step must have `score >= value` to start a takeover. Ongoing latched
takeovers are unchanged. Random, always, none, and default VoI behavior are
unchanged when the floor value is zero.

## Smoke Result

Smoke command completed under `results/r024_score_floor_smoke`:

- task: Lift
- seed: 0
- total steps: 300
- score floor: after step 150, require score >= 0.05
- trace: enabled
- restore best: enabled

This is only an engineering check. It verifies CLI forwarding, run labels,
trace creation, summary creation, and checkpoint restore. It is not a paper
result.

## Next Gate

Run Lift seeds 0-2 with the original LV-VoI scale3 configuration plus:

- `--voi_score_floor_after_step 4000`
- `--voi_score_floor_after_value 0.05`

Compare against the existing R023/R021 `random_b350` evidence. Expand only if
the variant is not dominated on success and best-step human cost.
