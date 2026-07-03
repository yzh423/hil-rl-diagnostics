# R051 Citation Context Audit

Date: 2026-07-03

## Summary

R051 reran the citation-context audit after R050 deepened the manuscript theme
from trigger diagnostics to human-attention allocation diagnostics. The audit
checked all 15 current citation keys and all current `\cite{...}` contexts.

Verdict: PASS.

- Cited entries audited: 15.
- Wrong-context citations found: 0.
- Missing cited keys found: 0.
- Bibliography metadata changes in this run: 0.
- BibTeX validation: 15 valid entries, 0 errors, 13 recommended-field warnings.

## R050 Theme Check

The new phrase "human-attention allocation" is a manuscript framing term, not a
claim that a single cited paper coined that phrase. The framing is supported
across the existing source set:

- `retzlaff2024hitl` supports broad HITL-RL workflow involvement across
  development, learning, evaluation, and deployment.
- `hoque2021thrifty` supports budget-aware querying/intervention and human
  supervisor burden in robot learning.
- `cai2025aim` supports adaptive robot-gated intervention, reduced monitoring
  effort, and take-over cost.
- `luo2025hilserl` supports HIL-RL robot manipulation systems that combine
  demonstrations, human corrections, and efficient RL.

No sentence currently attributes the full R050 framing to one source alone.

## Outputs

- `paper/CITATION_AUDIT.md`
- `paper/CITATION_AUDIT.json`
- `paper/.aris/citation-audit/contexts.txt`
- `paper/.aris/traces/citation-audit/2026-07-03_run01/manual_audit_trace.md`
- `results/r051_citation_context_audit/paper_references_validation_after_r051.json`

## Source URL Ledger

| Key | Source |
|---|---|
| `luo2025hilserl` | <https://arxiv.org/abs/2410.21845> |
| `retzlaff2024hitl` | <https://www.jair.org/index.php/jair/article/view/15348> |
| `ball2023rlpd` | <https://proceedings.mlr.press/v202/ball23a.html> |
| `mandlekar2021robomimic` | <https://proceedings.mlr.press/v164/mandlekar22a.html> |
| `hoque2021thrifty` | <https://proceedings.mlr.press/v164/hoque22a.html> |
| `cai2025aim` | <https://arxiv.org/abs/2506.09176> |
| `chua2018pets` | <https://arxiv.org/abs/1805.12114> |
| `janner2019mbpo` | <https://papers.nips.cc/paper_files/paper/2019/hash/5faf461eff3099671ad63c6f3f094f7f-Abstract.html> |
| `guo2017calibration` | <https://proceedings.mlr.press/v70/guo17a.html> |
| `haarnoja2018sac` | <https://proceedings.mlr.press/v80/haarnoja18b.html> |
| `sac2018applications` | <https://arxiv.org/abs/1812.05905> |
| `robosuite2020` | <https://arxiv.org/abs/2009.12293> |
| `henderson2018deeprlmatters` | <https://ojs.aaai.org/index.php/AAAI/article/view/11694> |
| `agarwal2021statisticalprecipice` | <https://arxiv.org/abs/2108.13264> |
| `wilson1927score` | <https://doi.org/10.1080/01621459.1927.10502953> |

## Boundary

This audit did not add literature, change BibTeX, edit manuscript claims, or
modify experimental evidence. It only verifies that the R050 manuscript wording
still uses the existing citations in supported contexts.
