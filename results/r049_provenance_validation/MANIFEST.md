# R049 Provenance Validation Manifest

Date: 2026-07-02

## Purpose

R049 turns the R047/R048 provenance work into an executable validation gate. It
adds a reusable validation module, a CLI command, tests, and archived command
outputs showing both archival self-consistency and current working-tree drift
diagnosis.

This is not a new experiment. It does not change raw result CSVs, success
rates, cost numbers, citation keys, or the protected R021/R022/R024 scientific
interpretation.

## Code Artifacts

| Artifact | Role |
|---|---|
| `foresight_hil/evaluation/provenance_validation.py` | Reusable validators for hash ledgers, registry-source inventories, source snapshots, and checkpoint inventories. |
| `scripts/validate_provenance_package.py` | CLI for validating current R047/R048 provenance packages. |
| `tests/test_provenance_validation.py` | Unit tests for hash ledger, source snapshot, checkpoint inventory, and report formatting behavior. |

## Evidence Artifacts

| Artifact | Role |
|---|---|
| `default_validation_output.txt` | Output from archival self-consistency validation. |
| `drift_diagnostic_output.txt` | Output from `--compare-current-files`, showing expected drift after R048/R049 changed project-control files and source modules. |
| `PROVENANCE_VALIDATION_MODULE.md` | Human-readable explanation of validator modes and claim boundaries. |
| `r049_artifact_hashes.csv` | SHA-256 ledger for R049 code and evidence artifacts. |

## Validation Result

Default command:

```powershell
python scripts\validate_provenance_package.py
```

Observed output:

```text
[provenance] OK checks=6 files=289 issues=0
[provenance] root=.
```

Drift-diagnostic command:

```powershell
python scripts\validate_provenance_package.py --compare-current-files
```

Observed output reports 38 issues. These are expected drift signals from comparing
historical R047/R048 ledgers against the current post-R048 working tree. They
are recorded in `drift_diagnostic_output.txt` and should not be interpreted as
new experimental evidence.

## Claim Boundary

Use R049 to claim that provenance validation is now automated and covered by
tests. Do not use it to claim a new algorithmic result, a valid Git commit, or a
fixed LV-VoI trigger.
