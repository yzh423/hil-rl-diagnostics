# Paper Claim Audit

Date: 2026-07-03

## Verdict

PASS after R056 methodology-extension integration and visual QA.

The current manuscript's main numerical, comparison, methodology, and scope
claims are supported by the evidence registry and primary sources inspected in
this audit. The protected scientific position still holds:

- R021 `random_b350` dominates LV-VoI scale3 on Lift under cost matching.
- R022 minimum-disagreement and R024 score-floor repairs remain dominated by
  same-seed `random_b350`.
- R023/R024 traces diagnose intervention-spending mechanisms; they do not
  overturn the R021 success-cost result.

R056 adds a derived protocol gate matrix, failure-mode taxonomy, stop-rule
metrics, and methodology-first Fig. 1 candidate from registered R021/R023/R024
evidence. This changes the clarity and auditability of the methodology
presentation, not the empirical claim boundary. The earlier R052
reproducibility wording repair remains in force: current source state is
tracked in GitHub while R048 preserves the earlier invalid-Git source snapshot
and command-provenance boundary.

## Audit Scope

Execution note: the current environment requires explicit user authorization
before spawning a sub-agent, so this is a direct file-driven audit rather than a
delegated fresh-reviewer audit.

Manuscript and display artifacts checked:

- `paper/main.tex`
- `paper/sections/01_introduction.tex`
- `paper/sections/03_protocol_setup.tex`
- `paper/sections/04_results.tex`
- `paper/sections/05_discussion.tex`
- `paper/sections/06_conclusion.tex`
- `paper/sections/07_reproducibility_inventory.tex`
- `figures/TABLE_registry_costmatched_results_r036.tex`
- `figures/TABLE_registry_trigger_repairs_r036.tex`
- `figures/TABLE_protocol_checklist.tex`
- `figures/TABLE_protocol_gate_matrix_r056.tex`
- `figures/TABLE_failure_taxonomy_r056.tex`
- `figures/fig1_methodology_protocol_r056.pdf`
- `figures/fig1_methodology_protocol_r056.png`
- `figures/fig1_methodology_protocol_r056_grayscale.png`
- `figures/fig_attention_allocation_diagnostics_r054.pdf`
- `results/r054_attention_allocation_figure_optimization/attention_allocation_trace_profile.csv`
- `results/r056_methodology_extension/protocol_gate_matrix.csv`
- `results/r056_methodology_extension/failure_taxonomy.csv`
- `results/r056_methodology_extension/derived_attention_metrics.csv`
- `results/r056_methodology_extension/MANIFEST.md`
- `foresight_hil/evaluation/attention_diagnostics.py`
- `foresight_hil/evaluation/protocol_diagnostics.py`
- `scripts/generate_methodology_extension.py`
- `figures/gen_r056_methodology_figure.py`
- `tests/test_attention_diagnostics.py`
- `tests/test_protocol_diagnostics.py`

Primary evidence sources checked:

- `results/EXPERIMENT_EVIDENCE_REGISTRY.csv`
- `results/r020_lift_highn_reliability/r020_lift_highn_aggregate.csv`
- `results/r021_random_costmatch/r021_costmatch_aggregate.csv`
- `results/r022_lift_min_disagree_seed0_2/r022_min_disagree_aggregate.csv`
- `results/r023_real_trace_seed0_2/r023_trace_strategy_diagnostics.csv`
- `results/r024_score_floor_seed0_2/r024_score_floor_aggregate.csv`
- `results/r024_score_floor_seed0_2/r024_trace_strategy_compare.csv`
- `results/r018_stack_multiseed_alignment/r018_stack_multiseed_aggregate.csv`
- `results/r047_evidence_provenance_package/EVIDENCE_PROVENANCE_AUDIT.md`
- `results/r048_version_command_provenance/VERSION_PROVENANCE_REPAIR.md`

## Claim Checks

| Claim family | Manuscript location | Source checked | Verdict |
|---|---|---|---|
| Cost-matched reversal: `random_b350` has higher repeated success and lower realized human-step cost than LV-VoI scale3. | `paper/main.tex:21`, `paper/sections/01_introduction.tex:7`, `paper/sections/04_results.tex:3` | R021 aggregate and registry rows: `439/500 = 87.8%`, CI `[84.6, 90.4]`, cost `177.0`; LV-VoI `416/500 = 83.2%`, CI `[79.7, 86.2]`, cost `202.0`. | PASS |
| Original higher-cost random comparison is superseded by the random-family sweep. | `paper/sections/03_protocol_setup.tex:3`, `paper/sections/04_results.tex:14`, `paper/sections/05_discussion.tex:3` | R020 aggregate and R021 aggregate: original random/random_b600 `426/500 = 85.2%`, cost `269.2`; random_b450 `426/500`, cost `250.0`; random_b350 `439/500`, cost `177.0`. | PASS |
| Trigger repairs remain negative under same-seed comparison. | `paper/sections/04_results.tex:16`, `paper/sections/06_conclusion.tex:3` | R022/R024 aggregates: min-disagree `226/300 = 75.3%`, CI `[70.2, 79.9]`, cost `211.7`; score-floor `233/300 = 77.7%`, CI `[72.6, 82.0]`, cost `253.3`; same-seed random `259/300 = 86.3%`, CI `[82.0, 89.8]`, cost `95.0`. | PASS |
| Trace diagnosis: LV-VoI is not simply querying far from the cube. | `paper/sections/03_protocol_setup.tex:13`, `paper/sections/04_results.tex:27`, `paper/sections/05_discussion.tex:7` | R023 trace diagnostics: LV-VoI mean g2c norm `0.217166` vs random `0.284851`; LV-VoI mean g2c xy `0.152267` vs random `0.235331`; starts `96` vs `55`. | PASS |
| Score-floor repair mechanically removes low-score post-floor starts but remains too unselective. | `paper/sections/04_results.tex:29`, `paper/sections/05_discussion.tex:7` | R024 trace compare: score-floor starts `94`; original LV-VoI starts `96`; random starts `55`; `after_floor_low_score_starts = 0`; median accepted score `0.067165`. | PASS |
| R054 diagnostic figure does not add a new empirical claim. | `paper/sections/04_results.tex:20` | R054 manifest and profile table show the figure is derived from registered R021/R023/R024 sources; the caption states that it is diagnostic visualization and not a new positive method claim. | PASS |
| R056 methodology extension is derived from registered evidence and does not add a new experiment. | `paper/sections/03_protocol_setup.tex:5`, `paper/sections/04_results.tex:5`, `paper/sections/05_discussion.tex:11` | R056 manifest, gate matrix, taxonomy, derived metrics, helper module, and figure assets trace to R021/R023/R024. The figure and tables formalize protocol verdicts and failure modes; they do not claim LV-VoI superiority. | PASS |
| Stack is boundary evidence, not positive generalization. | `paper/sections/03_protocol_setup.tex:15`, `paper/sections/04_results.tex:31`, `paper/sections/05_discussion.tex:15` | R018 aggregate: no-online matched BC `131/180 = 72.8%`, cost `0.0`; random matched BC `107/180 = 59.4%`, cost `478.0`; Stack-tuned LV-VoI `107/180 = 59.4%`, cost `433.3`. R019 variants remain below no-online seed0 reference. | PASS |
| Scripted privileged-state oracle and non-real-human boundary. | `paper/main.tex:25`, `paper/sections/03_protocol_setup.tex:17`, `paper/sections/05_discussion.tex:15` | Manuscript repeatedly states that the intervention source is scripted and simulated; no claim of real teleoperator or hardware validation was found. | PASS |
| Reproducibility provenance language. | `paper/sections/07_reproducibility_inventory.tex:24`, `paper/sections/07_reproducibility_inventory.tex:44`, `paper/sections/07_reproducibility_inventory.tex:49` | R047/R048/R049 and current Git state checked. Wording distinguishes current public Git source tracking from R048 historical invalid-Git snapshot. | PASS AFTER REPAIR |

## Issue Log

| ID | Severity | Finding | Action |
|---|---|---|---|
| R052-I1 | Low | Reproducibility appendix still described invalid local `.git` metadata as the current source-provenance state, although the project now has a valid public GitHub repository. | Updated `paper/sections/07_reproducibility_inventory.tex` to state that current source state is tracked in GitHub and R048 is the historical repair record. |
| R055-I1 | Low | The optimized R054 diagnostic composite existed as a paper artifact but was not yet connected to the Results narrative or current claim-audit state. | Included the figure in `paper/sections/04_results.tex`, added an explicit no-new-claim caption, and updated the current audit scope. |
| R056-I1 | Low | The methodology contribution still relied partly on narrative checklist wording and the older R029 hero, leaving the gate/stop protocol less auditable than the underlying evidence. | Added R056 derived gate matrix, failure taxonomy, stop-rule metrics, and methodology-first Fig. 1; integrated them into Methods, Results, Discussion, and the asset indexes. |

## Boundaries To Preserve

- Do not turn the R021 reversal into a positive LV-VoI method claim.
- Do not treat R023/R024 traces as primary success-rate evidence.
- Do not present Stack as a broad robotics-transfer success.
- Do not claim complete historical wall-clock accounting; R047 only supports
  partial compute accounting where historical CSVs recorded it.
- Do not claim complete original R020/R021 launch logs; R048 provides bounded
  reconstruction and source-snapshot provenance.
- Do not claim real-human or real-robot validation.

## Input Hashes

| File | SHA-256 |
|---|---|
| `paper/main.tex` | `D23DF1DBC3AFC20F4BC5EDB0467405B13319A3F54B74BF99F90C94DCC3A111E6` |
| `paper/sections/01_introduction.tex` | `59EF6A010B14B650DC58916334780403EAB82EB0AE559799660F2832385E7BF1` |
| `paper/sections/03_protocol_setup.tex` | `7E7357E848BBEFD5A095261E067564AE3BCF091847396DF124B663C10EBF905F` |
| `paper/sections/04_results.tex` | `683AAEB019C20759C0B6B8F17CDDF4AF4F6BAE6BA4F105453A5B5AFCDCC5770E` |
| `paper/sections/05_discussion.tex` | `4CD75348E15C5AB6C82AEFE9216D9F2F072D6E81227E2F256198D118450987B7` |
| `paper/sections/07_reproducibility_inventory.tex` | `DEC1A2670EEF5DA7649A8A59241BDD77C92B388991DF3082E815673295E63109` |
| `figures/TABLE_registry_costmatched_results_r036.tex` | `F437FA8A45D3DE8E76D5DA944536A49BDA02523F82A3236AE504470D5316D6CE` |
| `figures/TABLE_registry_trigger_repairs_r036.tex` | `1CFC17081C58231E4BCB2673C02321C5ED75606D2EFAE09D19E5CC9659A97650` |
| `figures/TABLE_protocol_gate_matrix_r056.tex` | `0DD62557C96CCCFBF5A24D3B75698D491102951D83E214153DDE347C9E93DC23` |
| `figures/TABLE_failure_taxonomy_r056.tex` | `8816A461FD67761F93774DB9CE3993869EBABF1C2E5ED46625BC9F6FA5D50A79` |
| `figures/fig1_methodology_protocol_r056.pdf` | `98EB6059302FD4D09EADAA3560E2EF4DB81A852DA76B6DCE64EAAA00FB2E3D3F` |
| `figures/fig_attention_allocation_diagnostics_r054.pdf` | `968E20E41ECB515087C702BDA590F61260A4F6ABC7DA0779E43FCB04D7959238` |
| `results/r054_attention_allocation_figure_optimization/attention_allocation_trace_profile.csv` | `71A72BD986896C5F1416EABC235D90FBA7A8A40001EBEA96581A3BCD532F8CE1` |
| `results/r056_methodology_extension/protocol_gate_matrix.csv` | `C357FF17DB008E35EB41A0313955C297AFAD3E3B7FCE6706CF186D707030A7FE` |
| `results/r056_methodology_extension/failure_taxonomy.csv` | `6F5A81D045D8AA42C40C0A75931CA8A29624E6084AC7C9C541A893F1CD782030` |
| `results/r056_methodology_extension/derived_attention_metrics.csv` | `709EBD015E398E85EED8AE70C372D40E410C4D358E1F8357F9C778F9537BB61A` |
| `results/r056_methodology_extension/MANIFEST.md` | `A0D85DC82478A25BA4543FF506EB7383B87060C96BFE058C76927CF062382B78` |
| `foresight_hil/evaluation/attention_diagnostics.py` | `5611867D89B59995549E1C71092877928A0E0B2D038416C19EBAAC81609548B8` |
| `foresight_hil/evaluation/protocol_diagnostics.py` | `0E520B7CE5FE55E01E5301526B464BA594365D70C06172F68982C3ED5F2C8C18` |
| `tests/test_attention_diagnostics.py` | `C96891B9DA6A560A95DC792D2337DFF329CF5BB30EB1DC636EA0D91C31E24E3E` |
| `tests/test_protocol_diagnostics.py` | `095CA6A28B2D4A4946543A3BCEABA10507477C8C03B982F5E7710E0B354741DA` |
| `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` | `133E1EA26086533B2B012FBE72B0BDAD1AF148E73373D1BD7C02EBDF8F954A81` |
| `results/r021_random_costmatch/r021_costmatch_aggregate.csv` | `00BC94D47414DB10B135CAE4CA8476506E6B7812EF771BEE408E77B4A22173DE` |
| `results/r022_lift_min_disagree_seed0_2/r022_min_disagree_aggregate.csv` | `63C5800AA911BCA61A0FD1EE887C2631A95F48CBEC1DD12AC87ED5DF55F46BEE` |
| `results/r023_real_trace_seed0_2/r023_trace_strategy_diagnostics.csv` | `45943D9865F89DB3554C305BF3603FAABE9B707137D9B2BC78C2BFC8E1D186D2` |
| `results/r024_score_floor_seed0_2/r024_score_floor_aggregate.csv` | `ECF086FD3C772AB8DE6590938D80CC05A076E628CEA89BBA849828C46F726625` |
| `results/r024_score_floor_seed0_2/r024_trace_strategy_compare.csv` | `38EAAB99325A934192E594C9FC6C262F9ADDFA336E7BC7AB0E29F34CE4937C3A` |
| `results/r018_stack_multiseed_alignment/r018_stack_multiseed_aggregate.csv` | `E1D84D583717A60C5D03726DDC654A3459BE0EB1201128459EAD5BDE25D8EBD0` |
| `results/r047_evidence_provenance_package/EVIDENCE_PROVENANCE_AUDIT.md` | `E3B50385B088DA3909F4D484FD5B895BD87390A6A698831E034A4DFAEDFEF025` |
| `results/r048_version_command_provenance/VERSION_PROVENANCE_REPAIR.md` | `864DA9FCE05840658E6CC8CC70327F3073EE4BF6E7AD8AADEBDC09040C5A3D54` |
