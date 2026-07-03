# Results Index

Last updated: 2026-07-03

This file is a human-readable map of `results/`. The machine-readable claim
source is `results/EXPERIMENT_EVIDENCE_REGISTRY.csv`.

## Rules

- Raw run directories are evidence archives. Do not edit historical run CSVs.
- Paper claims should cite a registry row plus its primary source.
- Smoke runs prove code paths only.
- Superseded runs remain useful for debugging history but should not support
  current manuscript claims.

## Paper-Core Evidence

| Run | Directory / source | Status | Use |
|---|---|---|---|
| R018 | `results/r018_stack_multiseed_alignment/` | Registered boundary evidence | Stack multiseed boundary comparison; no-online matched BC dominates online intervention variants. |
| R020 | `results/r020_lift_highn_reliability/` | Paper-core, superseded in interpretation by R021 | Shows the initially plausible LV-VoI result before stricter cost matching. |
| R021 | `results/r021_random_costmatch/` | Paper-core | Main cost-matched reversal: `random_b350` dominates LV-VoI scale3. |
| R022 | `results/r022_lift_min_disagree_seed0_2/` | Paper-core | Negative repair result for minimum-disagreement LV-VoI. |
| R023 | `results/r023_real_trace_seed0_2/` | Paper-core | Start-level trace diagnosis for random_b350 vs LV-VoI scale3. |
| R024 | `results/r024_score_floor_seed0_2/` | Paper-core | Negative score-floor repair result and follow-up trace tables. |
| R025 | `results/r025_paper_pivot/` | Paper-core | Claim matrix, negative findings table, and protocol recommendation. |
| R027 | `results/r027_citation_source_bank/` | In progress | Citation support bank and staged candidate bibliography. |
| R028 | `results/r028_framework_refinement/` | Paper-core | Final paper identity: diagnostic protocol + robotic case study. |
| R029 | `results/r029_protocol_hero/` | Paper-core | Protocol checklist and hero-figure rationale. |
| R030 | `results/r030_structure_audit/` | Project-structure support | Structure audit, indexes, and next module-deepening targets. |
| R031 | `results/r031_trace_schema_module/` | Project-structure support | Trace schema module extraction and compatibility tests. |
| R032 | `results/r032_strategy_spec_module/` | Project-structure support | Strategy specification extraction and all-code framework review. |
| R033 | `results/r033_evaluation_protocol_module/` | Project-structure support | Repeated-evaluation protocol module extraction. |
| R034 | `results/r034_registry_validation/` | Project-structure support | Evidence registry source validation and R023 registry correction. |
| R035 | `results/r035_registry_numeric_audit/` | Project-structure support | Evidence registry numeric audit against primary CSV rows. |
| R036 | `results/r036_claim_tables/` | Paper artifact support | Registry-driven Markdown and LaTeX claim tables. |
| R037 | `results/r037_citation_audit_batch1/` | Citation support | First metadata/context-use audit for staged candidate citations. |
| R038 | `results/r038_manuscript_skeleton/` and `paper/` | Manuscript support | First current-route LaTeX manuscript skeleton. |
| R039 | `results/r039_project_organization/` plus root dashboard files | Project-structure support | Root dashboard, future-agent rules, and synchronized organization indexes. |
| R040 | `results/r040_manuscript_polish/` and `paper/` | Manuscript support | First prose-polish pass for abstract, introduction, protocol/setup, and conclusion. |
| R041 | `results/r041_results_discussion_polish/` and `paper/` | Manuscript support | Results and Discussion prose-polish pass. |
| R042 | `results/r042_citation_context_audit/` and `paper/CITATION_AUDIT.md` | Citation support | Final citation-context audit for the current manuscript citation keys. |
| R043 | `results/r043_venue_targeting/` | Paper-planning support | Target journal matrix and T-ASE primary route decision. |
| R044 | `results/r044_environment_reproducibility_audit/` | Project-audit support | Local environment, reproducibility, innovation, and rigor audit. |
| R045 | `results/r045_tase_reproducibility_alignment/` and `paper/` | Manuscript support | T-ASE-style Note to Practitioners and reproducibility appendix inventory. |
| R047 | `results/r047_evidence_provenance_package/` | Evidence-provenance support | Registry source inventory, artifact hashes, available compute accounting, command provenance inventory, and gap analysis. |
| R048 | `results/r048_version_command_provenance/` | Version and command provenance support | Deterministic source snapshot, Git failure diagnostic, R020/R021 checkpoint inventories, and reconstructed command templates. |
| R049 | `results/r049_provenance_validation/` | Provenance-validation support | Tested validator and CLI for R047/R048 package self-consistency plus optional current-file drift diagnosis. |
| R050 | `results/r050_theme_deepening/` | Manuscript/theme support | Deepens the paper spine around human-attention allocation diagnostics without adding experiments, citations, or positive LV-VoI claims. |
| R051 | `results/r051_citation_context_audit/` | Citation support | Audits all 15 current citation contexts after the R050 theme update and finds no wrong-context citations. |
| R052 | `results/r052_paper_claim_audit/` | Paper-claim audit support | Audits current manuscript numerical, comparison, and scope claims after R050/R051 and repairs stale provenance wording. |
| R053 | `results/r053_stack_boundary_appendix/` | Paper artifact support | Packages registered Stack boundary evidence into an appendix-ready table without changing the negative transfer interpretation. |
| R054 | `results/r054_attention_allocation_figure_optimization/` | Paper artifact support | Adds a scipilot-guided multi-panel attention-allocation diagnostic figure, trace profile, and visual QA from R021/R023/R024. |
| R055 | `results/r055_project_quality_pass/` | Project-quality support | Reviews documentation/code consistency after R054, extracts tested attention-diagnostic profiling helpers, and integrates the R054 figure into the manuscript. |
| R056 | `results/r056_methodology_extension/` | Paper artifact support | Derives a protocol gate matrix, failure taxonomy, stop-rule metrics, and methodology-first Fig. 1 candidate from registered R021/R023/R024 evidence. |
| R057 | `results/r057_document_code_quality_pass/` | Project-quality support | Adds repeatable Markdown local-link validation and repairs row-aligned attention-profile gap handling without changing experimental claims. |
| R058 | `results/r058_submission_packaging_readiness/` | Submission-packaging support | Records Tectonic cache repair, current PDF compilation, visual QA, public Git source-state tracking, and final source-archive decision. |
| R059 | `results/r059_evidence_experiment_optimization/` | Experiment-planning support | Defines an evidence-first optimization route with trace/offline gates and cost-matched stop rules for any future experiment. |
| R060 | `results/r060_offline_trace_trigger_audit/` | Trace/offline diagnostic support | Audits R023/R024 accepted-start traces with phase summaries and post-hoc gates; useful as a design screen, not online method evidence. |

## Baseline And Historical Runs

Earlier `r004`-`r019` directories document how the project reached the current
route. They are important for understanding rejected claims and task-transfer
limits, but they should be cited only when the manuscript explicitly discusses
development history or limitations.

Examples:

- `results/r018_stack_multiseed_alignment/`: registered Stack boundary
  evidence; current Stack online-intervention claim is negative.
- `results/r019_stack_mechanism_redesign/`: rejected Stack mechanism variants.
- `results/r011_*` and `results/r012_*`: earlier Lift LV-VoI candidate
  development, superseded by R020-R021.

## Smoke And Plumbing Runs

Directories with names such as `*_smoke`, `local_*`, `diag*`, or `debug_*` are
execution checks and debugging artifacts. They should not be used as paper
evidence unless promoted through a new registry row with a clear primary source.

## Voided Or Misrouted Artifacts

| Directory | Status | Reason |
|---|---|---|
| `results/r046_robocasa_dynamics_pilot_triage/` | VOID, excluded from registry and public repository tracking | Created from a user message later corrected as belonging to another project. Do not use for this paper. |

## Current Registry Rows

The registry currently covers R018 and R020-R060, excluding voided R046. Add new rows when:

- a result supports or rejects a paper claim;
- a derived paper artifact is created;
- a structure/citation/framework decision changes what future work should use.
