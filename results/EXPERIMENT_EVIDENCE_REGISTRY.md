# Experiment Evidence Registry

This registry is the single entry point for paper-facing R018 and R020-R062
evidence.
Use `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` as the machine-readable source
when drafting claims, tables, captions, or rebuttal text.

## Rules

- Do not quote a success/cost number in the manuscript unless it appears in the
  registry or in a cited primary CSV listed by the registry.
- Run `python scripts/validate_evidence_registry.py` before drafting or revising
  paper claims.
- Run `python scripts/audit_registry_numbers.py` before copying registry
  numbers into prose, tables, captions, or rebuttal text.
- Run `python scripts/generate_claim_tables.py` to regenerate
  registry-derived Markdown and LaTeX claim tables.
- Run `python scripts/generate_methodology_extension.py` to regenerate the R056
  protocol gate matrix, failure taxonomy, stop-rule metrics, and LaTeX tables.
- Run `python scripts/generate_offline_trace_audit.py` to regenerate the R060
  offline trace audit tables and narrative.
- Run `python scripts/generate_stack_boundary_appendix.py` to regenerate the
  R053 Stack appendix table.
- Treat R018 Stack rows as registered boundary evidence only; do not use them
  to claim positive robotics transfer.
- Treat R021 `random_b350` as the decisive cost-matched check for Lift.
- Treat R022 and R024 as negative trigger-repair gates; do not expand either
  without a substantially different mechanism.
- Treat R023 as a trace diagnostic, not as the main success-rate evidence.
- Treat R025/R026/R028/R029 as paper-preparation artifacts, not new experimental
  results.
- Treat R030-R062 as structure, manuscript-theme, citation-audit,
  paper-claim-audit, paper-artifact, evidence-discipline,
  experiment-planning, trace-offline diagnostic, and instrumentation
  artifacts, not new experimental results.

## Current Verdict

The registry supports the diagnostic-benchmark paper route:

- R021 rejects the current LV-VoI superiority claim after cost matching.
- R018 registers Stack as boundary evidence: no-online matched BC beats the
  current online-intervention variants under the matched Stack setup.
- R022 and R024 show that two simple trigger repairs remain dominated.
- R023 explains the failure as over-triggering and score/timing mismatch rather
  than a simple far-from-cube geometry issue.
- R025/R026 package the evidence for manuscript drafting.
- R028 refines the paper identity: diagnostic evaluation protocol plus robotic
  manipulation case study, not a negative-findings-only paper.
- R029 makes that protocol contribution visible with a protocol-centered hero
  figure candidate and checklist table.
- R030-R033 stabilize the code and artifact interfaces for bookkeeping, trace
  schema, strategy specifications, and repeated-evaluation summaries.
- R034 validates registry primary sources and corrected malformed R023 rows.
- R035 audits registry numeric fields against primary CSV rows; the current
  registry reports 0 numeric issues.
- R036 generates manuscript-ready claim tables directly from audited registry
  rows, reducing manual copying before drafting.
- R037 audits the first batch of staged candidate citations for method/setup
  and evaluation-protocol claims, while leaving final `\cite{}` context audit
  until a manuscript skeleton exists.
- R038 creates the first current-route manuscript skeleton under `paper/`,
  importing R029/R036 assets and R027/R037-supported citations.
- R039 adds a root project dashboard, future-agent rules, and synchronized
  organization indexes without changing raw evidence or experiment behavior.
- R040 polishes the abstract, Introduction, Diagnostic Protocol and
  Experimental Setup, and Conclusion without changing evidence boundaries or
  adding citation keys.
- R041 polishes Results and Discussion around the cost-matched reversal,
  negative repairs, trace mechanism, Stack boundary evidence, and stop/redesign
  rules without adding new experiments or citation keys.
- R042 audits all current manuscript citation contexts, applies six metadata
  fixes, and reports no wrong-context citation in the current draft.
- R043 selects IEEE T-ASE as the primary target route and records stretch and
  fallback venues with official source URLs and target-driven revision tasks.
- R044 audits the local runtime, smoke readiness, reproducibility entry points,
  innovation gaps, and rigor roadmap without adding new scientific result
  claims.
- R045 aligns the manuscript to the T-ASE route with a Note to Practitioners
  and reproducibility appendix inventory, without changing evidence boundaries
  or adding citation keys.
- R047 adds a source/hash/compute/command provenance package for the current
  evidence chain, records that all registered primary sources are present, and
  keeps invalid Git metadata plus incomplete R020/R021 command provenance as
  explicit reproducibility gaps.
- R048 replaces the unavailable Git commit provenance with a deterministic
  source snapshot and clarifies R020/R021 command provenance through checkpoint
  inventories, raw-run inventories, and reconstructed command templates.
- R049 adds a tested provenance-validation gate so R047/R048 package
  self-consistency and optional current-file drift diagnosis are executable
  checks rather than manual inspection.
- R050 deepens the paper spine from trigger diagnostics to human-attention
  allocation diagnostics without adding experiments, citations, or a positive
  LV-VoI claim.
- R051 reruns citation-context audit after R050, confirming that all 15 current
  citation keys still support their manuscript contexts.
- R052 audits current manuscript numerical, comparison, and scope claims against
  the registry and primary sources, repairing one stale Git-provenance wording
  issue while preserving the negative LV-VoI boundary.
- R053 packages the Stack boundary evidence into a registry-driven appendix
  table and keeps the interpretation negative.
- R054 adds a scipilot-guided attention-allocation diagnostic figure and trace
  profile from R021/R023/R024, improving presentation without adding a new
  scientific result claim.
- R055 records a project-wide documentation/code quality pass, extracts the
  R054 trace-profile logic into a tested evaluation module, and integrates the
  R054 figure into the Results narrative without changing experimental result
  claims.
- R056 derives a protocol gate matrix, failure-mode taxonomy, stop-rule metrics,
  and methodology-first Fig. 1 candidate from registered R021/R023/R024
  evidence, strengthening the method contribution without adding a new
  experiment or positive LV-VoI claim.
- R057 adds a repeatable Markdown local-link validator and repairs row-aligned
  attention-profile gap handling, improving project quality without changing
  experimental result claims.
- R058 records the submission-packaging readiness pass: bundled Tectonic now
  compiles the current PDF through a project-local cache and `paper/figures/`
  snapshots, first visual QA is complete, public Git is the current source-state
  tracker, and a frozen institutional/source archive should be produced only
  from the final verified submission tag.
- R059 records the evidence-first experiment optimization route: resolve
  packaging gates, harden existing audits, use cheap R023/R024 trace/offline
  diagnostics before new training, and require cost-matched stop gates before
  any future positive method claim.
- R060 executes the first R059 trace/offline diagnostic extension from R023/R024
  accepted-start traces. It can support phase/count/gate-retention statements,
  but it cannot support online success-rate or method-superiority claims.
- R061 adds tested candidate-state logging for future VoI gate evaluations,
  including accepted and rejected states. It is instrumentation for future
  online experiments, not online performance evidence.
- R062 pre-registers the candidate-logging smoke gate and the R063+ formal
  online-repair criteria. It is a planning/readiness artifact, not a new
  empirical result.
