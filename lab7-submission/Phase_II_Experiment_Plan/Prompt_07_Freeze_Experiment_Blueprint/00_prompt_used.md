# PROMPT 07 | Freeze an experiment blueprint before viewing results

**SAVE (as required by the assignment):** Frozen evaluation protocol, flowchart and pre-experiment checklist.

## Prompt as used

> Design a reproducible protocol for **[RQ1: with Qwen2.5-7B-Instruct fixed, is a 4-specialist tumor board (9 calls) more accurate than self-consistency with 9 samples? + RQ2 role ablation + RQ3 discussion effects]** on **[pooled oncology subsets of MedQA-USMLE (5-option test) and MedMCQA (dev); full MedQA test as secondary]** comparing **[B1 greedy zero-shot CoT; B2 self-consistency @k = 1, 3, 5, 9, 15]** with **[specialist tumor board (4 roles, 2 rounds + chair) and generic-agent board ablation]**. Include precise input/output definitions, modules, preprocessing, Mermaid architecture diagram, data partitions, controls, training or processing settings, evaluation metrics (with whether higher/lower is better), random seed plan, computational budget and expected table/figure formats. Include at least one deep analysis: ablation, error/failure, robustness, efficiency or sensitivity. Define threats to validity and a pre-experiment checklist to freeze the primary metric, test split and comparison protocol before viewing results. Explain how legitimate protocol changes should be logged later. Never fabricate anticipated outcomes.

Placeholders filled: [QUESTION], [DATASET], [BASELINES], [PROPOSED STUDY].
Tool: Claude (claude.ai project workspace, Linux workspace without GPU).

## Files in this folder

- `frozen_evaluation_protocol.md` — the protocol (14 sections: I/O definitions, modules, preprocessing, partitions, controls, metrics, seeds, budget, table/figure shells, deep analyses, threats, pre-experiment checklist, change-logging rules, decisions L-20–L-21)
- `frozen_protocol.yaml` — machine-readable protocol v1.1 used by the code
- `experiment_architecture.mmd` + `experiment_architecture.png` — Mermaid flowchart (rendered with mermaid-cli)
