# R015 Decision Note

R015 started the second-task breadth check on robosuite `Stack`.

## Infrastructure result

The original non-Lift scripted oracle failed (`0/3` success on Stack/PickPlace/Nut/Door). The Stack path is now enabled by exposing `cubeA_pos`, `cubeB_pos`, `gripper_to_cubeA`, and `gripper_to_cubeB` from `privileged_state()`, plus a Stack-specific pick-place scripted oracle. A direct oracle smoke test reached `5/5` Stack success.

## Learning result

Stack is substantially harder than Lift under the current autonomous policy setup. A BC-only probe with 20 demos and 5000 BC steps produced only `3/20` raw eval success before online RL.

Seed-0 repeated best-checkpoint results:

- No-intervention restore-best: `28/60 = 46.7%`, Wilson CI `34.6-59.1%`, best-step cost `0`.
- Random restore-best, budget 600: `26/60 = 43.3%`, Wilson CI `31.6-55.9%`, best-step cost `373`.
- Learning-value VoI, budget 600, scale 3: `22/60 = 36.7%`, Wilson CI `25.6-49.3%`, best-step cost `80`.

## Interpretation

This is a negative transfer result for the current Lift-tuned method. It should not be expanded to Stack seeds 1-2 as a main comparison yet. The useful next step is to diagnose Stack-specific failure modes and retune the intervention trigger or task curriculum before claiming robotics breadth.
