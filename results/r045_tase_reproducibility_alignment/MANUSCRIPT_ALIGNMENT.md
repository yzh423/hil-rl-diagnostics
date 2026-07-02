# R045 Manuscript Alignment

Date: 2026-07-02

## Summary

R045 performs a targeted manuscript optimization after the R043 venue decision
and the R044 environment/reproducibility audit. The goal is to make the current
paper read less like a failed-method report and more like a T-ASE-compatible
automation-science contribution: a practical diagnostic protocol for evaluating
human-intervention allocation in robotic HIL-RL.

## Edits

- Shortened and retargeted the title toward cost-matched diagnostics for
  human-in-the-loop robot learning intervention triggers.
- Added a `Note to Practitioners` after the abstract. The note explains the
  practical stop/redesign rule, the need for random-budget sweeps, repeated
  checkpoint evaluation, and intervention-start traces.
- Added `paper/sections/07_reproducibility_inventory.tex` as an appendix.
- Added two appendix tables:
  - reproducibility artifact inventory;
  - compute and evidence-accounting status.
- Preserved the current limitations: scripted privileged-state oracle,
  simulation-only evidence, no real teleoperator, no real robot validation, and
  no positive LV-VoI superiority claim.

## No New Claims

This pass adds no new citations, no new numerical experiment results, and no
new method claim. It packages existing evidence so a reviewer can see the
protocol contribution, inspect artifacts, and understand remaining provenance
gaps.

## Recommended Follow-Up

The next high-value work is version-provenance repair and a small robotics
breadth decision. If more evidence is added, it should be a separately
registered R046+ package rather than an edit to historical result archives.
