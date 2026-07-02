# R037 Citation Metadata/Context Audit Batch 1

Date: 2026-07-02

Purpose: finish the first authoritative check of the R027 candidate citations
needed before drafting the SCI-Q1-oriented diagnostic-protocol manuscript.

## Scope

This is a source-bank audit, not the final submission citation audit. There is
not yet a manuscript `.tex` file with real `\cite{...}` contexts, so the final
per-citation context audit remains deferred.

Audited files:

- `results/r027_citation_source_bank/citation_support_bank.csv`
- `results/r027_citation_source_bank/bibtex_candidates_to_add.bib`
- `proposal/references.bib` only as the existing main bibliography baseline

## Batch Verdict

| Cite key | Verdict | Metadata | Context use | Action |
|---|---|---|---|---|
| `haarnoja2018sac` | KEEP | Verified via PMLR ICML 2018 | Use as primary SAC algorithm citation. | Added to candidate pool. |
| `sac2018applications` | KEEP | Verified via arXiv 1812.05905 | Use as optional SAC applications/robotics stability citation. | Kept as secondary, not primary SAC venue. |
| `robosuite2020` | KEEP | Verified via arXiv 2009.12293 | Use for robosuite/Lift/Stack simulator substrate. | Candidate ready, with v3-2025 note. |
| `henderson2018deeprlmatters` | FIX_APPLIED | Verified via official AAAI proceedings DOI. | Use for reproducibility, variance, and reporting discipline. | Candidate upgraded from arXiv-only to AAAI metadata. |
| `agarwal2021statisticalprecipice` | KEEP_WITH_CAUTION | arXiv title/authors verified; NeurIPS comment present. | Use for few-run RL uncertainty, interval estimates, and robust aggregate reporting. | Keep as arXiv until official NeurIPS proceedings URL is resolved. |
| `wilson1927score` | KEEP | Verified via CrossRef DOI. | Use narrowly for Wilson/binomial-proportion confidence interval formula. | Candidate ready. |

## Source Notes

- PMLR verifies the original SAC paper as ICML 2018, PMLR 80:1861--1870.
- arXiv verifies SAC Algorithms and Applications as arXiv:1812.05905 and
  provides the arXiv DOI `10.48550/arXiv.1812.05905`.
- arXiv verifies robosuite as arXiv:2009.12293, with v3 revised in 2025.
- AAAI verifies Henderson et al. as Proceedings of AAAI, volume 32, issue 1,
  published 2018-04-29, DOI `10.1609/aaai.v32i1.11694`.
- arXiv verifies Agarwal et al. as arXiv:2108.13264 and states the NeurIPS
  2021 Outstanding Paper note. The automated official proceedings lookup did
  not resolve the canonical URL in this pass, so the candidate remains cited as
  arXiv rather than a fabricated proceedings entry.
- CrossRef verifies Wilson 1927 as Journal of the American Statistical
  Association 22(158):209--212, DOI `10.1080/01621459.1927.10502953`.

## Policy Decision

Do not merge these candidates into `proposal/references.bib` until the first
manuscript skeleton exists and the target journal family is chosen. At that
point, add only the keys actually cited by the draft and run the full
citation-audit pass over real citation contexts.

## Remaining Citation Risks

- Many existing main-bib entries are valid but still have recommended-field
  warnings, mostly arXiv-only or proceedings entries without pages/DOIs.
- `agarwal2021statisticalprecipice` should be upgraded to a canonical NeurIPS
  proceedings record if the official URL is found later.
- 2025/2026 HIL-RL competitors should remain latest-context references, not the
  backbone of the paper's novelty claim.

## Next Candidate

R038 should build a minimal manuscript skeleton that imports R029/R036 assets
and uses only R027/R037-supported citation keys. The full final
`citation-audit` should wait until that skeleton contains real `\cite{...}`
contexts.
