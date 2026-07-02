# Annotated Related Work — FORESIGHT-HIL

Grouped by axis. Each entry: **takeaway** + *relation to us* (how we differ / build on it).
Keys match `references.bib`.

## A. Human-in-the-loop RL for manipulation (the core line we extend)

- **HIL-SERL** [`luo2025hilserl`] — Real-robot vision RL: sparse-reward classifier + SpaceMouse interventions + RLPD; near-perfect success in 1–2.5 h. *Our system backbone & primary baseline; human decides timing — we make it model-predictive & budgeted.*
- **PACT** [`liu2026pact`] — Treats intervention-containing trajectories as heterogeneous; progress model locates suboptimal segments; counterfactual preference penalizes Bellman targets. *We replace single-point directional credit with model-based counterfactual rollouts; orthogonal to our trigger.*
- **SERL** [`luo2024serl`] — Software suite for sample-efficient real-robot RL; provides `franka_sim`. *Open-source + sim backbone.*
- **UniIntervene** [`uniintervene2026`] — Agentic, model-free trigger via future-conditioned action-value + temporal value-risk; retrieves recovery targets; −57% human interventions. *Closest competitor; ours uses an explicit dynamics ensemble for anticipatory VoI and adds parallel budgeting.*
- **SiLRI** [`silri2025`] — State-wise Lagrangian trust between human (low-entropy) vs RL (high-entropy); robust to suboptimal interventions; notes timing strongly affects convergence. *Motivates our robustness-to-imperfect-human objective; we add proactive triggering.*
- **OHP-RL** [`ohprl2026`] — State-dependent preference gate; interventions as online preferences. *Feeds our modality-selection module.*
- **ROVE** [`rove2026`] — Humanoid VLA post-training; optimistic value estimation from mixed-quality data; cross-embodiment critic from human videos. *Mixed-quality-data handling relevant to robustness.*
- **Sirius** [`liu2023sirius`] — Human-in-the-loop autonomy *during deployment*; trust-weighted behavioral cloning re-weights samples by approximate human trust. *Closest "learn-while-deployed" cousin; reactive human-gated takeover (no anticipatory VoI / budget) — the gap we fill.*

## B. Robot-/uncertainty-gated requesting (who/when to ask)

- **AIM** [`cai2025aim`] — Robot-gated interactive IL; proxy-Q mimics human intervention rule; −40% takeover cost vs Thrifty-DAgger. *IL setting; we operate in model-based RL with VoI.*
- **Thrifty-DAgger** [`hoque2021thrifty`] — Novelty/risk-based query in interactive IL. *Reactive, uncertainty-only; we add model lookahead + budget.*
- **MILE** [`mile2025`] — Model of *when/how* humans intervene; learns from non-intervention timesteps too. *We infer transferable intent, not just timing.*
- **AC-Teach** [`kurenkov2019acteach`] / **APIL multi-teacher** [`zhang2020apil`] — Leverage ensembles of suboptimal/non-deterministic teachers via Bayesian critic / progress-aware querying. *Relevant if we extend to "who to ask".*

## C. World models + human / correction

- **Hi-WM** [`hiwm2026`] — Human edits rollouts inside an action-conditioned world model; cache/rewind/branch for dense recovery data. *WM as offline data factory; ours uses WM online for triggering & credit.*
- **VLA-in-the-Loop** [`vlaintheloop2026`] — Lightweight composite WM as on-demand corrector for VLA grasping. *Event-triggered correction; complements our trigger.*

## D. Model-based RL foundations (sample efficiency + the instrument for VoI)

- **Moerland survey** [`moerland2023mbrl`] — Dynamics-model learning + planning/learning integration + implicit MBRL. *Design space for our ensemble/latent model.*
- **Luo (NJU) survey** [`luo2022mbrlsurvey`] — Model generalization error; value-/policy-aware model learning; offline & meta MBRL. *Justifies value-aware models and our transfer angle.*
- **Hybrid Control (MB+MF)** [`pinosky2022hybrid`] — Optimal switching by model–policy agreement/uncertainty. *Generalized to human–model–policy gating.*
- **RLPD** [`ball2023rlpd`] — Efficient online RL with offline data (50/50 sampling). *Underlying learner in HIL-SERL/PACT and ours.*
- **PETS** [`chua2018pets`] — Probabilistic ensembles + trajectory sampling; epistemic vs aleatoric. *Our uncertainty source.*
- **DreamerV3** [`hafner2023dreamerv3`] — Scalable latent world model. *Option for contact-rich latent rollouts.*
- **MBPO** [`janner2019mbpo`] — "When to trust your model": short model rollouts branched from real data. *Bounds the lookahead-horizon trade-off our trigger inherits.*

### World models for control / manipulation (rollout-engine options, M3)

- **TD-MPC2** [`hansen2024tdmpc2`] — Decoder-free latent world model + local trajectory optimization; one hyperparameter set across 104 tasks; capability scales with model/data. *Top candidate to replace Module A's MLP-ensemble rollout engine for longer-horizon contact-rich foresight; also grounds X2 (query-savings scaling).*
- **MuZero** [`schrittwieser2020muzero`] — Learns reward/value/policy model sufficient for planning, not next-state pixels. *Canonical value-equivalent model; motivates M1's decision-aware objective.*
- **DayDreamer** [`wu2022daydreamer`] — DreamerV3 world model trained directly on 4 physical robots (incl. reset-free quadruped). *Evidence latent WMs work on real contact dynamics; supports the WM-rollout option.*
- **IRIS** [`micheli2023iris`] / **TWM** [`robine2023twm`] / **STORM** [`zhang2023storm`] — Transformer/discrete-latent world models, Atari-100k sample-efficient. *Pixel-domain longer-horizon imagination; reference points for the WM-foresight swap (heavier than state-based for contact).*
- **DIAMOND** [`alonso2024diamond`] — Diffusion world model preserving visual detail; strong Atari-100k. *Diffusion-WM option; pixel-centric, used to scope M3 feasibility/risk.*

### Decision-aware / value-equivalent model learning (the M1 instrument)

- **VAML** [`farahmand2017vaml`] / **IterVAML** [`farahmand2018itervaml`] — Model loss that respects the value function, with finite-sample error bounds (IterVAML). *Theoretical backbone of M1's value-equivalent loss term and of the X1 model-error → budget-regret glue.*
- **Value-Equivalence Principle** [`grimm2020valueequiv`] — Two models are equivalent if they induce the same Bellman updates; the equivalent class shrinks as policies/functions grow. *Formal justification for fitting the trigger model only where it changes the gate.*
- **Wasserstein↔VAML** [`asadi2018wasserstein`] — Minimizing VAML ≡ minimizing a Wasserstein distance. *Connects our value-aware term to a tractable metric.*
- **Model-Advantage VAML** [`modhe2021modeladvantage`] — Practical value-aware objective (model-advantage bound) that works in continuous control on SLBO/MBPO. *Shows value-aware losses are deployable; recipe we adapt for the ensemble.*
- **λ-models** [`voelcker2023lambda`] — Decision-aware RL needs latent models to work empirically; MuZero loss is biased in stochastic envs. *Directly motivates keeping the MLE anchor (β<1) in M1 to stay stable under contact noise.*

## E. HITL position / explainability

- **Retzlaff et al.** [`retzlaff2024hitl`] — RL is fundamentally HITL; 4 phases (develop/learn/evaluate/deploy); explainability requirements. *Conceptual framing for when/why humans are involved.*

## F. Shared autonomy / HIL-RL in autonomous driving (cross-domain prior art, in case of pivot)

- **HACO** [`li2022haco`] — Human-AI copilot optimization; human-gated takeover in MetaDrive.
- **HAIM-DRL** [`huang2024haim`] — Human-as-AI-mentor; reward-free proxy values; minimal intervention.
- **SafeHIL-RL** [`huang2024safehil`] — Frenet dynamic potential field for safe intervention assessment; curriculum guidance; robust to guidance quality.
- **PE-RLHF** [`huang2024perlhf`] — Human feedback + physics knowledge with a trustworthy performance bound under imperfect feedback.
*All human-gated and/or non-model-predictive triggering → the same gap our VoI trigger fills, should we pivot to driving.*

## G. Query-budget / interactive theory (for an optional theory result)

- **Asking-for-Help under irreversible dynamics** [`asking2025help`] — Sublinear regret AND sublinear mentor queries via state-transfer; self-sufficiency proof. *Template for a budgeted VoI bound.*
- **Multi-source imperfect preferences** [`multisource2026`] — Regret \(\tilde O(\sqrt{K/M}+\omega)\) under per-source imperfection budget. *Robustness-to-imperfect-human theory analogue.*
- **Online exploration for RLHF** [`onlinerlhf2025`] — Principled query selection / exploration with provable guarantees. *D-optimal-design view of which queries to spend budget on.*

## H. Plasticity / sample-efficiency / offline→online (training-side, T1/T2)

- **Primacy Bias** [`nikishin2022primacy`] — Early data permanently caps later learning in deep RL; periodic resets fix it. *The core pathology HIL's bursty correction data + high UTD triggers; resets are our T1 mechanism.*
- **ReDo** [`sokar2023redo`] — Dormant-neuron phenomenon; recycle inactive units to preserve expressivity. *Targeted, low-disruption plasticity tool we apply to the actor/critic/dynamics head.*
- **BBF** [`schwarzer2023bbf`] — Scales sample-efficient Atari RL via resets + higher replay ratio. *Demonstrates plasticity care unlocks high-UTD scaling — the regime our learner runs in.*
- **Understanding Plasticity** [`lyle2023plasticity`] — Mechanistic study: plasticity loss tied to loss-landscape curvature; parameterization/optimizer fixes. *Diagnostics & design choices for T1.*
- **Maintaining Plasticity** [`dohare2024plasticity`] — Continual backprop reinitializes least-used units to keep plasticity indefinitely. *Continual-learning lens on intervention-induced distribution shift.*
- **REDQ** [`chen2021redq`] — Model-free high-UTD (≫1) via Q-ensemble + in-target minimization. *Reference for running the RLPD learner at high UTD safely.*
- **Cal-QL** [`nakamoto2023calql`] — Calibrated value init (lower-bound learned, upper-bound reference) for fast offline→online. *Calibration framing we port from the value fn to the trigger (M2) and to T2 budget allocation.*

## I. Calibration & active querying / information gain (M2, T4)

- **Guo et al., Calibration of NNs** [`guo2017calibration`] — Modern nets are miscalibrated; temperature/Platt scaling fixes it; ECE/reliability diagrams. *Exact toolkit for M2 (calibrating the trigger's predicted-failure probability so one τ transfers across envs).*
- **Deep Bayesian Active Learning** [`gal2017activelearning`] — Uncertainty-driven acquisition functions (BALD) for label-efficient learning. *Information-gain machinery behind D-optimal feedback-modality selection (T4).*

## J. Preference-based RL (feedback-efficiency + imperfect teachers)

- **SURF** [`park2022surf`] — Semi-supervised + augmentation reward learning to cut preference queries. *Feedback-efficiency technique for Module C's preference modality.*
- **B-Pref** [`lee2021bpref`] — Benchmark that *simulates irrational/imperfect teachers* and metrics for robustness to them. *Directly supports our imperfect-human family and robustness evaluation protocol.*

## K. Reset-free recovery & system tooling

- **Leave no Trace** [`eysenbach2018leavenotrace`] — Joint forward+reset policies; reset value fn flags impending irreversible states for uncertainty-aware aborts. *Template for instantiating Module A's "self-recover" branch and recover-vs-query margin (T3).*
- **robomimic** [`mandlekar2021robomimic`] — What matters in offline learning from human demos; reproducible datasets/algos. *Offline-data backbone & fair-comparison reference.*
- **ManiSkill3** [`tao2025maniskill3`] — GPU-parallel contact-rich manipulation sim (30k+ FPS), TD-MPC2/PPO/SAC baselines. *Candidate substrate for Module B's cross-env budget allocation (alternative to MJX).*
- **MBRL-Lib** [`pineda2021mbrllib`] — PETS/MBPO ensembles + planners. *Reusable model-based components for the ensemble/dynamics head.*
- **CleanRL** [`huang2022cleanrl`] / **d3rlpy** [`seno2022d3rlpy`] / **LeRobot** [`cadene2026lerobot`] — Single-file RL baselines / offline-RL library / end-to-end robot-learning stack. *Implementation references; LeRobot situates the system-artifact contribution.*

## L. VLA + world-model coupling (M4 surrogate-human direction)

- **WorldVLA** [`cen2025worldvla`] — Unified autoregressive action+world model; action and world model mutually improve. *Evidence the WM can predict action-conditioned futures tightly — basis for "imagine the human's correction" (M4).*
- **RynnVLA-002** [`cen2025rynnvla2`] — Unified VLA + world model; integrated WM boosts real-robot success ~50%. *Reinforces the action↔WM coupling M4 exploits to cut real queries.*
