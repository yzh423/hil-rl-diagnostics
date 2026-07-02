# R044 Manifest: Environment, Reproducibility, and Innovation Audit

Date: 2026-07-02

## Purpose

R044 records a project-environment and reproducibility audit for the current
cost-matched HIL-RL diagnostic-protocol route. It does not add a new
scientific result and should not be cited as method superiority evidence.

## Artifacts

| Artifact | Role |
|---|---|
| `PROJECT_ENVIRONMENT_REPRODUCIBILITY_AUDIT.md` | Main audit of local runtime, smoke readiness, evidence discipline, risks, and next gates. |
| `REPRODUCTION_COMMANDS.md` | Central command sheet for verification, smoke runs, and paper-core result reproduction planning. |
| `INNOVATION_AND_RIGOR_ROADMAP.md` | Near-term route for strengthening novelty while keeping claims honest. |
| `smoke_reacher/robosuite_hil_summary.csv` | Short Reacher fallback environment smoke output. Not paper evidence. |
| `smoke_reacher/run_Reacher_none_b4000_seed44.csv` | Per-evaluation CSV for the Reacher fallback smoke. Not paper evidence. |

## Claim Boundary

- This package supports project governance, reproducibility, and paper-planning
  discipline.
- It does not change the protected R021/R022/R023/R024 scientific verdicts.
- Smoke outputs here prove code-path viability only.
- Any new method or robotics-breadth evidence must be created under a later
  `results/r0xx_*` directory and registered separately.

## Verification Status

Fresh verification after R044 registry and index synchronization:

| Command | Result |
|---|---|
| `python scripts\validate_evidence_registry.py` | OK, `rows=33`, `sources=33`, `csv_sources=14`, `issues=0` |
| `python scripts\audit_registry_numbers.py` | OK, `rows=33`, `skipped=19`, `checks=76`, `issues=0` |
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
