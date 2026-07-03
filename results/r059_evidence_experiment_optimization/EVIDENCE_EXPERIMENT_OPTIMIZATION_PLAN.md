# R059 Evidence And Experiment Optimization Plan

Date: 2026-07-03

## Optimization Principle

Optimize the evidence chain before optimizing the method. The current paper is
strongest as a cost-matched diagnostic protocol for human-attention allocation,
not as a positive LV-VoI method paper. Any future experiment must preserve that
boundary unless it produces new, registered, cost-matched evidence.

## Phase 0: Finish Packaging Gates

Run before any new experiment:

1. Resolve local or CI PDF compilation.
2. Complete PDF visual QA.
3. Run the full verification menu.
4. Update paper-claim and citation audits only if manuscript claims or citation
   contexts change.
5. Keep the public Git repository clean; defer the final source archive until a
   verified submission tag exists.

Stop gate: do not launch expensive training if the manuscript cannot yet be
compiled and visually checked.

## Phase 1: Evidence Hardening Without New Training

Goal: make existing claims easier to trust without changing the empirical
story.

Recommended actions:

- Re-run registry validation, numeric audit, provenance validation, document
  link validation, and unit tests after every paper-facing change.
- Add a final paper-claim audit pass after PDF compile if any caption, table,
  abstract sentence, or conclusion sentence changes.
- Add a final source archive from a clean Git tag only after all checks pass.
- Keep R021/R022/R023/R024 as the core Lift evidence and R053 as boundary
  robotics breadth.

Stop gate: if all current claims are supported and reviewer risk is mainly
packaging/clarity, do not create new experiments just to add volume.

## Phase 2: Cheap Diagnostic Extensions From Existing Traces

Goal: extract more diagnostic value from R023/R024 before spending compute.

Candidate derived analyses:

| Candidate | Inputs | Value | Boundary |
|---|---|---|---|
| Phase-aware trace summary | R023/R024 trace CSVs | Tests whether interventions concentrate before/after grasp/contact phases. | Diagnostic only; no success-rate claim. |
| Intervention-spend efficiency curve | R021/R023/R024 summaries | Shows success per human-step family across checkpoints. | Derived visualization only. |
| Counterfactual trigger audit | R023/R024 traces | Scores proposed trigger gates offline against observed privileged-state traces. | Does not prove online performance. |
| Failure-taxonomy refinement | R056 plus R023/R024 | Tightens stop/redesign criteria. | No new method superiority claim. |

Stop gate: promote a derived analysis only if it clarifies the diagnostic
protocol or directly reduces reviewer confusion. Register it under a new R060+
directory before manuscript use.

## Phase 3: Minimal New Training, Only If Needed

Use new training only for one of these manuscript-critical questions:

| Question | Minimal experiment | Expected contribution |
|---|---|---|
| Is the R021 reversal robust to more seeds? | Add a fresh R060-style reproduction/extension of the cost-matched random/LV-VoI comparison with preserved stdout/stderr and registry rows. | Strengthens confidence in the negative result. |
| Can a trace-derived repair beat the random baseline? | Run one pre-registered phase/contact-aware trigger against `random_b350` under matched human-step cost. | Tests whether R023/R024 diagnosis can produce a real method improvement. |
| Is robotics breadth necessary for the target venue? | Add one carefully chosen extra task only if target feedback demands it. | Strengthens breadth, but increases verification and writing burden. |

Do not run a new method experiment in the same step as a refactor of
`scripts/train_robosuite_hil.py` unless tests are expanded first.

Stop gate: a method candidate must beat the cost-matched random family before
it can be described as a positive method result. Otherwise it remains a
diagnostic negative/repair result.

## Recommended Next Experiment If Compute Is Available

If the user wants one experiment next, choose the cheapest claim-relevant path:

1. Offline R023/R024 counterfactual trigger audit from existing traces.
2. If the offline audit identifies a plausible gate, run one cost-matched online
   trigger repair in a fresh `results/r060_*` directory.
3. Compare against `random_b350` and LV-VoI scale3 using registry-driven tables.
4. Register the row before changing manuscript prose.

This sequence keeps compute risk low and prevents a weak trigger idea from
becoming an unsupported paper claim.

## Must-Have Logging For Any New Run

Every future R060+ experiment should archive:

- exact command line;
- stdout/stderr log;
- Git commit hash or source snapshot ID;
- environment summary;
- raw result CSVs;
- repeated checkpoint summaries when applicable;
- manifest explaining claim boundary;
- registry row before manuscript use.
