# R027 Local Citation Audit

Date: 2026-07-01

## Scope

Audited local bibliography pool:

- `proposal/references.bib`

This is a local pre-audit, not the final citation audit. It validates structure
and identifies missing citation support before manuscript drafting. Final audit
still needs per-entry authoritative metadata checks and context checks after the
LaTeX draft contains real `\cite{...}` calls.

## Local Validation Result

Command:

```powershell
python C:\Users\14228\.codex\skills\citation-management\scripts\validate_citations.py proposal\references.bib --venue neurips --report results\r027_citation_validation_pre.json --verbose
```

Observed output:

- Total entries: 74
- Valid entries: 74
- Errors: 0
- Duplicate entries: 0
- Warnings: 114

Most warnings are recommended-field gaps, especially missing DOI/pages/volume
for arXiv preprints or conference papers. This does not block drafting, but it
does mean final submission should either upgrade preprints to final venue
records or explicitly cite them as preprints.

## Highest-Priority Citation Gaps

| Gap | Current state | Action |
|---|---|---|
| SAC backbone | Not explicit enough in main BibTeX | Add audited SAC citation. |
| robosuite simulator | Not explicit enough in main BibTeX | Add audited robosuite citation. |
| Deep RL evaluation reliability | Missing from current BibTeX | Add Henderson et al. and Agarwal et al. after metadata audit. |
| Wilson confidence intervals | Mentioned in README/PAPER_PLAN but not in BibTeX | Add Wilson 1927 or cite statistical package/method if preferred. |
| 2025/2026 HIL-RL competitors | Many are arXiv/under-review | Use as latest-context only; rely on stable sources for core claims. |

## Candidate Additions

See `bibtex_candidates_to_add.bib`. These are intentionally not merged into
`proposal/references.bib` yet.

R037 update (2026-07-02):

- Added `haarnoja2018sac` as the preferred primary SAC citation from ICML/PMLR
  2018.
- Kept `sac2018applications` as a secondary arXiv companion citation for SAC
  applications and robotics stability, not as the main SAC venue.
- Added arXiv DOIs for SAC applications and robosuite.
- Upgraded `henderson2018deeprlmatters` to official AAAI DOI metadata.
- Verified `wilson1927score` through CrossRef DOI metadata.
- Kept `agarwal2021statisticalprecipice` as arXiv-verified with a caution:
  title/authors and NeurIPS note are verified on arXiv, but the canonical
  NeurIPS proceedings URL was not resolved in this pass.

Post-R037 candidate validation:

- Total candidate entries: 6
- Valid entries: 6
- Errors: 0
- Duplicate entries: 0
- Warnings: 7, all recommended-field gaps for arXiv or proceedings records
  without non-fabricated pages/volumes.

Detailed R037 ledger:

- `results/r037_citation_audit_batch1/CITATION_METADATA_CONTEXT_AUDIT.md`
- `results/r037_citation_audit_batch1/candidate_metadata_context_audit.csv`
- `results/r037_citation_audit_batch1/candidate_validation_after.json`

## Drafting Rule

When writing the first manuscript sections, every literature claim should map to
one row in `citation_support_bank.csv`. If a claim needs a source not listed
there, add it to the source bank first and mark whether it is already in
`proposal/references.bib` or still a candidate.

Do not run the final `citation-audit` until a manuscript skeleton contains real
`\cite{...}` contexts.
