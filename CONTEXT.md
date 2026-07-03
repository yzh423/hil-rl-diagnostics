# FORESIGHT-HIL Context

Last updated: 2026-07-03

This file gives future humans and agents the project vocabulary. Use it before
editing experiment logic, paper claims, result summaries, or figure captions.

## Current Research Route

FORESIGHT-HIL is currently framed as a cost-matched HIL-RL diagnostic protocol
paper about human-attention allocation in robotic manipulation. The current
LV-VoI trigger is not claimed as superior. R020-R024 show that the conclusion
changes under stronger evaluation: `random_b350` dominates LV-VoI scale3 after
cost matching, and two simple trigger repairs remain dominated.

The paper contribution is therefore:

- strict cost-matched evaluation of human-attention allocation claims;
- repeated checkpoint evaluation instead of single-checkpoint reporting;
- intervention trace diagnostics at the start level;
- explicit negative findings that motivate protocol discipline before trigger
  redesign.

## Domain Glossary

| Term | Meaning in this repo |
|---|---|
| HIL-RL | Human-in-the-loop reinforcement learning with a scarce intervention budget. |
| Simulated human | A privileged scripted oracle used as the intervention source. It is not a real teleoperator. |
| Intervention trigger | A rule deciding when to request or apply oracle control. |
| Human-attention allocation | The current paper framing for intervention timing: the trigger decides when scarce human correction effort is spent. |
| LV-VoI trigger | The learning-value Value-of-Information trigger implemented through `VoIGate` and related flags. |
| Random budget family | Random intervention baselines swept across budgets so cost can be matched. |
| Cost matching | Comparing strategies at similar realized human-step cost, not only at nominal budget. |
| Repeated checkpoint evaluation | Re-evaluating selected checkpoints across repeated episodes, e.g. `5 x 20`, to reduce checkpoint noise. |
| Intervention trace | Per-intervention-start diagnostics such as training step, budget fraction, geometry, score, and `p_fail`. |
| Paper-core result | Evidence that can support the current manuscript route. R018 is registered boundary evidence; R020-R029 are paper-core unless later superseded. |
| Smoke result | A short execution or plumbing check. It proves code paths, not scientific claims. |
| Superseded result | A result kept for history but not used to support the current claim. |

## Claim Rules

- Do not claim LV-VoI trigger superiority unless the evidence registry contains
  a cost-matched, repeated-evaluation result that supports it.
- Treat `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` as the claim index.
- Treat `PAPER_PLAN.md` as the manuscript route index.
- Treat raw result directories as immutable evidence. Add new manifests or
  derived summaries instead of editing historical run outputs.
- When a number enters the paper, trace it back to a registry row and a primary
  source CSV or manifest.

## Architecture Vocabulary

Use these terms when discussing code structure:

- A module has an interface and implementation.
- A seam is where a module interface lives.
- A deep module hides complex implementation behind a small interface.
- A shallow module exposes an interface nearly as complex as its implementation.
- Locality means a bug or change is concentrated in one module.
- Leverage means one interface supports many callers or tests.

Current shallow module candidate: `scripts/train_robosuite_hil.py`. It still
mixes CLI configuration, training, evaluation, and summary writing. R030
extracted a first bookkeeping module at
`foresight_hil/experiments/bookkeeping.py`; R031 extracted trace schema and row
construction at `foresight_hil/experiments/trace.py`; R032 extracted driver
strategy identity and training CLI construction at
`foresight_hil/experiments/strategy_specs.py`; R033 extracted repeated
checkpoint evaluation summaries at `foresight_hil/evaluation/protocol.py`. The
R034 added registry/source validation at
`foresight_hil/evaluation/registry_validation.py` and fixed malformed R023
registry rows. R035 added numeric registry auditing at
`foresight_hil/evaluation/registry_numeric_audit.py`; the current registry
numbers match their primary CSV rows. R036 added registry-driven claim table
generation at `foresight_hil/evaluation/claim_tables.py`, producing
manuscript-ready Markdown and LaTeX tables from the audited registry. R037
completed the first source-bank citation audit for candidate method/setup and
evaluation references, keeping them staged outside the main bibliography. R038
created the first current-route manuscript skeleton under `paper/`, importing
R029/R036 assets and using only R027/R037-supported citation keys. PDF
compilation is blocked on this machine by the incomplete local LaTeX runtime,
not by a known source-file error. R039 adds `PROJECT_DASHBOARD.md`, `AGENTS.md`,
and `results/r039_project_organization/` so future work starts from a compact
project dashboard before touching evidence, code, or manuscript claims. R040
polishes the abstract, Introduction, Diagnostic Protocol and Experimental Setup,
and Conclusion while preserving the current evidence boundaries and citation key
set. R041 polishes Results and Discussion around the cost-matched reversal,
negative repairs, trace mechanism, Stack boundary evidence, and stop/redesign
rules. R042 audits all current manuscript citation contexts, fixes six
bibliographic metadata entries, and leaves no wrong-context citation known in
the current draft. R043 selects IEEE T-ASE as the primary target route, with
T-RO as a stretch target and RA-L/RAS/EAAI as contingencies. The next
paper-facing gates are target-specific manuscript alignment, optional robotics
breadth evidence, compute accounting, public source packaging, and local PDF
compile/runtime resolution. R044 audits the local runtime and reproducibility
state: Python 3.11.13, the pinned robosuite/MuJoCo stack, and CUDA-enabled
PyTorch are available, smoke paths run locally, but `.git` metadata is invalid
and the project still needs submission-grade provenance repair. R045 adds the
first T-ASE-style Note to Practitioners and reproducibility appendix inventory
without adding new citations, experiments, or trigger-superiority claims. R047
adds the current evidence-provenance package: all registered primary sources are
present and hashable, selected paper/project artifacts are hashed, partial
compute accounting and command inventories are recorded, and the invalid Git
state plus incomplete R020/R021 command provenance remain explicit gaps. R048
adds a deterministic source snapshot as the current replacement for invalid Git
commit provenance and clarifies R020/R021 provenance: R020 is a repeated
checkpoint-evaluation consolidation over earlier checkpoints, R021 random_b350
and random_b450 have raw run summaries/checkpoints, and reconstructed commands
are templates rather than archived original launch logs. R049 adds an automated
provenance-validation gate: the default command validates R047/R048 package
self-consistency, while `--compare-current-files` intentionally reports drift
between historical ledgers and the current working tree. After the public GitHub
initialization, the current source state is tracked by a valid Git repository;
R048 remains the historical repair artifact for the earlier invalid-Git
workspace state. R050 deepens the current paper spine from trigger diagnostics
to human-attention allocation diagnostics, updating the manuscript, plan, and
public project framing without changing evidence boundaries, citations, or raw
results. R051 reruns the citation-context audit after R050 and finds no
wrong-context citation in the current 15-key manuscript bibliography. R052
audits current manuscript numerical, comparison, and scope claims against the
registry and primary sources, repairing one stale provenance wording issue while
preserving the negative LV-VoI boundary. R053 registers the Stack boundary rows
and generates a ready-to-include appendix table from the registry, keeping Stack
as negative robotics breadth rather than positive transfer evidence. R054 adds
a scipilot-guided attention-allocation diagnostic figure package from
R021/R023/R024, replacing compressed or dual-axis-style presentation with
separate decision-gate, timing, budget, geometry, and score diagnostics.
