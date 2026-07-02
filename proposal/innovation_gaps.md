# FORESIGHT-HIL — Deeper Research Gaps & Innovation Angles

> Purpose: extend the existing proposal with **model-side** and **training-side** innovation
> angles that *deepen* or are *genuinely new* relative to the four claimed novelties
> (foresighted model-based VoI "when-to-ask" trigger; budgeted query allocation across many
> parallel sim envs; robustness to imperfect humans; model-based counterfactual credit
> assignment). Setting assumed: **sim-only** (robosuite/MuJoCo, optional Isaac Lab/MJX),
> single **RTX 4090 Laptop (16 GB)**, top-venue target.
>
> Accuracy note: every paper/repo below was checked against arXiv / OpenReview / PMLR /
> GitHub during this pass. arXiv IDs that were confirmed on the page are given bare; IDs taken
> from a search-result synthesis (not the primary page) are flagged "(ID per arXiv listing)".
> Items I could not fully confirm are flagged "(unverified)". Nothing here should be copied
> into `references.bib` without a final per-entry check — see the candidate-additions section.

---

## 1. Design-space map (filled vs. open cells)

Rows = research questions a HIL-RL system must answer. Columns mark whether the FORESIGHT-HIL
proposal already covers it, whether the *literature* covers it, and where the open cells are.

| Question / axis | Covered by proposal? | Nearest prior art (verified) | Open cell we can still take |
|---|---|---|---|
| **When** to ask the human | Yes — model-based VoI trigger (Module A) | UniIntervene, AIM, Thrifty-DAgger, EnsembleDAgger | *What model* powers the trigger (decision-aware vs MLE); *uncertainty calibration* of the trigger |
| **What/whom** to ask (modality) | Partly — modality selection (Module C) | OHP-RL, PEBBLE (2106.05091), DPO (2305.18290), Christiano (1706.03741) | Active/D-optimal *query selection* per modality; language feedback |
| **How** to use feedback (credit) | Yes — model-based counterfactual credit | PACT, SiLRI, ROVE | (leave as-is; do not re-propose) |
| **Budget** allocation across N envs | Yes — Module B headline | none in HIL-RL (new) | Couple allocation to *value calibration* / curriculum |
| **Dynamics model** objective | No — uses MLE-style ensemble (PETS) | VAML, IterVAML, Value-Equivalence, λ-models, MuZero, TD-MPC2 | **Decision/VoI-aware model learning** for the trigger (open) |
| **Rollout engine** for foresight | Partial — short-horizon ensemble; DreamerV3 noted | TD-MPC2 (2310.16828), DIAMOND (2405.12399), IRIS, STORM, TWM | Latent/diffusion/transformer WM for **longer-horizon contact-rich** anticipation |
| **Sample efficiency / UTD** | Implicit (RLPD) | RLPD (h11j9w1ucU), BBF (2305.19452) | **Plasticity loss under intervention-induced distribution shift** (open) |
| **Offline→online** init | Implicit (RLPD prior data) | Cal-QL (2303.05479) | Calibration-driven budget spending (open) |
| **Reset-free / autonomous** recovery | Partial — "self-recover" branch | EARL (2112.09605), Reset-Free (2104.11203), Walk-in-Park (2208.07860) | Use reset-free policy *as* the self-recover instrument under VoI |
| **Imagined human feedback** | No | Hi-WM (data factory), MILE (intervention model) | **World-model-as-human-surrogate** to cut real queries (open) |
| **Theory** | Optional VoI/regret note | Asking-for-Help (2502.14043), Multi-source prefs (2603.20453), IterVAML bound | **Decision-aware model error → VoI/budget-regret bound** (open) |
| **Scaling laws** for human cost | No | TD-MPC2 scaling, BBF scaling | How query savings scale with WM/data size (open analysis) |

**Takeaway.** The proposal is strong on *decision policy* (when/what/budget/credit) but treats the
**dynamics model and the learner as black boxes**. The richest untaken cells are exactly there:
*what kind of model* drives the trigger, *how well-calibrated* its uncertainty is, and *how the
HIL data stream interacts with sample-efficient training (plasticity, UTD, offline→online)*.

---

## 2. GitHub landscape — what each repo gives you, and the gap it leaves

| Repo | URL | Provides | Missing (gap to fill) |
|---|---|---|---|
| HIL-SERL / SERL | github.com/rail-berkeley/hil-serl · github.com/rail-berkeley/serl | RLPD + human-intervention loop, `franka_sim`, classifier rewards | No *anticipatory* trigger, no budget, no model-based foresight, single human/robot |
| LeRobot | github.com/huggingface/lerobot | PyTorch policies, datasets, hardware, sim bridges | No HIL VoI triggering; no model-based query budgeting |
| robosuite / robomimic | github.com/ARISE-Initiative/robosuite · /robomimic | MuJoCo manipulation tasks, offline-from-demo learning | No online HIL trigger / budget tooling |
| ManiSkill3 | github.com/haosulab/ManiSkill | **GPU-parallel** manipulation sim; vectorized PPO/SAC + **TD-MPC2** baseline | No HIL intervention API; no cross-env query allocation |
| Isaac Lab | github.com/isaac-sim/IsaacLab | Massively-parallel envs (the Module-B substrate) | No HIL intervention / budget primitives |
| mbrl-lib | github.com/facebookresearch/mbrl-lib (archived) | PETS/MBPO ensembles, planners | Archived; no decision-aware loss, no HIL hooks |
| dreamerv3 / tdmpc2 | github.com/danijar/dreamerv3 · github.com/nicklashansen/tdmpc2 | Latent world models, planning, 300+ checkpoints | No uncertainty-for-querying, no HIL |
| DIAMOND | github.com/eloialonso/diamond | Diffusion world model (visual detail) | Pixel-domain, Atari-centric; no control-query coupling |
| d3rlpy | github.com/takuseno/d3rlpy | Offline RL algorithms, scikit-style API | No online HIL / model-based trigger |
| CleanRL | github.com/vwxyzjn/cleanrl | Single-file, reproducible RL baselines | Not modular; no HIL / MBRL trigger |

**Implication for the system contribution:** there is **no repo that exposes a model-based,
budget-aware human-query API across vectorized envs**. Building one on top of HIL-SERL's loop +
ManiSkill3/Isaac Lab parallelism + a TD-MPC2/PETS model is itself a defensible artifact.

---

## 3. Ranked innovation angles

Rating legend — **Feasibility** (4090, sim-only): High / Med / Low. **Novelty-vs-crowding**:
Crowded / Moderate / Open. Each angle says how it plugs into FORESIGHT-HIL.

### MODEL-SIDE

#### M1 — Decision-aware (VoI-aware) dynamics model for the trigger  ★ top pick
- **Gap.** The proposal's trigger reads failure-cost + epistemic uncertainty from an *MLE/PETS*
  ensemble trained for state-prediction accuracy. But the trigger only needs predictions that
  change the *decision* (continue / recover / query). A model optimized for prediction wastes
  capacity (and uncertainty) on decision-irrelevant detail.
- **Who's nearby (verified).** VAML (Farahmand, Barreto, Nikovski, AISTATS 2017); IterVAML
  (Farahmand, NeurIPS 2018, finite-sample bound); Value-Equivalence Principle (Grimm, Barreto,
  Singh, Silver, NeurIPS 2020, arXiv:2011.03506); λ-models (arXiv:2306.17366, authors not
  re-verified); Wasserstein↔VAML equivalence (arXiv:1806.01265); Model-Advantage VAML
  (arXiv:2106.14080); TD-MPC2 (arXiv:2310.16828) as a practical decoder-free value-aware model;
  MuZero (Schrittwieser et al., Nature 2020, arXiv:1911.08265).
- **Plug-in.** Replace/augment Module A's ensemble loss with a **VoI-weighted, value-equivalent
  loss** so model error and ensemble disagreement are concentrated where they flip the gate.
  Reuse the existing ensemble for epistemic uncertainty.
- **Feasibility.** High (state-based, small nets; TD-MPC2-scale fits 4090).
- **Novelty.** Open — decision-aware models exist, but *driving a human-query VoI trigger with
  one* is new.
- **Output / risk.** Tighter, cheaper trigger + a clean ablation (MLE vs decision-aware model).
  Risk: VAML-style losses can be unstable in stochastic dynamics (documented by λ-models) — keep
  MLE as a fallback term.

#### M2 — Calibrated epistemic uncertainty so VoI thresholds transfer  ★ fold-in
- **Gap.** VoI(s) scales failure-cost by ψ(u(s)); if `u` (ensemble disagreement) is
  miscalibrated, the τ-threshold must be re-tuned per task/env and queries are mis-spent. No HIL
  work calibrates the *trigger's* uncertainty.
- **Who's nearby (verified).** PETS (1805.12114, already cited); Cal-QL value calibration
  (2303.05479); RLPD ensemble+LayerNorm design (OpenReview h11j9w1ucU). Calibration framing:
  lower-bound learned-policy value, upper-bound a reference (Cal-QL).
- **Plug-in.** Add a calibration objective/diagnostic to Module A; report reliability diagrams
  for "query ⇔ true impending failure" (the proposal already promises this metric — this makes
  it principled). Lets a *single* τ transfer across the N parallel envs in Module B.
- **Feasibility.** High. **Novelty.** Moderate. **Risk.** Low; mostly strengthens existing claims.

#### M3 — Latent/diffusion/transformer world model for longer-horizon contact-rich foresight
- **Gap.** MLP ensembles compound error fast on discontinuous contact dynamics, capping the
  lookahead H and thus how *early* the trigger can fire. Latent WMs roll out longer, more stably.
- **Who's nearby (verified).** TD-MPC2 (2310.16828, ICLR'24, decoder-free latent, ManiSkill2
  results); DreamerV3 (2301.04104, already cited); DIAMOND diffusion WM (2405.12399, NeurIPS'24);
  IRIS (ICLR'23, OpenReview vhFu1Acb0xb); STORM (NeurIPS'23, arXiv:2310.09615, ID per listing);
  TWM (ICLR'23, arXiv:2303.07109, ID per listing).
- **Plug-in.** Swap Module A's rollout engine to a TD-MPC2-style latent model for the foresight
  step; keep an ensemble *over latent dynamics* for uncertainty.
- **Feasibility.** High for TD-MPC2 (state) on a 4090; Med for pixel diffusion/transformer WMs
  (Atari-100k-scale fits, contact-rich pixels heavier).
- **Novelty.** Moderate (engineering swap), but "anticipatory VoI on a latent WM" is new.
- **Risk.** Latent model error in contact; mitigate with the proposal's ground-truth-model
  upper-bound ablation.

#### M4 — World-model-as-human-surrogate: imagine the correction before paying for it  ★ separate-paper candidate
- **Gap.** Hi-WM uses a WM as an *offline* data factory (human edits rollouts); MILE models *when*
  humans intervene. Nobody uses the WM *online* to **predict the human's likely correction and
  its value**, querying the real human only when that surrogate is uncertain — directly closing
  the loop between model uncertainty and human cost.
- **Who's nearby (verified).** Hi-WM (`hiwm2026`, in refs); MILE (`mile2025`, in refs); WorldVLA
  (arXiv:2506.21539, github.com/alibaba-damo-academy/WorldVLA) and RynnVLA-002 (arXiv:2511.17502)
  show tight action↔world-model coupling and mutual enhancement.
- **Plug-in.** Adds a 4th branch to Module A: "ask the *imagined* human"; real queries reserved
  for high-surrogate-uncertainty states — a multiplicative reduction in human cost.
- **Feasibility.** Med (needs a learned human-advantage/correction model + WM). **Novelty.** Open.
- **Output / risk.** Could carry an entire paper ("imagination-augmented HIL"). Risk: surrogate
  bias → must gate on surrogate uncertainty, not trust it blindly.

### TRAINING-SIDE

#### T1 — Plasticity-preserving high-UTD training under intervention-induced distribution shift  ★ top pick
- **Gap.** HIL injects *bursts* of off-distribution expert/correction data and rewards high
  update-to-data ratios for sample efficiency — exactly the regime that triggers **primacy bias /
  plasticity loss / dormant neurons**. No HIL-RL paper (HIL-SERL, PACT, SiLRI, UniIntervene)
  studies this; yet a plastic learner needs *fewer* human queries to recover, coupling training
  health to the budget objective.
- **Who's nearby (verified).** Primacy Bias / resets (Nikishin et al., ICML'22, arXiv:2205.07802);
  ReDo / dormant neurons (Sokar, Agarwal, Castro, Evci, ICML'23, arXiv:2302.12902); BBF
  (Schwarzer et al., ICML'23, arXiv:2305.19452); RLPD (h11j9w1ucU).
- **Plug-in.** Add resets/ReDo + tuned replay ratio to the RLPD learner; **measure plasticity as a
  function of query timing/volume**; show that plasticity care reduces the queries needed to hit a
  success threshold (ties straight into the proposal's main "human cost" metric).
- **Feasibility.** High (cheap, single-GPU-proven interventions).
- **Novelty.** Open (plasticity × HIL is untouched). **Risk.** Low.
- **Output.** A strong analysis section *or* a standalone empirical paper.

#### T2 — Calibration-driven budget allocation (offline→online)  ★ fold-in
- **Gap.** Module B allocates the budget by top-VoI. An orthogonal, principled signal: spend
  queries where the *value function is least calibrated* (largest gap between pessimistic and
  reference value), à la Cal-QL — value-uncalibrated envs are where human signal helps most.
- **Who's nearby (verified).** Cal-QL (Nakamoto et al., NeurIPS'23, arXiv:2303.05479); RLPD
  (h11j9w1ucU).
- **Plug-in.** Add a calibration-gap term to the Module-B selection score; Cal-QL-style init
  reduces early-fine-tuning interventions.
- **Feasibility.** High. **Novelty.** Moderate–Open. **Risk.** Low.

#### T3 — Reset-free / autonomous recovery *as* the self-recover branch
- **Gap.** Module A's "self-recover" branch is underspecified. The autonomous-RL literature
  already builds backup/reset policies; nobody uses them *under a VoI human budget*, querying the
  human only when model-predicted reset-free recovery has low success margin.
- **Who's nearby (verified, already in refs).** EARL (2112.09605); Reset-Free dexterous
  (2104.11203); A Walk in the Park (2208.07860).
- **Plug-in.** Instantiate "self-recover" with a learned reset/backup controller; the VoI gate
  becomes recover-vs-query on its predicted margin.
- **Feasibility.** High. **Novelty.** Moderate. **Risk.** Low–Med (recovery policy quality).

#### T4 — Active, D-optimal feedback-modality selection
- **Gap.** The proposal *selects* a modality (action/preference/success) but not *which specific
  query* maximizes information per cost. Preference-based RL + active learning give the machinery.
- **Who's nearby (verified, in refs).** PEBBLE (2106.05091); DPO (2305.18290); Christiano et al.
  (1706.03741); online-exploration-for-RLHF / D-optimal design (`onlinerlhf2025`, 2509.22633).
- **Plug-in.** Replace heuristic modality choice in Module C with an info-gain/D-optimal query
  selector. Partly overlaps existing scope — frame as a *deepening*, not a new headline.
- **Feasibility.** High. **Novelty.** Moderate (some crowding in preference-RL). **Risk.** Low.

### CROSS-CUTTING / CREATIVE

#### X1 — Theory: decision-aware model error → VoI/budget-regret bound  ★ fold-in (top-venue glue)
- **Gap.** The proposal flags an optional VoI/regret note. Combining IterVAML's finite-sample
  *value-aware* model-error bound with budget-query regret would yield a bound that *directly*
  ties model quality to wasted queries — strong NeurIPS/ICLR fit.
- **Who's nearby (verified).** IterVAML bound (Farahmand, NeurIPS'18); Asking-for-Help under
  irreversible dynamics (2502.14043, in refs); Multi-source imperfect preferences (2603.20453, in
  refs).
- **Feasibility.** Med (analysis). **Novelty.** Open. **Risk.** Med (theory effort) but optional.

#### X2 — Scaling/data laws for *human-query efficiency*
- **Gap.** TD-MPC2 and BBF show capability scales with model/data size; nobody asks how **queries
  saved** scales with WM/data size. A clean "more model ⇒ fewer human queries" curve is a
  memorable, cheap-to-produce result.
- **Who's nearby (verified).** TD-MPC2 scaling (2310.16828); BBF scaling (2305.19452).
- **Feasibility.** High (reuse checkpoints/ablations). **Novelty.** Moderate–Open. **Risk.** Low.

#### X3 — Object-centric / structured dynamics for transferable failure localization  (speculative)
- **Gap.** Manipulation failures are object/contact-localized; a structured model could predict
  *which* interaction fails and transfer the trigger across tasks, improving interpretability of
  "why we queried." I did **not** verify a specific recent object-centric dynamics paper in this
  pass — treat as an open direction and verify a citation before use.
- **Feasibility.** Med. **Novelty.** Open. **Risk.** Med–High (representation engineering).

---

## 4. Recommended upgrade

**Fold into FORESIGHT-HIL for top-venue strength (pick 2–3):**
1. **M1 — decision-aware (VoI-aware) dynamics model.** This is the single highest-leverage upgrade:
   it makes the *model* serve the *decision*, turns the trigger from heuristic into principled, and
   gives a clean headline ablation (MLE vs value-equivalent model driving the same VoI gate).
2. **T1 — plasticity-preserving high-UTD training under intervention shift.** Cheap, single-GPU,
   genuinely untouched in HIL-RL, and it feeds *directly* into the proposal's main "human-cost"
   metric (a plastic learner asks fewer questions). Strong, low-risk empirical contribution.
3. **X1 — the decision-aware-model-error → budget-regret bound** as the light theory leg, plus
   **M2** (uncertainty calibration) as the connective tissue that makes a single VoI threshold
   transfer across the many parallel envs (Module B).

Together these convert the contribution from "a clever decision policy" into "a *model-and-training
co-designed* HIL system with calibrated, decision-aware foresight and a regret guarantee" — a much
harder target for reviewers to call incremental.

**Spin out as a separate paper:** **M4 — world-model-as-human-surrogate ("imagination-augmented
HIL").** Using the WM to *predict the human's correction and its value*, and querying the real
human only when the surrogate is uncertain, is a self-contained idea with its own formulation,
baselines (Hi-WM, MILE), and metric (real-queries saved at fixed success). It is too big to be a
sub-module and strong enough to stand alone.

---

## 5. Candidate additions (verified) — for review only, NOT auto-added to references.bib

Confidence: ✓ = arXiv ID/venue confirmed on a primary page this pass; ◐ = venue/authors
confirmed, arXiv ID from a search synthesis (re-check before citing); ⚠ = partial — verify.

```
# --- Model-side: world models / planning ---
✓ TD-MPC2: Scalable, Robust World Models for Continuous Control.
   Hansen, Su, Wang. ICLR 2024 (Spotlight). arXiv:2310.16828. github.com/nicklashansen/tdmpc2
✓ Diffusion for World Modeling: Visual Details Matter in Atari (DIAMOND).
   Alonso, Jelley, Micheli, Kanervisto, Storkey, Pearce, Fleuret. NeurIPS 2024 (Spotlight).
   arXiv:2405.12399. github.com/eloialonso/diamond
◐ STORM: Efficient Stochastic Transformer-based World Models for RL. NeurIPS 2023.
   arXiv:2310.09615 (ID per listing).
◐ Transformer-based World Models (TWM). Robine, Höftmann, Uelwer, Harmeling. ICLR 2023.
   arXiv:2303.07109 (ID per listing).
◐ Transformers are Sample-Efficient World Models (IRIS). Micheli, Alonso, Fleuret. ICLR 2023.
   OpenReview:vhFu1Acb0xb (arXiv:2209.00588, ID not re-verified). github.com/eloialonso/iris

# --- Model-side: decision-aware / value-equivalent model learning ---
✓ The Value-Equivalence Principle for Model-Based RL. Grimm, Barreto, Singh, Silver.
   NeurIPS 2020. arXiv:2011.03506
✓ Iterative Value-Aware Model Learning (IterVAML). Farahmand. NeurIPS 2018. (proceedings.neurips.cc)
◐ Value-Aware Loss Function for Model-based RL (VAML). Farahmand, Barreto, Nikovski. AISTATS 2017.
✓ Equivalence Between Wasserstein and Value-Aware Loss for MBRL. arXiv:1806.01265
✓ Model-Advantage and Value-Aware Models for MBRL. arXiv:2106.14080
✓ λ-models: Effective Decision-Aware RL with Latent Models. arXiv:2306.17366 (authors not re-verified)
◐ MuZero (Mastering ... by Planning with a Learned Model). Schrittwieser et al. Nature 2020.
   arXiv:1911.08265

# --- Training-side: plasticity / sample efficiency / offline->online ---
✓ The Primacy Bias in Deep RL. Nikishin, Schwarzer, D'Oro, Bacon, Courville. ICML 2022.
   arXiv:2205.07802
✓ The Dormant Neuron Phenomenon in Deep RL (ReDo). Sokar, Agarwal, Castro, Evci. ICML 2023.
   arXiv:2302.12902
✓ Bigger, Better, Faster: Human-level Atari with human-level efficiency (BBF). Schwarzer et al.
   ICML 2023. arXiv:2305.19452
✓ Cal-QL: Calibrated Offline RL Pre-Training for Efficient Online Fine-Tuning. Nakamoto, Zhai,
   Singh, Mark, Ma, Finn, Kumar, Levine. NeurIPS 2023. arXiv:2303.05479

# --- Cross-cutting: VLA + world model ---
✓ WorldVLA: Towards Autoregressive Action World Model. Cen et al. 2025. arXiv:2506.21539.
   github.com/alibaba-damo-academy/WorldVLA
✓ RynnVLA-002: A Unified Vision-Language-Action and World Model. Cen et al. 2025. arXiv:2511.17502

# --- Tooling / benchmarks (for the GitHub-gap & system-artifact argument) ---
✓ LeRobot: An Open-Source Library for End-to-End Robot Learning. Cadene et al. ICLR 2026.
   arXiv:2602.22818. github.com/huggingface/lerobot
✓ ManiSkill3: GPU Parallelized Robotics Simulation and Rendering. Tao et al. RSS 2025.
   arXiv:2410.00425. github.com/haosulab/ManiSkill
✓ MBRL-Lib: A Modular Library for Model-based RL. Pineda, Amos, Zhang, Lambert, Calandra. 2021.
   arXiv:2104.10159. github.com/facebookresearch/mbrl-lib (archived)
✓ CleanRL: High-quality Single-file Implementations of Deep RL Algorithms. Huang et al.
   JMLR 23(274), 2022. github.com/vwxyzjn/cleanrl
✓ d3rlpy: An Offline Deep RL Library. Seno, Imai. JMLR 2022. arXiv:2111.03788. github.com/takuseno/d3rlpy
◐ robomimic (What Matters in Learning from Offline Human Demonstrations). Mandlekar et al.
   CoRL 2021. arXiv:2108.03298 (ID not re-verified). github.com/ARISE-Initiative/robomimic
```

> Already present in `references.bib` and therefore **not** re-listed as new: HIL-SERL, PACT,
> SERL, UniIntervene, SiLRI, OHP-RL, ROVE, AIM, Thrifty-DAgger, MILE, AC-Teach, APIL, Hi-WM,
> VLA-in-the-Loop, Moerland/Luo MBRL surveys, Hybrid Control, RLPD, PETS, DreamerV3, Retzlaff,
> HACO/HAIM-DRL/SafeHIL/PE-RLHF, Asking-for-Help, Multi-source preferences, online-RLHF, DAgger,
> HG-DAgger, EnsembleDAgger, LazyDAgger, IWR, MBPO, Christiano, PEBBLE, DPO, Reset-Free, EARL,
> Walk-in-the-Park.
