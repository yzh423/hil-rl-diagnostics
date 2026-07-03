from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foresight_hil.evaluation.attention_diagnostics import (  # noqa: E402
    TRACE_STRATEGY_ORDER,
    collect_attention_trace_rows,
    rows_for_strategy,
)
from foresight_hil.evaluation.offline_trace_audit import (  # noqa: E402
    build_offline_gate_audit,
    build_phase_trace_summary,
    write_csv_rows,
)


R060 = ROOT / "results" / "r060_offline_trace_trigger_audit"


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def row_by_id(rows, gate_id):
    for row in rows:
        if row["gate_id"] == gate_id:
            return row
    raise ValueError(f"missing audit row: {gate_id}")


def build_decision_rows(audit_rows):
    original = row_by_id(audit_rows, "r023_lv_voi_original")
    actual_floor = row_by_id(audit_rows, "r024_score_floor_observed")
    posthoc_floor = row_by_id(audit_rows, "posthoc_score_after4k_ge0p05")
    phase_only = row_by_id(audit_rows, "posthoc_late_after4k_only")
    budget_cap = row_by_id(audit_rows, "posthoc_budget_frac_le0p60")
    saturation = row_by_id(audit_rows, "posthoc_drop_score_ge9p9")
    earliest_cap = row_by_id(audit_rows, "posthoc_earliest_random_count_cap")
    return [
        {
            "decision_id": "D1",
            "observation": (
                f"Post-hoc score floor keeps {posthoc_floor['retained_starts']} of "
                f"{original['retained_starts']} R023 LV-VoI starts, but the actual R024 "
                f"score-floor run still records {actual_floor['retained_starts']} starts."
            ),
            "implication": (
                "Accepted-start filtering is optimistic because online intervention "
                "decisions change later visited states and replacement starts."
            ),
            "recommendation": (
                "Do not expand the existing score-floor repair; require candidate-state "
                "logs or a new cost-matched online run before claiming a better trigger."
            ),
        },
        {
            "decision_id": "D2",
            "observation": (
                f"Phase-only gating after 4k keeps {phase_only['retained_starts']} starts, "
                f"leaving {phase_only['excess_starts_vs_random']} starts above the random target."
            ),
            "implication": "A phase gate alone does not explain or solve the over-triggering.",
            "recommendation": "Use phase information only as one component of a future pre-registered gate.",
        },
        {
            "decision_id": "D3",
            "observation": (
                f"Budget fraction <=0.60 keeps {budget_cap['retained_starts']} starts, while an "
                f"earliest-count cap keeps {earliest_cap['retained_starts']} starts to match random."
            ),
            "implication": (
                "Hard caps can control spending, but the trace does not show that the retained "
                "interventions improve success."
            ),
            "recommendation": (
                "Treat cost caps as experimental-control tools, not positive method evidence."
            ),
        },
        {
            "decision_id": "D4",
            "observation": (
                f"Dropping saturated score >=9.9 keeps {saturation['retained_starts']} starts, "
                f"still {saturation['excess_starts_vs_random']} above the random target."
            ),
            "implication": (
                "Score saturation is diagnostically useful, but removing saturated starts is "
                "not enough to match random spending."
            ),
            "recommendation": "Keep score saturation as a failure signal in the paper, not as a validated repair.",
        },
    ]


def build_manifest():
    return """# R060 Offline Trace Trigger Audit

Date: 2026-07-03

## Purpose

R060 executes the cheap trace/offline diagnostic step recommended by R059. It
uses existing R023/R024 intervention-start traces to audit whether simple
counterfactual gates would reduce LV-VoI intervention starts toward the
cost-matched random baseline.

This package does not add a new training run, edit historical CSVs, change
manuscript numerical claims, add citation keys, or support a positive LV-VoI
method claim.

## Inputs

| Source | Role |
|---|---|
| `results/r023_real_trace_seed0_2/trace_Lift_random_b350_seed*.csv` | Random b350 intervention-start reference. |
| `results/r023_real_trace_seed0_2/trace_Lift_voi_b600_seed*.csv` | Original LV-VoI scale3 intervention-start traces. |
| `results/r024_score_floor_seed0_2/trace_Lift_voi_b600_seed*.csv` | Observed score-floor repair intervention-start traces. |
| `results/r059_evidence_experiment_optimization/MANIFEST.md` | Planning source for the trace/offline audit route. |

## Outputs

| Artifact | Purpose |
|---|---|
| `phase_trace_summary.csv` | Phase-binned start counts and medians for random, original LV-VoI, and score-floor traces. |
| `offline_gate_audit.csv` | Post-hoc gate audit rows and observed-trace reference rows. |
| `offline_audit_decision_matrix.csv` | Decision rows translating the offline audit into next-experiment rules. |
| `TRACE_OFFLINE_AUDIT.md` | Human-readable audit narrative, limitations, and recommendation. |
| `foresight_hil/evaluation/offline_trace_audit.py` | Tested helper module for trace audit tables. |
| `scripts/generate_offline_trace_audit.py` | Regenerates this R060 package. |
| `tests/test_offline_trace_audit.py` | Regression tests for the R060 helper behavior. |

## Claim Boundary

R060 is diagnostic evidence about recorded intervention-start traces. It can
support statements about trace-level start counts, post-hoc gate retention, and
why accepted-start filtering should not be treated as online performance
evidence.

R060 does not support claims that a counterfactual gate improves success rate,
that score-floor LV-VoI is a positive method result, or that trace filtering
overturns the R021 cost-matched random dominance.

## Regeneration

```powershell
python scripts\\generate_offline_trace_audit.py
```

## Verification Record

Executed on 2026-07-03 after R060 code, registry, and documentation updates:

| Command | Result |
|---|---|
| `python scripts\\generate_claim_tables.py` | PASS: regenerated 5 R036 claim-table assets. |
| `python scripts\\generate_methodology_extension.py` | PASS: regenerated 3 R056 CSVs and 2 LaTeX tables. |
| `python scripts\\generate_offline_trace_audit.py` | PASS: regenerated 5 R060 audit artifacts. |
| `python scripts\\generate_stack_boundary_appendix.py` | PASS: regenerated 2 R053 Stack appendix assets. |
| `python scripts\\validate_evidence_registry.py` | PASS: 51 rows, 51 sources, 0 issues. |
| `python scripts\\audit_registry_numbers.py` | PASS: 94 numeric checks, 0 issues. |
| `python scripts\\validate_provenance_package.py` | PASS: 6 checks, 289 files, 0 issues. |
| `python scripts\\validate_document_links.py` | PASS: 135 documents, 33 links, 0 issues. |
| `python -m unittest discover -s tests` | PASS: 89 tests. A Gym deprecation warning was printed and is not a current test failure. |
| `git diff --check` | PASS: no whitespace errors; Git printed line-ending normalization warnings for generated text assets. |
"""


def build_audit_markdown(audit_rows, decision_rows):
    random_ref = row_by_id(audit_rows, "r023_random_reference")
    original = row_by_id(audit_rows, "r023_lv_voi_original")
    actual_floor = row_by_id(audit_rows, "r024_score_floor_observed")
    posthoc_floor = row_by_id(audit_rows, "posthoc_score_after4k_ge0p05")
    phase_only = row_by_id(audit_rows, "posthoc_late_after4k_only")
    budget_cap = row_by_id(audit_rows, "posthoc_budget_frac_le0p60")
    earliest_cap = row_by_id(audit_rows, "posthoc_earliest_random_count_cap")
    saturation = row_by_id(audit_rows, "posthoc_drop_score_ge9p9")
    decision_table = "\n".join(
        f"| {row['decision_id']} | {row['observation']} | {row['recommendation']} |"
        for row in decision_rows
    )
    return f"""# R060 Offline Trace Trigger Audit

Date: 2026-07-03

## Verdict

The offline audit is useful as a design screen, but it does not justify a new
positive method claim. The strongest result is a cautionary one: post-hoc
filtering of accepted LV-VoI starts can look aggressive, while the actual
online score-floor repair still spends nearly as many starts and remains
dominated in R024.

Observed start counts:

| Trace | Starts | Relation to random target |
|---|---:|---|
| R023 random b350 | {random_ref['retained_starts']} | Reference |
| R023 LV-VoI scale3 | {original['retained_starts']} | {original['excess_starts_vs_random']} above random |
| R024 observed score-floor LV-VoI | {actual_floor['retained_starts']} | {actual_floor['excess_starts_vs_random']} above random |

## Key Offline Findings

| Gate / comparison | Retained starts | Excess vs random | Interpretation |
|---|---:|---:|---|
| Post-hoc score >=0.05 after 4k on R023 LV-VoI | {posthoc_floor['retained_starts']} | {posthoc_floor['excess_starts_vs_random']} | Looks like it would over-reduce historical accepted starts, but actual R024 replacement dynamics contradict this as an online budget predictor. |
| Keep only starts after 4k | {phase_only['retained_starts']} | {phase_only['excess_starts_vs_random']} | Phase-only filtering removes early starts but leaves substantial over-triggering. |
| Drop score >=9.9 saturation | {saturation['retained_starts']} | {saturation['excess_starts_vs_random']} | Saturation is a diagnostic symptom, not enough by itself to match random spending. |
| Budget fraction <=0.60 | {budget_cap['retained_starts']} | {budget_cap['excess_starts_vs_random']} | A hard cap can nearly match the start-count target, but gives no success-rate evidence. |
| Earliest count cap matching random starts | {earliest_cap['retained_starts']} | {earliest_cap['excess_starts_vs_random']} | Matches count by construction; useful only as a control-design reminder. |

## Decision Matrix

| ID | Observation | Recommendation |
|---|---|---|
{decision_table}

## Boundary

These rows are derived from intervention-start traces only. They do not include
the full sequence of non-triggered candidate states, and they do not replay the
policy after a counterfactual rejection. Therefore, they should be used to
choose or reject future experiments, not to claim online trigger performance.

The next online experiment should be launched only if a gate is pre-registered,
logs accepted and rejected candidate states, and is compared against the
cost-matched random family before manuscript prose changes.
"""


def main():
    R060.mkdir(parents=True, exist_ok=True)
    trace_rows = collect_attention_trace_rows(ROOT)
    random_rows = rows_for_strategy(trace_rows, "random_b350")
    lv_rows = rows_for_strategy(trace_rows, "lv_voi_scale3")
    score_floor_rows = rows_for_strategy(
        trace_rows, "score_floor_vlv3_after4000_floor0p05"
    )

    phase_rows = build_phase_trace_summary(trace_rows, TRACE_STRATEGY_ORDER)
    audit_rows = build_offline_gate_audit(random_rows, lv_rows, score_floor_rows)
    decision_rows = build_decision_rows(audit_rows)

    write_csv_rows(R060 / "phase_trace_summary.csv", phase_rows)
    write_csv_rows(R060 / "offline_gate_audit.csv", audit_rows)
    write_csv_rows(R060 / "offline_audit_decision_matrix.csv", decision_rows)
    write_text(R060 / "MANIFEST.md", build_manifest())
    write_text(R060 / "TRACE_OFFLINE_AUDIT.md", build_audit_markdown(audit_rows, decision_rows))

    print(f"[r060] wrote {R060 / 'phase_trace_summary.csv'}")
    print(f"[r060] wrote {R060 / 'offline_gate_audit.csv'}")
    print(f"[r060] wrote {R060 / 'offline_audit_decision_matrix.csv'}")
    print(f"[r060] wrote {R060 / 'MANIFEST.md'}")
    print(f"[r060] wrote {R060 / 'TRACE_OFFLINE_AUDIT.md'}")


if __name__ == "__main__":
    main()
