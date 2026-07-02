# FORESIGHT-HIL

> Current route (2026-07-02): this repository is now organized around an
> SCI Q1-oriented **cost-matched HIL-RL diagnostic benchmark** rather than a
> positive superiority claim for the current LV-VoI trigger. R020-R024 show
> that `random_b350` dominates LV-VoI scale3 after cost matching, and that
> simple trigger repairs remain dominated. The defensible paper contribution is
> strict cost-matched evaluation, repeated checkpoint estimates, trace-level
> intervention diagnostics, and negative findings that motivate better
> evaluation protocols before future trigger redesign. Start with
> [`PROJECT_DASHBOARD.md`](PROJECT_DASHBOARD.md), then see
> [`PAPER_PLAN.md`](PAPER_PLAN.md), [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md),
> [`results/EXPERIMENT_EVIDENCE_REGISTRY.csv`](results/EXPERIMENT_EVIDENCE_REGISTRY.csv),
> [`results/RESULTS_INDEX.md`](results/RESULTS_INDEX.md), and
> [`figures/FIGURE_ASSET_INDEX.md`](figures/FIGURE_ASSET_INDEX.md).

Foresighted, budget-aware **Human-in-the-Loop RL** via **model-based Value-of-Information**.

Research prototype + proposal for an SCI Q1-oriented **HIL-RL / model-based RL**
paper, with robotics-relevant manipulation tasks as the main application anchor.
The project unifies *when to ask*, *what to ask*, and *robustness to imperfect
humans* in HIL-RL, and studies **allocating a scarce human-query budget across
many parallel learning rollouts** (MJX on a single GPU; Isaac Lab optional).

See [`proposal/FORESIGHT-HIL_proposal.md`](proposal/FORESIGHT-HIL_proposal.md) for the
full plan, [`proposal/related_work.md`](proposal/related_work.md) for annotated prior
work, and [`proposal/references.bib`](proposal/references.bib) for BibTeX.

## Project navigation

For the current R020-R049 diagnostic-protocol route, use:

| Need | Entry point |
|---|---|
| Single-page current project status | [`PROJECT_DASHBOARD.md`](PROJECT_DASHBOARD.md) |
| Current manuscript thesis and section plan | [`PAPER_PLAN.md`](PAPER_PLAN.md) |
| Project vocabulary, claim rules, and architecture terms | [`CONTEXT.md`](CONTEXT.md) |
| Directory map and next structure targets | [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md) |
| Paper-claim evidence rows | [`results/EXPERIMENT_EVIDENCE_REGISTRY.csv`](results/EXPERIMENT_EVIDENCE_REGISTRY.csv) |
| Human-readable result archive index | [`results/RESULTS_INDEX.md`](results/RESULTS_INDEX.md) |
| Figure and table asset index | [`figures/FIGURE_ASSET_INDEX.md`](figures/FIGURE_ASSET_INDEX.md) |
| Current citation-context audit | [`paper/CITATION_AUDIT.md`](paper/CITATION_AUDIT.md) |
| Target journal matrix | [`results/r043_venue_targeting/VENUE_TARGET_MATRIX.md`](results/r043_venue_targeting/VENUE_TARGET_MATRIX.md) |
| Environment and reproducibility audit | [`results/r044_environment_reproducibility_audit/PROJECT_ENVIRONMENT_REPRODUCIBILITY_AUDIT.md`](results/r044_environment_reproducibility_audit/PROJECT_ENVIRONMENT_REPRODUCIBILITY_AUDIT.md) |
| T-ASE manuscript alignment | [`results/r045_tase_reproducibility_alignment/MANUSCRIPT_ALIGNMENT.md`](results/r045_tase_reproducibility_alignment/MANUSCRIPT_ALIGNMENT.md) |
| Evidence provenance package | [`results/r047_evidence_provenance_package/EVIDENCE_PROVENANCE_AUDIT.md`](results/r047_evidence_provenance_package/EVIDENCE_PROVENANCE_AUDIT.md) |
| Version and command provenance repair | [`results/r048_version_command_provenance/VERSION_PROVENANCE_REPAIR.md`](results/r048_version_command_provenance/VERSION_PROVENANCE_REPAIR.md) |
| Provenance validation gate | [`results/r049_provenance_validation/PROVENANCE_VALIDATION_MODULE.md`](results/r049_provenance_validation/PROVENANCE_VALIDATION_MODULE.md) |
| Future agent working rules | [`AGENTS.md`](AGENTS.md) |

## Original method motivation (superseded by the R021-R026 diagnostic pivot)
The HIL-RL space is crowded along "how to use intervention data" (PACT, SiLRI,
OHP-RL, ROVE) and "auto-recovery" (UniIntervene, AIM), but most systems assume a
single agent/robot, a single human, and a sequential setting with a *reactive*
trigger. We:
1. trigger interventions **anticipatorily** via an ensemble **dynamics model** +
   epistemic uncertainty, formalized as **Value of Information** (VoI);
2. study **budgeted query allocation across N parallel envs**, a problem made
   concrete by large-scale simulation and robotics-relevant parallel rollouts
   (MJX / Isaac Lab);
3. make the trigger **robust to imperfect humans** (delay/noise/bias) — which
   simulation lets us *control and sweep* (a strength, not a weakness);
4. choose **which feedback modality** to request per state.

## Design scope & non-goals (RL route)
FORESIGHT-HIL is a **reinforcement-learning** project: the "model" here is a
**dynamics / world model** used for foresighted rollouts, *not* a supervised
time-series predictor. To keep the contribution focused (VoI trigger + budget
allocation + robustness + decision-aware dynamics), a few common add-ons are
deliberately scoped:

- **Recurrent dynamics model — optional, only under partial observability.** If a
  task is a POMDP or has history-dependent contact dynamics, the dynamics model
  may be made sequential (**GRU / RSSM / Transformer preferred over a plain
  LSTM**) so the VoI lookahead conditions on history; this folds into the **M1**
  decision-aware-dynamics module. For fully-observed state (e.g. the current
  `Lift` 60-D obs) a feedforward ensemble is used.
- **Bayesian optimization — a tuning utility, not a contribution.** BO (or
  cheaper grid/manual search) may tune `τ`, lookahead `H`, value-aware mix `β`,
  ensemble size, etc. Since each RL evaluation costs a full (hours-long) training
  run, prefer cheap search; BO is **never** presented as a novelty.
- **Deliberately NOT added:** CNN visual backbones (only relevant if we switch to
  image observations, where a pretrained ResNet is standard, not novel) and the
  "lightweight module / multi-sensor fusion" PHM template — these do not raise
  novelty for SCI Q1 AI/RL/engineering venues and would dilute the core story.

## Quick start (numpy-only, no sim engine needed)
```bash
pip install -r requirements.txt          # just numpy for the core demo
python scripts/run_demo.py               # default run
python scripts/run_demo.py --num_envs 256 --budget 8 --takeover_len 10 \
    --horizon 10 --tau 0.05 --human_noise 0.3 --human_delay 1   # robustness sweep
```
The demo compares intervention strategies on a vectorized reach-avoid task under
a shared per-step query budget and reports success/failure, human-step cost, and
trigger precision/recall. Expected reading: `voi` ≈ `always`-level success at a
fraction of the human cost, and beats `random` at equal budget.

Example output:
```
strategy | success | failure | engage | humanstep |  prec |   rec
    none |    2.3% |   97.7% |      0 |         0 |   nan |   nan
  always |   69.5% |   30.5% |    418 |      3396 |   nan |   nan
  random |   42.2% |   57.8% |    115 |       958 |  0.85 |  0.14
     voi |   47.7% |   52.3% |    111 |       933 |  0.86 |  0.13
```

## Robotics-relevant simulated HIL track (robosuite / MuJoCo + SAC)

This connects the method prototype to a robotics-relevant manipulation simulator
(robosuite `Lift`, single Panda arm, OSC_POSE controller, proprio+object obs, no
images) with a **learning SAC actor** (stable-baselines3) and a
**scripted-oracle human**.

### What this is / isn't (please read)
- **It is** an HIL-SERL-*style* simulation baseline: off-policy SAC trained
  RLPD-style with a **50/50 demo+online replay mix**; a privileged-state
  **scripted oracle** can intervene, and intervention transitions are added to
  **both** the demo and RL buffers (as in HIL-SERL). FORESIGHT-HIL plugs in on
  top to decide **WHO/WHEN** intervenes via a model-based **Value-of-Information**
  trigger (`VoIGate` + ensemble dynamics) under a **query budget**.
- **It is NOT** an exact reproduction of the HIL-SERL real-robot system or its
  numbers. In current experiments, the "human" is a **scripted privileged-state controller** (a
  *simulated* teleoperator), clearly labeled as such. We do **not** claim
  paper-matching results.
- The VoI "failure" signal for `Lift` is a **task-progress risk proxy**
  (predicted gripper→cube distance exceeding a threshold within the model
  rollout), since `Lift` has no irrecoverable hazard. Documented honestly in
  `scripts/train_robosuite_hil.py`.

### Setup
```bash
pip install -r requirements.txt
# PyTorch CUDA build (RTX 4090, verified with torch 2.4.0+cu124):
pip install torch --index-url https://download.pytorch.org/whl/cu124
```
Windows note: a `KMP_DUPLICATE_LIB_OK=TRUE` workaround for the torch/mujoco
OpenMP clash ("OMP: Error #15") is set automatically at the top of the train
script.

### Smoke run (verified end-to-end on Windows + RTX 4090)
Proves the pipeline executes and writes results; **not** long enough to learn
(success stays ~0% at this step budget — expected):
```bash
# compare all four intervention strategies (short)
python scripts/train_robosuite_hil.py --task Lift --strategy none   --total_steps 600 --n_demos 5 --learning_starts 200 --eval_every 600 --eval_episodes 3 --seed 0
python scripts/train_robosuite_hil.py --task Lift --strategy always --total_steps 600 --n_demos 5 --learning_starts 200 --eval_every 600 --eval_episodes 3 --seed 0
python scripts/train_robosuite_hil.py --task Lift --strategy random --budget 150 --total_steps 600 --n_demos 5 --learning_starts 200 --eval_every 600 --eval_episodes 3 --seed 0
python scripts/train_robosuite_hil.py --task Lift --strategy voi    --budget 150 --total_steps 600 --n_demos 5 --learning_starts 200 --eval_every 600 --eval_episodes 3 --seed 0
python scripts/plot_results.py        # -> results/success_vs_human_cost.png + CSVs
```

### Full run (documented; takes hours — not run here)
```bash
# run each strategy (and a few seeds) to a real training budget, then plot
python scripts/train_robosuite_hil.py --task Lift --strategy voi --budget 4000 \
    --total_steps 150000 --n_demos 20 --learning_starts 1000 \
    --eval_every 5000 --eval_episodes 20 --seed 0
# repeat with --strategy none / always / random and seeds 0..2, then:
python scripts/plot_results.py
```
Configurable via argparse: `--task --strategy --budget --human_noise
--human_delay --human_skill --human_dropout --total_steps --seed` (full list in
`--help`). Outputs per-run CSVs, a cross-strategy summary CSV, and the
success-vs-human-cost plot under `results/`.

## Layout
```
foresight_hil/
  envs/toy_reach.py          # vectorized reach-avoid env + the backend step contract
  envs/robosuite_env.py      # gymnasium wrapper over robosuite Lift/Door (+ Reacher fallback)
  models/ensemble_dynamics.py# online linear ensemble dynamics (numpy, toy)
  models/torch_ensemble.py   # neural MLP ensemble dynamics for high-dim robosuite state
  oracle/scripted_human.py   # configurable imperfect "human" (noise/delay/bias/skill/dropout)
  oracle/robosuite_oracle.py # scripted privileged-state pick-and-lift oracle (simulated human)
  gating/voi_gate.py         # Module A: foresighted VoI trigger (now takes a generic risk_fn)
  allocation/budget.py       # Module B: budgeted query allocation across N envs
  hil/mixed_replay_buffer.py # RLPD-style 50/50 demo+online buffer (HIL-SERL backbone)
  hil/intervention.py        # none / always / random@budget / voi@budget controller
  agents/policy.py           # weak hazard-unaware policy (toy learner stand-in)
scripts/run_demo.py            # toy: vectorized strategy comparison + trigger calibration
scripts/train_robosuite_hil.py # real-sim: HIL-SERL-style SAC + VoI trigger on robosuite
scripts/plot_results.py        # aggregate runs -> success-vs-human-cost plot + CSV
proposal/                      # proposal, annotated related work, references.bib
```

## Extending to real tasks
- **MuJoCo / robosuite / Meta-World**: implement the same API as
  `VectorReachEnv` (`reset`, `step`, and an eval-only `true_dynamics`) and swap a
  real SAC/RLPD actor for `WeakReachPolicy`. Replace the linear ensemble with a
  neural PETS ensemble.
- **MJX (GPU-parallel MuJoCo, primary) / Isaac Lab (optional)**: wrap the
  vectorized env; the budgeted allocator in `allocation/budget.py` is already
  written for `N` parallel envs. This is where the headline experiment (query
  budget vs. success Pareto, trigger calibration) runs — via MJX on a single
  4090, with Isaac Lab as optional extra scale (WSL2/Linux).
- **HIL-SERL backbone**: `rail-berkeley/hil-serl` provides the actor-learner +
  intervention infra; FORESIGHT-HIL slots in as the *trigger + allocator + credit*
  layer on top.

> Note: numbers above are from the toy proof-of-concept and only validate the
> pipeline/mechanism, not paper-grade results.

## Experiment notes

- Low-N evaluation warning: `eval_episodes < 20` is useful only for smoke tests.
  The trainer logs `successes/episodes` and a Wilson 95% confidence interval,
  because `0/5` can still be statistically compatible with a non-trivial success
  rate. Use at least 20 evaluation episodes for any paper claim.
- `always` in the robosuite track is not an upper bound. It is a budget-unaware
  oracle-data stress test: training data may be all oracle actions, but
  evaluation still measures the autonomous SAC policy acting alone.
- Value-mode VoI uses `--voi_value_scale_floor 1.0` and `--voi_score_clip 10.0`
  by default. These stabilize early training, when the SAC critic value can be
  near zero and otherwise create meaningless relative-decline scores.
- If short robosuite runs report all-zero final success, check the per-step CSV
  before assuming the environment is broken. The trainer supports
  `--eval_at_start`, `--bc_pretrain_steps`, and `--bc_actor_reg_coef` to diagnose
  whether successful demonstrations reach the autonomous actor and whether SAC
  updates later erase that behavior. In local diagnostics, BC warm-start produced
  non-zero intermediate success, while later SAC updates could still collapse,
  so `best_success_rate`, return curves, and `bc_reg_loss_mean` should be read
  together.
- The trainer now saves a best-policy checkpoint whenever an evaluation improves
  success, under `results/.../checkpoints/best_<run_tag>.zip`, and records
  `best_eval_step` plus `best_checkpoint_path` in the summary CSV. This is
  important because several Lift runs show high intermediate success followed by
  final-policy collapse. Use `--no_save_best_model` only for smoke tests where
  checkpoint files are unwanted.
- Best-checkpoint probe: `results/best_checkpoint_collapse_probe` reran a
  collapse-prone VOI setting (`tau=0.01`, `c_query=0`, budget 600,
  `takeover_len=20`, seed 1). Training eval saved the best checkpoint at step
  2000 with `20/20` success, while the final policy reached `17/20`. Reloading
  the saved checkpoint from disk and independently evaluating 20 episodes also
  gave `17/20`, so low-N evaluation noise is part of the apparent best/final
  gap. A repeated checkpoint re-evaluation script
  (`scripts/evaluate_checkpoint.py`) now writes per-repeat and aggregate CSVs;
  running the saved checkpoint for `3 x 20` episodes gave `50/60` success
  (mean 83.3%, Wilson CI 72.0-90.7%) under
  `results/best_checkpoint_collapse_probe/checkpoint_reeval_3x20_summary.csv`.
  Paper-grade checkpoint claims should use this repeated protocol or larger
  evaluation batches.
- Anti-collapse schedule probe: the trainer now supports
  `--bc_actor_reg_schedule linear_late --bc_actor_reg_late_coef ...` to increase
  the actor demonstration anchor late in training. On the collapse-prone Lift
  VOI setting (`budget=600`, `takeover_len=20`, seed 1), a `50 -> 150` late
  schedule reached only `4/20` final success, with best training eval `16/20`
  at step 2000. Reloading that best checkpoint for `3 x 20` episodes gave
  `51/60` success (mean 85.0%, Wilson CI 73.9-91.9%) under
  `results/anti_collapse_linear_late_probe`. Interpretation: actor anchoring
  alone is not enough to prevent final-policy collapse; best-checkpoint/early
  stopping, update freezing, or critic/actor plasticity controls are now higher
  priority than simply increasing the late BC coefficient.
- Early-stop / restore-best probe: the trainer now supports
  `--restore_best_model_at_end`. When enabled, the summary CSV reports
  `final_success_rate` from a freshly reloaded best checkpoint, while preserving
  the training-end policy as `raw_final_success_rate` and labeling the source in
  `final_policy_source`. New summaries also record `best_human_steps`,
  `best_budget_used_frac`, and `best_engagements`, so best-checkpoint success is
  paired with the human cost at the actual best eval step rather than the
  training-end cost. A seed-0 Lift probe with `budget=600`,
  `takeover_len=20`, `tau=0.01`, `c_query=0`, and `eval_episodes=20` is saved
  under `results/r004_restorebest_seed0_probe`. Restoring best checkpoints
  improved reported final over raw final (`none: 65% vs 30%`,
  `random: 70% vs 35%`, `voi: 55% vs 10%`), confirming late-policy collapse.
  However, repeated best-checkpoint evaluation over `3 x 20` episodes ranked
  `none=49/60` (81.7%), `random=45/60` (75.0%), and `voi=32/60` (53.3%).
  Interpretation: restore-best is useful bookkeeping, but the current tuned VoI
  trigger does not yet beat the strong BC/SAC baseline on seed 0.
- Learning-value VoI probe: the gate now optionally multiplies the value-based
  VoI score by policy-reference action disagreement via
  `--voi_reference_policy demo_nn --voi_learning_value_scale ...`. The current
  reference is a nearest-neighbor action lookup over demonstration states, so no
  extra model is trained. On the same seed-0 Lift setting, `demo_nn` with scale
  `2.0` reached a training best of `18/20` at step 2000 after only 60 human
  steps, and repeated best-checkpoint evaluation gave `48/60` success (80.0%,
  Wilson CI 68.2-88.2%) under `results/r008_learning_value_seed0_probe`. This
  is a strong improvement over plain tuned VoI (`32/60`, 53.3%) and random
  (`45/60`, 75.0%), but it is still statistically close to the no-intervention
  best checkpoint (`49/60`, 81.7%). R009 repeated the same learning-value VoI on
  seeds 1-2. Combined over seeds 0-2, repeated best-checkpoint evaluation is
  `131/180` success (72.8%, Wilson CI 65.9-78.8%), with best-policy human costs
  `60`, `80`, and `390` steps (mean 176.7). This supports learning-value gating
  as the current best VoI direction, but seed 2 is weaker and the result is not
  yet a decisive main-paper dominance claim. See
  `results/r009_learning_value_seeds1_2/learning_value_multiseed_repeated_summary.csv`.
- R010 repaired the weak seed-2 case with a small budget/scale ablation. Reducing
  the budget to 300 at scale 2.0 gave `45/60` repeated best success (75.0%) with
  best-step human cost 255; increasing scale to 3.0 at budget 600 gave `47/60`
  (78.3%) with best-step cost 384. Replacing only seed 2 in the R008/R009
  aggregate yields `138/180` (76.7%, CI 70.0-82.3%) for the budget-300 option
  and `140/180` (77.8%, CI 71.2-83.2%) for the scale-3 option. Interpretation:
  budget 300 is now the more efficient Pareto candidate, while scale 3 is the
  higher-success candidate. See `results/r010_learning_value_ablation_seed2`.
- R011 repeated the budget-300 / scale-2 repair on seeds 0-1 and overturned the
  early Pareto interpretation. Training best success remained respectable
  (`80%` on seed 0, `70%` on seed 1, both at 40 human steps), but repeated
  best-checkpoint evaluation dropped to `36/60` and `37/60`. Combining these
  with the R010 seed-2 repair gives `118/180` success (65.6%, Wilson CI
  58.4-72.1%) at mean best-step cost 111.7. This is cheaper but less reliable
  than the original R008/R009 learning-value run, so budget 300 should be treated
  as an efficiency ablation rather than the main claim. See
  `results/r011_budget300_scale2_seeds0_1`.
- R012 repeated the higher-success R010 repair (`budget=600`,
  `learning_value_scale=3.0`) on seeds 0-1. Repeated best-checkpoint evaluation
  reached `50/60` on seed 0 and `55/60` on seed 1; combined with the R010 seed-2
  scale-3 result (`47/60`), the three-seed aggregate is `152/180` success
  (84.4%, Wilson CI 78.4-89.0%) with mean best-step human cost 283.3. This is
  the current strongest learning-value VoI candidate: more costly than the
  budget-300 ablation, but substantially more reliable and stronger than the
  original R008/R009 scale-2 aggregate (`131/180`, 72.8%). Next evidence gap:
  repeat no-intervention and random baselines under the same three-seed,
  repeated-checkpoint protocol. See `results/r012_budget600_scale3_seeds0_1`.
- R013 aligned those baselines. Reusing compatible R004 seed-0 baselines and
  adding R013 seeds 1-2, no-intervention restore-best achieved `134/180`
  repeated best success (74.4%, Wilson CI 67.6-80.3%) at zero human cost.
  Random restore-best with budget 600 also achieved `134/180` (74.4%, CI
  67.6-80.3%) with mean best-step human cost 342.0, but had high seed variance
  (`60/60` on seed 1, `29/60` on seed 2). The current learning-value VoI
  candidate therefore improves aggregate success by 10.0 percentage points
  (`152/180` vs. `134/180`) and uses fewer mean best-step human steps than
  random (`283.3` vs. `342.0`). This is the first credible main-result table,
  while seeds 3-4 or a second manipulation task are still needed for stronger
  SCI-level robustness. See `results/r013_baseline_alignment_seeds1_2`.
- R014 expanded the aligned Lift comparison to five seeds. On the new seeds 3-4,
  learning-value VoI remained strong (`104/120`, 86.7%) and reached its best
  checkpoints at only 80 mean human steps, but random was near-saturated
  (`117/120`, 97.5%) at 160 mean human steps. The five-seed aggregate is now:
  learning-value VoI `256/300` (85.3%, CI 80.9-88.9%, cost 202.0),
  no-intervention `237/300` (79.0%, CI 74.0-83.2%, cost 0), and random
  `251/300` (83.7%, CI 79.1-87.4%, cost 269.2). Interpretation: the method
  still beats no-intervention and remains the best aggregate success point, but
  the advantage over random shrinks to 1.7 percentage points. The paper claim
  should therefore emphasize human-efficiency at matched/near-matched success,
  and the next major evidence gap is a second manipulation task. See
  `results/r014_robustness_seeds3_4_method`.
- R015 started that second-task check on robosuite `Stack`. The environment
  wrapper now exposes Stack object state (`cubeA_pos`, `cubeB_pos`,
  `gripper_to_cubeA`, `gripper_to_cubeB`) and the scripted oracle has a
  Stack-specific pick-place routine; oracle smoke reached `5/5` Stack success.
  The learning result is negative for the current Lift-tuned method: on Stack
  seed 0, repeated best-checkpoint success was no-intervention `28/60` (46.7%),
  random `26/60` (43.3%), and learning-value VoI `22/60` (36.7%). Interpretation:
  the second-task infrastructure is now viable, but the current LV-VoI trigger
  does not transfer positively to Stack. Next work should diagnose Stack-specific
  failure modes before expanding seeds. See `results/r015_stack_seed0_method`.
- R016 diagnosed that Stack failure. Stronger imitation (`50` demos and `10000`
  BC steps, no online RL) improved repeated best success to `32/60` (53.3%),
  while always-oracle online replay was negative (`4/20` restored single eval
  after 6000 oracle-controlled steps). Lowering the VoI threshold to
  `tau=0.0` improved Stack seed-0 repeated best to `33/60` (55.0%), the best
  Stack diagnostic so far, but it spent the full 600-step budget. Interpretation:
  Stack needs task-specific trigger/curriculum tuning; more human data alone is
  not enough, and online updates can degrade the autonomous actor. See
  `results/r016_stack_failure_diagnosis`.
- R017 combined the two positive Stack signals: stronger imitation (`50` demos,
  `10000` BC steps) and aggressive Stack querying (`tau=0.0`, `demo_nn`,
  learning-value scale `3.0`). On Stack seed 0, repeated best-checkpoint success
  reached `47/60` (78.3%, Wilson CI 66.4-86.9%) with best-step human cost 600.
  This is a large recovery over R015 no-intervention (`28/60`), random (`26/60`),
  Lift-tuned LV-VoI (`22/60`), and R016 tau0 with only 20 demos (`33/60`).
  Interpretation: Stack is no longer only a negative transfer case, but the
  tuned candidate is not yet an efficiency claim because it uses more demos and
  the full online human budget. See `results/r017_stack_tuned_candidate`.
- R018 aligned that Stack candidate against matched 50-demo baselines over seeds
  0-2. The result is negative for the current Stack LV-VoI formulation:
  no-online matched BC reached `131/180` (72.8%, Wilson CI 65.9-78.8%) at zero
  online human cost, while random human and Stack-tuned LV-VoI both reached
  `107/180` (59.4%, Wilson CI 52.2-66.4%) with mean best-step human costs 478.0
  and 433.3. Interpretation: the R017 seed-0 recovery does not reproduce as a
  general Stack advantage; the current online-intervention mechanism is
  dominated by strong demo-regularized SAC on Stack. Use Stack as a
  failure-analysis and redesign target, not as a positive breadth claim yet. See
  `results/r018_stack_multiseed_alignment`.
- R019 tested two Stack redesign hooks: `--intervention_demo_mode` to reduce
  how much takeover data enters the demo/BC replay, and `--voi_phase_guard
  stack_pick_place` to start interventions only near contact-sensitive Stack
  pick/place windows. On seed 0, none of the redesigns beat the strong matched
  no-online baseline under repeated evaluation: no-online and R017 tau0 both
  reached `47/60` (78.3%), while starts-only demo replay reached `38/60`
  (63.3%), phase-guard budget600 reached `35/60` (58.3%), and phase-guard
  budget300 reached `34/60` (56.7%). Interpretation: the Stack issue is not
  fixed by lightweight replay filtering or a hand-coded phase mask; do not
  expand these variants to more seeds. See `results/r019_stack_mechanism_redesign`.
- R020 upgraded the main Lift checkpoint reliability check from `3 x 20` to
  `5 x 20` autonomous evaluations per seed. Over five seeds, no-online reached
  `400/500` (80.0%, Wilson CI 76.3-83.3%) at zero online human cost, random
  reached `426/500` (85.2%, CI 81.8-88.0%) at mean best-step cost 269.2, and
  LV-VoI scale3 reached `416/500` (83.2%, CI 79.7-86.2%) at mean best-step cost
  202.0. Interpretation at the time: the high-N result suggested a possible
  human-efficiency claim at near-random success, but it still did not support
  success dominance over random. This interpretation is superseded by the R021
  cost-matched random check below. See `results/r020_lift_highn_reliability`.
- R021 added the missing cost-matched random check and overturned that current
  LV-VoI efficiency claim. A lower-budget random baseline (`random_b350`) reached
  `439/500` (87.8%, Wilson CI 84.6-90.4%) at mean best-step human cost 177.0,
  while LV-VoI scale3 remained `416/500` (83.2%, CI 79.7-86.2%) at cost 202.0.
  Interpretation: current LV-VoI scale3 is dominated by cost-matched random on
  Lift, so it should not be used as the main positive Pareto claim. Treat R021
  as the pivot into trigger redesign and failure-aware diagnostics. See
  `results/r021_random_costmatch`.
- R022 starts that trigger redesign with
  `--voi_learning_value_min_disagreement`, a conservative learning-value filter
  that only allows a reference-policy VoI intervention when the actor differs
  enough from the demo-nearest reference action. A 300-step smoke run completed
  under `results/r022_min_disagree_smoke`; this is an engineering check only,
  not a paper result. The next gate is a Lift seeds 0-2 run against the
  `random_b350` seed subset before any five-seed expansion.
- R022's formal seeds 0-2 gate is negative. With `vlvmin0p25`, min-disagreement
  LV-VoI reached `226/300` (75.3%, Wilson CI 70.2-79.9%) at mean best-step cost
  211.7, while same-seed `random_b350` reached `259/300` (86.3%, CI
  82.0-89.8%) at cost 95.0. Interpretation: action disagreement with the
  demo-nearest reference is not enough to identify high-value intervention
  states. Do not expand this variant; switch to intervention-timing diagnostics.
  See `results/r022_lift_min_disagree_seed0_2`.
- R023 begins that diagnosis with optional intervention-start tracing. The new
  `--trace_interventions` flag writes one row per takeover start with budget,
  VoI score/p_fail when available, and privileged geometry such as
  gripper-to-cube distance. A short random/VoI smoke run under
  `results/r023_trace_smoke` confirmed non-empty trace files. This is diagnostic
  infrastructure only; the next gate is to rerun the real seeds 0-2 comparison
  with tracing enabled.
- R023 real traces on Lift seeds 0-2 are saved under
  `results/r023_real_trace_seed0_2`. The diagnosis does not support a simple
  "LV-VoI intervenes too far from the cube" story: LV-VoI starts are closer to
  the cube than random on average (`g2c_norm` 0.217 vs 0.285; `g2c_xy` 0.152 vs
  0.235). The stronger pattern is score/timing mismatch: LV-VoI produces
  saturated early starts (`score=10`, `p_fail=1`), then no starts in 2-4k, then
  many low-score starts in 4-6k. Interpretation: R024 should prioritize
  score-calibrated gating / low-confidence mid-late suppression rather than a
  pure contact-window heuristic.
- R024 now has a default-off score-calibrated VoI start gate:
  `--voi_score_floor_after_step` and `--voi_score_floor_after_value`. It only
  affects new VoI takeover starts after the configured step; ongoing takeovers
  and the original default LV-VoI behavior are unchanged. The formal Lift
  seeds 0-2 gate is negative: R024 score-floor LV-VoI reached `233/300`
  repeated success (77.7%, Wilson CI 72.6-82.0%) at mean best-step human cost
  253.3, while same-seed `random_b350` remains `259/300` (86.3%, CI
  82.0-89.8%) at cost 95.0. Trace diagnostics show the floor mechanically
  blocked starts below score 0.05 after step 4000, but total starts barely
  changed (`94` vs `96` for original LV-VoI scale3, versus `55` for
  random_b350). Interpretation: do not expand R024; pivot toward a
  cost-matched HIL-RL diagnostic benchmark / negative-findings paper unless a
  substantially different trigger mechanism is introduced.
- R025 performs that pivot. The root [`PAPER_PLAN.md`](PAPER_PLAN.md) now frames
  the project as an empirical diagnostic / benchmark paper rather than an
  unsupported trigger-superiority paper. Supporting files live under
  `results/r025_paper_pivot/`: a claims-evidence matrix, negative-findings
  table, figure/table plan, and evaluation-protocol recommendation. The next
  writing step is to turn these into polished main figures and LaTeX-ready
  result tables, then run citation search/audit before drafting related work.
- R026 builds the first paper artifact set under `figures/`: five vector PDF
  figures, three LaTeX-ready result tables, and `latex_includes.tex`. The figures
  are generated reproducibly by `figures/gen_r026_paper_figures.py` from the
  existing R021/R024/R025 CSVs. The hero figure is a data-driven draft and should
  be visually refined before submission, but the main success-cost, repair, and
  trace figures are ready to use as paper evidence.
- Current local 1k-step diagnosis favors a stronger actor demo regularizer:
  `--bc_pretrain_steps 5000 --bc_actor_reg_coef 50.0 --learning_starts 500`
  reached `7/10` final evaluation success on seed 0, while weaker regularization
  stayed around `1/10` or collapsed back to zero. Treat this as a tuning
  direction, not a paper-grade claim, until repeated over seeds and longer runs.
- Windows startup note: robosuite imports numba-jitted utilities. The wrapper now
  sets `NUMBA_CACHE_DIR` to the project-local `.numba_cache` directory before
  importing robosuite, because probing Anaconda `site-packages` for numba cache
  writability can hang for minutes on this machine.
- Current local 5k-step trend run (Lift / robosuite, seeds 0-2, `n_demos=20`,
  `budget=1000`, `eval_episodes=10`, `bc_pretrain_steps=5000`,
  `bc_actor_reg_coef=50.0`) is saved under `results/local_bc_reg50_5000_clean`.
  Best-success means: `none=86.7%`, `random=93.3%`, `voi=96.7%`. Final-success
  means: `none=50.0%`, `random=76.7%`, `voi=90.0%`. Mean human steps:
  `none=0`, `random=1000`, `voi=163.3`. This is a promising efficiency trend,
  not a paper-grade claim yet; use `eval_episodes>=20`, longer training, and more
  seeds for manuscript numbers.
- Current 10k-step / `eval_episodes=20` run (Lift / robosuite, seeds 0-2, same
  BC regularization) is saved under `results/local_bc_reg50_10000_eval20_s0`.
  Final-success means: `none=51.7%`, `random=85.0%`, `voi=73.3%`; best-success
  means: `none=90.0%`, `random=96.7%`, `voi=83.3%`; mean human steps:
  `none=0`, `random=1000`, `voi=113.3`. Interpretation: at this budget and
  trigger threshold, `random` has higher absolute success, while `voi` reaches
  a strong improvement over `none` using only about 11% of the random human
  cost. Seed 2 exposes a useful failure case for VoI calibration / budget pacing,
  so the next paper-facing experiment should report the success-cost Pareto
  frontier rather than claiming unconditional dominance.
- Seed-2 VoI gate/budget diagnostic is saved under
  `results/voi_gate_sweep_seed2_10000_eval20`. Key points: default VoI
  (`tau=0.10`, `c_query=0.05`, budget 1000) used only 110 human steps and reached
  55% final success; an over-aggressive trigger (`tau=0`, `c_query=0`) spent the
  full 1000 steps but collapsed to 15%; a moderate trigger (`tau=0.01`,
  `c_query=0`) reached 100% only when allowed to spend the full 1000 steps.
  With budget 600, increasing `takeover_len` from 10 to 20 improved final
  success from 75% to 80% at the same human cost. This suggests the next
  innovation target is not simply "lower the threshold", but jointly learning or
  scheduling trigger threshold, budget pacing, and takeover duration.
- The promising seed-2 point (`tau=0.01`, `c_query=0`, budget 600,
  `takeover_len=20`) did not hold up over seeds 0-2: final-success mean was
  53.3% at 600 human steps, while its best-success mean was 90.0%. This gap
  reinforces that late-policy collapse / retention, not only gate selectivity,
  is the current bottleneck. The comparison table and plot are
  `results/voi_gate_sweep_seed2_10000_eval20/pareto_three_seed_comparison.csv`
  and `.png`.
- For a local trend run that is more informative than the 600-step smoke test:

```bash
python scripts/run_comparison.py --seeds 0 --strategies none random voi \
    --total_steps 30000 --budget 4000 --eval_every 5000 --eval_episodes 20 \
    --takeover_len 20 --voi_tau 0.01 --voi_cquery 0.0 \
    --restore_best_model_at_end --out_dir results/local_trend_30000
python scripts/plot_results.py --summary results/local_trend_30000/robosuite_hil_summary.csv \
    --metric best_success_rate --out results/local_trend_30000/success_vs_human_cost_best.png \
    --out_csv results/local_trend_30000/strategy_comparison_best.csv
```
