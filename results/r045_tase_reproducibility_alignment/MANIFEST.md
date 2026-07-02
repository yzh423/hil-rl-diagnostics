# R045 Manifest: T-ASE Reproducibility Alignment

Date: 2026-07-02

## Purpose

R045 aligns the current manuscript with the R043/R044 route: an IEEE T-ASE-style
diagnostic protocol paper with clear practitioner value and a reproducibility
inventory. It does not add new experimental results, new citation keys, or a new
method-superiority claim.

## Artifacts

| Artifact | Role |
|---|---|
| `MANUSCRIPT_ALIGNMENT.md` | Summary of paper-facing edits and claim boundaries. |
| `paper/main.tex` | Adds a shorter automation-science title, a Note to Practitioners, and appendix inclusion. |
| `paper/sections/07_reproducibility_inventory.tex` | Adds a reproducibility inventory and compute/provenance status tables. |

## Claim Boundary

- R021 remains the decisive cost-matched reversal.
- R022 and R024 remain negative lightweight repair gates.
- R023 remains a trace diagnostic, not a primary success-rate result.
- The new appendix documents artifact and provenance status; it does not fill
  missing historical wall-time values retrospectively.

## Verification

Fresh verification after R045 registry/index synchronization:

| Command | Result |
|---|---|
| `python scripts\validate_evidence_registry.py` | OK, `rows=34`, `sources=34`, `csv_sources=14`, `issues=0` |
| `python scripts\audit_registry_numbers.py` | OK, `rows=34`, `skipped=20`, `checks=76`, `issues=0` |
| `python scripts\generate_claim_tables.py` | OK, wrote 5 registry-derived claim-table files |
| `python -m unittest discover -s tests` | OK, 72 tests |

The test run prints the known upstream Gym compatibility warning from
Stable-Baselines3 imports; it does not fail the suite.

Verification commands:

```powershell
python scripts\validate_evidence_registry.py
python scripts\audit_registry_numbers.py
python scripts\generate_claim_tables.py
python -m unittest discover -s tests
```
