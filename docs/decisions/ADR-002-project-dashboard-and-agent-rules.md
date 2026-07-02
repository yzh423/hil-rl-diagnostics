# ADR-002: Project Dashboard And Agent Rules

Date: 2026-07-02

## Status

Accepted.

## Context

The repository now contains code modules, raw experiment archives, paper figures,
manuscript files, citation-audit outputs, and multiple result indexes. R020-R038
also changed the scientific route from a positive LV-VoI method claim to a
cost-matched diagnostic protocol paper. Without a compact entry point, future
work risks using superseded claims, smoke runs, or unaudited citations.

## Decision

Make two root-level files first-class project artifacts:

- `PROJECT_DASHBOARD.md` for the current human-readable project state.
- `AGENTS.md` for future agent operating rules.

Keep detailed evidence and history in the existing registry, result index,
figure index, tracker, and paper plan. The dashboard should route readers to
those canonical files instead of duplicating their full contents.

## Consequences

- Future work has a shorter first-read path.
- Paper claims stay tied to the evidence registry.
- Agent sessions have explicit guardrails for raw evidence, citations, and
  manuscript claims.
- The dashboard must be updated when the current paper route or canonical
  verification commands change.
