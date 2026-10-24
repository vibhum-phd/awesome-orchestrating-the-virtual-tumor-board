# PROMPT 12 | Choose and evaluate a defensible contribution

**SAVE (as required by the assignment):** Chosen contribution pathway and executable comparison plan.

## Prompt as used

> My baseline **[greedy zero-shot CoT + self-consistency, Qwen2.5-7B-Instruct]** has been validated, and its actual results are **[NOT YET AVAILABLE — implementation audit complete (Prompt 10 Part A), real-model results pending (Part B)]**. My research question is **[RQ1: specialist tumor board vs call-matched SC@9; RQ2 role ablation; RQ3 discussion effects]**, supported by **[EvoMDT (Liu et al. 2026); Kim et al. 2025 MLHC; MDAgents (Kim et al. 2024); Wang et al. 2024; Smit et al. 2023]**. Compare three feasible study pathways: A. reproduce an existing approach under a justified new condition; B. conduct a controlled comparative study of performance, generalization, robustness or efficiency; C. make a targeted, theoretically motivated extension or modification. For each, explain the scientific question, expected code changes, compute burden, advantages, failure risks and evidence needed. Recommend the most defensible pathway for my resources. Develop a fair test plan with appropriate comparisons and an ablation or failure analysis. If modification is chosen, guide me in making one isolated change while preserving the baseline implementation. Do not guarantee gains or mistake a routine comparison for novelty.

Placeholders filled: [NAME], [RESULTS] (honestly: pending), [QUESTION], [LITERATURE EVIDENCE].

## Files in this folder

- `contribution_pathway_and_comparison_plan.md` — A/B/C comparison at code level, recommendation (B, provisional), fair test plan with ablations and failure analyses, executable plan, what changes if baseline results differ, isolated-change guidance, decisions L-34–L-36
- `03_main_grid_kaggle.ipynb` — the executable comparison plan (gated on baseline validation)
