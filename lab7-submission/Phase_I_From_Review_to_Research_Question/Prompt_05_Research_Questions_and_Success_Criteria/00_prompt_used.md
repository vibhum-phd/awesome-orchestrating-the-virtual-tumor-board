# PROMPT 05 | Frame research questions and success criteria

**SAVE (as required by the assignment):** One-page problem brief with questions and measurable outcomes.

## Prompt as used

> Here is my verified gap **[G4: multi-agent tumor-board claims lack an independent, fair comparison — review Sec. 7, fourth gap]**, selected study **[study B: 4-specialist board vs call-matched self-consistency, Qwen2.5-7B-Instruct, oncology exam items, generic-agent ablation]** and source evidence **[EvoMDT (Liu et al. 2026); Kim et al. 2025, MLHC; MDAgents (Kim et al. 2024); Wang et al. 2024; Smit et al. 2023; Zheng et al. 2024]**. Write one precise research problem, two or three testable research questions, and hypotheses only where appropriate. For each question identify the input data, comparator, independent/dependent variables when relevant, evaluation metric, meaningful success threshold or decision rule, and an observation that would contradict my expectation. Separate the contribution I intend to investigate from a contribution already demonstrated. Flag overbroad questions and provide a one-page research brief that can be reviewed before implementation.

Placeholders filled: [GAP], [IDEA], [SOURCES].
Tool: Claude (claude.ai project workspace, web search, Linux workspace without GPU).

## Files in this folder

- research_questions_and_success_criteria.md — problem, RQ1–RQ3 tables, contribution split, overbroad/power flags, decision-log entries
- research_brief_one_page.pdf (+ .tex) — the one-page brief (assignment §11 template)
- power_mcnemar.py + power_mcnemar_results.csv — the power simulation behind the sample-size flag (real run, assumed inputs)
