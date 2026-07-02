# R047 Compute And Command Gap Analysis

Date: 2026-07-02

## Compute Accounting

R047 performs a best-effort scan of the paper-core result directories R020-R024.
The scan found 82 CSV files and extracted available row counts, seeds, training
steps, evaluation episodes, and wall-time columns where those fields were
present.

Only three CSVs contain explicit `wall_time_s` fields:

| Source | Rows | Seeds | Steps | Eval episodes | Wall time sum (s) |
|---|---:|---|---:|---:|---:|
| `results/r022_lift_min_disagree_seed0_2/robosuite_hil_summary.csv` | 3 | 0;1;2 | 10000 | 20 | 2062.9 |
| `results/r023_real_trace_seed0_2/robosuite_hil_summary.csv` | 6 | 0;1;2 | 10000 | 20 | 3649.1 |
| `results/r024_score_floor_seed0_2/robosuite_hil_summary.csv` | 3 | 0;1;2 | 10000 | 20 | 3235.8 |

The explicitly recorded wall time sums to 8947.8 seconds. This is not the full
historical compute cost of the project. It is the recoverable wall-clock
accounting available from the scanned CSV fields.

## Command Provenance

The command inventory found five archived command files:

| Command file | Bytes | Use |
|---|---:|---|
| `results/r023_real_trace_seed0_2/driver.cmd.txt` | 526 | Preferred R023 driver command evidence. |
| `results/r023_real_trace_seed0_2/random_b350.cmd.txt` | 522 | Preferred R023 random_b350 command evidence. |
| `results/r024_score_floor_seed0_2/run_driver.cmd` | 808 | Preferred R024 driver command evidence. |
| `results/r024_score_floor_seed0_2/driver.cmd.txt` | 605 | R024 archived driver command evidence. |
| `results/r024_score_floor_seed0_2/hidden_test.cmd` | 155 | Helper command only; do not cite as a paper-core reproduction command. |

R020 and R021 do not contain complete central launch command files in their
result directories. For those runs, use the registry rows, primary CSVs, R044
reproduction command sheet, run labels, and checkpoint records as supporting
reproducibility context, while stating the command-provenance gap plainly.

## Interpretation

R047 improves reproducibility by converting implicit project knowledge into
inspectable ledgers. It does not fully reconstruct historical wall-clock cost or
all original launch commands. That limitation should be treated as an artifact
review disclosure and a design requirement for future runs.

## Future Run Requirement

Every future paper-facing run should archive the following before or at launch:

- Exact command line.
- Environment snapshot.
- Source snapshot or valid commit hash.
- Standard output and standard error logs.
- Result manifest.
- Wall-clock runtime and hardware note.
- Registry row before the result is cited in prose.
