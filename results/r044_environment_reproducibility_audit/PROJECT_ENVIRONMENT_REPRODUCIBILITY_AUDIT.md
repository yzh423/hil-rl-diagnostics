# R044 Project Environment, Reproducibility, and Innovation Audit

Date: 2026-07-02

## Executive Verdict

The local project is runnable enough for verification, smoke reproduction, and
continued manuscript work. The strongest scientific route remains the
cost-matched HIL-RL diagnostic protocol with a robotic manipulation case study,
not a positive LV-VoI trigger-superiority claim.

The main strengths are:

- an evidence registry with source and numeric audit tooling;
- repeated checkpoint evaluation for paper-core Lift claims;
- trace diagnostics for intervention starts;
- explicit protected boundaries around scripted-oracle, simulation-only
  evidence.

The main gaps before an SCI Q1 submission are:

- invalid local Git metadata, which weakens version provenance;
- no prior single central reproduction command sheet for R020-R024;
- no dedicated compute/wall-time accounting table for paper-core runs;
- no T-ASE-style Note to Practitioners or reproducibility appendix inventory;
- limited robotics breadth beyond Lift, with Stack currently serving as
  boundary evidence rather than a positive transfer result;
- unresolved local LaTeX compile environment.

## Local Runtime Snapshot

Observed in the local workspace:

| Component | Observed state |
|---|---|
| Python | `Python 3.11.13` |
| NumPy | `1.26.4` |
| Gymnasium | `0.28.1` |
| Stable-Baselines3 | `2.3.2` |
| MuJoCo | `3.3.0` |
| robosuite | `1.5.2` |
| PyTorch | `2.4.0+cu124` |
| CUDA from PyTorch | available, CUDA `12.4` |

CLI import/help checks completed for:

- `python scripts\run_demo.py --help`
- `python scripts\run_comparison.py --help`
- `python scripts\evaluate_checkpoint.py --help`
- `python scripts\plot_results.py --help`
- `python scripts\train_robosuite_hil.py --help`

Known warning: Stable-Baselines3 imports the old `gym` compatibility layer and
prints the upstream Gym unmaintained warning. This is a warning, not a current
test failure; the project wrapper itself uses Gymnasium-style APIs.

## Smoke Runs

Two short smoke checks were run to verify code-path viability only.

### Toy Demo Smoke

Command:

```powershell
python scripts\run_demo.py --num_envs 32 --episodes 2 --max_steps 30 --budget 2 --takeover_len 3 --horizon 3 --seed 44
```

Observed summary:

| Strategy | Smoke success |
|---|---:|
| none | 3.1% |
| always | 6.2% |
| random | 9.4% |
| voi | 21.9% |

Interpretation: this is a toy-path smoke only. It should not be transferred to
the robosuite paper claim.

### Reacher Fallback Smoke

Command:

```powershell
python scripts\train_robosuite_hil.py --task Reacher --strategy none --total_steps 5 --n_demos 1 --learning_starts 20 --batch_size 8 --gradient_steps 1 --eval_every 5 --eval_episodes 1 --seed 44 --out_dir results\r044_environment_reproducibility_audit\smoke_reacher --no_save_best_model
```

Observed files:

- `results/r044_environment_reproducibility_audit/smoke_reacher/robosuite_hil_summary.csv`
- `results/r044_environment_reproducibility_audit/smoke_reacher/run_Reacher_none_b4000_seed44.csv`

Observed state:

- backend: `reacher_fallback`;
- device: CUDA was selected by SAC;
- evaluation: `0/1`, which is expected to be uninformative at five training
  steps;
- wall time: about `1.6` seconds.

Interpretation: the smoke confirms a training/evaluation/write path. It is not
a learning claim.

## Evidence And Reproducibility Status

Strong assets already in the project:

- `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` is the machine-readable claim
  index.
- `scripts/validate_evidence_registry.py` checks primary source existence and
  CSV readability.
- `scripts/audit_registry_numbers.py` checks registry numbers against primary
  CSV rows.
- `scripts/generate_claim_tables.py` regenerates manuscript-facing tables from
  the registry.
- R020-R024 define the current paper-core evidence chain.
- R036 removes manual table copying for the main cost-matched and repair
  comparisons.
- R042 audits current manuscript citation contexts.

Gaps to close for a submission-grade reproducibility package:

1. Repair or replace version provenance, because local `.git` metadata is
   present but not recognized as a valid repository.
2. Archive exact full rerun commands and stdout/stderr for every future
   paper-core run at creation time.
3. Add a compute-accounting table with hardware, wall time, seeds, steps,
   evaluation repeats, and checkpoint-selection policy.
4. Add a paper appendix inventory that maps each claim, table, figure, and
   command to its source artifact.
5. Resolve local LaTeX compilation before camera-ready iteration, or document a
   deterministic remote/container compile route.

## Innovation Assessment

The strongest near-term innovation is not a new trigger variant. It is the
evaluation protocol itself:

- cost-matched random-family baselines;
- repeated checkpoint evaluation;
- start-level intervention trace diagnostics;
- explicit stop/redesign rules when a trigger is dominated.

This is a better fit for the R043 T-ASE route than an unsupported algorithmic
superiority story. To strengthen novelty while staying truthful, the next paper
revision should make the protocol look like a reusable automation-science
methodology, not merely a report that LV-VoI failed.

## Recommended Gates

Recommended next sequence:

1. R045: align the manuscript to T-ASE with a Note to Practitioners,
   reproducibility appendix inventory, and clearer automation-system value.
2. R046: decide a small robotics-breadth package: cleaned Stack appendix,
   no-new-run boundary analysis, or a separately approved feasibility pilot.
3. R047: fix version provenance and compute-accounting artifacts.
4. Only after those gates, consider a later R0xx method experiment designed from
   R023/R024 trace diagnostics.
