# R023 Start Note: Intervention Timing Trace

## Purpose

R021 and R022 show that current LV-VoI trigger variants are dominated by cost-matched random. R023 therefore starts with diagnosis instead of another trigger heuristic: record where intervention starts occur, then compare random and LV-VoI budget spending patterns.

## Instrumentation Added

`scripts/train_robosuite_hil.py` now supports:

```powershell
--trace_interventions
--trace_path <optional csv path>
```

When enabled, the trainer writes one CSV row per intervention start. The trace includes:

- training step, episode, episode step
- strategy, seed, human steps, budget fraction, engagement count
- VoI candidate / score / p_fail when available
- privileged simulator geometry for diagnosis: eef height, cube height, gripper-to-cube distance, and Stack cubeA/cubeB fields when present

Default behavior is unchanged when tracing is disabled.

## Smoke Check

Command:

```powershell
python -u scripts\run_comparison.py --task Lift --seeds 0 --strategies random voi --budget 60 --total_steps 300 --n_demos 2 --learning_starts 50 --batch_size 64 --gradient_steps 1 --bc_pretrain_steps 20 --bc_actor_reg_coef 5.0 --eval_at_start --eval_every 150 --eval_episodes 2 --takeover_len 5 --voi_tau 0.01 --voi_cquery 0.0 --voi_reference_policy demo_nn --voi_learning_value_scale 3.0 --voi_learning_value_clip 1.0 --voi_learning_value_min_disagreement 0.25 --trace_interventions --restore_best_model_at_end --force --out_dir results\r023_trace_smoke
```

Smoke result:

| Strategy | Trace Rows | First Start | Last Start | Mean gripper-to-cube norm |
|---|---:|---:|---:|---:|
| random | 13 | step 1 | step 296 | 0.2295 |
| voi | 3 | step 1 | step 54 | 0.2795 |

This is an engineering check only. It shows the trace path works and records non-empty geometry; it is not a paper result.

## Next Gate

Run instrumented traces on the actual R021/R022 comparison settings for seeds 0-2, then compare intervention start timing and geometry before proposing another trigger.
