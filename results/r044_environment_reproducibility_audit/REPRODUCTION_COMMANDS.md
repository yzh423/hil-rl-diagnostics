# R044 Reproduction Commands

Date: 2026-07-02

This command sheet is a central reproduction entry point. Historical result
directories must not be overwritten. Regenerations should write to a fresh
`results/r0xx_*` directory and then be compared against the registry.

## Repository Verification

Run after project-structure, evidence-registry, paper-asset, or evaluation-code
changes:

```powershell
python scripts\validate_evidence_registry.py
python scripts\audit_registry_numbers.py
python scripts\generate_claim_tables.py
python -m unittest discover -s tests
```

Run when bibliography entries change:

```powershell
python C:\Users\14228\.codex\skills\citation-management\scripts\validate_citations.py paper\references.bib --report results\r042_citation_context_audit\paper_references_validation_after_r042.json --verbose
```

## Smoke Checks

Toy smoke:

```powershell
python scripts\run_demo.py --num_envs 32 --episodes 2 --max_steps 30 --budget 2 --takeover_len 3 --horizon 3 --seed 44
```

Reacher fallback smoke:

```powershell
python scripts\train_robosuite_hil.py --task Reacher --strategy none --total_steps 5 --n_demos 1 --learning_starts 20 --batch_size 8 --gradient_steps 1 --eval_every 5 --eval_episodes 1 --seed 44 --out_dir results\r044_environment_reproducibility_audit\smoke_reacher --no_save_best_model
```

Robosuite Lift smoke template:

```powershell
python scripts\train_robosuite_hil.py --task Lift --strategy none --total_steps 600 --n_demos 5 --learning_starts 200 --eval_every 600 --eval_episodes 3 --seed 0 --out_dir results\r0xx_lift_smoke --no_save_best_model
```

Smoke runs should not be used as paper evidence.

## Paper-Core Reproduction Planning

Full paper-core reruns are expensive. Use fresh output directories, preserve
stdout/stderr, and compare regenerated aggregates against the registry before
drafting any updated claim.

### R021 Cost-Matched Random Family Template

Use this only as a fresh reproduction target, not to overwrite
`results/r021_random_costmatch/`:

```powershell
python -u scripts\run_comparison.py --task Lift --seeds 0 1 2 3 4 --strategies random --budget 350 --total_steps 10000 --n_demos 20 --learning_starts 500 --batch_size 256 --gradient_steps 1 --bc_pretrain_steps 5000 --bc_actor_reg_coef 50.0 --eval_at_start --eval_every 2000 --eval_episodes 20 --takeover_len 20 --voi_tau 0.01 --voi_cquery 0.0 --voi_reference_policy demo_nn --voi_learning_value_scale 3.0 --voi_learning_value_clip 1.0 --restore_best_model_at_end --out_dir results\r0xx_reproduce_random_b350
```

For `random_b450` and `random_b600`, change `--budget` and output directory.
Regenerate repeated checkpoint summaries before comparing to the registry.

### R023 Real Trace Reproduction

Historical exact commands are already archived:

```powershell
Get-Content results\r023_real_trace_seed0_2\driver.cmd.txt
Get-Content results\r023_real_trace_seed0_2\random_b350.cmd.txt
```

The archived main command:

```powershell
python -u scripts\run_comparison.py --task Lift --seeds 0 1 2 --strategies random voi --budget 600 --total_steps 10000 --n_demos 20 --learning_starts 500 --batch_size 256 --gradient_steps 1 --bc_pretrain_steps 5000 --bc_actor_reg_coef 50.0 --eval_at_start --eval_every 2000 --eval_episodes 20 --takeover_len 20 --voi_tau 0.01 --voi_cquery 0.0 --voi_reference_policy demo_nn --voi_learning_value_scale 3.0 --voi_learning_value_clip 1.0 --trace_interventions --restore_best_model_at_end --out_dir results\r023_real_trace_seed0_2
```

For a new reproduction, change `--out_dir` to a fresh directory.

### R024 Score-Floor Reproduction

Historical command file:

```powershell
Get-Content results\r024_score_floor_seed0_2\run_driver.cmd
```

Core command:

```powershell
python -u scripts\run_comparison.py --task Lift --seeds 0 1 2 --strategies voi --budget 600 --total_steps 10000 --n_demos 20 --learning_starts 500 --batch_size 256 --gradient_steps 1 --bc_pretrain_steps 5000 --bc_actor_reg_coef 50.0 --eval_at_start --eval_every 2000 --eval_episodes 20 --takeover_len 20 --voi_tau 0.01 --voi_cquery 0.0 --voi_reference_policy demo_nn --voi_learning_value_scale 3.0 --voi_learning_value_clip 1.0 --voi_score_floor_after_step 4000 --voi_score_floor_after_value 0.05 --trace_interventions --restore_best_model_at_end --out_dir results\r0xx_reproduce_score_floor_seed0_2
```

### Repeated Checkpoint Evaluation Template

Use this after locating a saved `best_*.zip` checkpoint:

```powershell
python scripts\evaluate_checkpoint.py --checkpoint <path\to\best_checkpoint.zip> --task Lift --episodes 20 --repeats 5 --seed <seed> --out_csv results\r0xx_reproduce\checkpoint_reeval.csv --summary_csv results\r0xx_reproduce\checkpoint_reeval_summary.csv
```

### Claim Table Regeneration

After registry updates:

```powershell
python scripts\generate_claim_tables.py
```

Check the generated files in `figures/` before referencing them in the
manuscript.
