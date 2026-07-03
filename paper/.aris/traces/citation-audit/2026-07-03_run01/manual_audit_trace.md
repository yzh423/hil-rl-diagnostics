# R051 Manual Citation Audit Trace

Date: 2026-07-03

This trace records a direct web/source citation-context audit after the R050
human-attention allocation theme pass. No reviewer subagent was spawned; the
audit used local manuscript contexts plus authoritative source pages.

## Inputs

- `paper/references.bib`
- `paper/main.tex`
- `paper/sections/01_introduction.tex`
- `paper/sections/02_related_work.tex`
- `paper/sections/03_protocol_setup.tex`
- `paper/sections/04_results.tex`
- `paper/sections/05_discussion.tex`
- `paper/sections/06_conclusion.tex`
- `paper/sections/99_references.tex`
- `paper/.aris/citation-audit/contexts.txt`

## Verdict

PASS. All 15 cited entries support their current contexts after R050. No
wrong-context citation, missing cited key, hallucinated entry, or bibliography
metadata edit was found in this run.

## Source Checks

- arXiv checked for `luo2025hilserl`, `cai2025aim`, `chua2018pets`,
  `sac2018applications`, `robosuite2020`, and
  `agarwal2021statisticalprecipice`.
- JAIR checked for `retzlaff2024hitl`.
- PMLR checked for `ball2023rlpd`, `mandlekar2021robomimic`,
  `hoque2021thrifty`, `guo2017calibration`, and `haarnoja2018sac`.
- NeurIPS proceedings checked for `janner2019mbpo`; PETS was checked through
  its arXiv record because the NeurIPS page was less accessible in the current
  browser output.
- AAAI proceedings checked for `henderson2018deeprlmatters`.
- The `wilson1927score` DOI and CrossRef status are retained from R037/R042;
  no manuscript wording changed its use.

## R050-Specific Note

The new manuscript term "human-attention allocation" is treated as an authorial
framing synthesized from HITL-RL workflow, budget-aware intervention/querying,
and supervisor-burden sources. It is not cited as terminology coined by a
single prior paper.
