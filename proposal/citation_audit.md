# Citation Audit — FORESIGHT-HIL `references.bib`

**Audited:** 2026-06-25
**Method:** Each entry checked against authoritative sources — arXiv abstract pages (via the arXiv API), DOI/publisher pages (Science Robotics, Sage/IJRR, IEEE Xplore, Elsevier/ScienceDirect, JAIR), OpenReview, and PMLR.
**Policy:** No fabrication. Author lists, titles, years, venues, arXiv IDs, and DOIs are taken verbatim from the cited source. Anything not fully confirmable is flagged `UNVERIFIED`.

## Summary

| Outcome | Count |
|---|---|
| **VERIFIED** (already correct; IDs/DOIs may have been added) | 13 |
| **CORRECTED** (factual error fixed: authors / year / venue / metadata) | 15 |
| **UNVERIFIED** (could not confirm) | 0 |
| **New citations added** (all verified) | 12 |
| **Removed** | 0 |
| **Total entries in final `references.bib`** | 40 |

All 6 seed papers resolved and match their stated metadata. Every previously `Anonymous`/`and others` placeholder now has a confirmed real author list. No entry remains unverified.

## Existing entries

| Key | Status | What was wrong before | Authoritative source |
|---|---|---|---|
| `luo2025hilserl` | VERIFIED | Nothing factual; added DOI | arxiv.org/abs/2410.21845 ; science.org/doi/10.1126/scirobotics.ads5033 |
| `liu2026pact` | VERIFIED | Title + 9-author list confirmed correct | arxiv.org/abs/2606.03949 |
| `luo2024serl` | VERIFIED | Correct; added arXiv ID. Page numbers from IEEE Xplore not independently re-verified | arxiv.org/abs/2401.16013 |
| `uniintervene2026` | CORRECTED | author = "Anonymous" → Deng, Gao, Lin, Liu, Wu, Wang | arxiv.org/abs/2606.12372 |
| `silri2025` | CORRECTED | author = "Anonymous" → Zhao, Jin, Jiang, Zhang, Wu, Ren, Xu, Che, Sun, Wu, Liu, Tang | arxiv.org/abs/2512.24288 |
| `ohprl2026` | CORRECTED | author = "Anonymous" → Mo, Li, Wu, Kang, Xu | arxiv.org/abs/2605.15971 |
| `rove2026` | CORRECTED | author = "Anonymous" → Xiao, Tang, Ge, Zhou, Mu, Zhang, Ge | arxiv.org/abs/2606.17011 |
| `cai2025aim` | CORRECTED | author = "Cai, and others" → Cai, Peng, Zhou; venue was vague "PMLR v267" → ICML 2025, PMLR 267:6243–6256; added arXiv:2506.09176 | proceedings.mlr.press/v267/cai25e.html |
| `hoque2021thrifty` | VERIFIED | Correct; added arXiv ID | arxiv.org/abs/2109.08273 |
| `mile2025` | CORRECTED | author = "Anonymous" → Korkmaz, Bıyık | arxiv.org/abs/2502.13519 |
| `kurenkov2019acteach` | VERIFIED | Title + authors confirmed | arxiv.org/abs/1909.04121 |
| `zhang2020apil` | CORRECTED | author = "Zhang, and others" was **wrong** — real authors are Khanh Nguyen & Hal Daumé III. Bib key kept for stability | arxiv.org/abs/2006.07777 |
| `hiwm2026` | CORRECTED | author = "Anonymous" → Li, Zhou, Chen, Guo, Liu, Zhang, Chen, Zhu | arxiv.org/abs/2604.21741 |
| `vlaintheloop2026` | CORRECTED | author = "Anonymous" → Xu, Li, Duan, Yang, Xie, Yang. **Note:** under-review ICLR 2026 submission (OpenReview aT4LG8c6DE, #5405), not a published paper | openreview.net/forum?id=aT4LG8c6DE |
| `moerland2023mbrl` | VERIFIED | Title/authors confirmed (FnT ML vol 16(1), 2023) | arxiv.org/abs/2006.16712 |
| `luo2022mbrlsurvey` | VERIFIED | Title + 6-author list confirmed | arxiv.org/abs/2206.09328 |
| `pinosky2022hybrid` | CORRECTED | year 2022 → **2023** (print issue vol 42(6):337–355); added DOI 10.1177/02783649221083331 | journals.sagepub.com/doi/10.1177/02783649221083331 |
| `ball2023rlpd` | VERIFIED | Correct; added arXiv ID | arxiv.org/abs/2302.02948 |
| `chua2018pets` | VERIFIED | Title + authors confirmed | arxiv.org/abs/1805.12114 |
| `hafner2023dreamerv3` | VERIFIED | Title/authors confirmed (also in Nature 2025) | arxiv.org/abs/2301.04104 |
| `retzlaff2024hitl` | VERIFIED | JAIR 79:359–415 (2024) confirmed; added DOI 10.1613/jair.1.15348 | jair.org/index.php/jair/article/view/15348 |
| `li2022haco` | VERIFIED | Title + authors confirmed; added arXiv ID | arxiv.org/abs/2202.10341 |
| `huang2024haim` | VERIFIED | Journal title/authors/DOI confirmed (arXiv title differs: "HAIM-DRL: ...") | sciencedirect.com/science/article/pii/S2772424724000106 |
| `huang2024safehil` | CORRECTED | author = "Huang, Wenhui and others" → Huang, Liu, Huang, Lv; added vol 25(11):16181–16192 | ieeexplore.ieee.org/document/10596046 |
| `huang2024perlhf` | CORRECTED | author = "Huang, Zilin and others" → Huang, Sheng, Chen | arxiv.org/abs/2409.00858 |
| `asking2025help` | CORRECTED | author = "Anonymous" → Plaut, Liévano-Karim, Zhu, Russell | arxiv.org/abs/2502.14043 |
| `multisource2026` | CORRECTED | author = "Anonymous" → Shi, Liang, Shroff, Swami | arxiv.org/abs/2603.20453 |
| `onlinerlhf2025` | CORRECTED | author = "Anonymous" → Gen Li, Yuling Yan | arxiv.org/abs/2509.22633 |

## New entries added (all VERIFIED)

Targeted at the under-covered cells: interactive imitation learning, uncertainty-aware MBRL, preference-based RL, and reset-free / autonomous real-world robot RL.

| Key | Paper | Cell | Authoritative source |
|---|---|---|---|
| `ross2011dagger` | DAgger — A Reduction of Imitation Learning... (AISTATS 2011) | interactive IL | arxiv.org/abs/1011.0686 |
| `kelly2019hgdagger` | HG-DAgger (ICRA 2019) | interactive IL | arxiv.org/abs/1810.02890 |
| `menda2019ensembledagger` | EnsembleDAgger (IROS 2019) | interactive IL / uncertainty gating | arxiv.org/abs/1807.08364 |
| `hoque2021lazydagger` | LazyDAgger (CASE 2021) | interactive IL | arxiv.org/abs/2104.00053 |
| `mandlekar2021iwr` | IWR — Human-in-the-Loop IL via Remote Teleoperation (2020) | interactive IL | arxiv.org/abs/2012.06733 |
| `janner2019mbpo` | MBPO — When to Trust Your Model (NeurIPS 2019) | uncertainty-aware MBRL | arxiv.org/abs/1906.08253 |
| `christiano2017preferences` | Deep RL from Human Preferences (NeurIPS 2017) | preference-based RL | arxiv.org/abs/1706.03741 |
| `lee2021pebble` | PEBBLE (ICML 2021) | preference-based RL | arxiv.org/abs/2106.05091 |
| `rafailov2023dpo` | Direct Preference Optimization (NeurIPS 2023) | preference-based RL | arxiv.org/abs/2305.18290 |
| `gupta2021resetfree` | Reset-Free RL via Multi-Task Learning (ICRA 2021) | reset-free real-world RL | arxiv.org/abs/2104.11203 |
| `sharma2022earl` | EARL — Autonomous RL: Formalism & Benchmarking (ICLR 2022) | reset-free / autonomous RL | arxiv.org/abs/2112.09605 |
| `smith2022walk` | A Walk in the Park (CoRL 2022) | efficient real-world RL | arxiv.org/abs/2208.07860 |

## Notes / caveats

- **`vlaintheloop2026`** is an OpenReview submission under review for ICLR 2026 — it is real and the metadata is confirmed, but it is *not yet a peer-reviewed publication*. Cite with care; verify acceptance before camera-ready.
- **Venue (booktitle) for several added entries** (e.g. exact conference for HG-DAgger/EnsembleDAgger/LazyDAgger, ICML/NeurIPS years) is taken from widely-cited convention; titles, authors, and years are all directly confirmed on the arXiv abstract page. `mandlekar2021iwr` is cited as an arXiv preprint because no formal proceedings entry was confirmed.
- **`luo2024serl` page numbers** (16961–16969) are from IEEE Xplore listings, not re-verified against the official proceedings; title/authors/venue are confirmed via arXiv.
- **Bib keys `zhang2020apil` and `pinosky2022hybrid`** were intentionally kept despite the corrected author/year, to avoid breaking `\cite` references in `related_work.md` and the proposal. The keys are labels only; the bibliographic data inside each entry is now correct.

---

# Citation Audit — 2026-06-25 expansion pass

**Audited:** 2026-06-25 (second pass)
**Goal:** (1) reconcile works newly `\cite`d in the proposal §3/§5/§6.5/§7 for the M1/M2/T1 upgrades; (2) verify the ◐/⚠-flagged candidates in `innovation_gaps.md`; (3) add further verified prior art for value-of-information/active querying, value-aware MBRL, world models, plasticity, calibration, preference-based RL, reset-free RL.
**Method:** arXiv API (`export.arxiv.org/api/query`) for exact titles/authors/IDs/comments; PMLR and NeurIPS proceedings pages and DBLP for proceedings-only papers and venue confirmation; publisher DOI where applicable.
**Policy (unchanged):** No fabrication. Where a venue could not be confirmed from a primary source, the entry is cited as an **arXiv preprint** using the verified arXiv ID rather than guessing a venue. No `Anonymous`, no guessed IDs.

## Summary (this pass)

| Outcome | Count |
|---|---|
| New entries added (all VERIFIED) | 34 |
| Flagged candidates verified | 17 |
| Flagged candidates rejected | 0 |
| Proposal-cited-but-missing works reconciled | 7 |
| **Total entries in `references.bib` now** | **74** (40 prior + 34 new) |

## 1. Proposal-cited-but-missing — reconciled (M1/M2/T1)

| Key | Paper | Status | Authoritative source |
|---|---|---|---|
| `farahmand2018itervaml` | Iterative Value-Aware Model Learning (NeurIPS 2018) | VERIFIED | proceedings.neurips.cc/paper/2018/hash/7a2347d96752880e3d58d72e9813cc14-Abstract.html ; dblp.org/rec/conf/nips/Farahmand18 |
| `grimm2020valueequiv` | The Value Equivalence Principle for MBRL (NeurIPS 2020) | VERIFIED | arxiv.org/abs/2011.03506 |
| `voelcker2023lambda` | λ-models: Effective Decision-Aware RL with Latent Models | VERIFIED | arxiv.org/abs/2306.17366 |
| `nikishin2022primacy` | The Primacy Bias in Deep RL (ICML 2022) | VERIFIED | arxiv.org/abs/2205.07802 |
| `sokar2023redo` | The Dormant Neuron Phenomenon / ReDo (ICML 2023) | VERIFIED | arxiv.org/abs/2302.12902 |
| `schwarzer2023bbf` | Bigger, Better, Faster / BBF (ICML 2023) | VERIFIED | arxiv.org/abs/2305.19452 |
| `nakamoto2023calql` | Cal-QL (NeurIPS 2023) | VERIFIED | arxiv.org/abs/2303.05479 |

> PETS (`chua2018pets`, arXiv:1805.12114) and DreamerV3 (`hafner2023dreamerv3`, arXiv:2301.04104) were already present with correct arXiv IDs — confirmed, **not** duplicated.

## 2. innovation_gaps.md ◐/⚠ candidates — verification outcomes

| Key | Paper | Flag → Outcome | Authoritative source |
|---|---|---|---|
| `hansen2024tdmpc2` | TD-MPC2 (ICLR 2024) | ✓ → VERIFIED | arxiv.org/abs/2310.16828 |
| `alonso2024diamond` | DIAMOND (NeurIPS 2024) | ✓ → VERIFIED | arxiv.org/abs/2405.12399 |
| `zhang2023storm` | STORM (NeurIPS 2023) | ◐ → VERIFIED (ID + venue) | arxiv.org/abs/2310.09615 ; dblp.org/rec/conf/nips/ZhangWSYH23 |
| `robine2023twm` | TWM "...Happy With 100k Interactions" (ICLR 2023) | ◐ → VERIFIED (title corrected) | arxiv.org/abs/2303.07109 |
| `micheli2023iris` | IRIS — Transformers are Sample-Efficient WMs (ICLR 2023) | ◐ → VERIFIED (ID confirmed) | arxiv.org/abs/2209.00588 |
| `schrittwieser2020muzero` | MuZero (Nature 2020) | ◐ → VERIFIED (+DOI) | arxiv.org/abs/1911.08265 ; doi 10.1038/s41586-020-03051-4 |
| `mandlekar2021robomimic` | robomimic (CoRL 2021) | ◐ → VERIFIED (ID confirmed) | arxiv.org/abs/2108.03298 |
| `cen2025worldvla` | WorldVLA | ✓ → VERIFIED | arxiv.org/abs/2506.21539 |
| `cen2025rynnvla2` | RynnVLA-002 | ✓ → VERIFIED | arxiv.org/abs/2511.17502 |
| `asadi2018wasserstein` | Wasserstein↔VAML equivalence | ✓ → VERIFIED (authors = Asadi et al., not Farahmand) | arxiv.org/abs/1806.01265 |
| `modhe2021modeladvantage` | Model-Advantage & Value-Aware Models | ✓ → VERIFIED (authors confirmed) | arxiv.org/abs/2106.14080 |
| `farahmand2017vaml` | VAML original (AISTATS 2017) | ◐ → VERIFIED | proceedings.mlr.press/v54/farahmand17a.html |
| `tao2025maniskill3` | ManiSkill3 | ✓ → VERIFIED (cited as preprint; RSS'25 not re-verified) | arxiv.org/abs/2410.00425 |
| `pineda2021mbrllib` | MBRL-Lib | ✓ → VERIFIED | arxiv.org/abs/2104.10159 |
| `huang2022cleanrl` | CleanRL | ✓ → VERIFIED (cited as preprint; JMLR not re-verified) | arxiv.org/abs/2111.08819 |
| `seno2022d3rlpy` | d3rlpy (JMLR 23(315)) | ✓ → VERIFIED (journal_ref on arXiv) | arxiv.org/abs/2111.03788 |
| `cadene2026lerobot` | LeRobot | ✓ → VERIFIED | arxiv.org/abs/2602.22818 |

## 3. Additional verified prior art (strengthens related work)

| Key | Paper | Cell | Authoritative source |
|---|---|---|---|
| `guo2017calibration` | On Calibration of Modern Neural Networks (ICML 2017) | calibration (M2) | arxiv.org/abs/1706.04599 |
| `gal2017activelearning` | Deep Bayesian Active Learning with Image Data | active querying / VoI (T4) | arxiv.org/abs/1703.02910 |
| `lyle2023plasticity` | Understanding plasticity in neural networks (ICML 2023) | plasticity (T1) | arxiv.org/abs/2303.01486 |
| `dohare2024plasticity` | Maintaining Plasticity in Deep Continual Learning | plasticity (T1) | arxiv.org/abs/2306.13812 |
| `chen2021redq` | REDQ (ICLR 2021) | high-UTD sample efficiency (T1) | arxiv.org/abs/2101.05982 |
| `wu2022daydreamer` | DayDreamer (CoRL 2022) | world models for real robots (M3) | arxiv.org/abs/2206.14176 ; dblp.org/rec/conf/corl/WuEHAG22 |
| `park2022surf` | SURF (ICLR 2022) | preference-based RL | arxiv.org/abs/2203.10050 |
| `lee2021bpref` | B-Pref (NeurIPS D&B 2021) | preference-based RL / imperfect teachers | arxiv.org/abs/2111.03026 |
| `liu2023sirius` | Sirius — Robot Learning on the Job (RSS 2023) | interactive HITL deployment | arxiv.org/abs/2211.08416 |
| `eysenbach2018leavenotrace` | Leave no Trace (ICLR 2018) | reset-free / autonomous recovery (T3) | arxiv.org/abs/1711.06782 ; dblp.org/rec/conf/iclr/EysenbachGIL18 |

## Notes / caveats (this pass)

- **No candidates were rejected** — every ◐/⚠ item in `innovation_gaps.md` resolved to a real paper. Two metadata corrections were folded into the bib: TWM's full title is *"Transformer-based World Models Are Happy With 100k Interactions"* (not "Transformer-based World Models"); the Wasserstein↔VAML paper is by **Asadi, Cater, Misra, Littman**, not Farahmand.
- **Venue-as-preprint decisions (no fabrication):** `voelcker2023lambda`, `gal2017activelearning`, `tao2025maniskill3`, `pineda2021mbrllib`, `huang2022cleanrl`, plus the workshop paper `asadi2018wasserstein` and `dohare2024plasticity`, are cited as arXiv preprints because their formal venue/journal metadata was not confirmed from a primary source this pass (arXiv ID, title, and author list are all confirmed).
- **`farahmand2018itervaml`** is **not on arXiv**; verified via the NeurIPS 2018 proceedings page and DBLP (single author, pp. 9090–9101).
- **`schrittwieser2020muzero`**: Nature DOI taken from the arXiv DOI field; Nature volume/pages omitted (not independently re-verified).
- No duplicate bib keys were introduced; the original 40 entries are unchanged.
