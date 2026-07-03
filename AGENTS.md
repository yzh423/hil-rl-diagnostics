# Agent Working Rules

Last updated: 2026-07-03

This file is for Codex agents and future automation working in this repository.
Read it before changing experiments, evidence rows, paper text, or project
structure.

## Required First Reads

Before making paper-facing changes, read:

1. `PROJECT_DASHBOARD.md`
2. `CONTEXT.md`
3. `PROJECT_STRUCTURE.md`
4. `results/RESULTS_INDEX.md`
5. `results/EXPERIMENT_EVIDENCE_REGISTRY.md`
6. `PAPER_PLAN.md`
7. `results/r047_evidence_provenance_package/EVIDENCE_PROVENANCE_AUDIT.md`
8. `results/r048_version_command_provenance/VERSION_PROVENANCE_REPAIR.md`

## Current Scientific Position

The current paper route is a cost-matched HIL-RL diagnostic protocol for
human-attention allocation in robotic manipulation. The current LV-VoI trigger
is not a positive method result.

Protected claim:

- R021 `random_b350` dominates LV-VoI scale3 under cost matching.
- R022 and R024 lightweight trigger repairs remain dominated.
- R023 traces diagnose intervention spending patterns; they do not overturn
  the R021 result.

## Evidence Rules

- Treat raw `results/r0xx_*` outputs as immutable evidence archives.
- Do not edit historical CSVs to make a claim fit.
- Add new derived artifacts under a new `results/r0xx_*` directory with a
  manifest.
- Add or update `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` before using a
  result number in manuscript prose.
- Use `results/EXPERIMENT_EVIDENCE_REGISTRY.md` for human-readable claim rules.
- Run validation and numeric audit before claiming that evidence is ready.

## Paper Rules

- Current manuscript files live in `paper/`.
- Historical proposal material lives in `proposal/` and should not be treated as
  the current paper spine.
- Use only citation keys present in `paper/references.bib` unless a new source
  has been verified.
- Do not add citations from memory.
- Use `paper/CITATION_AUDIT.md` for the current citation-context audit state;
  rerun the audit if citation contexts or bibliography entries change.
- Be explicit that the current experiments use a scripted privileged-state
  oracle, not a real teleoperator.

## Code Rules

- Keep behavior-preserving refactors small and covered by tests.
- Do not refactor `scripts/train_robosuite_hil.py` and run a new scientific
  experiment in the same step unless tests are expanded first.
- Prefer the extracted modules in `foresight_hil/experiments/` and
  `foresight_hil/evaluation/` over duplicating logic in scripts.
- Use registry-driven table generation instead of manually copying result
  numbers into LaTeX.

## Verification Menu

Use the smallest relevant set, and run the full set before claiming a
paper-facing organization or code change is complete:

```powershell
python scripts\validate_evidence_registry.py
python scripts\audit_registry_numbers.py
python scripts\generate_claim_tables.py
python scripts\validate_provenance_package.py
python -m unittest discover -s tests
```

For bibliography changes:

```powershell
python C:\Users\14228\.codex\skills\citation-management\scripts\validate_citations.py paper\references.bib --report results\r042_citation_context_audit\paper_references_validation_after_r042.json --verbose
```

## Current High-Value Next Tasks

- Keep public GitHub packaging clean: track source, registry-backed evidence,
  figures, tables, audits, and paper files; keep local process notes,
  third-party PDFs, caches, checkpoints, and bulky generated archives untracked.
- Use the current public Git repository for source-state tracking after the
  repository initialization, while keeping R048 as the historical record of the
  earlier invalid-Git/source-snapshot repair and R020/R021 command-provenance
  boundaries.
- Use R049 to validate R047/R048 provenance package self-consistency before
  claiming the provenance layer is ready.
- Decide whether submission packaging also needs an institutional source archive
  in addition to the public Git repository and R048 source snapshot.
- Use R047 as the current source/hash/compute/command provenance package before
  making paper-facing evidence claims.
- Keep the R051 citation-context audit current if citation contexts or
  bibliography entries change again.
- Decide whether to add small robotics breadth evidence before submission:
  cleaned Stack appendix, an explicitly scoped new in-project pilot, or no new
  runs.
- Resolve local LaTeX compile environment if PDF iteration becomes necessary.
- If future methods are considered later, design them from the R023/R024
  trace diagnosis rather than from the earlier unsupported LV-VoI superiority
  story.
