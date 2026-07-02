# R048 Version Provenance Repair

Date: 2026-07-02

## Verdict

The local Git state is not recoverable as a commit identifier inside this
workspace: `.git` exists as an empty directory, and `git rev-parse`, `git
status`, and `git log` all fail with `fatal: not a git repository (or any of the
parent directories): .git`.

R048 therefore uses a deterministic source snapshot as the current
submission-facing replacement for Git provenance. This does not pretend to be
repository history. It records exactly what source, paper-control, test, and
provenance files were present at this point in the project.

## What Is Repaired

- The project now has an explicit source snapshot archive:
  `source_snapshot_r048.zip`.
- Every included file has a SHA-256 row in `source_snapshot_manifest.csv`.
- The archive itself is hashed in `source_snapshot_summary.json`.
- The Git failure state is preserved in `git_status_diagnostic.json`.

Current archive details:

- Included files: 156.
- Archive size: 766287 bytes.
- Archive SHA-256:
  `b4bed68cb8abbe8f8bdf1fa046993626139f3e129952bb1561b66c5f89c42358`.

## What Is Not Repaired

- R048 does not recreate missing Git history.
- R048 does not prove when older experiments were originally launched.
- R048 does not make R020/R021 central command files appear where they were not
  archived.
- R048 does not change any experimental result.

## Snapshot Scope

The snapshot is intentionally a current-source and paper-control snapshot, not a
full raw-results archive. It includes:

- Root project-control files such as `README.md`, `AGENTS.md`, `CONTEXT.md`,
  `PROJECT_DASHBOARD.md`, `PROJECT_STRUCTURE.md`, and `PAPER_PLAN.md`.
- Core Python source under `foresight_hil/`.
- Experiment and evaluation scripts under `scripts/`.
- Regression tests under `tests/`.
- Current paper source under `paper/`.
- Figure/table source and lightweight figure/table artifacts under `figures/`.
- Evidence registry and human-readable result indexes.
- R047 provenance documents and R048 machine-readable provenance tables needed
  to interpret the source state. R048 narrative documents live beside the
  archive to avoid a self-referential archive hash.

It excludes heavyweight or historical raw result archives, checkpoints outside
the focused R020/R021 provenance inventories, local caches, invalid `.git`
metadata, and R048 narrative docs that record the archive hash. R047 remains
the source/hash/compute ledger for registered evidence artifacts; R048 is the
current-source snapshot that can travel with a submission or artifact review.

## Reviewer-Facing Language

Use cautious language:

> Because the local Git metadata was unavailable in this working copy, we
> provide a deterministic source snapshot archive with per-file and archive
> SHA-256 hashes, plus a separate evidence-source hash ledger.

Do not write that the paper has a valid Git commit hash unless a future step
creates one from a valid repository.
