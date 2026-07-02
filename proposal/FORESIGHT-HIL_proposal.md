# FORESIGHT-HIL: Foresighted, Budget-Aware Human-in-the-Loop RL via Model-Based Value-of-Information

> Working title (tentative). Target venue: SCI Q1 journal in HIL-RL / model-based RL / engineering AI, with robotics-relevant validation.
> Evidence strategy: simulation-first, hardware-optional. **Primary:** MuJoCo/robosuite and other control/manipulation tasks; **parallel-budget headline:** MJX or ManiSkill-style GPU-parallel simulation on a single RTX 4090; **optional validation:** Isaac Lab or a small real-robot task if hardware time becomes available.
> Application anchor: contact-rich robotic manipulation (currently wired on robosuite `Lift`; extendable to insertion/assembly + Allegro/Shadow in-hand reorientation), while the formulation remains a general budgeted HIL-RL method.

---

## 1. One-paragraph pitch

Human-in-the-loop RL (HIL-RL) can make learning safer and more sample-efficient, but it is **supervision-bound**: a human cannot continuously monitor every rollout or decide intervention timing at scale. State-of-the-art systems (HIL-SERL, PACT, UniIntervene, SiLRI, OHP-RL) study *how to use* intervention data or auto-recover, yet most assume a **single agent/robot, single human, sequential** setting and rely on reactive intervention timing. We reframe intervention as a **decision-theoretic, budget-constrained Value-of-Information (VoI) problem under a learned dynamics/world model**: the agent rolls its policy forward in an ensemble world model, estimates the **expected cost of impending failure** and its **epistemic uncertainty**, and *proactively* decides, for each state and across many parallel rollouts, whether to (i) continue, (ii) self-recover with a model-based controller, or (iii) **spend a scarce query** on the human. We further (a) make the trigger **robust to imperfect humans** (delay / noise / over- or under-intervention) and (b) optionally let the agent choose **which feedback modality** to request (corrective action vs. preference vs. success label) to maximize information per unit human effort. The result is a general HIL-RL framework answering **when to ask, whom/what to ask, and how to be robust**, with robotics-relevant manipulation tasks serving as a demanding validation domain rather than the only scope of the method.

---

## 2. Background & the 6 seed papers

| # | Paper | Role in this proposal |
|---|-------|------------------------|
| 1 | Moerland et al., *Model-based RL: A Survey* (2022) | Taxonomy of dynamics-model learning + planning/learning integration → our world-model design space |
| 2 | Luo et al. (NJU), *A Survey on Model-based RL* (2022) | Model generalization error → model usage / value-aware learning; offline & meta MBRL → our transfer angle |
| 3 | Retzlaff et al., *HITL RL: A Survey & Position* (JAIR 2024) | 4 phases of human involvement; "RL is fundamentally HITL"; explainability → *when/why* to involve humans |
| 4 | Pinosky et al., *Hybrid Control: combining MB & MF RL* (IJRR 2023) | Model–policy agreement / uncertainty switching → generalized into a **human–model–policy** gate |
| 5 | Luo, Levine et al., *HIL-SERL* (Science Robotics 2025) | Open-source HIL-RL system (RLPD + interventions) → our **baseline & system backbone** |
| 6 | Liu et al., *PACT* (2026) | Preference-calibrated credit reassignment on suboptimal segments → our **"how to use"** baseline |

**Two legs of the seed set** — *model-based RL* (#1,#2,#4) for sample efficiency and *human-in-the-loop RL* (#3,#5,#6) for guidance — are bridged here by treating the **learned model as the instrument that decides human involvement**.

## 3. Gap analysis (why this is novel in mid-2026)

The 2026 literature is crowded but along **specific axes**:

- **HOW to use intervention data** — PACT (segment credit), SiLRI (state-wise Lagrangian trust), OHP-RL (preference gate), ROVE (optimistic value, mixed-quality). *Crowded.*
- **Auto-recovery / who acts** — UniIntervene (value-risk trigger + recovery policy), AIM (robot-gated proxy-Q). *Crowded, but model-free & reactive.*
- **World model + human** — Hi-WM (human edits inside a world model, offline data factory), VLA-in-the-Loop (WM as corrector). *Different goal (data generation), not online triggering.*
- **Driving shared autonomy** — HACO, HAIM-DRL, SafeHIL-RL, PE-RLHF. *Human-gated takeover; imperfect-human handled via APF/physics, not model-based VoI.*
- **Theory** — query-budget regret (Safe-Learning-by-Asking-for-Help 2025; multi-source preferences 2603). *Owned by theorists; abstract.*

**Open cells we target:**
1. **Anticipatory, model-predictive triggering** (predict failure *before* it manifests) via a learned **dynamics ensemble + epistemic uncertainty**, formalized as **VoI**. (vs. UniIntervene's reactive, model-free value-stagnation trigger.)
2. **Budgeted query allocation across massively-parallel learning rollouts** — a problem exposed by large-scale simulation and especially relevant to robotics-style parallel training (MJX / ManiSkill / Isaac Lab), but formulated as a general HIL-RL budget-allocation problem.
3. **Robustness to imperfect-human timing/quality distribution shift** — flagged by SiLRI as decisive, never solved as a first-class objective (simulation lets us *control & sweep* the human model — a strength, not a weakness).
4. **Feedback-modality selection** — choose the cheapest informative feedback type per state (almost untouched in HIL-RL).

**Deepening the model and the learner (vs. treating them as black boxes).** Prior HIL-RL work — and our own first draft — drove the trigger from an off-the-shelf MLE/PETS ensemble and an off-the-shelf RLPD learner. Three further open cells make the *instrument* itself part of the contribution, raising the bar from "a clever decision policy" to a *model-and-training co-designed* HIL system:

5. **Decision-aware (value-equivalent) dynamics for the trigger (M1).** The trigger needs predictions that change the *decision* (continue / recover / query), not raw next-state accuracy; an MLE model spends capacity (and uncertainty) on decision-irrelevant detail. We add an IterVAML/value-equivalence-style loss term (Farahmand, NeurIPS 2018; Grimm et al., *Value-Equivalence Principle*, NeurIPS 2020, arXiv:2011.03506; cf. λ-models, arXiv:2306.17366) so model error and ensemble disagreement concentrate where they *flip the gate*. Decision-aware models exist, but *driving a human-query VoI trigger with one* is new.
6. **Calibrated trigger uncertainty so one threshold transfers (M2).** VoI scales failure-cost by ψ(u(s)); if `u` is miscalibrated, τ must be re-tuned per env and the cross-env budget (Module B) is mis-spent. We calibrate the trigger's predicted-failure signal (temperature/Platt scaling; reliability-diagram + ECE), in the calibration spirit of Cal-QL (Nakamoto et al., NeurIPS 2023, arXiv:2303.05479) but applied to the *trigger* rather than the value function. No HIL work calibrates the trigger's uncertainty.
7. **Plasticity under intervention-induced distribution shift (T1).** HIL injects *bursts* of off-distribution correction data at high update-to-data ratios — exactly the regime that triggers primacy bias / loss of plasticity / dormant neurons (Nikishin et al., ICML 2022, arXiv:2205.07802; ReDo, Sokar et al., ICML 2023, arXiv:2302.12902; BBF, Schwarzer et al., ICML 2023, arXiv:2305.19452). No HIL-RL paper studies this, yet a plastic learner needs *fewer* queries to recover — coupling training health directly to our human-cost objective.

## 4. Problem formulation

### 4.1 Budgeted Interactive MDP (BI-MDP)
Augment an MDP \( \mathcal{M}=(\mathcal{S},\mathcal{A},P,r,\gamma) \) with:
- a **human/oracle operator** \( \mathcal{H} \) that, when queried at state \(s\), returns feedback \(f\) of a chosen modality \(m\in\mathcal{F}\) at cost \(c_m\) (human time / cognitive load);
- a per-round **query budget** \(B\) shared across \(N\) parallel environments;
- a learned **ensemble dynamics model** \(\{\hat P_{\phi_k}\}_{k=1}^{K}\) (or a latent world model) and value function \(Q_\theta\).

Objective: maximize task return **subject to** total queries \(\le B\) (equivalently, a Pareto front of *success rate* vs. *human cost*), while being robust to a family of human models \(\mathcal{H}\in\Pi_H\) (varying skill, delay, noise, intervention bias).

### 4.2 Decision at each (env, state)
A 3-way gate \( g(s)\in\{\texttt{continue},\texttt{self-recover},\texttt{query-human}\} \) chosen by comparing model-based VoI against query cost (see §5.2).

## 5. Method (three modules)

### Module A — Foresighted VoI Trigger (*when to ask*)
1. From \(s_t\), roll the current policy \(H\) steps in each ensemble member; estimate:
   - **predicted failure cost** \( \widehat{C}(s_t)=\mathbb{E}_{\hat P,\pi}[\text{cost of terminal/irrecoverable state within } H] \);
   - **epistemic uncertainty** \( u(s_t)= \) ensemble disagreement on returns/next-states.
2. Estimate the counterfactual cost **if the human corrected**, \( \widehat{C}_{\mathcal H}(s_t) \), from a learned human-advantage model.
3. **Value of Information**: \( \text{VoI}(s_t)=\big(\widehat{C}(s_t)-\widehat{C}_{\mathcal H}(s_t)\big)\cdot \psi(u(s_t)) - c_m \), where \(\psi\) up-weights uncertain states.
4. Gate: query if \( \text{VoI}>\tau \); else self-recover if a model-based recovery has positive margin; else continue.
   *Generalizes Pinosky's model–policy agreement to a human–model–policy gate.*

**Decision-aware dynamics for the trigger (M1).** Rather than fitting the ensemble purely to next-state likelihood, we add an *optional* value-equivalent / IterVAML loss term so the model is accurate where it matters for the gate. For a transition \((s,a,s')\) and a value estimate \(V\) (we use \(V(s)=\min_i Q_{\theta_i}(s,\pi(s))\) from the RLPD critic), each member \(\hat P_{\phi_k}\) minimizes
\[ \mathcal L_k = (1-\beta)\,\underbrace{\lVert \hat s' - s' \rVert^2}_{\text{MLE / PETS anchor}} \;+\; \beta\,\underbrace{\lVert V(\hat s') - V(s') \rVert^2}_{\text{value-equivalent term}},\qquad \hat s' = s + \hat P_{\phi_k}(s,a). \]
The MLE anchor is always retained (\(\beta<1\)) because pure value-aware losses can be unstable under stochastic/contact dynamics (documented for λ-models, arXiv:2306.17366); \(\beta=0\) recovers the original MLE ensemble exactly. This concentrates both the model's error *and its ensemble disagreement* \(u(s)\) on decision-relevant regions, tightening the VoI signal the gate reads. Grounded in VAML/IterVAML (Farahmand et al.) and the Value-Equivalence Principle (Grimm et al., arXiv:2011.03506). *Headline ablation: MLE vs. value-equivalent model driving the **same** gate (§6.5).*

### Module B — Budgeted Allocation across N parallel rollouts (*parallel-sim headline; MJX/ManiSkill on a single 4090, Isaac Lab optional*)
Given per-env \( \text{VoI}_i \) and budget \(B\), select the top-\(B\) (or solve a knapsack/submodular selection accounting for redundancy among similar states). Study **calibration**: do the queried states correspond to *actually* failing trajectories (precision/recall of the trigger)? This is the new scientific object enabled by parallelism.

**Calibrated trigger uncertainty for a transferable threshold (M2).** Comparing \( \text{VoI}_i \) across heterogeneous envs is only meaningful if the trigger's predicted-failure probability \(p_\text{fail}(s)\) is *calibrated* — i.e. states assigned probability \(q\) fail about a \(q\) fraction of the time. We therefore (i) **log a reliability diagram and Expected Calibration Error (ECE)** for the event "trigger fires ⇔ true impending failure" (turning §6.4's promised metric into a principled diagnostic), and (ii) optionally apply **temperature / Platt scaling** \(p_\text{cal}=\sigma(\,\text{logit}(p_\text{fail})/T\,)\) fit on held-out (trigger, outcome) pairs. Calibrated probabilities let a **single** threshold τ transfer across the \(N\) parallel envs instead of being re-tuned per env, so the shared budget is spent on genuinely failure-prone states. Calibration framing follows Cal-QL (arXiv:2303.05479), here applied to the *trigger* rather than the value function; the PETS ensemble (arXiv:1805.12114) supplies the raw uncertainty.

### Module C — Robust + Multi-modal use of feedback (*what to ask & robustness*)
- **Robustness**: model the human as a noisy/delayed policy; use an uncertainty-aware trust weight (cf. SiLRI/PE-RLHF) so corrupted feedback cannot destabilize training; evaluate under a *sweep* of human models.
- **Modality selection**: pick \(m\in\{\text{corrective action}, \text{preference pair}, \text{success label}\}\) maximizing expected info per cost \(c_m\); reuse PACT-style preference-calibrated credit for the chosen modality.
- **Credit assignment**: model-based **counterfactual advantage** (roll the "no-mistake" branch) to correct Bellman targets — a tighter alternative to PACT's single-point directional penalty.

### Module D — Plasticity-preserving learner under intervention shift (*training-side, T1*)
The RLPD learner (and the dynamics ensemble) are trained at a high update-to-data ratio on a replay stream that receives **bursts** of off-distribution expert/correction transitions whenever the gate fires. This is precisely the setting that induces **primacy bias / loss of plasticity / dormant neurons** (Nikishin et al., arXiv:2205.07802; ReDo, arXiv:2302.12902; BBF, arXiv:2305.19452), where early or skewed data permanently caps the network's capacity to fit later data. We add an *optional* plasticity-preservation mechanism:
- **ReDo-style dormant-unit recycling** — periodically estimate each unit's normalized activation; reinitialize the incoming weights of dormant units and zero their outgoing weights so they re-enter learning without perturbing current outputs.
- **Periodic shrink-and-perturb / partial reset** — soft-reset a fraction of parameters (and their optimizer moments) on a fixed schedule.
Applied to the actor/critic and/or the dynamics head, this keeps the learner plastic across intervention-induced distribution shift. The hypothesis tying it to our headline objective: **a more plastic learner recovers from each intervention with fewer subsequent queries**, so plasticity care *lowers total human cost* to reach a success threshold. This is, to our knowledge, the first study of plasticity × HIL.

## 6. Experimental design

### 6.1 Simulators & tasks
- **MuJoCo / robosuite (primary, portable)**: robotics-relevant contact-rich manipulation — currently wired on **robosuite `Lift`** (single Panda, OSC_POSE), extending to peg/PCB insertion, pick-place, assembly (robosuite/Meta-World). Matches the HIL-SERL/PACT line for comparability and runs on the laptop 4090.
- **MJX / ManiSkill-style GPU-parallel simulation — the parallel-budget headline**: many vectorized control/manipulation rollouts on a single RTX 4090, used for Module B's budget allocation and trigger-calibration figures.
- **Isaac Lab or real robot (optional validation)**: Franka insertion/assembly, Allegro/Shadow in-hand reorientation, or a small physical-arm task if hardware time becomes available.

### 6.2 Simulated human (the feasibility crux → also a contribution)
- **Oracle expert** = privileged-state scripted controller / motion planner / pre-trained expert policy.
- **Human-model family \(\Pi_H\)**: clean oracle; + action noise \(\sigma\); + reaction delay \(d\); + over-intervention / under-intervention bias; + locally-inconsistent (mixture) experts. Released as a **reproducible HIL protocol**.

### 6.3 Baselines
RLPD (no human) · HIL-SERL · PACT · SiLRI · OHP-RL · UniIntervene · AIM/Thrifty-DAgger (robot-gated request).

### 6.4 Metrics
- Success rate & sample efficiency (return vs. env steps).
- **Human cost**: #queries / #intervention steps to reach a success threshold (our main win).
- **Pareto front**: success vs. human cost (the proposed canonical metric).
- **Trigger calibration**: precision/recall of "query ⇔ true impending failure"; reliability diagram.
- **Robustness curves**: performance vs. human-model degradation (\(\sigma, d\), bias).

### 6.5 Ablations
Lookahead \(H\) · ensemble size \(K\) · VoI threshold \(\tau\) · anticipatory vs. reactive trigger · model-based counterfactual credit on/off · budget \(B\) and allocation strategy (top-\(B\) vs. submodular) · feedback-modality selection on/off · ground-truth-model upper bound.

**Model-and-training co-design ablations (M1 / M2 / T1):**
- **M1 — decision-aware model (headline).** MLE/PETS ensemble vs. value-equivalent ensemble driving the *same* VoI gate; sweep the mixing coefficient \(\beta\in\{0,0.25,0.5,1\}\) (\(\beta=0\) reproduces the current MLE run exactly). Report queries-to-threshold and trigger precision/recall to show the model serving the *decision* rather than next-state MSE.
- **M2 — trigger calibration.** Reliability diagram + ECE/MCE/Brier for "fire ⇔ true impending failure", raw vs. temperature/Platt-scaled; and the key transfer test: **a single τ across all \(N\) envs** with vs. without calibration (mis-spent-query rate).
- **T1 — plasticity.** Reset on/off (ReDo vs. shrink-and-perturb vs. none) under matched UTD; track dormant-unit fraction over training and, crucially, **queries needed to hit the success threshold** with vs. without plasticity care, plus a sweep of intervention burstiness.

*All three are exposed as default-OFF flags (`--dyn_value_aware`, `--plasticity`, `--calibrate`) so the baseline configuration is byte-for-byte the current system.*

## 7. Expected contributions
1. **BI-MDP formulation** of HIL-RL as budgeted, model-based VoI (when/whom/what unified).
2. **FORESIGHT-HIL algorithm**: foresighted trigger + parallel budget allocation + robust multi-modal feedback use.
3. **Query-budget allocation across massively-parallel learning rollouts** — a robotics-relevant but generally formulated problem, evaluated with success-vs-human-cost Pareto fronts and trigger calibration.
4. **Reproducible simulated-HIL protocol** with a controllable imperfect-human family.
5. Empirical evaluation of **human cost** at matched success or matched budget against PACT/UniIntervene/SiLRI-style baselines, random allocation, and reactive triggers, with robustness analysis.
6. **Decision-aware (value-equivalent) dynamics for the trigger (M1)** — the first use of an IterVAML/value-equivalence model to *power a human-query VoI gate*, with a clean MLE-vs-value-equivalent headline ablation isolating the effect of model objective from model quality.
7. **Calibrated triggering (M2)** — reliability-diagram/ECE diagnostics and temperature/Platt scaling that make a **single VoI threshold transfer** across many parallel envs (Module B), turning a promised metric into a principled mechanism.
8. **Plasticity-preserving HIL training (T1)** — the first study coupling plasticity loss (resets/ReDo) to intervention-induced distribution shift, with the thesis (and measurement) that plasticity care *reduces total human queries* to a success threshold.

*Together (6–8) deepen the contribution from "a clever decision policy" to a **model-and-training co-designed** HIL system: the dynamics model is optimized for the decision, its uncertainty is calibrated for transfer, and the learner stays plastic so each human query buys more. All three are additive, default-OFF options over the base system.*

## 8. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Dynamics model error in contact-rich tasks | short-horizon rollouts; latent world model (Dreamer-style); ground-truth-model **upper-bound ablation** to isolate the idea from model quality |
| "Is the simulated human credible?" (reviewer) | multi-model human family + sensitivity sweep; clearly label scripted-oracle results; add optional small real-robot or human-teleoperation validation if available |
| SCI Q1 reviewers may see the work as too simulator-specific | position as **algorithmic + decision-theoretic + analysis + benchmark**, with robotics-relevant tasks as validation rather than the only scope; add a light VoI/budget-regret argument if it remains clean |
| Overlap with UniIntervene/PACT | differentiation table (§3): model-based *anticipatory* trigger + *budgeted parallel* allocation + *robustness* are all outside their scope |
| Compute / Isaac Lab on Windows | Do the parallel-budget headline with **MJX** (GPU-parallel MuJoCo) on the laptop 4090 — no Isaac/Omniverse needed; single-env robosuite covers most ablations; Isaac Lab is optional extra scale via WSL2/Linux. |

## 9. Timeline (≈ 5–6 months)
> (Month labels to avoid clashing with the M1/M2 model-upgrade names above.)
1. **Month 1** *(in progress)*: MuJoCo/robosuite + scripted-oracle HIL harness; HIL-SERL-style baseline; metrics & logging. *(harness + smoke run done; full `voi`/`always` runs training now.)*
2. **Month 2**: ensemble dynamics model + foresighted VoI trigger (Module A) + decision-aware model (M1) + trigger calibration (M2); single-env results.
3. **Month 3**: MJX/ManiSkill-style vectorized port; budgeted parallel allocation (Module B); the headline budget-vs-success + calibration experiment.
4. **Month 4**: robustness sweep + multi-modal feedback (Module C) + plasticity (T1); full ablations.
5. **Month 5**: (optional) theory result; writing; figures; journal-style limitations and reproducibility package.
6. **Month 6**: buffer / optional Isaac Lab scale-up (WSL2) / optional real-robot demo / SCI Q1 submission package.

## 10. Implementation status & next steps

**Done**
- [x] Project scaffold (`foresight_hil/`) + dependency-light runnable prototype (ensemble dynamics + VoI gate + budgeted allocation + scripted oracle); smoke test passes.
- [x] Annotated related work (`related_work.md`) + **verified** `references.bib` (74 entries, audited in `citation_audit.md`; no placeholder/anonymous authors).
- [x] Innovation/gap scan (`innovation_gaps.md`, 11 ranked angles).
- [x] robosuite/MuJoCo backend wired (Lift, Panda, OSC_POSE) + HIL-SERL-*style* loop (SAC + RLPD-style demo/online buffers + scripted-oracle interventions); end-to-end smoke run on the 4090.
- [x] M1/M2/T1 implemented as default-OFF flags (`--dyn_value_aware`, `--calibrate`, `--plasticity`).

**In progress**
- [~] Full `voi` + `always` runs (Lift, 150k steps, seed 0) → first full-run success-vs-human-cost numbers + trigger precision/recall.

**Next**
- [ ] Add `none` + `random` strategies and seeds 1–2; produce the success-vs-human-cost Pareto + calibration plots.
- [ ] MJX or ManiSkill-style vectorized port for the parallel-budget headline (Module B).
- [ ] Run the M1/M2/T1 ablations against the byte-identical baseline.
- [ ] Re-verify the ◐-flagged arXiv IDs from `innovation_gaps.md` before importing any into `references.bib`.
- [ ] (Optional) Isaac Lab scale-up via WSL2; (optional) VoI/regret theory bound.
