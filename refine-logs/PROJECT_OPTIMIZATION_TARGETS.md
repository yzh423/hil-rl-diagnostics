# Project Optimization Targets

Date: 2026-07-01

Scope: full-project audit of FORESIGHT-HIL after R026, focused on SCI Q1
readiness, reproducibility, code maintainability, and method-redesign options.

## Executive Diagnosis

The strongest near-term optimization target is not another heuristic trigger.
The project now has enough negative evidence to support a cost-matched HIL-RL
diagnostic-benchmark paper, but its artifacts still carry two competing stories:

- the original positive-method framing in `README.md` and the proposal material;
- the current R021-R026 evidence that the LV-VoI trigger is dominated by
  cost-matched random baselines and should be framed as a diagnostic result.

The second strongest target is engineering reproducibility. The main training
entry point, `scripts/train_robosuite_hil.py`, is about 60 KB and mixes CLI
configuration, run identity, checkpoint bookkeeping, robosuite setup, trace
logging, SAC training, evaluation, and summary writing. This makes future
experiments slower to verify and raises the risk of configuration drift.

## Priority Targets

| Rank | Target | Priority | Why It Matters | First Action |
|---|---|---:|---|---|
| 1 | Paper-story alignment | MUST | The README still reads like a positive VoI-method paper, while `PAPER_PLAN.md` has correctly pivoted to diagnostic/negative findings. Reviewers will punish inconsistent framing. | Rewrite README top sections and proposal-facing summary around cost-matched evaluation, repeated checkpoint evaluation, and trace diagnostics. |
| 2 | Citation and source audit | MUST | `PAPER_PLAN.md` still marks Related Work and method claims as `[VERIFY]`. SCI Q1 submission needs verified, authoritative references before drafting. | Execute R027: build a citation support bank from `proposal/references.bib`, verify BibTeX, and map each intro/related-work claim to sources. |
| 3 | Experiment evidence registry | MUST | R020-R026 facts are duplicated across README, tracker, plan, figures, CSVs, and manual notes. This invites claim drift. | Create one machine-readable evidence index for R020-R026, then generate tables/figure inputs and claim matrices from it. |
| 4 | Training script modularization | MUST | `scripts/train_robosuite_hil.py` is the central shallow module. Any config/schema/trace change touches the same large script. | Extract run config, bookkeeping, trace schema, and evaluation helpers into `foresight_hil/experiments/` with tests. |
| 5 | Strategy/config identity cleanup | SHOULD | `scripts/run_comparison.py` and the training script both build labels and pass many VoI flags. Earlier budget matching problems show this is a scientific risk, not just style. | Introduce declarative strategy specs that support per-strategy budgets and canonical run IDs. |
| 6 | Result artifact hygiene | SHOULD | `results/` contains many historical runs, 457 CSV files, and 75 checkpoint zip files. Without manifests, it is hard to tell paper evidence from scratch artifacts. | Add `results/RESULTS_INDEX.csv` or YAML plus archival tags: paper-core, diagnostic, smoke, superseded. |
| 7 | Evaluation protocol module | SHOULD | Repeated checkpoint evaluation, Wilson intervals, best-checkpoint reporting, and trace diagnostics are core contributions but currently spread across scripts. | Move evaluation summarization and CI utilities into a reusable module and make R020-R026 tables consume it. |
| 8 | Figure 1 polish | SHOULD | R026 data plots are usable, but the hero diagnostic summary is still marked draft. A SCI Q1 paper benefits from a crisp first visual. | Redesign Fig. 1 as a final narrative figure: protocol, cost-matched reversal, and trigger diagnosis. |
| 9 | Parallel-budget allocation module | LATER | `foresight_hil/allocation/budget.py` still has the original submodular/diversity TODO. This could support a future positive contribution, but it is not needed for the current diagnostic paper. | Defer until after R027/manuscript skeleton, unless the paper needs a new method contribution. |
| 10 | Second-task/robotics breadth | LATER | Stack currently gives boundary/negative evidence, not positive transfer. Starting RoboCasa or new tasks now may dilute the story. | Keep Stack as limitation/boundary evidence; only expand tasks after the paper skeleton exposes a real need. |

## Recommended Next Sequence

1. Run R027 citation audit and source bank.
2. Align README and paper-facing project summary with the diagnostic-benchmark
   thesis.
3. Build the evidence registry for R020-R026 and regenerate current tables from
   that registry.
4. Extract experiment bookkeeping/config modules from the training script.
5. Draft Introduction and Evaluation Protocol sections using only verified
   citations and registry-backed numbers.

## Stop Rule

Do not start a new R024-style trigger repair unless it is motivated by a clear
diagnostic failure mode and evaluated first against same-seed `random_b350` with
repeated checkpoint evaluation. The current best route is paper credibility and
evidence discipline, not more small heuristic variants.
