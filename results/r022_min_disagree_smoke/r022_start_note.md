# R022 Start Note: Learning-Value Minimum Disagreement Gate

## Why R022 Exists

R021 showed that current LV-VoI scale3 is dominated by a lower-budget random baseline on Lift. The failure suggests the trigger is not yet selecting intervention states better than random at matched human cost.

## Mechanism Added

R022 adds `--voi_learning_value_min_disagreement`, a conservative filter for learning-value VoI. When a reference policy is available, the VoI gate now requires the current actor action to differ from the reference action by at least this normalized threshold before starting an intervention.

The intended effect is to avoid spending human budget on states where the actor already agrees with the demonstration-nearest reference action. This is a selectivity change, not a larger-budget change.

## Smoke Check

Command shape:

```powershell
python -u scripts\run_comparison.py --task Lift --seeds 0 --strategies voi --budget 60 --total_steps 300 --n_demos 2 --learning_starts 50 --batch_size 64 --gradient_steps 1 --bc_pretrain_steps 20 --bc_actor_reg_coef 5.0 --eval_at_start --eval_every 150 --eval_episodes 2 --takeover_len 5 --voi_tau 0.01 --voi_cquery 0.0 --voi_reference_policy demo_nn --voi_learning_value_scale 3.0 --voi_learning_value_clip 1.0 --voi_learning_value_min_disagreement 0.25 --restore_best_model_at_end --force --out_dir results\r022_min_disagree_smoke
```

Result: the run completed, the new parameter appeared in both the run label and summary schema, and the per-run CSV recorded candidate/score diagnostics. This is only an engineering smoke test, not a scientific result.

## Next Paper-Facing Gate

Run seeds 0-2 before any five-seed expansion:

```powershell
python -u scripts\run_comparison.py --task Lift --seeds 0 1 2 --strategies voi --budget 600 --total_steps 10000 --n_demos 20 --learning_starts 500 --batch_size 256 --gradient_steps 1 --bc_pretrain_steps 5000 --bc_actor_reg_coef 50.0 --eval_at_start --eval_every 2000 --eval_episodes 20 --takeover_len 20 --voi_tau 0.01 --voi_cquery 0.0 --voi_reference_policy demo_nn --voi_learning_value_scale 3.0 --voi_learning_value_clip 1.0 --voi_learning_value_min_disagreement 0.25 --restore_best_model_at_end --out_dir results\r022_lift_min_disagree_seed0_2
```

Decision rule: continue only if the redesigned trigger is not dominated by random_b350 on the same seed subset.
