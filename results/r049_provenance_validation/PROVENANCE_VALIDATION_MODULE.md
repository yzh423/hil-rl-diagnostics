# R049 Provenance Validation Module

Date: 2026-07-02

## Verdict

R049 strengthens the evidence framework by adding an executable validator for
the provenance packages built in R047 and R048. The validator separates two
questions that were previously easy to mix up:

1. Are the archived provenance packages internally self-consistent?
2. Does the current working tree still match historical source/hash snapshots?

The default mode answers the first question and is suitable for normal
verification. The optional drift mode answers the second question and is
expected to fail after new R0xx packages change project-control files.

## Interfaces

Reusable module:

```python
from foresight_hil.evaluation.provenance_validation import (
    validate_current_provenance,
    format_provenance_report,
)
```

CLI:

```powershell
python scripts\validate_provenance_package.py
python scripts\validate_provenance_package.py --compare-current-files
```

## Checks

The default current-provenance check validates:

- R047 registry-source inventory existence.
- R047 artifact-hash ledger existence, without treating later project-file
  edits as failures.
- R048 source snapshot archive/manifest self-consistency.
- R048 package artifact hashes.
- R048 R020/R021 checkpoint inventory hashes.
- R048 R021 raw-run checkpoint hashes.

The drift mode additionally compares historical source/hash ledgers against the
current working tree. It is useful before submission packaging, because it shows
whether a newer R0xx package should create a fresh source snapshot.

## Current Outcome

Default validation passes with 6 checks, 289 files, and 0 issues.

Drift mode currently reports 38 issues. The reported differences are from
project-control and provenance files updated after R047 plus source files
updated after the R048 source snapshot. This is evidence that the drift detector
works, not evidence that R047/R048 raw artifacts were corrupted.

## Use In The Verification Menu

Add the default CLI to paper-facing verification:

```powershell
python scripts\validate_provenance_package.py
```

Run drift mode only when deciding whether a fresh source snapshot is needed.
