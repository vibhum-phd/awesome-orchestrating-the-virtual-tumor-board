# Phase IV — Contribution and evidence (Prompts 12–14)

Status: **code and plans complete; evidence PENDING real runs.** Nothing in this phase reports a model result.
Files from the mock backend are in folders named `SYNTHETIC_…` and are watermarked.

| Prompt | Folder | SAVE item | State |
|---|---|---|---|
| 12 | `Prompt_12_Choose_a_Defensible_Contribution/` | Chosen contribution pathway and executable comparison plan | Pathway B (provisional until the baseline is validated); notebook 03 ready, gated |
| 13 | `Prompt_13_Evaluate_Using_Real_Outputs_Only/` | Metrics script, actual result CSV, tables and figures | Script complete and tested (46/46); now follows protocol v1.1 (DBG-11 closed). **Actual CSV PENDING** |
| 14 | `Prompt_14_Interpret_Outcomes_Including_Negative_Results/` | Results and Discussion outline with limitations | Pre-registered interpretation plan + outline with slots; **interpretation PENDING** |

Phase-level file: `research_decisions_phase_IV.md` (L-30 to L-38).

## Run order on Kaggle
01 (environment + smoke) → 02 (baseline) → fill Prompt 10 Part B, create `results/baseline/VALIDATED` → 03 (main grid) → `evaluate.py` → Prompt 14 slots.
