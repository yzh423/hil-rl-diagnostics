# R047 Evidence Provenance Audit

Date: 2026-07-02

## Verdict

R047 materially strengthens the evidence chain without changing the scientific
result boundary. All unique primary sources referenced by the current evidence
registry are present in the workspace and have SHA-256 hashes. The package also
hashes selected paper-core, figure/table, citation, planning, and project-control
artifacts so future edits can be separated from historical evidence.

The main remaining provenance risk is real and should be preserved honestly:
the local `.git` metadata is not recognized as a valid repository, so this
workspace cannot currently provide a reliable Git commit hash. Historical
R020/R021 command provenance is also incomplete; later command sheets and
driver command files help, but they should not be misrepresented as original
launch logs.

## What R047 Adds

| Evidence layer | Output | Status |
|---|---|---|
| Registry source existence | `registry_source_inventory.csv` | 26/26 unique registered primary sources present. |
| Source and artifact hashes | `artifact_hashes.csv` | 62 selected artifacts hashed; zero missing rows in the generated ledger. |
| Runtime snapshot | `environment_snapshot.json` | Python, OS, package versions, CUDA visibility, and Git failure state recorded. |
| Compute accounting | `available_compute_accounting.csv` | Best-effort scan complete; explicit wall time exists only where historical CSVs recorded it. |
| Command provenance | `command_provenance_inventory.csv` | Five archived command files found; R020/R021 central launch commands remain absent. |

## Registered Source Status

The registry source inventory contains 26 unique primary sources. Every listed
source exists locally. This covers experimental result rows and derived
paper-facing artifacts from the current R020-R047 route, excluding the voided
R046 wrong-project directory.

Because R047 is a derived audit package, it does not alter any historical raw
CSV. If a future artifact changes, rerun the hash inventory rather than editing
historical outputs.

## Environment Status

`environment_snapshot.json` records the local environment through lightweight
package metadata lookup to avoid heavy simulator imports. The snapshot records:

- Python 3.11.13 from Anaconda.
- Windows 10 platform string `Windows-10-10.0.26200-SP0`.
- `numpy==1.26.4`, `gymnasium==0.28.1`,
  `stable-baselines3==2.3.2`, `mujoco==3.3.0`,
  `robosuite==1.5.2`, `torch==2.4.0+cu124`, and
  `matplotlib==3.10.8`.
- CUDA is visible to PyTorch in this environment, with Torch CUDA version 12.4.
- Git provenance is invalid in this local checkout.

This is enough to support a reproducibility audit claim, but it is not enough
for submission-grade code provenance until a valid source snapshot or commit
identifier is added.

## Evidence Gaps To Keep Visible

- Invalid local Git metadata prevents a trustworthy commit-hash claim.
- R020 and R021 do not contain complete original launch command files in their
  result directories.
- Only three scanned paper-core CSVs expose explicit `wall_time_s`; most
  historical CSVs support result auditing but not complete wall-clock accounting.
- R046 remains voided as wrong-project material and must stay excluded from
  manuscript evidence and registry rows.

## Allowed Use

Use R047 for claims such as:

- The current evidence registry sources are present and hashable.
- The project now separates reproducibility provenance from performance claims.
- The remaining reproducibility risks are explicitly documented rather than
  hidden.

Do not use R047 to claim a method improvement, a new benchmark result, or a
positive LV-VoI trigger conclusion.
