# R043 Venue Target Matrix

Date: 2026-07-02

## Decision

Primary target route: **IEEE Transactions on Automation Science and Engineering
(T-ASE)**.

Stretch target: **IEEE Transactions on Robotics (T-RO)**, only if the paper is
strengthened with a larger robotics validation story, preferably real-hardware
or substantially broader manipulation evidence.

Fast/short route: **IEEE Robotics and Automation Letters (RA-L)**, only if the
manuscript is compressed into a concise letter and the diagnostic story can fit
within the page budget.

Fallback route: **Robotics and Autonomous Systems (RAS)** or **Engineering
Applications of Artificial Intelligence (EAAI)**, depending on whether the final
paper is framed as a robotics evaluation protocol or an applied-AI
benchmarking/reproducibility protocol.

Important boundary: official publisher pages verify current impact factors,
scope, page constraints, and review-positioning signals. They do not replace a
final institutional check in Web of Science JCR and the Chinese Academy of
Sciences journal partition table before submission.

## Why T-ASE Is The Best Primary Fit

The current project is not a positive robot-learning method paper. It is a
diagnostic evaluation protocol with a robotic manipulation case study:
cost-matched random-family evaluation, repeated checkpoint evaluation, trace
diagnostics, and negative trigger-repair findings. T-ASE explicitly welcomes
methodologies, models, systems, and case studies that improve efficiency,
quality, productivity, and reliability. That language matches the manuscript's
strongest contribution better than T-RO's "major advances" framing.

T-ASE also has a practical review culture fit: the official page reports a 2025
impact factor of 7.9, about 29% acceptance rate, first decision under 3 months,
and submission-to-online publication under 9 months. Those numbers make it a
strong SCI Q1-oriented target if final JCR/CAS checks confirm the required
partition.

## Candidate Matrix

| Rank | Venue | Role | Official signals | Fit to current paper | Main risk | Required positioning |
|---:|---|---|---|---|---|---|
| 1 | IEEE T-ASE | Primary | IF 7.9 in 2025; publishes abstractions, algorithms, theory, methodologies, models, systems, and case studies; emphasizes efficiency, quality, productivity, reliability. | Strong. The protocol is an automation-science contribution, not a failed trigger story. | Reviewers may ask for broader task coverage and practical relevance. | Frame as "diagnostic evaluation protocol for intervention-trigger claims in robotic HIL-RL"; add a Note to Practitioners style paragraph. |
| 2 | IEEE T-RO | Stretch | IF 10.5 in 2024; publishes major advances across robotics. | Prestigious but demanding. The current paper is simulation-only and negative for the trigger. | "No real robot / no real human / no positive robotics advance" could be fatal. | Use only if adding stronger robotics evidence, real-hardware complement, or a crisp benchmark release that looks like a field-level contribution. |
| 3 | IEEE RA-L | Fast concise route | IF 5.3 in 2024; six pages plus at most two paid extra pages; fast review; conference-presentation transfer option. | Possible if compressed to a compact diagnostic letter. | The current argument needs space for protocol, evidence, traces, and limitations. | Turn into a concise "evaluation lesson" letter and move most diagnostics to supplement. |
| 4 | Robotics and Autonomous Systems | Robotics fallback | IF 5.2; scope includes robot control, learning, autonomous systems, and theoretical/computational/experimental aspects. | Good robotics fit and more forgiving for simulation-based autonomous-system studies. | May be less prestigious than IEEE T-ASE/T-RO for an SCI1 target depending on partition year. | Emphasize autonomous manipulation learning, simulator protocol, reproducible benchmark artifacts. |
| 5 | Engineering Applications of Artificial Intelligence | Applied-AI fallback | IF 8.0; requires novel AI contribution and real-world engineering validation or public datasets; robotics is listed in scope. | Viable only if the public benchmark/protocol angle is made central. | Current novelty is evaluation protocol, not a new AI algorithm. | Present as an engineering-AI validation protocol with public data/code and clear AI contribution. |
| 6 | Autonomous Robots | Defer unless robotics evidence improves | IF 6.0 in 2025; explicitly features performance data on actual robots in the real world. | Topic fit is good, but evidence fit is weak. | The current experiments use simulation and a scripted oracle. | Add real-robot or much stronger physical-robotics validation before targeting. |
| 7 | IEEE Transactions on Robot Learning | Future-fit, not strict SCI route yet | Scope is excellent for robot learning, benchmarks, reproducibility, and HRI/robot collaboration; real hardware in addition to or complementing simulation is expected. | Conceptually excellent for a future expanded version. | New venue status and hardware expectation make it risky for the immediate SCI Q1 goal. | Track for later, especially if RoboCasa/real-robot evidence is added. |

## Target-Driven Revision Tasks

### T-ASE Primary Revision

1. Rewrite the title and abstract toward automation-science language:
   "diagnostic evaluation protocol", "human-intervention allocation",
   "cost-matched evaluation", "reliability", and "robotic manipulation case
   study".
2. Add a "Note to Practitioners" style paragraph that says what an HIL-RL
   practitioner should do differently: sweep random budget families, report
   repeated checkpoint intervals, trace intervention starts, and stop a method
   claim when cost-matched random dominates.
3. Make the negative result sound productive: the paper prevents an unsupported
   trigger-superiority claim and provides a reusable protocol.
4. Strengthen reproducibility: expose registry-driven tables, exact seeds,
   configs, trace schemas, and code paths as first-class artifacts.
5. Decide whether to add one additional robotics validation package before
   submission. The most useful options are:
   - a cleaned Stack boundary-evidence appendix from R018/R019;
   - a small RoboCasa feasibility/diagnostic pilot if the environment is
     already locally usable;
   - a compact cross-task table that emphasizes protocol behavior rather than
     method superiority.

### T-RO Stretch Gate

Do not target T-RO in the current form. Reconsider only if at least one of the
following becomes true:

- a real-robot or real-human intervention result is added;
- the evaluation protocol is released as a reusable benchmark package with
  multiple manipulation tasks and clear adoption value;
- a substantially new trigger mechanism beats cost-matched random under the
  R020-R024 discipline.

### RA-L Compression Gate

RA-L is useful if speed and conference presentation matter more than full
journal depth. To fit RA-L, the manuscript would need:

- one main claim table;
- one compact protocol/trace figure;
- one short results section;
- most trace diagnostics, citation detail, and Stack boundary evidence moved to
  supplementary material.

## Recommended Next Tasks

| Order | Task | Acceptance criteria |
|---:|---|---|
| 1 | T-ASE manuscript alignment pass | `paper/main.tex` and section headings use T-ASE/automation-science language without changing evidence claims. |
| 2 | Note to Practitioners draft | A short practitioner paragraph exists in `paper/sections/05_discussion.tex` or a target-specific notes file. |
| 3 | Reproducibility appendix inventory | A table lists scripts, seeds, configs, result directories, trace schema, and claim-table generation commands. |
| 4 | Decide additional robotics evidence | Choose one: no new runs, Stack appendix cleanup, RoboCasa feasibility pilot, or real-robot/human future work. |
| 5 | LaTeX compile/runtime fix | Local PDF build either works or the project explicitly keeps TeX-only drafting until submission formatting. |

## Source Ledger

| Venue | Source |
|---|---|
| IEEE T-RO | <https://www.ieee-ras.org/publications/t-ro/> |
| IEEE T-ASE | <https://www.ieee-ras.org/publications/t-ase/> |
| IEEE RA-L | <https://www.ieee-ras.org/publications/ra-l/> |
| Robotics and Autonomous Systems | <https://www.sciencedirect.com/journal/robotics-and-autonomous-systems> |
| Engineering Applications of Artificial Intelligence | <https://www.sciencedirect.com/journal/engineering-applications-of-artificial-intelligence> |
| Autonomous Robots | <https://link.springer.com/journal/10514> |
| IEEE Transactions on Robot Learning | <https://www.ieee-ras.org/publications/t-rl/> |
