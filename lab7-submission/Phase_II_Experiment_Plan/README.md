# Phase II — Experiment plan (Prompts 06–07)

Status: **complete** (24 Oct 2026). The protocol is frozen at v1.1 before any model output exists.

| Prompt | Folder | SAVE item required by the assignment | File(s) |
|---|---|---|---|
| 06 | `Prompt_06_Verify_Datasets_and_Comparators/` | Dataset and baseline validation sheet | `dataset_and_baseline_validation_sheet.md`, `dataset_sanity_checks.py` + output, `leakage_checks.py` + self-test output |
| 07 | `Prompt_07_Freeze_Experiment_Blueprint/` | Frozen evaluation protocol, flowchart and pre-experiment checklist | `frozen_evaluation_protocol.md`, `frozen_protocol.yaml`, `experiment_architecture.png` / `.mmd` |

Phase-level file: `research_decisions_phase_II.md` (L-16 to L-21).

## Phase II result in one paragraph
Primary data = pooled oncology subsets of MedQA (97 items, verified and hashed) and MedMCQA dev (size to be measured on Kaggle; the official README's split table is ambiguous). Baselines = greedy zero-shot CoT (Kojima et al. 2022) and self-consistency (Wang et al. 2023), with deviations from the originals recorded. Real model-free checks showed that always answering "B" scores 27.8% on the oncology subset, so that, not 20%, is the floor any method must beat. The protocol fixes the decision rule, the minimum-detectable-effect reporting for nulls, the seed plan, table and figure shells, threats to validity, and how later changes are logged.

## Open items carried into Phase III
- `evaluate.py` still lists the v1.0 comparisons (fix before any real evaluation; L-21)
- MedMCQA subset, leakage checks and smoke test can only run on Kaggle (Hugging Face is not reachable from the AI workspace)
