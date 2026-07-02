# Experiment Plan

**Problem**: Human-in-the-loop reinforcement learning for robotic manipulation can waste scarce human-control budget or suffer late-policy collapse after useful interventions.
**Method Thesis**: FORESIGHT-HIL should be evaluated as a success-cost Pareto method: foresighted VoI gates and anti-collapse training should improve autonomous success per human step, with best-checkpoint claims verified by repeated evaluation.
**Date**: 2026-06-29

## Claim Map

| Claim | Why It Matters | Minimum Convincing Evidence | Linked Blocks |
|---|---|---|---|
| C1: Budget-aware VoI improves intervention efficiency | This is the main novelty over random or always-on human intervention. | Across seeds, tuned VoI reaches a better success/human-cost tradeoff than none and a competitive Pareto point vs random. | B1, B2 |
| C2: Anti-collapse evaluation is necessary for honest HIL-RL reporting | Current runs show high intermediate success followed by final-policy instability. | Final policy, best checkpoint, and repeated checkpoint re-eval are all reported; retention mechanisms are accepted only if they reduce the best-final gap. | B3, B4 |

## Paper Storyline

- Main paper must prove: FORESIGHT-HIL trades a small human budget for meaningful success gains, and reports this as a Pareto frontier rather than unconditional dominance.
- Appendix can support: threshold sweeps, takeover length sweeps, risk-mode ablations, checkpoint re-eval details, and failed aggressive-trigger cases.
- Experiments intentionally cut for now: real-robot deployment, image observations, large RoboCasa suite, and Isaac Lab scale-up until the Lift evidence is stable.

## Experiment Blocks

### Block 1: Main Success-Cost Pareto
- Claim tested: C1
- Why this block exists: It is the main table/figure for reviewers.
- Dataset / split / task: robosuite Lift, scripted-oracle human, seeds 0-2 first, then 0-4 if stable.
- Compared systems: none, random@budget, default VoI, tuned VoI, tuned VoI + anti-collapse.
- Metrics: final success, best-checkpoint repeated success, human steps, engagements, Wilson CI, wall time.
- Setup details: 10k/30k steps, `eval_episodes>=20` during training, repeated checkpoint eval `3 x 20` or `1 x 100`.
- Current result: R004 seed 0 with restore-best showed collapse mitigation but not a VoI advantage: restored final none/random/voi = 65/70/55%, repeated best-checkpoint success = 81.7/75.0/53.3%.
- Learning-value update: R008/R009 add a demo-nearest reference-policy disagreement multiplier to VoI. On seed 0 it improved repeated best-checkpoint success from plain VoI 53.3% to 80.0%; over seeds 0-2 the repeated best estimate is 131/180 = 72.8% with mean best-step human cost 176.7. This is promising but not yet a decisive Pareto claim because seed 2 is weaker.
- Budget/scale repair and baseline alignment: R010 targeted weak seed 2. Budget300/scale2 reached 45/60 repeated best with best-step cost 255; budget600/scale3 reached 47/60 with cost 384. R011 then repeated budget300/scale2 on seeds 0-1 and found only 36/60 and 37/60 repeated best success. R012 repeated budget600/scale3 on seeds 0-1 and reached 50/60 and 55/60 repeated best success. R013 aligned no-intervention and random baselines. R014 expanded the aligned comparison to five Lift seeds: scale3 method is 256/300 = 85.3% at mean best-step cost 202.0; none is 237/300 = 79.0%; random is 251/300 = 83.7% at mean best-step cost 269.2. R020 repeated the same five-seed Lift checkpoints with `5 x 20` episodes per seed: LV-VoI scale3 is 416/500 = 83.2% at cost202.0, none is 400/500 = 80.0%, and random is 426/500 = 85.2% at cost269.2. R021 added the missing cost-matched random point: random_b350 reaches 439/500 = 87.8% at cost177.0, which dominates LV-VoI scale3 on both success and human cost. R015-R019 show Stack is currently a negative breadth/failure-analysis case rather than a positive second-task result.
- Success criterion: a redesigned tuned VoI must lie on the success-cost Pareto frontier, improve over none, and beat cost-matched random_b350 before it can be used as a main positive claim.
- Failure interpretation: R021 already shows cost-matched random beats the current LV-VoI scale3 candidate; the paper should now shift toward trigger redesign and failure-aware diagnostics rather than Pareto superiority unless R022 repairs the mechanism.
- R022 repair path result: the learning-value minimum-disagreement filter (`vlvmin0p25`) did not repair the random-dominance failure. On Lift seeds 0-2 with 5x20 repeated checkpoint evaluation, min-disagreement LV-VoI reached 226/300 = 75.3% at mean best-step cost211.7, while same-seed random_b350 reached 259/300 = 86.3% at cost95.0. Do not expand this variant. The next step is intervention-timing diagnosis: identify what random_b350 is doing right before adding another heuristic trigger.
- R023 diagnostic setup: `--trace_interventions` now records one row per intervention start with step, budget fraction, VoI score/p_fail, and privileged geometry. A short random/VoI smoke confirms trace files are non-empty. The next paper-facing diagnostic should rerun the real seeds 0-2 comparison with tracing enabled, then compare start timing and gripper-to-cube geometry.
- R023 real-trace result: LV-VoI scale3 does not fail by simply intervening far from the cube. Across Lift seeds 0-2, LV-VoI starts are closer to the cube than random_b350 (`g2c_norm` 0.217 vs 0.285; `g2c_xy` 0.152 vs 0.235), but it starts more often (96 vs 55), has saturated early starts (`score=10`, `p_fail=1`), no 2-4k starts, and many low-score 4-6k starts. R024 should test score-calibrated gating / low-confidence mid-late suppression rather than pure phase/contact gating. If that fails, pivot the paper story toward a cost-matched HIL-RL diagnostic benchmark with negative findings.
- R024 implementation note: a default-off score floor now supports `--voi_score_floor_after_step` and `--voi_score_floor_after_value`, blocking low-score VoI takeover starts only after the configured training step while preserving default LV-VoI behavior. A 300-step smoke passed under `results/r024_score_floor_smoke`. The first real gate should use original LV-VoI scale3 plus `after_step=4000`, `floor=0.05` on Lift seeds 0-2, then compare against `random_b350` before any expansion.
- R024 result: the score-floor repair is negative under the same-seed repeated-evaluation gate. R024 score-floor LV-VoI reached `233/300` = 77.7% repeated success (Wilson CI 72.6-82.0%) at mean best-step human cost 253.3, versus `random_b350` at `259/300` = 86.3% (CI 82.0-89.8%) and cost 95.0. Trace diagnostics show the floor worked mechanically (zero starts below score 0.05 after step 4000) but did not materially reduce start count (`94` starts vs original LV-VoI `96`; random_b350 `55`). Do not expand R024; the main paper should pivot toward a cost-matched HIL-RL diagnostic benchmark with negative findings and a redesigned evaluation protocol unless a substantially different trigger is introduced.
- R025 paper-pivot package is now created. `PAPER_PLAN.md` reframes the manuscript as an empirical diagnostic/benchmark paper, with supporting files in `results/r025_paper_pivot/`. The central thesis is no longer "current VoI trigger wins"; it is that HIL-RL intervention-trigger claims need cost-matched random families, repeated checkpoint evaluation, and trace-level diagnostics because intuitive trigger variants can be dominated. The next block should build paper-ready figures/tables from existing data rather than running another small heuristic trigger.
- R026 paper artifact build is complete. The `figures/` directory now contains reproducible vector figures (`fig1_hero_diagnostic_summary.pdf` through `fig5_score_over_time.pdf`), LaTeX-ready tables (`TABLE_main_costmatched_results.tex`, `TABLE_negative_findings.tex`, `TABLE_trace_diagnostics.tex`), and `latex_includes.tex`. The generated hero figure is a draft diagnostic summary; the data-driven success-cost, repair, timing, and score figures are ready for manuscript integration. Next: citation audit and first-section drafting, not new trigger tuning.
- Table / figure target: Main Fig. 1 success-cost Pareto.
- Priority: MUST-RUN

### Block 2: Trigger and Budget Ablation
- Claim tested: C1
- Why this block exists: It isolates whether gains come from foresighted VoI or just spending more human steps.
- Dataset / split / task: robosuite Lift, seed 2 diagnostic first, then seeds 0-2 for selected points.
- Compared systems: default VoI, `tau=0/c_query=0`, `tau=0.01/c_query=0`, budgets 300/600/1000, takeover lengths 10/20.
- Metrics: final success, best success, human steps, candidate rate, score mean, p_fail mean.
- Setup details: reuse existing `results/voi_gate_sweep_seed2_10000_eval20`; extend only promising points.
- Success criterion: identify one or two Pareto candidates for multi-seed runs.
- Failure interpretation: if lower threshold worsens results, threshold alone is not the method; pacing/retention matters.
- Table / figure target: Appendix ablation and failure-analysis plot.
- Priority: MUST-RUN

### Block 3: Anti-Collapse Training
- Claim tested: C2
- Why this block exists: Existing evidence shows high intermediate success can collapse later.
- Dataset / split / task: collapse-prone Lift/VOI settings, especially budget 600/takeover 20.
- Compared systems: constant BC actor regularization, `linear_late` BC actor schedule, best checkpoint selection, repeated checkpoint re-eval.
- Metrics: final success, best success, best-final gap, repeated checkpoint success, BC regularization loss.
- Setup details: `--bc_actor_reg_schedule linear_late --bc_actor_reg_late_coef {100,150,200} --bc_actor_reg_late_start_frac {0.5,0.7}`.
- Current result: R002 (`50 -> 150`, start 0.5) reached 20% final success, 80% best success at step 2000, and 85.0% repeated best-checkpoint success over 60 episodes; late actor anchoring alone is not enough.
- Success criterion: lower best-final gap without increasing human cost.
- Failure interpretation: collapse is not solved by actor anchoring alone; prioritize best-checkpoint/early-stop reporting, critic/actor plasticity controls, or freezing/regularizing updates after a strong checkpoint.
- Table / figure target: Main or appendix anti-collapse table.
- Priority: MUST-RUN

### Block 4: Evaluation Reliability
- Claim tested: C2
- Why this block exists: Single 20-episode evals can overstate checkpoint quality.
- Dataset / split / task: saved best checkpoints from main runs.
- Compared systems: final policy vs saved best checkpoint.
- Metrics: repeated success mean/std, total successes/episodes, Wilson CI.
- Setup details: `scripts/evaluate_checkpoint.py --repeats 3 --episodes 20` for development, `--episodes 100` for final claims.
- Success criterion: paper reports stable repeated estimates and avoids cherry-picking.
- Failure interpretation: if repeated eval is unstable, increase eval episodes before making claims.
- Table / figure target: Appendix reliability table.
- Priority: MUST-RUN

### Block 5: Robotics Generalization
- Claim tested: C1
- Why this block exists: A Q1 robotics/RL paper needs more than one manipulation setting.
- Dataset / split / task: second robosuite task first; RoboCasa only after Lift stabilizes.
- Compared systems: none, random, selected FORESIGHT-HIL variant.
- Metrics: same as Block 1.
- Setup details: start with the cheapest working task; avoid image observations initially.
- Current result: Stack support works at the oracle level (`5/5` scripted success). The initial Lift-tuned LV-VoI was negative (`22/60`) versus none (`28/60`) and random (`26/60`). R017's Stack-tuned candidate (`50` demos, `10000` BC, `tau=0.0`) reached `47/60` on seed0, but R018 matched the 50-demo protocol over seeds 0-2 and found no-online matched BC `131/180` (72.8%) dominating Stack-tuned LV-VoI `107/180` (59.4%) and random `107/180` (59.4%). R019 tried starts-only intervention demo replay and a Stack pick/place phase guard on seed0; the best repeated redesigned variant was `38/60`, below the no-online `47/60`.
- Success criterion: a future Stack intervention variant must beat the strong no-online matched-BC baseline at comparable or justified human cost; current R019 variants do not.
- Failure interpretation: the current method is task-specific; Stack should be reported as failure analysis unless a substantially different task-aware mechanism is introduced.
- Table / figure target: Appendix or secondary main result.
- Priority: NICE-TO-HAVE until Lift is stable.

## Run Order and Milestones

| Milestone | Goal | Runs | Decision Gate | Cost | Risk |
|---|---|---|---|---|---|
| M0 | Verify code path | Reacher smoke with `linear_late` and checkpoint | Tests and smoke pass | minutes | none |
| M1 | Anti-collapse probe | Lift seed 1, VOI b600/take20, `linear_late` late coef 150 | completed: negative final-policy result, strong repeated best checkpoint | ~10-15 min | stochastic variance |
| M2 | Pareto candidate check | selected tuned VoI budgets 600/1000, seeds 0-2 | continue only if a variant beats none on repeated checkpoint success or uses far less human cost than random | hours | none/random may dominate |
| M3 | Paper-grade main table | seeds 0-4, eval 50/100, repeated checkpoint eval | stable CIs and clear Pareto story | many hours | compute time |
| M4 | Generalization | second manipulation task | trend transfers | task-dependent | setup friction |

## Compute and Data Budget

- Total estimated GPU-hours for main Lift evidence: 10-30 hours depending on seeds and eval episodes.
- Data preparation needs: none beyond scripted demonstrations; store all summary CSVs and checkpoint re-eval CSVs.
- Human evaluation needs: none; human is scripted-oracle simulation and must be labeled as such.
- Biggest bottleneck: robosuite wall time and evaluation variance.

## Risks and Mitigations

- Risk: VoI is too conservative or too aggressive depending on threshold.
- Mitigation: report Pareto frontier and include failure cases.
- Risk: single-eval best checkpoint overstates success.
- Mitigation: use `scripts/evaluate_checkpoint.py` repeated evaluation.
- Risk: final-policy collapse masks useful intermediate policies.
- Mitigation: best checkpoint reporting, repeated checkpoint re-eval, and retention mechanisms that must prove a smaller best-final gap before entering the main method.
- Risk: Lift-only evidence is too narrow.
- Mitigation: add second robosuite task only after Lift main table is stable.

## Final Checklist

- [ ] Main paper tables are covered
- [ ] Novelty is isolated
- [ ] Simplicity is defended
- [ ] Frontier contribution is justified or explicitly not claimed
- [ ] Nice-to-have runs are separated from must-run runs
