# Human decision sign-off — to be completed by the student before submission

The AI proposed every decision below. Mark each one: **Agree** (and say why in one line, in your own words), **Change** (what and why), or **Not checked**. Do this from the evidence file, not from the AI's summary. Leave nothing marked Agree that you cannot explain in a viva.

| # | Decision (log ID) | Evidence to look at | Your verdict | Your reason (own words) | Date |
|---|---|---|---|---|---|
| 1 | Gap G4: board vs call-matched single model (L-05) | `docs/phase1/prompt02_gap_matrix.md`; your Lab 4 review §6–7 | | | |
| 2 | Narrowed novelty after Kim et al. 2025 and Kuerbanjiang et al. 2025 (L-08, L-43) | Kim PDF; Prompt 04 matrix + addendum | | | |
| 3 | Exam MCQs as the proxy for tumor-board decisions | Prompt 03 bridge; Limitations | | | |
| 4 | Qwen2.5-7B-Instruct, vLLM, Kaggle 2×T4 | Prompt 04 feasibility; protocol | | | |
| 5 | Oncology filter v1.0 (97 items) | `onc_filter_audit.csv` | | | |
| 6 | **Label the 97 items yourself** (`human_label`) | `onc_subset_human_audit.csv` (0/97 done) | | | |
| 7 | Primary = board vs SC@9, McNemar, α 0.05, 2-point threshold (L-11, L-12) | `frozen_protocol.yaml` | | | |
| 8 | Pool MedQA + MedMCQA; MedQA-only fallback (L-13) | power table | | | |
| 9 | Report nulls with MDE and CI (L-14) | protocol | | | |
| 10 | Protocol v1.2: SC@15 + tokens per comparison (L-42) | YAML header; review M2 | | | |
| 11 | **Read MDAgents Table 2** (self-consistency baseline?) | MDAgents paper | | | |
| 12 | **Read the MedAgentsBench results table** | Shao et al. 2025 | | | |
| 13 | **Read Table 1 of arXiv 2501.06458** (56.79% anchor; variant?) | that paper | | | |
| 14 | Baseline acceptance B1–B8, then create `results/baseline/VALIDATED` | Prompt 10 report + Kaggle output | | | |
| 15 | Interpretation of real results against the Prompt 14 decision table | `results/comparisons.csv` | | | |
| 16 | Title (review M5) | peer review | | | |
| 17 | Independent review of v0.2 by supervisor or peer (L-44) | v0.2 PDF | | | |
| 18 | Any other AI tool you used for Lab 7 (add rows to the provenance report §3) | — | | | |

Signed: ____________________  Date: __________
