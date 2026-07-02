# R016 Decision Note

R016 diagnosed why the Lift-tuned LV-VoI method failed to transfer to robosuite `Stack`.

## Evidence

- R015 Lift-tuned Stack LV-VoI (`tau=0.01`, `scale=3`) had low candidate rates and repeated best `22/60 = 36.7%`.
- Stronger BC capacity (`50` demos, `10000` BC steps, no online RL) improved repeated best to `32/60 = 53.3%`. This shows Stack is learnable, but imitation remains noisy and evaluation variance is high.
- Always-oracle online replay was negative: training best stayed at `25%`, restored single eval was `4/20 = 20%`, despite `6000` oracle-controlled steps. More oracle data alone is not sufficient; online updates can degrade the autonomous actor.
- Aggressive VoI (`tau=0.0`, `c_query=0`, `scale=3`, 6000 steps) improved repeated best to `33/60 = 55.0%`, the best Stack seed-0 result so far, but it spent the full 600-step human budget.

## Root-Cause Interpretation

The Stack failure is not just a missing oracle or lack of online human data. The main bottleneck is a combination of:

1. Stack needs stronger imitation/curriculum than Lift: 20 demos and 5000 BC steps are marginal.
2. The Lift-tuned trigger is too conservative for Stack: `tau=0.01` under-queries early, while `tau=0.0` recovers performance.
3. Online RL can collapse a decent Stack policy even with oracle data, so retention or curriculum control matters.

## Decision

Do not expand the original R015 Stack seeds yet. The next useful run is a Stack-tuned candidate: `tau=0.0`, stronger BC capacity, and either shorter online training or explicit checkpoint/retention emphasis. The paper framing should treat Stack as a failure-analysis and adaptation task until a tuned Stack variant beats none/random over multiple seeds.
