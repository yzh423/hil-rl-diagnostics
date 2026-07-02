# R048 Version And Command Provenance Manifest

Date: 2026-07-02

## Purpose

R048 repairs the remaining reproducibility gap left by R047 by replacing the
invalid local Git provenance with an explicit source snapshot and by clarifying
R020/R021 command provenance. It does not rerun experiments, alter historical
CSV files, or change any paper-claim number.

## Artifacts

| Artifact | Role |
|---|---|
| `git_status_diagnostic.json` | Machine-readable record that `.git` is an empty local directory and Git commands cannot provide commit provenance. |
| `source_snapshot_r048.zip` | Deterministic current-source snapshot for code, tests, paper-control files, project-control files, R047 support files, and R048 machine-readable provenance tables. |
| `source_snapshot_manifest.csv` | File-level SHA-256 manifest for every file included in the source snapshot. |
| `source_snapshot_summary.json` | Archive hash, archive size, file count, and exclusion policy for the source snapshot. |
| `r020_r021_checkpoint_inventory.csv` | Checkpoint and repeated-evaluation source inventory for R020/R021, with checkpoint existence and SHA-256 hashes. |
| `r021_raw_run_inventory.csv` | R021 random_b350/random_b450 raw run summary inventory with stored hyperparameters, wall time, and checkpoint hashes. |
| `r020_r021_command_reconstruction.csv` | Recommended reproduction commands and explicit caveats for R020/R021 configurations. |
| `r048_artifact_hashes.csv` | SHA-256 hash ledger for the R048 package artifacts. |
| `VERSION_PROVENANCE_REPAIR.md` | Human-readable version-provenance verdict and source snapshot policy. |
| `R020_R021_COMMAND_PROVENANCE_NOTE.md` | Human-readable command-provenance and checkpoint-source note. |

## Claim Boundary

R048 supports reproducibility and artifact-review claims only. It can be used to
say that this workspace now has a deterministic source snapshot and a transparent
R020/R021 command-provenance note. It cannot be used to claim a new performance
result, a real Git commit hash, or a positive LV-VoI trigger.

## Current Status

- Local `.git` exists but is empty; Git commands return
  `fatal: not a git repository (or any of the parent directories): .git`.
- `source_snapshot_r048.zip` contains 156 current source/control/provenance
  files and has SHA-256
  `b4bed68cb8abbe8f8bdf1fa046993626139f3e129952bb1561b66c5f89c42358`.
- R020 original training launch commands remain unavailable. R020 is best
  represented as a 5x20 repeated-evaluation consolidation over earlier
  checkpoint sources.
- R021 random_b350 and random_b450 central command files are unavailable, but
  raw run summaries, per-seed run CSVs, repeated-evaluation summaries, and
  checkpoint files are present and hashed.
- R021 none/LV-VoI/random_b600 rows inherit R020 evidence.
- `r020_r021_checkpoint_inventory.csv` records 28 source-checkpoint rows, with
  zero missing checkpoint files.
- `r021_raw_run_inventory.csv` records 10 raw random-budget run rows, with zero
  missing checkpoint files.
- `r048_artifact_hashes.csv` records 10 R048 package artifacts.

## Verification

Run the repository verification menu after registry/index synchronization:

```powershell
python scripts\validate_evidence_registry.py
python scripts\audit_registry_numbers.py
python scripts\generate_claim_tables.py
python -m unittest discover -s tests
```

Observed result after R048 synchronization:

- R048 internal hash consistency: source snapshot files=156, package artifacts=10,
  issues=0.
- `python scripts\validate_evidence_registry.py`: OK, rows=36,
  sources=36, csv_sources=14, issues=0.
- `python scripts\audit_registry_numbers.py`: OK, rows=36, skipped=22,
  checks=76, issues=0.
- `python scripts\generate_claim_tables.py`: wrote five registry-derived claim
  table files.
- `python -m unittest discover -s tests`: OK, 72 tests.
