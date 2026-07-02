# R020/R021 Command Provenance Note

Date: 2026-07-02

## Verdict

R020 and R021 are stronger than the earlier R047 gap note implied, but they
still do not have complete original launch-command provenance.

R020 is a repeated-evaluation consolidation. Its 5x20 evaluation CSVs point to
earlier checkpoint files from R004, R010, R012, R013, and R014. Those checkpoint
paths exist locally and are hashed in `r020_r021_checkpoint_inventory.csv`.
Because R020 consolidates earlier checkpoints, it should not be described as a
single original training launch.

R021 has better raw-run provenance for the new cost-matched random budgets.
The `random_b350` and `random_b450` source directories contain
`robosuite_hil_summary.csv`, per-seed `run_*.csv` files, 5x20 repeated
evaluation summaries, and the referenced best checkpoints. These are inventoried
and hashed in `r021_raw_run_inventory.csv` and
`r020_r021_checkpoint_inventory.csv`. However, no central original command file
was found for those runs, so the commands in
`r020_r021_command_reconstruction.csv` are recommended reproduction templates,
not archived original logs.

Machine-readable status:

- `r020_r021_checkpoint_inventory.csv`: 28 source-checkpoint rows, zero missing
  checkpoint files.
- `r021_raw_run_inventory.csv`: 10 R021 raw random-budget run rows, zero missing
  checkpoint files.
- `r020_r021_command_reconstruction.csv`: 6 recommended command-template rows.

## R020 Source Structure

R020 reports 5 seeds x 5 repeats x 20 episodes for three configurations:

- `none`
- `random` / random_b600 interpretation
- `method` / LV-VoI scale3 interpretation

The key source file is
`results/r020_lift_highn_reliability/r020_lift_highn_seed_table.csv`. Each
per-seed row links to a summary CSV, and each summary CSV links to a checkpoint
path. R048 verifies that all checkpoint paths listed from those summaries exist
and are hashable.

## R021 Source Structure

R021 combines:

- `random_b350`: new cost-matched random budget source in
  `results/r021_random_budget350_costmatch/`.
- `random_b450`: new random budget source in
  `results/r021_random_budget450_costmatch/`.
- `none`, `lv_voi_scale3`, and `random_b600`: inherited from the R020
  consolidation.

The main registry source remains
`results/r021_random_costmatch/r021_costmatch_aggregate.csv`, but reviewers can
inspect the R048 inventories to trace where the random_b350 and random_b450
rows came from.

## Command Boundary

Use `r020_r021_command_reconstruction.csv` as a command template source. Its
commands are reconstructed from stored hyperparameters, run labels, current CLI
interfaces, R044 reproduction templates, and the available raw summaries. They
should be useful for fresh reruns into new `results/r0xx_*` directories.

Do not call those commands the historical launch logs. That would overstate the
evidence.

## Practical Next Rule

All future paper-facing runs should save the launch command before starting the
run, together with stdout/stderr, environment snapshot, source snapshot hash,
result manifest, and registry row.
