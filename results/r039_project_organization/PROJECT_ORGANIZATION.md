# R039 Project Organization

Date: 2026-07-02

## Purpose

R039 organizes the project for continued research and manuscript work without
moving or rewriting historical evidence. The goal is to make the current route,
claim boundaries, verification commands, and next actions visible from the
repository root.

## What Changed

- Added `PROJECT_DASHBOARD.md` as the single-page project entry point.
- Added `AGENTS.md` with future-agent operating rules.
- Added `.gitignore` for Python caches, local environments, editor noise, and
  LaTeX intermediate files.
- Added this R039 organization package and manifest.
- Updated project indexes, registry documentation, and tracker rows so R039 is
  discoverable from the existing evidence chain.
- Added ADR-002 to record why dashboard and agent rules are now first-class
  project artifacts.

## What Did Not Change

- No raw experiment CSVs were moved, deleted, or rewritten.
- No training or evaluation behavior changed.
- No paper claims were upgraded beyond the current evidence registry.
- No citation entries were added.
- No manuscript prose was rewritten.

## Current Organization Model

The project is now organized around four interfaces:

| Interface | Artifact | Role |
|---|---|---|
| Navigation | `PROJECT_DASHBOARD.md` | First screen for humans and agents. |
| Scientific boundary | `CONTEXT.md` and `PAPER_PLAN.md` | Current route, claim limits, and paper spine. |
| Evidence boundary | `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` | Machine-readable paper-claim index. |
| Operational rules | `AGENTS.md` | How future agents should modify the repo safely. |

## Recommended Next Step

Do not start a new method immediately. The strongest next move is to strengthen
the current manuscript sections, especially Introduction and Diagnostic Protocol,
then run final citation-context audit on the stabilized `\cite{...}` contexts.

If a new method is later added, it should be designed from R023/R024 trace
evidence and should enter as a new R040+ experiment package.
