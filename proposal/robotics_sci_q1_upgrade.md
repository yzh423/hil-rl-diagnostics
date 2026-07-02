# SCI Q1 Upgrade Plan for FORESIGHT-HIL with Robotics-Relevant Evidence

> Goal: reposition the current FORESIGHT-HIL prototype as an SCI Q1 paper on
> human-in-the-loop / model-based reinforcement learning, with robotics-relevant
> tasks as the main application and evidence anchor. The paper does not need to
> be a pure robotics paper; robotics should provide realistic, high-value
> validation rather than constrain the whole contribution.
>
> Status: planning document. Do not treat every item below as a claim already
> supported by current experiments. In particular, current robosuite results
> should be reported cautiously until the VoI gate consistently beats random
> allocation under matched budgets.

## 1. Recommended Paper Positioning

### Working Title

**Predictive Budget-Aware Human Intervention for Model-Based Reinforcement Learning**

Alternative titles:

- **Foresighted Human-in-the-Loop Reinforcement Learning via Model-Based Value of Information**
- **Budgeted Predictive Human Assistance for Reinforcement Learning**
- **When Should an Agent Ask for Help? Model-Based Intervention Allocation with Robotic Validation**

### One-Sentence Thesis

Human-in-the-loop reinforcement learning can reduce supervision cost by using a
learned dynamics/world model to predict future failure, calibrate intervention
uncertainty, and allocate a limited human-query budget across parallel learning
rollouts, with robotic manipulation serving as a demanding and credible testbed.

### Robotics-Relevant Framing

The paper should be framed around a general HIL-RL problem with robotics as the
clearest application:

> A human supervisor cannot continuously monitor every learning rollout. The
> agent should decide when human help is worth the cost, before failure occurs,
> and should spend a limited intervention budget where it most improves learning
> or safety. Robotic manipulation is a natural validation domain because failures
> are costly, interventions are realistic, and delayed/noisy human corrections
> matter.

This framing keeps the paper eligible for AI/RL/engineering SCI Q1 venues while
retaining a strong robotics-related application story:

- contact-rich robotic manipulation as a primary benchmark,
- scarce teleoperation / teaching time,
- delayed or noisy human corrections,
- safe and sample-efficient learning,
- scalable simulation-to-real or simulation-to-robot validation when available.

## 2. Contribution Stack to Keep

For an SCI Q1 paper, keep the contribution stack narrow and defensible.
Avoid presenting too many optional modules as equal headline contributions.

### C1. Predictive Human-Intervention Trigger

Use a dynamics/world model to roll out the current policy and estimate whether
the agent is likely to enter a failure-prone or low-progress region.
The novelty is not merely "uncertainty"; it is anticipatory intervention:
asking before failure, not after value stagnation or human takeover.

### C2. Budgeted Allocation Across Parallel Learning Rollouts

Recast the current parallel-env module as a scarce-supervision problem: a single
human teacher/operator has a finite intervention budget while many rollouts,
digital twins, or simulated training instances run in parallel.

This is the cleanest distinctive angle. It is not covered by standard HIL-RL
systems, which typically assume one robot, one human, and sequential intervention.

### C3. Robustness to Imperfect Human Supervisors

SCI Q1 reviewers will care about whether the method survives realistic human
imperfections: delay, noisy correction, inconsistent skill, and over/under-
intervention. Robotic tasks make these imperfections concrete, but the claim can
remain general.

### C4. Calibration as a Mechanism, Not Just a Metric

Keep trigger calibration because it gives a principled reason why a single
threshold can transfer across tasks, seeds, or parallel rollouts. This is useful
for journal reviewers because it makes the method less like a hand-tuned heuristic.

### Optional C5. Real-Robot or Robotics-Relevant Validation

If hardware access becomes available, add a small real-robot validation task.
Do not make the paper depend on it. The primary evidence should remain:
multi-task robot simulation, matched budgets, multiple seeds, calibration, and
robustness sweeps.

## 3. What to De-Emphasize

The current proposal contains several ideas that are interesting but risk making
the paper feel scattered. For SCI Q1, push these into ablations or future work:

- multi-modal feedback selection: keep as an optional extension unless fully implemented;
- plasticity preservation: useful if results are strong, but not required for the main story;
- large VLA/world-model-human-surrogate direction: likely a separate paper;
- broad theory claims: include a light bound only if it is clean and correct;
- "top conference" wording: replace with SCI Q1 journal language.

## 4. Robotics Evidence Strategy

Because real robot access is possible but not guaranteed, design the evidence
chain in two layers. The first layer supports the method without hardware; the
second layer gives robotics credibility if hardware time becomes available.

### Main Evidence, Required

- robosuite / MuJoCo or similar control tasks with SAC/RLPD-style learner.
- A parallel simulation substrate such as MJX or ManiSkill for budget allocation.
- Three or more manipulation tasks, not only `Lift`.
- At least three seeds per main setting.
- Matched human-query budgets for random, reactive, and FORESIGHT-HIL variants.
- Robustness sweeps over human delay, noise, skill, dropout, and over-intervention.
- Trigger calibration: reliability diagram, ECE, Brier score, precision/recall.

### Real-Robot Evidence, Optional but High-Value

If a Panda/Franka/UR-style arm is available, use a small validation:

- one task: pick-and-place, peg insertion, or cube lifting;
- one human/operator or scripted teleoperation interface;
- compare: no intervention, random-budget intervention, reactive risk trigger, FORESIGHT-HIL;
- report: success rate, human intervention count, intervention time, recovery failures;
- avoid overclaiming sim-to-real generality from a single hardware task.

Recommended wording if the real-robot study is small:

> We use real-robot trials as a validation of the intervention interface and
> timing behavior, while the statistical evidence for budget allocation and
> robustness is obtained from controlled multi-task simulation.

## 5. Verified Literature Expansion

The table below separates papers already represented in the current project from
high-value additions. "Add" means useful to add to `proposal/references.bib`
after final metadata verification.

### A. Robotics and Robot Learning Foundations

| Paper | Source | Add? | Why It Matters |
|---|---|---:|---|
| Kober, Bagnell, Peters, **Reinforcement Learning in Robotics: A Survey**, IJRR 2013 | DOI: `10.1177/0278364913495721` | Yes | Authoritative robot RL background; supports why robot RL is sample-expensive and safety-sensitive. |
| Argall et al., **A Survey of Robot Learning from Demonstration**, Robotics and Autonomous Systems 2009 | DOI: `10.1016/j.robot.2008.10.024` | Yes | Classic human demonstration / teaching survey; useful for positioning HIL as a continuation of robot teaching. |
| Ravichandar et al., **Recent Advances in Robot Learning from Demonstration**, Annual Review 2020 | DOI: `10.1146/annurev-control-100819-063206` | Yes | Modern robot LfD survey; supports human-provided demonstrations and corrections. |
| Brunke et al., **Safe Learning in Robotics**, Annual Review 2022 | DOI: `10.1146/annurev-control-042920-020211` | Yes | Strong safety-learning reference; supports the need for interventions before unsafe or failed behavior. |
| Deisenroth and Rasmussen, **PILCO: A Model-Based and Data-Efficient Approach to Policy Search**, ICML 2011 | PMLR: `v15/deisenroth11a` | Yes | Foundational model-based robot learning; motivates model-based sample efficiency. |
| Levine et al., **End-to-End Training of Deep Visuomotor Policies**, JMLR 2016 | JMLR 17(39) | Optional | Useful if the paper discusses vision-based manipulation or real-robot visuomotor policies. |

### B. Human Intervention and Interactive Robot Learning

| Paper | Source | Add? | Why It Matters |
|---|---|---:|---|
| Luo et al., **HIL-SERL**, Science Robotics / arXiv 2025 | arXiv: `2410.21845`, DOI: `10.1126/scirobotics.ads5033` | Already | Primary robot HIL-RL baseline and system inspiration. |
| Liu et al., **PACT**, arXiv 2026 | arXiv: `2606.03949` | Already | Strong direct competitor for using intervention data. |
| Zhao et al., **Real-world RL from Suboptimal Interventions / SiLRI**, arXiv 2025 | arXiv: `2512.24288` | Already | Direct support for robustness to imperfect interventions. |
| Deng et al., **UniIntervene**, arXiv 2026 | arXiv: `2606.12372` | Already | Closest reactive/value-risk intervention competitor. |
| Cai, Peng, Zhou, **Robot-Gated Interactive Imitation Learning with Adaptive Intervention Mechanism**, ICML 2025 | PMLR / arXiv: `2506.09176` | Already | Robot-gated request baseline, but imitation-learning oriented. |
| Korkmaz and Biyik, **MILE: Model-based Intervention Learning**, arXiv 2025 | arXiv: `2502.13519` | Already | Important for modeling human intervention timing. |
| MacGlashan et al., **Interactive Learning from Policy-Dependent Human Feedback**, ICML 2017 | arXiv: `1701.06049` | Yes | Shows human feedback depends on learner policy and includes physical robot results. |
| Warnell et al., **Deep TAMER**, AAAI / arXiv 2018 | arXiv: `1709.10163` | Yes | Classic deep human-feedback learning reference. |
| Hoque et al., **ThriftyDAgger**, CoRL 2021 | arXiv: `2109.08273` | Already | Budget-aware querying baseline from interactive imitation learning. |
| Kelly et al., **HG-DAgger**, ICRA 2019 | arXiv: `1810.02890` | Already | Human-gated control transfer baseline. |

### C. Model-Based Robot Learning and World Models

| Paper | Source | Add? | Why It Matters |
|---|---|---:|---|
| Chua et al., **PETS**, NeurIPS 2018 | arXiv: `1805.12114` | Already | Ensemble uncertainty source for model-based rollouts. |
| Janner et al., **MBPO**, NeurIPS 2019 | arXiv: `1906.08253` | Already | Supports short-horizon model rollouts and model-trust tradeoff. |
| Hansen, Su, Wang, **TD-MPC2**, ICLR 2024 | arXiv: `2310.16828` | Already | Practical latent world-model candidate for manipulation foresight. |
| Grimm et al., **Value Equivalence Principle**, NeurIPS 2020 | arXiv: `2011.03506` | Already | Supports decision-aware dynamics models. |
| Farahmand, **Iterative Value-Aware Model Learning**, NeurIPS 2018 | NeurIPS proceedings | Already | Theory basis for value-aware model loss. |
| Hafner et al., **DreamerV3**, arXiv 2023 / Nature 2025 | arXiv: `2301.04104` | Already | General world-model baseline, but heavier than needed for state-based manipulation. |
| Wu et al., **DayDreamer**, CoRL 2022 | arXiv: `2206.14176` | Already | Important evidence that world models can train physical robots. |

### D. Calibration, Uncertainty, and Active Querying

| Paper | Source | Add? | Why It Matters |
|---|---|---:|---|
| Lakshminarayanan et al., **Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles**, NeurIPS 2017 | arXiv: `1612.01474` | Yes | Foundational uncertainty reference for ensemble disagreement. |
| Guo et al., **On Calibration of Modern Neural Networks**, ICML 2017 | arXiv: `1706.04599` | Already | Temperature scaling, reliability diagram, ECE. |
| Nakamoto et al., **Cal-QL**, NeurIPS 2023 | arXiv: `2303.05479` | Already | Useful analogy for calibrated offline-to-online robot RL. |
| Gal et al., **Deep Bayesian Active Learning with Image Data**, ICML workshop / arXiv 2017 | arXiv: `1703.02910` | Already | Information-gain idea behind active querying. |
| Kirsch et al., **BatchBALD**, NeurIPS 2019 | arXiv: `1906.08158` | Optional | Useful if modality/query selection becomes a contribution. |
| Ash et al., **BADGE**, ICLR 2020 | arXiv: `1906.03671` | Optional | Diversity-aware batch querying; relevant to parallel budget allocation. |

### E. Preference and Imperfect Human Feedback

| Paper | Source | Add? | Why It Matters |
|---|---|---:|---|
| Christiano et al., **Deep RL from Human Preferences**, NeurIPS 2017 | arXiv: `1706.03741` | Already | Foundational preference-feedback paper. |
| Lee et al., **PEBBLE**, ICML 2021 | arXiv: `2106.05091` | Already | Feedback-efficient preference RL. |
| Park et al., **SURF**, ICLR 2022 | arXiv: `2203.10050` | Already | Preference learning with fewer labels. |
| Lee et al., **B-Pref**, NeurIPS Datasets and Benchmarks 2021 | arXiv: `2111.03026` | Already | Useful for simulated irrational/imperfect teachers. |
| Casper et al., **Open Problems and Fundamental Limitations of RLHF**, TMLR 2023 | arXiv: `2307.15217` | Optional | Useful for broader human-feedback limitations, less robot-specific. |

### F. Robot Simulation, Benchmarks, and Open-Source Systems

| Paper / Project | Source | Add? | Why It Matters |
|---|---|---:|---|
| Zhu et al., **robosuite**, CoRL 2020 | arXiv: `2009.12293`, GitHub: `ARISE-Initiative/robosuite` | Yes | Current implementation substrate; must be cited directly. |
| Yu et al., **Meta-World**, CoRL 2019 | arXiv: `1910.10897` | Yes | Multi-task manipulation benchmark; useful expansion beyond Lift. |
| Tao et al., **ManiSkill3**, RSS / arXiv 2025 | arXiv: `2410.00425`, GitHub: `haosulab/ManiSkill` | Already | Strong GPU-parallel manipulation substrate. |
| Makoviychuk et al., **Isaac Gym**, arXiv 2021 | arXiv: `2108.10470` | Yes | GPU-parallel robot learning simulator reference. |
| Mandlekar et al., **robomimic**, CoRL 2021 | arXiv: `2108.03298` | Already | Offline human demonstration benchmark and tooling. |
| Luo et al., **SERL**, ICRA 2024 | arXiv: `2401.16013` | Already | HIL-SERL backbone ecosystem. |
| Cadene et al., **LeRobot**, arXiv 2026 | arXiv: `2602.22818` | Already | Modern open-source robot-learning stack; useful for system context. |

## 6. Literature Gap After Robotics-Relevant Reframing

A strong SCI Q1 introduction can be built around this gap chain:

1. RL with human supervision is powerful but supervision is costly and imperfect.
2. Human demonstrations and interventions improve sample efficiency, but human
   attention is scarce and interventions are noisy or delayed.
3. Existing HIL-RL and robot-learning systems mainly study how to use intervention data
   after the intervention occurs.
4. Existing robot-gated methods are usually reactive, model-free, or imitation-
   learning oriented.
5. Model-based RL can anticipate future outcomes, but prior work uses
   the model for planning or policy learning, not for deciding whether human help
   is worth paying for.
6. Therefore, the open problem is predictive, budget-aware human intervention:
   when should an agent ask for help, under a shared budget, before failure?

This is the most defensible version of the novelty claim.

## 7. Experimental Plan for SCI Q1

### E1. Task Suite with Robotics-Relevant Benchmarks

Do not rely only on robosuite `Lift`. A minimal SCI-ready suite should include
both generic control evidence and robotics-relevant benchmarks:

- one easy reaching/lifting task for sanity checking,
- one contact-rich assembly or insertion task,
- one dexterous or cluttered manipulation task,
- one GPU-parallel task suite for budget allocation.

Candidate simulators:

- robosuite: continuity with HIL-SERL and current code;
- Meta-World: broad manipulation task diversity;
- ManiSkill3: GPU-parallel manipulation and stronger system argument;
- MJX: clean parallel MuJoCo story if implementation time is limited.

### E2. Baselines

Required:

- SAC/RLPD without human;
- always-human or oracle upper bound;
- random intervention under matched budget;
- reactive risk trigger;
- HIL-SERL-style human-timed intervention if feasible;
- FORESIGHT-HIL with the same budget.

Recommended:

- UniIntervene-style value-risk trigger, if implementable;
- ThriftyDAgger/AIM-style uncertainty or novelty gate as a simpler robot-gated baseline;
- ground-truth model upper bound to separate model quality from gating logic.

### E3. Metrics

Primary:

- success rate versus human cost;
- queries or intervention seconds to reach a success threshold;
- area under the success-human-cost Pareto curve;
- sample efficiency: environment steps to target success.

Secondary:

- trigger precision/recall for impending failure;
- ECE, MCE, Brier score, and reliability diagrams;
- recovery rate after intervention;
- robustness curves under human noise, delay, skill, dropout, and bias.

### E4. Statistical Reporting

SCI Q1 reviewers will expect more than a best-seed plot:

- at least 3 seeds for expensive robot simulation; 5 seeds if feasible;
- mean plus confidence interval or bootstrap interval;
- fixed evaluation episodes and fixed random seeds;
- paired comparison where the same seeds/tasks are used across methods;
- report negative results honestly, especially if random matches or beats VoI.

Important current warning:

> `results/full/strategy_comparison_final.csv` currently shows `random` above
> `voi` on final success mean. The proposal should not claim FORESIGHT-HIL beats
> random until the trigger is improved or the correct metric shows a consistent
> advantage, such as earlier success, better robustness, better calibration, or
> lower query waste.

## 8. Method Changes That Would Strengthen the Project

### M1. Replace Raw VoI Score with Calibrated Failure Probability

Instead of relying only on ensemble disagreement, train or calibrate a predicted
failure probability:

```text
score(s) = expected_failure_cost(s) * calibrated_p_fail(s) - query_cost
```

Then evaluate whether calibrated scores transfer across tasks and budgets.

### M2. Add a Reactive Baseline

A random baseline is necessary but not enough. Add a reactive baseline:

- current distance-to-goal stagnation;
- value drop or critic uncertainty;
- model-free failure-risk classifier;
- intervention if predicted short-term progress is below threshold.

This is important because the key claim is "anticipatory beats reactive", not
only "VoI beats random".

### M3. Define Task-Relevant Risk Functions

For `Lift`, the current distance-risk proxy is acceptable for smoke testing but
weak for a paper. Upgrade risk definitions, especially for robotics-related tasks:

- object dropped or unstable grasp;
- object moved away from target;
- gripper-object distance increasing after attempted grasp;
- contact force / collision threshold where available;
- irreversible or reset-costly state for insertion/assembly.

### M4. Implement Diversity-Aware Budget Allocation

Top-k allocation can waste queries on many similar states. For the parallel
parallel setting, add a diversity-aware selector:

```text
select high VoI states while penalizing near-duplicate states in feature space
```

This links naturally to active learning and batch selection literature.

### M5. Add a Robotics Adapter Boundary

Even before hardware access, define the interface:

```text
RobotEnv.reset()
RobotEnv.step(action)
RobotEnv.observe()
RobotEnv.query_human(state, mode)
RobotEnv.true_oracle_action(state)  # only in sim/scripted experiments
```

This keeps the system robot-ready without making the whole paper depend on a
physical robot.

## 9. Suggested Manuscript Structure

1. **Introduction**
   - Human supervision in RL is useful but scarce and imperfect.
   - Robotics is a motivating domain where mistakes and supervision are costly.
   - Existing HIL systems are often reactive/sequential.
   - We propose predictive budget-aware intervention.

2. **Related Work**
   - human-in-the-loop RL and human feedback;
   - robot learning and safe robot learning as application context;
   - HIL-RL and robot-gated intervention;
   - model-based RL and uncertainty;
   - active querying and calibration.

3. **Problem Formulation**
   - Budgeted human-intervention MDP;
   - human model with cost, delay, noise, skill;
   - parallel rollout setting.

4. **Method**
   - predictive risk rollout;
   - calibrated VoI trigger;
   - budget allocation;
   - optional recovery branch.

5. **Experiments**
   - task suite;
   - baselines;
   - main Pareto results;
   - robustness;
   - calibration;
   - ablations;
   - optional real-robot or robotics-relevant validation.

6. **Discussion and Limitations**
   - real human vs scripted human;
   - sim-to-real limits;
   - dynamics model errors;
   - operator cognitive load;
   - path toward real robot deployment.

## 10. Near-Term Action List

1. Update README/proposal wording from "top conference" to "SCI Q1 HIL-RL / model-based RL with robotics-relevant validation".
2. Add verified HIL-RL, model-based RL, and robotics-application citations to `references.bib`.
3. Add a reactive intervention baseline.
4. Add a stronger risk function for at least one task beyond `Lift`.
5. Run a task suite where VoI can plausibly beat random under matched budget.
6. Generate calibration plots and query-waste analysis.
7. Decide whether real robot access is available; if yes, design one small validation task.

## 11. Safe Claims for the Paper

Use these claim forms only after corresponding experiments pass:

- Safe now as motivation: "Human supervision is costly and imperfect in HIL-RL, especially in robotics-relevant tasks."
- Safe now as method description: "We formulate intervention timing as a model-based VoI decision."
- Safe after multi-task evidence: "FORESIGHT-HIL improves the success-human-cost Pareto frontier."
- Safe after calibration evidence: "Calibration reduces misallocated queries and improves threshold transfer."
- Safe after robustness sweeps: "The method is more robust to delayed/noisy operators than reactive gates."
- Safe only after hardware trials: "The intervention interface transfers to a physical robot task."

Avoid until proven:

- "first" unless a final citation audit confirms no close prior work;
- "outperforms random" unless the final results support it;
- "real-world" if the main evidence is simulated;
- "human" if the experiment uses only a scripted oracle, unless clearly labeled.
