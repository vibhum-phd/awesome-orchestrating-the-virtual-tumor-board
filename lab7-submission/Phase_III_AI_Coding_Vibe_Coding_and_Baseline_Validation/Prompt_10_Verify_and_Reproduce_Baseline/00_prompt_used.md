# PROMPT 10 | Verify and reproduce the baseline

**SAVE (as required by the assignment):** Baseline reproduction/validation report, including discrepancies.

## Prompt as used

> I have implemented **[zero-shot CoT and self-consistency with Qwen2.5-7B-Instruct]** based on **[Kojima et al. 2022 (NeurIPS) and Wang et al. 2023 (ICLR); no official code reused]**. Here are the code, dataset partition, configurations, actual logs and measured results: **[src/vtb/*, scripts/*, configs/frozen_protocol.yaml v1.1, MedQA test + oncology subset manifest, unit-test logs; real-model results: NOT YET AVAILABLE — Kaggle run pending]**. Audit the implementation against the original methodology: preprocessing, architecture, hyperparameters, random seeds, evaluation metric, data split and benchmark protocol. Design unit/sanity tests, inspect any discrepancy with reported results, and distinguish acceptable adaptations from changes that invalidate comparison. Produce a baseline validation report with VERIFIED, UNCERTAIN and NEEDS CORRECTION items, plus the exact additional checks required. Do not state that code is correct simply because it runs, and do not demand exact numerical replication under different conditions. Only after validation should we test extensions or comparisons.

Placeholders filled: [BASELINE], [PUBLISHED PAPER / OFFICIAL CODE], [FILES] — with the honest note that real results do not exist yet.

## Files in this folder

- `baseline_validation_report.md` — Part A audit (13 items; 2 NEEDS CORRECTION, 1 fixed), Part B pre-registered acceptance criteria (measured column PENDING), Part C acceptable vs invalidating discrepancies, Part D exact next checks, decisions L-25–L-27
- `baseline_report.py` — the script that turns real baseline outputs into the Part B numbers
- `synthetic_pipeline_check/` — the same script run on mock outputs, clearly labelled SYNTHETIC

## Status
PARTIAL — Part B waits for `baseline_outputs.zip` from `02_baseline_kaggle.ipynb`.
