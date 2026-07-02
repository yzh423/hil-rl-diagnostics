# FORESIGHT-HIL Manuscript Skeleton

This directory is the first manuscript skeleton for the current diagnostic
protocol paper route.

Entry point:

```bash
main.tex
```

Current policy:

- Keep `proposal/` as historical proposal material.
- Use this `paper/` directory for the current cost-matched diagnostic-protocol
  manuscript.
- Use only citation keys that are present in `references.bib` and traceable to
  `results/r027_citation_source_bank/`, `results/r037_citation_audit_batch1/`,
  or the current R042 audit files.
- The current PDF skeleton uses `sections/99_references.tex` so bundled Tectonic
  can compile without BibTeX. Keep `references.bib` synchronized with the manual
  bibliography and use `CITATION_AUDIT.md` as the current audit ledger.
- Treat the R029 hero figure and R036 registry-generated tables as preferred
  first-draft display assets.
- `paper/figures/` contains compile-local snapshots of those assets so bundled
  Tectonic can build the draft in untrusted mode.
- R042 audited the current citation contexts. Rerun citation audit whenever
  citation contexts or bibliography entries change materially.
- R045 adds the first T-ASE-style Note to Practitioners and the reproducibility
  appendix at `sections/07_reproducibility_inventory.tex`; it adds no new
  citation keys or experimental claims.
