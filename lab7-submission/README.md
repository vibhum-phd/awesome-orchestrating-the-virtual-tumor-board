# Lab 7 — AI-assisted coding, vibe coding and evidence-based experimentation

Student: Vibhum Sharma (Topic ID T32) · Course: AI Tools for Research
Study: *Does the virtual tumor board need a board?* A call-matched test of a specialist multi-agent LLM board against self-consistency on oncology exam questions.

In this repository the code is in [`../board-eval/`](../board-eval) (the handbook's `AITR_Lab02_Project/` tree); this folder holds the per-prompt outputs.

Outputs are organised by the six phases and 18 prompts of the assignment sheet. Each prompt folder holds `00_prompt_used.md` plus the files that prompt's SAVE line asks for.

| Phase | Prompts | Status |
|---|---|---|
| `Phase_I_From_Review_to_Research_Question/` | 01–05 | **Complete** (24 Oct 2026) |
| `Phase_II_Experiment_Plan/` | 06–07 | **Complete** (24 Oct 2026) |
| `Phase_III_AI_Coding_Vibe_Coding_and_Baseline_Validation/` | 08–11 | Done to the GPU boundary; **waiting for Kaggle output** (Prompts 08, 10) |
| `Phase_IV_Contribution_and_Evidence/` | 12–14 | Code and plans done; **evidence PENDING real runs** |
| `Phase_V_Write_Review_and_Publish/` | 15–17 | Manuscript v0.2 + tested README done; **results sections PENDING real runs** |
| `Phase_VI_Human_AI_Accountability/` | 18 | Provenance report done; **student sign-off pending** |

Evidence labels used everywhere: **VERIFIED** (checked in the original source or by running code), **INFERRED** (plausible, or from an AI summary not yet read in full), **UNKNOWN** (no evidence yet).

## What only the student can do now
1. Run Kaggle notebooks 01 → 02 → 03 (`board-eval/notebooks/`) and share the output zips. They clone the repository from GitHub, so push first.
2. Label the 97 oncology items (`board-eval/data/processed/onc_subset_human_audit.csv`).
3. Read MDAgents Table 2, the MedAgentsBench results table and arXiv 2501.06458 Table 1.
4. Complete `Phase_VI_…/Prompt_18_…/human_decision_signoff.md` in your own words.
5. Push the repository to GitHub; get an independent review of the paper v0.2.
