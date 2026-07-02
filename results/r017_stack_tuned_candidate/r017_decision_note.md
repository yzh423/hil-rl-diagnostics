# R017 Decision Note

R017 tested a Stack-specific candidate that combines the two positive R016 signals:

- stronger imitation: `50` oracle demos and `10000` BC pretrain steps
- aggressive Stack querying: `tau=0.0`, `c_query=0`, `demo_nn` reference policy with learning-value scale `3.0`

## Result

Training best reached `60%` at step 6000 and the restored single evaluation was `17/20 = 85%`. Repeated checkpoint evaluation confirmed the improvement:

- R017 Stack-tuned VoI: `47/60 = 78.3%`, Wilson CI `66.4-86.9%`, best-step human cost `600`.

Relevant comparisons on Stack seed 0:

- R015 no-intervention baseline: `28/60 = 46.7%`.
- R015 random baseline: `26/60 = 43.3%`.
- R015 Lift-tuned VoI: `22/60 = 36.7%`.
- R016 BC capacity baseline: `32/60 = 53.3%`.
- R016 tau0 VoI with 20 demos: `33/60 = 55.0%`.

## Interpretation

This rescues Stack as a second-task direction. The failure was not inherent to Stack support; it was a mismatch between the Lift-tuned query threshold and Stack's harder imitation/curriculum needs. The current candidate is not yet an efficiency claim because it spends the full 600-step budget and uses 50 demos. It is a strong seed-0 breadth candidate that should next be repeated on seeds 1-2 with matched none/random baselines under the same 50-demo protocol.
