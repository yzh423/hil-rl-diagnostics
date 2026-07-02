# R027 Citation Source Bank Manifest

Date: 2026-07-01

Purpose: prepare citation support for the diagnostic-benchmark manuscript before
drafting Introduction, Related Work, Method/Setup, and Evaluation Protocol.

## Files

| File | Purpose |
|---|---|
| `citation_support_bank.csv` | Claim-to-source map for paper sections. |
| `bibtex_candidates_to_add.bib` | Candidate BibTeX entries not yet merged into `proposal/references.bib`. |
| `citation_audit_local.md` | Local BibTeX validation summary and unresolved audit actions. |
| `../r027_citation_validation_pre.json` | Raw validation output from the citation-management validator. |
| `../r037_citation_audit_batch1/` | First authoritative metadata/context-use audit of candidate additions. |

## Policy

Do not merge candidate BibTeX entries into the main bibliography until each has
been checked against an authoritative source. For the first manuscript draft,
prefer stable published or widely indexed sources over 2026 arXiv / under-review
items unless the claim specifically concerns the latest competing systems.

R037 completed the first authoritative check of the candidate additions and
kept them staged rather than merged into `proposal/references.bib`.
