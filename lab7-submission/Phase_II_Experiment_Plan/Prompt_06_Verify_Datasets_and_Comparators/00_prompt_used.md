# PROMPT 06 | Verify datasets and comparators

**SAVE (as required by the assignment):** Dataset and baseline validation sheet.

## Prompt as used

> My question is **[RQ1: with Qwen2.5-7B-Instruct fixed, is a 4-specialist tumor board (2 rounds + chair, 9 calls) more accurate than self-consistency with 9 samples on oncology exam questions? (plus RQ2 role ablation, RQ3 discussion effects)]** in **[medical multiple-choice question answering, oncology subset; zero-shot LLM inference]**. Recommend a primary dataset and two meaningful baseline methods or comparable controls, where feasible. For each candidate, identify the official source to verify, file structure, benchmark protocol, licensing/access terms, approximate compute requirement and common pitfalls. Explain an evaluation design appropriate to this domain: train/validation/test partitions when relevant, or a justified alternative for systems/HCI/security studies. Specify likely leakage risks such as patient-, subject-, document-, company- or time-level overlap as applicable. Do not present unverified access claims as facts. End by recommending the simplest credible baseline and a short independent-verification checklist.

Placeholders filled: [RESEARCH QUESTION], [TASK/DOMAIN].
Tool: Claude (claude.ai project workspace, web search, Linux workspace without GPU; Hugging Face not reachable from it).

## Files in this folder

- `dataset_and_baseline_validation_sheet.md` — the validation sheet (datasets, baselines vs original papers, evaluation design, leakage risks, checklist, decisions L-16–L-19)
- `dataset_sanity_checks.py` + `dataset_sanity_checks_output.json` — real model-free checks on the MedQA files (sizes, label balance, trivial-heuristic floors, near-duplicates)
- `leakage_checks.py` + `leakage_checks_selftest_output.txt` — cross-file overlap checker and its self-test on MedQA
