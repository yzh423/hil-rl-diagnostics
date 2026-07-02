# R047 Reviewer Reproducibility Checklist

Use this checklist before submission, rebuttal, or artifact-review packaging.

## Evidence Registry

- Run `python scripts\validate_evidence_registry.py`.
- Run `python scripts\audit_registry_numbers.py`.
- Regenerate registry-derived tables with
  `python scripts\generate_claim_tables.py`.
- Confirm R046 remains voided and absent from
  `results/EXPERIMENT_EVIDENCE_REGISTRY.csv`.
- Confirm R047 is described as evidence provenance, not a new experiment.

## Source And Artifact Integrity

- Inspect `registry_source_inventory.csv` and confirm all `exists` values are
  true.
- Inspect `artifact_hashes.csv` before and after any major paper-facing edit.
- If any primary source changes intentionally, create a new R0xx derived package
  rather than rewriting historical evidence.

## Environment And Version Provenance

- Inspect `environment_snapshot.json`.
- Replace the current invalid Git state with a valid commit hash, source
  archive hash, or institutional artifact snapshot before submission.
- Keep the package version capture lightweight unless a simulator smoke test is
  explicitly required.

## Compute And Commands

- Use `available_compute_accounting.csv` only as best-effort historical
  accounting.
- Do not claim full wall-clock cost from R020-R024; only three scanned CSVs
  expose explicit `wall_time_s`.
- Use archived command files for R023/R024 where present.
- State that R020/R021 original launch-command provenance is incomplete.

## Scientific Boundary

- Preserve the protected claim: R021 `random_b350` dominates LV-VoI scale3 under
  cost matching.
- Preserve the negative repair result: R022 and R024 remain dominated.
- Treat R023 traces as diagnosis, not a reversal of R021.
- Be explicit that the current experiments use a scripted privileged-state
  oracle, not a real teleoperator.
