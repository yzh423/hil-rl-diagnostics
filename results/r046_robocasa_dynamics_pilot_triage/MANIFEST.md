# R046 Manifest: RoboCasa Dynamics Pilot Triage

Date: 2026-07-02

## VOID Status

This package is void for the current FORESIGHT-HIL project. The user clarified
that the reported RoboCasa/MorphTAMP benchmark belonged to another project.
R046 has therefore been removed from the evidence registry and project indexes.
The files remain only as a correction trace.

## Purpose

This package should not be used. Its original purpose was to record a
user-reported external RoboCasa/MorphTAMP dynamics benchmark result and turn it
into a diagnostic plan, but that input was later identified as belonging to a
different project.

## Artifacts

| Artifact | Role |
|---|---|
| `USER_REPORTED_RUN.md` | Exact command and pasted terminal output from the external run. |
| `DIAGNOSTIC_PLAN.md` | Root-cause hypotheses, analysis commands, and next minimal benchmark slices. |
| `VOID_NOTICE.md` | Correction notice explaining that this package is excluded from FORESIGHT-HIL evidence. |

## Claim Boundary

- Do not cite this as a paper result.
- Do not treat `success=5/90` as FORESIGHT-HIL evidence.
- Do not use this package to guide the current manuscript.

## Verification

Historical verification before the user correction:

| Command | Result |
|---|---|
| `python scripts\validate_evidence_registry.py` | OK, `rows=35`, `sources=35`, `csv_sources=14`, `issues=0` |
| `python scripts\audit_registry_numbers.py` | OK, `rows=35`, `skipped=21`, `checks=76`, `issues=0` |
| `python scripts\generate_claim_tables.py` | OK, wrote 5 registry-derived claim-table files |
| `python -m unittest discover -s tests` | OK, 72 tests |

R046 is now excluded from registry validation because the registry row was
removed after the correction.
