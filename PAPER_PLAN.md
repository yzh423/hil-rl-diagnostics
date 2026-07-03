# Paper Plan

**Working title**: Cost-Matched Diagnostics for Human-Attention Allocation in Human-in-the-Loop Robot Learning

**Venue target**: Primary route is IEEE Transactions on Automation Science and
Engineering (T-ASE), with IEEE Transactions on Robotics (T-RO) as a stretch
target and RA-L / Robotics and Autonomous Systems / Engineering Applications of
Artificial Intelligence as contingencies. R043 records the source-backed venue
matrix in `results/r043_venue_targeting/`.

**Paper type**: Empirical diagnostic protocol paper with a robotic manipulation case study. The theme is human-attention allocation under scarce intervention budgets; negative findings are treated as evidence for the protocol, not as the paper identity.

**Date**: 2026-07-03

**Page budget**: 12-14 pages for journal-style draft, including references if targeting IEEE Transactions-style venues.

## Central Thesis

In HIL-RL for robot learning, an intervention trigger is a policy for allocating
scarce human attention during training. A trigger can appear human-efficient
under weak evaluation, but the conclusion can reverse once random baselines are
cost matched, checkpoints are repeatedly evaluated, and interventions are
traced at the start level. The paper's main contribution is a diagnostic
evaluation protocol for human-attention allocation claims in robotic HIL-RL,
demonstrated through a robosuite manipulation case study in which the current
LV-VoI trigger and two lightweight repairs are dominated by cost-matched random
baselines.

R028 refines this framing in `results/r028_framework_refinement/`. Use that
package before drafting claims, section prose, or rebuttal text.

R043 refines the submission route. Treat the manuscript as a T-ASE-style
automation-science paper: a diagnostic protocol and reproducibility discipline
for human-intervention allocation in robotic HIL-RL, not a failed-method report.

R044 audits the local environment and reproducibility state. Treat it as the
current gate for rigor improvements: centralize reproduction commands, add a
Note to Practitioners, repair version provenance, and add a compact
compute-accounting/reproducibility appendix before submission.

R045 completes the first target-specific manuscript alignment pass by adding a
T-ASE-style Note to Practitioners and a reproducibility appendix inventory. It
does not change the evidence boundary or add citation keys.

R047 adds the current evidence-provenance package: registry source inventory,
artifact hashes, partial compute accounting, command provenance inventory, and
an explicit gap analysis. It strengthens reproducibility evidence without adding
new scientific results.

R048 adds the current source-snapshot replacement for invalid Git provenance and
clarifies R020/R021 command provenance. Use it for artifact-review packaging and
for cautious reproducibility language; it does not add a Git commit hash or new
experimental results.

R049 adds the executable provenance-validation gate. Use the default command as
part of verification; use drift mode only to decide whether a fresh source
snapshot is needed.

R050 deepens the paper spine from "trigger diagnostics" to "human-attention
allocation diagnostics" without changing the evidence boundary. Use it as the
current narrative rule: the paper evaluates whether a trigger really improves
the allocation of scarce human intervention effort, not whether LV-VoI is a
positive method result.

R051 reruns citation-context audit after the R050 theme update. It finds that
all 15 current citation keys still support their manuscript contexts and makes
no bibliography changes.

R052 audits current manuscript numerical, comparison, and scope claims against
the registry and primary sources. It passes after one minor wording repair that
updates the reproducibility appendix to treat R048 as the historical invalid-Git
repair record while the current source state is tracked in the public Git
repository.

R053 packages Stack as cleaned robotics-breadth boundary evidence. It registers
R018 Stack rows, generates an appendix-ready table from the registry, and keeps
R019 as supporting mechanism-probe context rather than a multiseed method
claim.

## Claims-Evidence Matrix

| Claim | Evidence | Status | Section |
|---|---|---|---|
| Cost-matched random baselines are necessary for human-attention allocation claims. | R021 `random_b350` reached `439/500 = 87.8%` at cost 177.0, dominating LV-VoI scale3 `416/500 = 83.2%` at cost 202.0. | Supported | Section 4 |
| Repeated checkpoint evaluation is required for reliable HIL-RL attention-allocation claims. | R020-R024 use `5 x 20` checkpoint reevaluation; R024 seed results vary from 61% to 94%. | Supported | Section 3, Section 4 |
| Simple trigger repairs do not fix random dominance. | R022 min-disagree: `226/300 = 75.3%`, cost 211.7. R024 score-floor: `233/300 = 77.7%`, cost 253.3. Both lose to same-seed `random_b350`: `259/300 = 86.3%`, cost 95.0. | Supported | Section 5 |
| Trace diagnostics reveal over-triggering and score calibration issues. | R023: LV-VoI starts closer to cube than random but starts 96 times vs random 55. R024: floor blocks low-score starts but still starts 94 times. | Supported | Section 5 |
| Current method does not yet generalize to Stack. | R018 registered Stack rows and R053 appendix table show no-online matched BC at `131/180 = 72.8%`, while random and Stack-tuned LV-VoI are `107/180 = 59.4%`; R019 remains supporting seed-0 mechanism-probe context. | Supported limitation | Section 6 / Appendix |

## Structure

### 0. Abstract

- **Problem**: HIL-RL trigger claims are really human-attention allocation claims, and they can be fragile when random baselines are not cost matched and checkpoint variance is under-measured.
- **Approach**: Define and apply a diagnostic protocol with three validity gates: cost-matched random families, repeated checkpoint evaluation, and trace-level intervention diagnostics.
- **Key result**: A cost-matched random baseline (`random_b350`) dominates LV-VoI scale3 on Lift: `87.8%` repeated success at cost 177.0 vs `83.2%` at cost 202.0; two lightweight repairs also remain dominated.
- **Implication**: Before claiming intervention-trigger superiority, HIL-RL papers should show that the attention-allocation claim survives cost-matched random families, repeated checkpoint estimates, and trace-level budget diagnostics.

### 1. Introduction

- **Opening**: Human interventions can rescue RL from unsafe or unproductive trajectories, but intervention timing is a scarce human-attention allocation decision.
- **Gap**: Many evaluations compare against a single random budget or a single final checkpoint, leaving room for optimistic intervention-efficiency conclusions.
- **Research questions**:
  - RQ1: Does a foresighted VoI trigger remain Pareto-superior after cost matching?
  - RQ2: Can simple disagreement or score-calibration repairs recover the advantage?
  - RQ3: What diagnostics reveal why a trigger spends budget inefficiently?
- **Contributions**:
  1. A cost-matched HIL-RL trigger evaluation protocol for human-attention allocation in robotic manipulation.
  2. A case-study reversal: current LV-VoI variants are dominated by cost-matched random under this protocol.
  3. Trace diagnostics showing over-triggering and score/timing mismatch.
  4. Practical stop/continue rules for trigger redesign.
- **Hero figure**: Protocol gates + success-cost reversal + intervention start distribution.

### 2. Related Work

- Human-in-the-loop RL and intervention learning.
- Learning from demonstrations and intervention data in robotic manipulation.
- Active querying, value of information, and uncertainty-based intervention triggers.
- Evaluation reliability in RL: seeds, checkpoint selection, confidence intervals, and negative results.

Citation note: do not fill BibTeX from memory. Use `paper/references.bib` plus
the R037/R042 audit records before adding or rewriting literature claims.

### 3. Diagnostic Protocol and Experimental Setup

- **Environment**: robosuite Lift and Stack, scripted privileged-state oracle as simulated human.
- **Learning backbone**: SAC with demonstration replay / BC regularization.
- **Intervention strategies**: none, random@budget, LV-VoI scale3, min-disagreement LV-VoI, score-floor LV-VoI.
- **Protocol**:
  - repeated checkpoint evaluation (`5 x 20` episodes),
  - Wilson confidence intervals,
  - best-step human cost,
  - raw final vs restored best policy,
  - trace-level intervention diagnostics.
- **Limitations**: no real human, no real robot, privileged scripted oracle, limited tasks.

### 4. Main Case Study: Cost Matching Reverses the Initial Claim

- Present R020 as the initially promising result.
- Present R021 as the decisive cost-matched random check.
- Table 1: none, random_b350, random_b450, random_b600, LV-VoI scale3.
  Prefer registry-generated source `figures/TABLE_registry_costmatched_results_r036.tex`.
- Figure 2: success-cost frontier.
- Key message: LV-VoI should not be claimed as Pareto-superior.

### 5. Trigger Repairs and Mechanism Analysis

- R022: minimum disagreement filter fails.
- R024: score floor works mechanically but fails scientifically.
- R023/R024 traces:
  - LV-VoI is closer to the cube than random, so far-from-object triggering is not the explanation.
  - LV-VoI starts too often and score calibration is weak.
- Table 2: negative findings.
  Prefer registry-generated source `figures/TABLE_registry_trigger_repairs_r036.tex`
  for numeric repair comparisons, and keep `figures/TABLE_negative_findings.tex`
  for broader hypothesis/decision framing.
- Figure 3: repair comparison.
- Figure 4: timing bins.
- Figure 5: R024 score-over-time.

### 6. Discussion: Evaluation Rules for Future HIL-RL Attention Allocation

- Cost matching is not optional.
- Repeated checkpoint evaluation should be standard.
- Trigger scores need calibration and budget-control diagnostics.
- Negative findings can be useful when they prevent unsupported claims.
- Stack results show that task transfer remains unresolved.

### 7. Conclusion

The paper should conclude with the evaluation lesson, not the failed trigger:
before claiming that an intervention trigger allocates human effort more
efficiently, HIL-RL papers should show that the claim survives cost-matched
random families, repeated checkpoint estimates, and trace-level budget
diagnostics.

## Figure Plan

| ID | Description | Source |
|---|---|---|
| Fig. 1 | Hero diagnostic summary: HIL-RL pipeline, cost-matched reversal, intervention start counts. | R021/R023/R024 |
| Fig. 1b | Protocol-centered hero candidate: checklist gates, cost-matched reversal, trace diagnosis. | `figures/fig1_protocol_hero_r029.pdf` |
| Fig. 2 | Success-cost frontier for five-seed Lift. | `results/r021_random_costmatch/r021_costmatch_aggregate.csv` |
| Fig. 3 | R022/R024 negative trigger repairs vs random_b350. | `results/r024_score_floor_seed0_2/r024_score_floor_aggregate.csv` |
| Fig. 4 | Intervention timing distribution. | `results/r024_score_floor_seed0_2/r024_intervention_timing_bins_compare.png` |
| Fig. 5 | Score-over-time under R024. | `results/r024_score_floor_seed0_2/r024_score_over_time.png` |
| Table 1 | Registry-generated cost-matched Lift claims. | `figures/TABLE_registry_costmatched_results_r036.tex` |
| Table 2 | Registry-generated trigger-repair comparison. | `figures/TABLE_registry_trigger_repairs_r036.tex` |
| Table 4 | Diagnostic protocol checklist. | `figures/TABLE_protocol_checklist.tex` |
| Appendix Table A1 | Registry-generated Stack boundary evidence. | `figures/TABLE_stack_boundary_appendix_r053.tex` |

## Citation Plan

R027 source-bank preparation has started in `results/r027_citation_source_bank/`.
Use `citation_support_bank.csv` before drafting any literature sentence, and do
not merge `bibtex_candidates_to_add.bib` into the main bibliography until the
candidate entries pass metadata/context audit.

R037 completed the first candidate metadata/context-use audit. Use
`results/r037_citation_audit_batch1/CITATION_METADATA_CONTEXT_AUDIT.md` before
adding SAC, robosuite, Henderson, Agarwal, or Wilson citations to a draft.

R038 started the current manuscript skeleton in `paper/main.tex`. The skeleton
imports R029/R036 display assets and uses only R027/R037-supported citation
keys. PDF compilation still requires a complete local LaTeX runtime or a filled
Tectonic cache.

R051 completed the current manuscript citation-context audit after the R050
theme update. All 15 current citation keys support their manuscript contexts,
with no additional bibliography changes after the R042 metadata fixes. See
`paper/CITATION_AUDIT.md` and `results/r051_citation_context_audit/`.

R052 completed the current manuscript paper-claim audit after R050/R051. Use
`paper/PAPER_CLAIM_AUDIT.md` before revising numerical, comparison, or scope
claims.

- Intro: HIL-RL, intervention learning, robot manipulation with human corrections. `[AUDITED R042]`
- Related work: HIL-SERL-style systems, learning from interventions, active learning / VoI, uncertainty in model-based RL, negative results / reproducibility in RL. `[AUDITED R042]`
- Method/setup: SAC, robosuite, demonstration replay / RLPD, and oracle/simulator context citations passed current context audit. `[AUDITED R042]`
- Evaluation: Wilson intervals, repeated seeds/checkpoints, and RL evaluation reliability citations passed current context audit. `[AUDITED R042]`

No new BibTeX should be added until each reference is verified from an authoritative source.

## Reproducibility Plan

Use `results/r044_environment_reproducibility_audit/REPRODUCTION_COMMANDS.md`
as the central command sheet for verification, smoke checks, and future
paper-core reruns. Historical result directories should not be overwritten; any
rerun or new robotics-breadth result should write to a fresh `results/r0xx_*`
directory and receive a registry row before being used in prose.

R045 adds the first reproducibility appendix inventory that links claims,
tables, commands, environment state, and provenance caveats to their source
artifacts. The project now has a valid public Git repository for the current
source state; R048 remains the historical source-snapshot repair for the earlier
invalid-Git workspace state.

R047 adds source/hash/compute/command ledgers for the current evidence chain.
Use `results/r047_evidence_provenance_package/` before any artifact-review or
rebuttal packaging. The remaining reproducibility risks are invalid local Git
metadata, incomplete R020/R021 launch-command provenance, and partial rather
than complete wall-clock accounting for historical runs.

R048 resolves the first two risks for the pre-publication workspace by providing
a deterministic source snapshot and a transparent command-provenance boundary
note. For future submission packaging, cite the public Git repository for the
current source state and keep the R048 snapshot/hash as the historical repair
record for the earlier invalid-Git state.

R049 makes the provenance layer executable:

```powershell
python scripts\validate_provenance_package.py
```

Use `--compare-current-files` only as a drift diagnostic; a failure there means
the current working tree differs from older snapshots, not that raw evidence is
corrupt.

## Reviewer Feedback

Secondary reviewer-agent feedback was not run in this turn because sub-agent spawning requires explicit user authorization in the current environment. Self-review:

- The paper is stronger as a diagnostic benchmark than as a method paper.
- The biggest risk is perceived lack of positive algorithmic contribution.
- The minimum fix is to make the protocol itself crisp: cost-matched random families, repeated checkpoint evaluation, and trace diagnostics become the contribution for evaluating human-attention allocation claims.
- Another risk is limited task breadth; Stack should be framed as boundary evidence, not as positive transfer.
- R028 strengthens the framing further: call the paper a diagnostic protocol
  paper with a robotic case study, not a negative-findings paper.
- R043 strengthens the target fit: T-ASE is the primary route because its scope
  explicitly fits methodologies, systems, and case studies around efficiency and
  reliability. T-RO should remain a stretch target unless robotics validation is
  broadened.

## Next Steps

- [x] Use `results/r028_framework_refinement/` as the claim/section boundary before drafting.
- [x] Polish the hero figure so the protocol and cost-matched reversal are visible in the first figure (`figures/fig1_protocol_hero_r029.pdf`).
- [x] Build a protocol checklist table from R025/R028 (`figures/TABLE_protocol_checklist.tex`).
- [x] Generate registry-driven claim tables from audited evidence (`figures/TABLE_registry_costmatched_results_r036.tex`, `figures/TABLE_registry_trigger_repairs_r036.tex`).
- [x] Finish first-batch R027/R037 metadata/context audit for candidate method/setup/evaluation sources; do not cite from memory.
- [x] Start a current-route manuscript skeleton after framework, figure story, and first-batch citation support stabilized (`paper/main.tex`).
- [x] Add a project dashboard and future-agent rules so the current route and evidence boundaries are easy to recover (`PROJECT_DASHBOARD.md`, `AGENTS.md`).
- [x] Polish the abstract, Introduction, Diagnostic Protocol and Experimental Setup, and Conclusion as a first prose-strengthening pass (`results/r040_manuscript_polish/`).
- [x] Strengthen Results and Discussion into journal-grade prose (`results/r041_results_discussion_polish/`).
- [x] Run final citation-audit on real `\cite{...}` contexts (`results/r042_citation_context_audit/`).
- [x] Decide target journal family before formatting references and page budget (`results/r043_venue_targeting/`).
- [x] Check local environment, reproduction entry points, and innovation/rigor gaps (`results/r044_environment_reproducibility_audit/`).
- [x] Align manuscript language and structure to the T-ASE target route, including a Note to Practitioners (`results/r045_tase_reproducibility_alignment/`).
- [x] Add a reproducibility appendix inventory and compute-accounting status table (`paper/sections/07_reproducibility_inventory.tex`).
- [x] Add an evidence provenance package with source hashes, partial compute accounting, command inventory, and explicit gaps (`results/r047_evidence_provenance_package/`).
- [x] Replace invalid local Git provenance with a deterministic source snapshot (`results/r048_version_command_provenance/`).
- [x] Reconstruct and explicitly bound R020/R021 command-provenance context (`results/r048_version_command_provenance/`).
- [x] Add a tested provenance-validation gate (`results/r049_provenance_validation/`).
- [x] Initialize and publish a valid GitHub repository for the current source state.
- [x] Deepen the paper spine around human-attention allocation diagnostics (`results/r050_theme_deepening/`).
- [x] Rerun citation-context audit after the R050 theme update (`results/r051_citation_context_audit/`).
- [x] Audit current manuscript numerical, comparison, and scope claims after R050/R051 (`results/r052_paper_claim_audit/`).
- [x] Package cleaned Stack boundary evidence as an appendix-ready robotics breadth table (`results/r053_stack_boundary_appendix/`).
- [ ] Decide whether submission packaging also needs an institutional source archive.
- [ ] Decide whether any robotics breadth beyond the cleaned Stack appendix is worth adding before submission.
