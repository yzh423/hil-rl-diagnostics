# R058 Submission Packaging Review

Date: 2026-07-03

## Scope

This review executes the next packaging tasks identified after R057:

- diagnose/fix local PDF compilation;
- prepare PDF visual QA;
- decide how public Git, R047/R048 provenance, and a future source archive
  should relate;
- keep packaging and evidence boundaries explicit before further experiment
  optimization.

## Status Summary

| Gate | Status | Evidence |
|---|---|---|
| Local LaTeX/PDF compile | Complete with bundled Tectonic and project-local cache | `LATEX_RUNTIME_DIAGNOSTIC.md` |
| PDF visual QA | Complete for current draft | `PDF_VISUAL_QA.md` |
| Current source-state tracking | Ready through public Git | Current `main` is synced with `origin/main` at commit `761c7366d25483c0e0162f66b3ee955a9acb2778`. |
| Historical evidence provenance | Ready with known caveats | R047/R048/R049 remain the canonical provenance layer. |
| Institutional source archive | Recommended at final submission tag | `SOURCE_ARCHIVE_DECISION.md` |
| Evidence and experiment optimization | Ready as a gated plan, not as a new claim | R059 records the optimization route. |

## Packaging Rules For The Next Submission Pass

Track:

- source code under `foresight_hil/`, `scripts/`, and `tests/`;
- current paper source under `paper/`;
- registry-backed evidence documents and lightweight derived artifacts;
- generated figures/tables used by the manuscript;
- validation, provenance, citation-audit, and paper-claim-audit reports.

Do not track:

- local process notes;
- third-party PDFs unless redistribution rights are explicit;
- package caches and temporary build directories;
- raw checkpoints and bulky generated archives unless the submission package
  explicitly requires them;
- smoke outputs as evidence.

## Current Source-State Tracking

The current repository has a valid public remote:

```text
https://github.com/yzh423/hil-rl-diagnostics.git
```

Current checked commit at the time of this pass:

```text
761c7366d25483c0e0162f66b3ee955a9acb2778
```

This current Git repository should be used for ongoing source-state tracking.
R048 should remain in the paper package as the historical repair record for the
earlier invalid-Git workspace state and deterministic source snapshot.

## PDF Visual QA Result

The current draft compiles to
`results/r058_submission_packaging_readiness/main_compiled_r058.pdf`, and all
14 pages were rendered to PNG under
`results/r058_submission_packaging_readiness/pdf_visual_qa/`.

Visual QA confirms:

- Fig. 1 methodology asset is present and readable;
- Fig. 2 R054 attention-allocation diagnostic figure is present and readable;
- registry-generated tables fit within margins;
- the reproducibility appendix inventory is readable;
- references begin after appendix material;
- visible citation/reference link boxes are hidden;
- captions preserve the R021/R022/R023/R024 no-new-positive-claim boundary.

Remaining warnings are dense-table underfull/overfull box warnings and should
be treated as polish targets before venue-template submission, not as current
compile blockers.

## Boundary

R058 improves packaging discipline. It does not provide new empirical support
for any method claim.
