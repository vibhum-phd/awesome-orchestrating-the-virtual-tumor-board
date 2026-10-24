# PROMPT 13 | Evaluate using real outputs only

**SAVE (as required by the assignment):** Metrics script, actual result CSV, tables and research figures.

## Prompt as used

> I have real experimental outputs in **[results/raw/*.jsonl + run_meta.jsonl — NOT YET PRODUCED; Kaggle runs pending]** for **[greedy CoT, self-consistency @k, specialist tumor board, generic-agent board]**, evaluated on **[MedQA-USMLE oncology subset and MedMCQA-dev oncology subset (pooled + by source); full MedQA test as secondary]**. Write evaluation code that checks ID/label alignment, missing values, partitions and metric direction before computing **[accuracy, paired differences with bootstrap CIs, exact McNemar with Holm, member flip rates, efficiency]**. Compare methods under consistent conditions, summarize multiple runs or uncertainty where applicable, and export traceable results.csv plus publication-quality PNG/PDF figures. Show how to audit for leakage and incompatible comparator settings. Never invent example values inside the final evaluation tables or claim statistical significance without a valid test and assumptions. Ask for required files before interpreting my numerical results.

Placeholders filled: [CSV/LOG/FILE], [METHODS], [DATASET/SPLIT], [METRICS] — with the honest note that real outputs do not exist yet.

## Files in this folder

- `evaluation_procedure_and_audit.md` — checks run before metrics, comparison logic (protocol v1.1), uncertainty, outputs, leakage audit, comparator-settings audit, list of files required before interpretation, decisions L-30–L-33
- `evaluation_code/` — `evaluate.py`, `stats.py` (exact McNemar power / MDE, cluster bootstrap), the protocol YAML, test-suite result (46/46)
- `SYNTHETIC_demo_outputs_mock_backend/` — every output file produced from **mock** model outputs to show the format; watermarked; not results

## Status
Script complete and tested. **Actual result CSV: PENDING** real runs (notebook 03, Prompt 12).
