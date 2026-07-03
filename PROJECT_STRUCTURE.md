# Project Structure

Last updated: 2026-07-03

This is the navigation map for the current diagnostic-protocol paper route. It
separates paper-facing artifacts from historical experiment outputs so the
project stays readable as results accumulate.

## Start Here

| Need | File |
|---|---|
| Single-page current project status | `PROJECT_DASHBOARD.md` |
| Current paper thesis and section plan | `PAPER_PLAN.md` |
| Project vocabulary and claim rules | `CONTEXT.md` |
| Evidence rows for paper claims | `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` |
| Evidence registry validation | `python scripts/validate_evidence_registry.py` |
| Evidence numeric audit | `python scripts/audit_registry_numbers.py` |
| Registry claim table generation | `python scripts/generate_claim_tables.py` |
| Citation audit ledgers | `results/r037_citation_audit_batch1/CITATION_METADATA_CONTEXT_AUDIT.md` and `paper/CITATION_AUDIT.md` |
| Target journal route | `results/r043_venue_targeting/VENUE_TARGET_MATRIX.md` |
| Environment and reproducibility audit | `results/r044_environment_reproducibility_audit/PROJECT_ENVIRONMENT_REPRODUCIBILITY_AUDIT.md` |
| Evidence provenance package | `results/r047_evidence_provenance_package/EVIDENCE_PROVENANCE_AUDIT.md` |
| Version and command provenance repair | `results/r048_version_command_provenance/VERSION_PROVENANCE_REPAIR.md` |
| Provenance validation gate | `results/r049_provenance_validation/PROVENANCE_VALIDATION_MODULE.md` |
| Theme deepening package | `results/r050_theme_deepening/THEME_DEEPENING.md` |
| Post-R050 citation audit | `results/r051_citation_context_audit/CITATION_CONTEXT_AUDIT.md` |
| Paper-claim audit | `paper/PAPER_CLAIM_AUDIT.md` and `results/r052_paper_claim_audit/PAPER_CLAIM_AUDIT.md` |
| Stack boundary appendix | `results/r053_stack_boundary_appendix/STACK_BOUNDARY_APPENDIX.md` |
| Attention-allocation diagnostic figure | `results/r054_attention_allocation_figure_optimization/MANIFEST.md` |
| Project quality pass | `results/r055_project_quality_pass/MANIFEST.md` |
| Current manuscript skeleton | `paper/main.tex` |
| Human-readable result map | `results/RESULTS_INDEX.md` |
| Figure and table asset map | `figures/FIGURE_ASSET_INDEX.md` |
| Future agent working rules | `AGENTS.md` |

## Directory Map

| Path | Role | Notes |
|---|---|---|
| `PROJECT_DASHBOARD.md` | Root project dashboard | First file to read for current status, evidence chain, commands, and next moves. |
| `AGENTS.md` | Future-agent rules | Guardrails for evidence, paper claims, citations, and verification. |
| `foresight_hil/` | Library modules | Core reusable code: environments, gating, allocation, HIL replay, oracle, metrics, training utilities. |
| `scripts/` | Experiment entry points | CLI scripts for toy runs, robosuite training, comparison driving, plotting, and checkpoint evaluation. |
| `tests/` | Regression tests | Covers bookkeeping, metrics, intervention logic, checkpoint summaries, and robosuite startup/task oracles. |
| `results/` | Raw and derived experiment artifacts | Large historical archive. Use `results/RESULTS_INDEX.md` plus the evidence registry before citing. |
| `figures/` | Paper figures and LaTeX tables | R026 and R029 paper assets. Use `figures/FIGURE_ASSET_INDEX.md`. |
| `paper/` | Current manuscript skeleton | R038 diagnostic-protocol draft using R029/R036 assets and R042-audited citations. |
| `proposal/` | Proposal and literature notes | Earlier method-positive proposal material; useful for background, not the current claim source. |
| `docs/decisions/` | Architecture and research-decision records | Records decisions that future work should not re-litigate casually. |

Process-style experiment notes and local planning logs are intentionally kept
out of the public GitHub repository. Use the evidence registry, result index,
manifests, and audit packages for public-facing provenance.

## Paper-Facing Evidence Flow

1. Raw run CSVs and checkpoint summaries live under `results/r0xx_*`.
2. Paper-claim rows are curated in `results/EXPERIMENT_EVIDENCE_REGISTRY.csv`.
3. R047 records source hashes, environment state, partial compute accounting,
   command inventory, and known provenance gaps.
4. R048 provides the historical source snapshot and R020/R021 command-provenance
   boundary note for the earlier invalid-Git workspace state.
5. R049 validates provenance package self-consistency and optional current-file
   drift through `python scripts/validate_provenance_package.py`.
6. R050 records the current theme deepening from trigger diagnostics to
   human-attention allocation diagnostics.
7. R051 records the citation-context audit after the R050 theme update.
8. R052 records the current manuscript paper-claim audit after R050/R051.
9. R053 records the cleaned Stack boundary-evidence appendix package.
10. R054 records the optimized attention-allocation diagnostic figure package.
11. R055 records the project-quality pass and tested attention-diagnostic helper
    extraction.
12. Manuscript logic is maintained in `PAPER_PLAN.md`.
13. Derived figure/table assets are generated into `figures/`.
14. Figure/table provenance is tracked in `figures/FIGURE_ASSET_INDEX.md`.

The registry is the narrow interface for paper claims. Raw directories remain
the implementation detail behind that interface.

## Current Paper-Core Runs

| Run | Role |
|---|---|
| R018 | Registered Stack boundary evidence: no-online matched BC dominates online Stack intervention variants. |
| R020 | Five-seed Lift reliability check before cost matching. |
| R021 | Cost-matched random-family check that rejects current trigger superiority. |
| R022 | Minimum-disagreement trigger repair, negative. |
| R023 | Start-level trace diagnosis for random_b350 vs LV-VoI scale3. |
| R024 | Score-floor trigger repair and trace follow-up, negative. |
| R025 | Paper pivot package. |
| R026 | First paper figure/table build. |
| R027 | Citation/source bank preparation. |
| R028 | Diagnostic-protocol framework refinement. |
| R029 | Protocol-centered hero figure and checklist. |
| R030 | Project structure audit, index cleanup, and first bookkeeping-module extraction. |
| R031 | Trace schema module extraction. |
| R032 | Strategy specification module extraction and all-code framework review. |
| R033 | Evaluation protocol module extraction. |
| R034 | Evidence registry source validation and R023 registry correction. |
| R035 | Evidence registry numeric audit against primary CSV rows. |
| R036 | Registry-driven claim table generation for manuscript assets. |
| R037 | Citation candidate metadata/context audit batch 1. |
| R038 | Current-route manuscript skeleton. |
| R039 | Project dashboard, future-agent rules, and organization pass. |
| R040 | First manuscript prose-polish pass for abstract, introduction, protocol/setup, and conclusion. |
| R041 | Results and Discussion prose-polish pass. |
| R042 | Final citation-context audit for current manuscript citations. |
| R043 | Venue targeting and target-driven revision plan. |
| R044 | Local environment, reproducibility, innovation, and rigor audit. |
| R045 | T-ASE manuscript alignment and reproducibility appendix inventory. |
| R047 | Evidence provenance package: source inventory, hashes, compute accounting, command inventory, and gap analysis. |
| R048 | Version and command provenance repair: deterministic source snapshot, Git diagnostic, and R020/R021 command boundary note. |
| R049 | Provenance validation gate: tested validator and CLI for package self-consistency and optional drift diagnosis. |
| R050 | Theme deepening: reframes the paper spine around human-attention allocation diagnostics without changing evidence boundaries. |
| R051 | Post-R050 citation audit: verifies that all current citation contexts remain supported after the theme update. |
| R052 | Paper-claim audit: verifies current manuscript numerical, comparison, and scope claims after R050/R051 and repairs stale provenance wording. |
| R053 | Stack boundary appendix: packages registered Stack boundary evidence as an appendix-ready table without positive-transfer overclaiming. |
| R054 | Attention-allocation figure optimization: packages a scipilot-guided diagnostic composite, trace profile, and visual QA from R021/R023/R024. |
| R055 | Project quality pass: synchronizes documentation/code consistency after R054, extracts tested attention-diagnostic profiling helpers, and integrates the R054 figure into Results. |

## Module Deepening Candidates

These are the current code-structure targets after R030.

| Candidate module | Current friction | Proposed seam | Priority |
|---|---|---|---|
| Experiment bookkeeping | R030 extracted labels, summaries, best checkpoints, final-report choice, and cost metadata. | `foresight_hil/experiments/bookkeeping.py` with tests through one small interface. | Done first pass |
| Trace schema | R031 extracted trace columns and privileged-state row construction. | `foresight_hil/experiments/trace.py` returning stable rows from controller + privileged state. | Done first pass |
| Strategy specification | R032 extracted comparison strategy order, pace flags, run identity, and training CLI construction. | `foresight_hil/experiments/strategy_specs.py` consumed by the comparison driver. | Done first pass |
| Evaluation protocol | R033 extracted repeated checkpoint summary aggregation and summary-row formatting. | `foresight_hil/evaluation/protocol.py` for repeated-eval summaries and claim-table inputs. | Done first pass |
| Registry/source validation | R034 added source existence and CSV parse validation for registry rows. | `foresight_hil/evaluation/registry_validation.py` plus `scripts/validate_evidence_registry.py`. | Done first pass |
| Paper-claim numeric audit | R035 cross-checks registry numeric fields against source CSV rows. | `foresight_hil/evaluation/registry_numeric_audit.py` plus `scripts/audit_registry_numbers.py`. | Done first pass |
| Claim table generation | R036 emits Markdown and LaTeX claim tables from audited registry rows. | `foresight_hil/evaluation/claim_tables.py` plus `scripts/generate_claim_tables.py`. | Done first pass |
| Citation support audit | R037 audited first-batch candidate metadata and context-use boundaries. | `results/r037_citation_audit_batch1/` plus the R027 source bank. | Done first pass |
| Manuscript skeleton | R038 created the first claim-tethered LaTeX skeleton. | `paper/main.tex` and `paper/sections/*.tex`. | Done first pass |
| Project dashboard and agent rules | R039 added a root-level dashboard and future-agent guardrails. | `PROJECT_DASHBOARD.md`, `AGENTS.md`, and `results/r039_project_organization/`. | Done first pass |
| Manuscript prose polish | R040 strengthened the abstract, introduction, protocol/setup, and conclusion without changing evidence boundaries. | `paper/main.tex`, `paper/sections/01_introduction.tex`, `paper/sections/03_protocol_setup.tex`, `paper/sections/06_conclusion.tex`. | Done first pass |
| Results/Discussion prose polish | R041 strengthened the Results and Discussion evidence chain without changing evidence boundaries. | `paper/sections/04_results.tex`, `paper/sections/05_discussion.tex`. | Done first pass |
| Citation-context audit | R042 audited all current manuscript `\cite{...}` contexts and fixed six metadata entries. | `paper/CITATION_AUDIT.md`, `paper/CITATION_AUDIT.json`, and `results/r042_citation_context_audit/`. | Done first pass |
| Venue targeting | R043 selects IEEE T-ASE as the primary target route and records stretch/fallback venues. | `results/r043_venue_targeting/VENUE_TARGET_MATRIX.md`. | Done first pass |
| Reproducibility package | R044 audits local runtime, smoke paths, reproduction entry points, innovation gaps, and version-provenance risks. | `results/r044_environment_reproducibility_audit/`. | Done first pass |
| T-ASE manuscript alignment | R045 adds a Note to Practitioners and reproducibility appendix inventory without changing the evidence boundary. | `paper/main.tex`, `paper/sections/07_reproducibility_inventory.tex`, and `results/r045_tase_reproducibility_alignment/`. | Done first pass |
| Evidence provenance package | R047 records registry-source hashes, selected artifact hashes, partial compute accounting, command inventory, and explicit gaps. | `results/r047_evidence_provenance_package/`. | Done first pass |
| Version and command provenance | R048 replaces invalid local Git provenance with a source snapshot and clarifies R020/R021 command reconstruction boundaries. | `results/r048_version_command_provenance/`. | Done first pass |
| Provenance validation | R049 adds a tested validator for R047/R048 self-consistency and current-file drift diagnosis. | `foresight_hil/evaluation/provenance_validation.py`, `scripts/validate_provenance_package.py`, and `results/r049_provenance_validation/`. | Done first pass |
| Theme deepening | R050 deepens the manuscript and public project framing around human-attention allocation without adding evidence or citations. | `results/r050_theme_deepening/`, `PAPER_PLAN.md`, `paper/`, `README.md`, and project indexes. | Done first pass |
| Post-R050 citation audit | R051 audits current citation contexts after the human-attention theme update. | `paper/CITATION_AUDIT.md`, `paper/CITATION_AUDIT.json`, and `results/r051_citation_context_audit/`. | Done first pass |
| Paper-claim audit | R052 audits current manuscript numerical, comparison, and scope claims after the R050/R051 updates. | `paper/PAPER_CLAIM_AUDIT.md`, `paper/PAPER_CLAIM_AUDIT.json`, and `results/r052_paper_claim_audit/`. | Done first pass |
| Stack boundary appendix | R053 registers Stack boundary rows and generates an appendix-ready table from the registry. | `scripts/generate_stack_boundary_appendix.py`, `figures/TABLE_stack_boundary_appendix_r053.tex`, and `results/r053_stack_boundary_appendix/`. | Done first pass |
| Attention-allocation diagnostic figure | R054 replaces compressed/dual-axis-style diagnostics with a multi-panel figure and visual QA record. | `figures/gen_r054_attention_allocation_diagnostics.py`, `figures/fig_attention_allocation_diagnostics_r054.pdf`, and `results/r054_attention_allocation_figure_optimization/`. | Done first pass |
| Attention-diagnostic helper extraction | R055 moves R054 trace-profile collection and summarization out of the plotting script. | `foresight_hil/evaluation/attention_diagnostics.py`, `tests/test_attention_diagnostics.py`, and `results/r055_project_quality_pass/`. | Done first pass |

## Editing Rules

- Add new experiment results under a new `results/r0xx_*` directory.
- Add one manifest for every paper-facing derived artifact package.
- Add or update registry rows before using a number in the manuscript.
- Keep smoke outputs out of paper claims.
- Keep `PROJECT_DASHBOARD.md` and `AGENTS.md` synchronized when the paper route
  or canonical verification commands change.
- Do not refactor training logic in the same step as a scientific experiment
  unless the regression tests are expanded first.
