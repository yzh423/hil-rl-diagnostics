# R047 Evidence Provenance Package Manifest

Date: 2026-07-02

## Purpose

R047 strengthens the non-writing evidence layer for the current diagnostic
HIL-RL paper route. It inventories registered primary sources, hashes project
and result artifacts, records the local package/runtime state, and makes command
and compute-accounting gaps explicit.

This is not a new scientific experiment. It does not change raw result CSVs,
paper-claim numbers, or the protected interpretation that R021 `random_b350`
dominates LV-VoI scale3 under cost matching.

## Artifacts

| Artifact | Role |
|---|---|
| `registry_source_inventory.csv` | Unique primary sources referenced by the evidence registry, with existence and SHA-256 status. |
| `artifact_hashes.csv` | SHA-256 ledger for selected paper-core evidence, project-control, figure/table, and audit artifacts. |
| `available_compute_accounting.csv` | Best-effort scan of paper-core CSVs for available row counts, seeds, steps, evaluation episodes, and wall-time fields. |
| `command_provenance_inventory.csv` | Inventory of archived command files found under paper-core result directories. |
| `environment_snapshot.json` | Local Python/platform/package snapshot plus current Git-provenance failure state. |
| `EVIDENCE_PROVENANCE_AUDIT.md` | Human-readable audit verdict and claim boundaries. |
| `COMPUTE_AND_COMMAND_GAP_ANALYSIS.md` | Best-effort compute accounting plus command-provenance gap analysis. |
| `REVIEWER_REPRODUCIBILITY_CHECKLIST.md` | Checklist for future manuscript, rebuttal, or artifact-review use. |

## Machine-Readable Summary

- Registry primary-source inventory rows: 26.
- Missing registered primary sources: 0.
- Artifact hash rows: 62.
- Available compute-accounting CSV rows: 82.
- CSVs with explicit `wall_time_s`: 3.
- Explicit `wall_time_s` total available from those CSVs: 8947.8 seconds.
- Archived command files found: 5.
- Local Git provenance: invalid in this workspace; `git rev-parse` returns
  `fatal: not a git repository (or any of the parent directories): .git`.

## Claim Boundary

R047 supports reproducibility and evidence discipline claims only. It can be
used to say that the project now has a source/hash/compute/command provenance
package with explicit gaps. It cannot be used to claim a new success rate, a new
trigger advantage, or a fixed LV-VoI method.

## Verification

Final verification was run after the R047 registry and index synchronization:

```powershell
python scripts\validate_evidence_registry.py
python scripts\audit_registry_numbers.py
python scripts\generate_claim_tables.py
python -m unittest discover -s tests
```

The final verification result for this package is recorded in the session
summary after these commands complete.

Observed result:

- `python scripts\validate_evidence_registry.py`: OK, rows=35,
  sources=35, csv_sources=14, issues=0.
- `python scripts\audit_registry_numbers.py`: OK, rows=35, skipped=21,
  checks=76, issues=0.
- `python scripts\generate_claim_tables.py`: wrote five registry-derived claim
  table files.
- `python -m unittest discover -s tests`: OK, 72 tests.
