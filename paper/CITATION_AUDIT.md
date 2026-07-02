# Citation Audit Report

**Date**: 2026-07-02
**Bib file**: `references.bib`
**Cited entries audited**: 15
**Overall verdict after fixes**: PASS

## Summary

| Finding type | Count | Status |
|---|---:|---|
| Context-supported cited entries | 15 | PASS |
| Metadata fixes applied | 6 | FIXED |
| Wrong-context citations | 0 | PASS |
| Missing cited keys | 0 | PASS |
| Hallucinated/nonexistent entries after fixes | 0 | PASS |

This audit checked every current `\cite{...}` occurrence in `paper/sections/*.tex`
against `paper/references.bib` and fresh web/source lookups. The audit found no
wrong-context citations, but it did find metadata drift in several entries. The
metadata fixes were applied directly to `paper/references.bib` and the manual
bibliography in `paper/sections/99_references.tex`.

## Applied Metadata Fixes

### `luo2025hilserl`

- **Issue**: The BibTeX entry claimed a Science Robotics publication and DOI
  that were not verified by the web lookup or the local PDF first page.
- **Action**: Replaced the entry with arXiv metadata for `arXiv:2410.21845`.
- **Context verdict**: KEEP. The citation supports claims about HIL-RL systems
  combining demonstrations, human corrections, and off-policy RL for robotic
  manipulation.

### `ball2023rlpd`

- **Issue**: Metadata lacked PMLR volume/series/publisher details.
- **Action**: Updated to the PMLR ICML 2023 record, volume 202, pages
  1577--1594.
- **Context verdict**: KEEP. The citation supports using offline data with
  online off-policy RL.

### `mandlekar2021robomimic`

- **Issue**: Entry used CoRL 2021 placeholder-style metadata.
- **Action**: Updated to the PMLR CoRL proceedings record: volume 164, pages
  1678--1690, year 2022.
- **Context verdict**: KEEP. The citation supports claims about robot
  manipulation from offline human demonstrations and robomimic-style
  demonstration infrastructure.

### `hoque2021thrifty`

- **Issue**: Entry used CoRL 2021 placeholder-style metadata.
- **Action**: Updated to the PMLR CoRL proceedings record: volume 164, pages
  598--608, year 2022.
- **Context verdict**: KEEP. The citation supports budget-aware novelty/risk
  gating for interactive imitation learning.

### `cai2025aim`

- **Issue**: Entry claimed PMLR 267 pages 6243--6256, but that PMLR page is a
  different paper. The verifiable AIM record is `arXiv:2506.09176`, with an
  arXiv note that it was an ICML 2025 Poster.
- **Action**: Replaced the proceedings entry with arXiv metadata.
- **Context verdict**: KEEP. The citation supports adaptive robot-gated
  intervention mechanisms and reduced take-over cost.

### `guo2017calibration`

- **Issue**: Metadata lacked PMLR volume/pages/publisher.
- **Action**: Updated to PMLR volume 70, pages 1321--1330.
- **Context verdict**: KEEP. The citation supports the statement that modern
  neural-network confidence estimates can be miscalibrated.

## Per-Entry Context Verdicts

| Key | Existence / metadata source | Context verdict | Notes |
|---|---|---|---|
| `luo2025hilserl` | arXiv:2410.21845 | KEEP | Supports HIL-SERL-style real-robot HIL-RL with demonstrations, corrections, and efficient RL. |
| `retzlaff2024hitl` | JAIR 79, DOI 10.1613/jair.1.15348 | KEEP | Supports broad HITL-RL framing and human involvement across phases. |
| `ball2023rlpd` | PMLR 202:1577--1594 | KEEP | Supports offline data mixed with online off-policy RL. |
| `mandlekar2021robomimic` | PMLR 164:1678--1690 | KEEP | Supports learning from offline human demonstrations for robot manipulation. |
| `hoque2021thrifty` | PMLR 164:598--608 | KEEP | Supports budget-aware novelty/risk expert-query gating. |
| `cai2025aim` | arXiv:2506.09176 | KEEP | Supports robot-gated adaptive intervention and take-over cost reduction claims. |
| `chua2018pets` | NeurIPS 2018 proceedings | KEEP | Supports uncertainty-aware probabilistic dynamics models. |
| `janner2019mbpo` | NeurIPS 2019 proceedings | KEEP | Supports short model rollouts and model-trust framing. |
| `guo2017calibration` | PMLR 70:1321--1330 | KEEP | Supports neural-network calibration/miscalibration context. |
| `haarnoja2018sac` | PMLR 80:1861--1870 | KEEP | Supports SAC as an off-policy maximum-entropy actor-critic algorithm. |
| `sac2018applications` | arXiv:1812.05905 | KEEP | Supports SAC applications and stability/robotics-oriented SAC context. |
| `robosuite2020` | arXiv:2009.12293 | KEEP | Supports robosuite as the simulator/framework substrate. |
| `henderson2018deeprlmatters` | AAAI 2018 proceedings, DOI 10.1609/aaai.v32i1.11694 | KEEP | Supports RL reproducibility and reporting-discipline concerns. |
| `agarwal2021statisticalprecipice` | arXiv:2108.13264 | KEEP | Supports uncertainty in few-run deep RL evaluation and interval reporting. |
| `wilson1927score` | JASA 22(158):209--212, DOI 10.1080/01621459.1927.10502953 | KEEP | Supports Wilson/binomial-proportion interval use. |

## Verified Source URLs

| Key | URL |
|---|---|
| `luo2025hilserl` | <https://arxiv.org/abs/2410.21845> |
| `retzlaff2024hitl` | <https://www.jair.org/index.php/jair/article/view/15348> |
| `ball2023rlpd` | <https://proceedings.mlr.press/v202/ball23a.html> |
| `mandlekar2021robomimic` | <https://proceedings.mlr.press/v164/mandlekar22a.html> |
| `hoque2021thrifty` | <https://proceedings.mlr.press/v164/hoque22a.html> |
| `cai2025aim` | <https://arxiv.org/abs/2506.09176> |
| `chua2018pets` | <https://papers.nips.cc/paper_files/paper/2018/hash/3de568f8597b94bda53149c7d7f5958c-Abstract.html> |
| `janner2019mbpo` | <https://papers.nips.cc/paper_files/paper/2019/hash/5faf461eff3099671ad63c6f3f094f7f-Abstract.html> |
| `guo2017calibration` | <https://proceedings.mlr.press/v70/guo17a.html> |
| `haarnoja2018sac` | <https://proceedings.mlr.press/v80/haarnoja18b.html> |
| `sac2018applications` | <https://arxiv.org/abs/1812.05905> |
| `robosuite2020` | <https://arxiv.org/abs/2009.12293> |
| `henderson2018deeprlmatters` | <https://ojs.aaai.org/index.php/AAAI/article/view/11694> |
| `agarwal2021statisticalprecipice` | <https://arxiv.org/abs/2108.13264> |
| `wilson1927score` | R037 CrossRef-verified DOI: <https://doi.org/10.1080/01621459.1927.10502953> |

## Source Notes

- The final manuscript should not cite `luo2025hilserl` as Science Robotics
  unless a canonical Science/DOI page is verified later.
- `cai2025aim` should remain arXiv metadata until an official ICML/OpenReview
  proceedings record is located; the previous PMLR page pointed to a different
  paper.
- The cite keys `mandlekar2021robomimic` and `hoque2021thrifty` were kept for
  continuity, even though the corrected metadata year is 2022.

## Next Actions

No citation-context rewrite is required after this audit. Before final
submission, choose the target journal family and format references consistently
for that venue.
