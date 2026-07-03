# R058 Source Archive Decision

Date: 2026-07-03

## Decision

Use the public GitHub repository as the primary current source-state tracker,
and prepare an institutional or submission-system source archive at the final
submission tag.

This means the project should use both mechanisms, but for different purposes:

| Mechanism | Purpose |
|---|---|
| Public GitHub repository | Ongoing source history, review-time access, issue/PR traceability, and public reproducibility. |
| R047/R048 provenance package | Historical evidence-source hashes, command-provenance boundaries, and repair record for the earlier invalid-Git state. |
| Final institutional/source archive | Frozen submission artifact for venue, institution, or artifact-review retention. |

## Rationale

Public Git is the best day-to-day source-state tracker, but it is mutable by
design: branches can move, repository visibility can change, and large evidence
artifacts may not belong in the repository. A small source archive produced
from a clean final tag gives the submission a stable, citable source snapshot
without pretending to replace the evidence ledgers.

## Timing

Do not create the final source archive before the following are complete:

1. PDF compile and visual QA pass.
2. Registry, numeric, provenance, document-link, and unit-test verification
   pass.
3. Final paper-claim audit if any numerical, comparison, or scope claim changes.
4. Final citation-context audit if citation contexts or bibliography entries
   change.
5. Clean Git status at a named submission tag.

## Archive Scope

The archive should include:

- root project-control files;
- source code, scripts, and tests;
- current paper source;
- figure/table source and lightweight manuscript-used outputs;
- registry and provenance/audit packages needed to interpret the claims;
- a manifest with SHA-256 hashes and the Git commit/tag.

The archive should exclude:

- local caches;
- temporary build directories;
- third-party PDFs without redistribution permission;
- bulky raw checkpoints unless required by the venue;
- process-only planning notes not needed for public reproducibility.

## Reviewer-Facing Language

Use language like:

```text
The current source is tracked in a public Git repository. Historical evidence
and source-snapshot boundaries are documented in the R047/R048 provenance
packages. A frozen source archive will be produced from the final submission
tag for institutional or venue retention.
```

Do not claim that R048 is the current Git history. It is the historical repair
record for the earlier invalid-Git workspace.
