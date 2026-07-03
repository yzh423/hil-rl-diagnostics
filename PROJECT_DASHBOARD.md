# FORESIGHT-HIL Project Dashboard

Last updated: 2026-07-03

This is the one-page entry point for the current project state. Use it before
running new experiments, editing paper claims, or revising the manuscript.

## Current Route

FORESIGHT-HIL is currently a cost-matched HIL-RL diagnostic protocol paper about
human-attention allocation in robotic manipulation. The current LV-VoI trigger
is not claimed as superior.

The defensible contribution is:

- cost-matched random-family evaluation for human-attention allocation claims;
- repeated checkpoint evaluation rather than single-checkpoint reporting;
- start-level intervention trace diagnostics;
- negative trigger-repair findings that motivate protocol discipline before
  new method design.

The strongest current evidence is R020-R024. R021 is the decisive cost-matched
reversal: `random_b350` outperforms LV-VoI scale3 while using less human-step
cost.

## Read First

| Need | File |
|---|---|
| Project vocabulary and claim boundaries | `CONTEXT.md` |
| Directory and artifact map | `PROJECT_STRUCTURE.md` |
| Current paper route and section plan | `PAPER_PLAN.md` |
| Result archive map | `results/RESULTS_INDEX.md` |
| Machine-readable evidence registry | `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` |
| Human-readable evidence rules | `results/EXPERIMENT_EVIDENCE_REGISTRY.md` |
| Figure and table assets | `figures/FIGURE_ASSET_INDEX.md` |
| Current manuscript skeleton | `paper/main.tex` |
| Current citation-context audit | `paper/CITATION_AUDIT.md` |
| Target journal matrix | `results/r043_venue_targeting/VENUE_TARGET_MATRIX.md` |
| Environment and reproducibility audit | `results/r044_environment_reproducibility_audit/PROJECT_ENVIRONMENT_REPRODUCIBILITY_AUDIT.md` |
| T-ASE manuscript alignment | `results/r045_tase_reproducibility_alignment/MANUSCRIPT_ALIGNMENT.md` |
| Evidence provenance package | `results/r047_evidence_provenance_package/EVIDENCE_PROVENANCE_AUDIT.md` |
| Version and command provenance repair | `results/r048_version_command_provenance/VERSION_PROVENANCE_REPAIR.md` |
| Provenance validation gate | `results/r049_provenance_validation/PROVENANCE_VALIDATION_MODULE.md` |
| Theme deepening package | `results/r050_theme_deepening/THEME_DEEPENING.md` |
| Post-R050 citation audit | `results/r051_citation_context_audit/CITATION_CONTEXT_AUDIT.md` |
| Paper-claim audit | `paper/PAPER_CLAIM_AUDIT.md` and `results/r052_paper_claim_audit/PAPER_CLAIM_AUDIT.md` |
| Stack boundary appendix | `results/r053_stack_boundary_appendix/STACK_BOUNDARY_APPENDIX.md` |
| Attention-allocation diagnostic figure | `results/r054_attention_allocation_figure_optimization/MANIFEST.md` |
| Project quality pass | `results/r055_project_quality_pass/MANIFEST.md` |
| Methodology extension | `results/r056_methodology_extension/MANIFEST.md` |
| Document/code quality follow-up | `results/r057_document_code_quality_pass/MANIFEST.md` |
| Submission packaging readiness | `results/r058_submission_packaging_readiness/MANIFEST.md` |
| Evidence/experiment optimization plan | `results/r059_evidence_experiment_optimization/MANIFEST.md` |
| Offline trace trigger audit | `results/r060_offline_trace_trigger_audit/MANIFEST.md` |
| Candidate-state logging interface | `results/r061_candidate_state_logging/MANIFEST.md` |
| Repair pre-registration and smoke plan | `results/r062_repair_preregistration/MANIFEST.md` |
| Future agent rules | `AGENTS.md` |

## Evidence Chain

| Layer | Canonical artifact | Rule |
|---|---|---|
| Raw evidence | `results/r0xx_*` | Do not edit historical CSVs or checkpoint summaries. |
| Claim index | `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` | Every paper number must trace to a registry row. |
| Numeric audit | `python scripts/audit_registry_numbers.py` | Run before copying numbers into prose, tables, or captions. |
| Source audit | `python scripts/validate_evidence_registry.py` | Run after changing registry rows or cited sources. |
| Paper-claim audit | `paper/PAPER_CLAIM_AUDIT.md` | Check manuscript numerical, comparison, and scope claims against registry-backed evidence. |
| Stack appendix table | `python scripts/generate_stack_boundary_appendix.py` | Regenerate the R053 Stack boundary appendix table from registry rows. |
| Provenance package | `results/r047_evidence_provenance_package/` | Use for source hashes, partial compute accounting, command inventory, and known provenance gaps. |
| Source snapshot | `results/r048_version_command_provenance/` | Use as the historical repair record for the earlier invalid-Git source snapshot and R020/R021 command provenance boundaries. |
| Provenance validation | `python scripts/validate_provenance_package.py` | Run after evidence/provenance package changes; use `--compare-current-files` only for drift diagnosis. |
| Document link validation | `python scripts\validate_document_links.py` | Run after documentation or project-index changes. |
| Display assets | `figures/` | Prefer R056/R054/R036 assets for the current route. |
| Project-quality pass | `results/r055_project_quality_pass/` | Records documentation/code consistency checks and tested attention-diagnostic helper extraction. |
| Submission packaging | `results/r058_submission_packaging_readiness/` | Records the current PDF compile path, visual QA, public Git source-state tracking, and final source-archive decision. |
| Experiment optimization | `results/r059_evidence_experiment_optimization/` | Use trace/offline diagnostic gates and cost matching before any future method claim. |
| Offline trace audit | `results/r060_offline_trace_trigger_audit/` | Treat accepted-start gate filtering as a design screen, not online trigger evidence. |
| Candidate-state logging | `results/r061_candidate_state_logging/` | Use before any future online trigger repair; archive accepted and rejected gate-evaluation states. |
| Repair pre-registration | `results/r062_repair_preregistration/` | Use before launching formal R063+ repair compute; R062 is a planning/smoke gate, not performance evidence. |
| Manuscript | `paper/` | Keep current-route writing separate from historical `proposal/`. |

## Canonical Commands

Run these after changing project structure, evidence rows, paper assets, or
evaluation code:

```powershell
python scripts\validate_evidence_registry.py
python scripts\audit_registry_numbers.py
python scripts\generate_claim_tables.py
python scripts\generate_methodology_extension.py
python scripts\generate_offline_trace_audit.py
python scripts\generate_stack_boundary_appendix.py
python scripts\validate_provenance_package.py
python scripts\validate_document_links.py
python -m unittest discover -s tests
```

Use this citation check when `paper/references.bib` changes:

```powershell
python C:\Users\14228\.codex\skills\citation-management\scripts\validate_citations.py paper\references.bib --report results\r042_citation_context_audit\paper_references_validation_after_r042.json --verbose
```

## Paper Assets

| Asset | Preferred source |
|---|---|
| Fig. 1 methodology protocol | `figures/fig1_methodology_protocol_r056.pdf` |
| Fig. 1 methodology preview | `figures/fig1_methodology_protocol_r056.png` and `figures/fig1_methodology_protocol_r056_grayscale.png` |
| Attention-allocation diagnostic composite | `figures/fig_attention_allocation_diagnostics_r054.pdf` and `results/r054_attention_allocation_figure_optimization/` |
| Main cost-matched table | `figures/TABLE_registry_costmatched_results_r036.tex` |
| Trigger-repair table | `figures/TABLE_registry_trigger_repairs_r036.tex` |
| Protocol checklist | `figures/TABLE_protocol_checklist.tex` |
| Manuscript entry point | `paper/main.tex` |
| Skeleton manifest | `results/r038_manuscript_skeleton/MANIFEST.md` |
| First prose-polish manifest | `results/r040_manuscript_polish/MANIFEST.md` |
| Results/Discussion polish manifest | `results/r041_results_discussion_polish/MANIFEST.md` |
| Citation-context audit | `paper/CITATION_AUDIT.md` and `results/r042_citation_context_audit/` |
| Venue targeting matrix | `results/r043_venue_targeting/VENUE_TARGET_MATRIX.md` |
| Reproducibility audit | `results/r044_environment_reproducibility_audit/` |
| Practitioner and reproducibility appendix pass | `results/r045_tase_reproducibility_alignment/` |
| Evidence provenance package | `results/r047_evidence_provenance_package/` |
| Version and command provenance repair | `results/r048_version_command_provenance/` |
| Provenance validation gate | `results/r049_provenance_validation/` |
| Theme deepening package | `results/r050_theme_deepening/` |
| Post-R050 citation audit | `results/r051_citation_context_audit/` |
| Paper-claim audit | `paper/PAPER_CLAIM_AUDIT.md`, `paper/PAPER_CLAIM_AUDIT.json`, and `results/r052_paper_claim_audit/` |
| Stack boundary appendix | `figures/TABLE_stack_boundary_appendix_r053.tex` and `results/r053_stack_boundary_appendix/` |
| Figure optimization package | `figures/fig_attention_allocation_diagnostics_r054.pdf`, `figures/fig_attention_allocation_diagnostics_r054_grayscale.png`, and `results/r054_attention_allocation_figure_optimization/` |
| Project quality pass | `results/r055_project_quality_pass/` and `foresight_hil/evaluation/attention_diagnostics.py` |
| Methodology extension | `figures/fig1_methodology_protocol_r056.pdf`, `figures/TABLE_protocol_gate_matrix_r056.tex`, `figures/TABLE_failure_taxonomy_r056.tex`, and `results/r056_methodology_extension/` |
| Document/code quality follow-up | `results/r057_document_code_quality_pass/` and `foresight_hil/evaluation/document_links.py` |
| Submission packaging readiness | `results/r058_submission_packaging_readiness/` |
| Evidence/experiment optimization plan | `results/r059_evidence_experiment_optimization/` |
| Offline trace trigger audit | `results/r060_offline_trace_trigger_audit/` |
| Candidate-state logging interface | `results/r061_candidate_state_logging/` |
| Repair pre-registration and smoke plan | `results/r062_repair_preregistration/` |

Current compile caveat: R058 resolves the local PDF compile gate for the
current draft by using bundled Tectonic 0.16.9 with a project-local
`TECTONIC_CACHE_DIR` and compile-local `paper/figures/` snapshots. TeX
Live/MiKTeX tools are still not on `PATH`, and the Tectonic cache is local and
ignored by Git, so final venue-template integration should rerun compile and
visual QA.

Current citation caveat: R051 audited all 15 citation keys after the R050
human-attention theme update and found no wrong-context citations. It did not
expand the literature review or choose the final journal reference style.

Current venue caveat: R043 selects IEEE T-ASE as the primary target route based
on official scope and metric pages. Final SCI Q1 / CAS partition status still
needs an institutional JCR/CAS check before submission.

Current reproducibility caveat: R048 records the pre-publication state where a
valid Git commit was unavailable and replaces it with a deterministic source
snapshot. The project now also has a valid public GitHub repository for the
current source state, while R047/R048 remain the provenance records for
historical evidence and source-snapshot boundaries. R020/R021 original central
launch commands are still not archival logs, and only three scanned paper-core
CSVs expose explicit `wall_time_s`. R049 adds a default provenance validation
command; its drift mode reports expected differences between historical R047/R048
ledgers and the current working tree.

Current manuscript caveat: R050 deepens the manuscript theme from trigger
diagnostics to human-attention allocation diagnostics. It does not add new
citations, experiments, or a positive LV-VoI method claim. R052 audits the
current manuscript claims and repairs stale provenance wording; R055 adds the
R054 diagnostic composite to Results and records the no-new-claim boundary.
R056 strengthens the methodology presentation with a derived gate matrix,
failure taxonomy, stop-rule metrics, and Fig. 1 candidate from registered
R021/R023/R024 evidence. It does not add a new experiment or positive trigger
claim. R057 adds repeatable Markdown local-link validation and repairs
row-aligned attention-profile gap handling without changing experimental
claims. R058 records the current submission-packaging compile/visual-QA pass
and source-archive decision. R059 records the evidence-first experiment optimization route:
resolve packaging gates, harden existing audits, run cheap R023/R024
trace/offline diagnostics before any new training, and require cost-matched
stop gates before future positive method claims.
Rerun or update the claim audit after numeric, comparison, or scope claims
change.

Current trace/offline caveat: R060 shows that post-hoc filtering of accepted
LV-VoI starts can look much more selective than the actual R024 score-floor
follow-up. Use it to reject weak repair ideas or design logging requirements,
not to claim online performance.

Current experiment-instrumentation caveat: R061 adds `--trace_candidates` for
VoI gate-evaluated states, including accepted and rejected decisions. R062
pre-registers the candidate-logging smoke and formal-run gate. Future R063+
online repairs still need fresh result directories, repeated evaluation, and
cost-matched random comparison before any method claim changes.

## Code Map

| Area | Current role |
|---|---|
| `foresight_hil/experiments/bookkeeping.py` | Run labels, summaries, best checkpoints, and cost metadata. |
| `foresight_hil/experiments/trace.py` | Stable intervention-start and candidate-state trace schemas and row construction. |
| `foresight_hil/experiments/strategy_specs.py` | Comparison strategy identity and CLI construction. |
| `foresight_hil/evaluation/protocol.py` | Repeated checkpoint summary aggregation. |
| `foresight_hil/evaluation/attention_diagnostics.py` | Trace-row collection and profile generation for attention-allocation diagnostic figures. |
| `foresight_hil/evaluation/protocol_diagnostics.py` | Derived protocol gate matrix, failure taxonomy, and stop-rule metric generation for R056. |
| `foresight_hil/evaluation/offline_trace_audit.py` | Phase summaries and post-hoc gate audits for R060 offline trace diagnostics. |
| `foresight_hil/evaluation/document_links.py` | Local Markdown link validation for project-control documentation. |
| `foresight_hil/evaluation/registry_validation.py` | Registry source existence and CSV readability checks. |
| `foresight_hil/evaluation/registry_numeric_audit.py` | Registry numeric checks against primary CSV rows. |
| `foresight_hil/evaluation/claim_tables.py` | Registry-driven Markdown and LaTeX claim tables. |
| `scripts/train_robosuite_hil.py` | Still the largest mixed training/evaluation script. Refactor only with tests. |

## Do Not Claim

- Do not claim LV-VoI superiority for the current Lift setup.
- Do not claim real-human or real-robot validation.
- Do not use smoke runs as paper evidence.
- Do not treat R023 traces as the main success-rate evidence.
- Do not add references from memory. Use audited citation artifacts first.

## Best Next Moves

1. Rerun PDF compile and visual QA after venue-template integration or major
   layout changes.
2. Keep the public GitHub package clean: source, registry-backed evidence,
   figures, tables, and audits should stay tracked, while local process notes,
   checkpoints, caches, and third-party PDFs should stay untracked.
3. Create a frozen institutional/source archive only from the final verified
   submission tag.
4. Use R062 before spending compute on new formal repairs: the candidate-logging
   smoke must pass before any R063+ online repair, and that repair still needs
   repeated evaluation plus a cost-matched random comparison before it can
   affect claims.
5. Keep `paper/CITATION_AUDIT.md` current if citation contexts or bibliography
   entries change again, and keep `paper/PAPER_CLAIM_AUDIT.md` current if
   numerical, comparison, or scope claims change.
6. Only after the diagnostic paper spine is stable, decide whether a future
   method should be phase-aware, contact-aware, or a separate benchmark-only
   extension.
