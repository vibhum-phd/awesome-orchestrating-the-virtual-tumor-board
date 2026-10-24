# Phase I — From review to research question (Prompts 01–05)

Status: **complete** (24 Oct 2026). Gate G1 (research brief) is ready for review.

| Prompt | Folder | SAVE item required by the assignment | File(s) |
|---|---|---|---|
| 01 | `Prompt_01_Accountable_Research_Workspace/` | Workspace and decision log; review scope | `workspace_and_decision_log.md`, `review_scope.md` |
| 02 | `Prompt_02_Evidence_Based_Research_Gaps/` | Gap matrix: source evidence → candidate question → possible experiment | `gap_matrix.md` |
| 03 | `Prompt_03_Literature_to_Experiment_Map/` | Mandatory bridge: original papers → selected method → executable baseline → planned test | `literature_to_experiment_bridge.md`, `prompt03_bridge.png` |
| 04 | `Prompt_04_Feasibility_Novelty_and_Resource_Access/` | Novelty/feasibility matrix and go/no-go decision | `novelty_feasibility_matrix_and_go_no_go.md` |
| 05 | `Prompt_05_Research_Questions_and_Success_Criteria/` | One-page problem brief with questions and measurable outcomes | `research_brief_one_page.pdf`, `research_questions_and_success_criteria.md`, power script + output |

Every prompt folder starts with `00_prompt_used.md` (the prompt as run, brackets filled).

Phase-level files:
- `research_decisions_phase_I.md` — cumulative decision log L-01 to L-15
- `previously_submitted_pdfs/` — the PDFs already submitted for Prompts 01–02 (22 Oct) and 03–04 (23 Oct)

## Phase I result in one paragraph
The review's fourth gap (multi-agent boards have the strongest results but the weakest independent validation) was checked against the original papers. EvoMDT compares its DeepSeek-based board only with other models run once. Kim et al. (MLHC 2025) already tested specialist roles and discussion on 31 private oncology cases, judged by an LLM and with unequal call counts. The study was therefore narrowed to a controlled comparison: one open model (Qwen2.5-7B-Instruct), a 4-specialist board vs self-consistency at the same 9 calls, on public oncology exam items, plus a generic-agent ablation and error-propagation counts. A power simulation showed the 97 MedQA oncology items alone can only detect differences of about 12–15 points, so the primary set pools MedQA and MedMCQA oncology items.

## Carried into Phase II
- Build the MedMCQA oncology subset and confirm its size (Prompt 06).
- Freeze the protocol with the decision rules and power limits from Prompt 05 (Prompt 07).
- Personal checks still open: EvoMDT repo and Fig. 2; MDAgents Table 2; MedAgentsBench table; Kim et al. Appendix B; Kaggle quota; MedMCQA dataset card.
