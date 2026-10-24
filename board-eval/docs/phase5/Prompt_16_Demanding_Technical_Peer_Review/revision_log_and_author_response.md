# Manuscript revision log and author-response table (v0.1 → v0.2)

Date: 2026-10-24. Every change below is in `manuscript_draft_v0.2_RESULTS_PENDING.pdf` and the repository (`paper/`, `configs/`, `scripts/evaluate.py`, `tests/`).

## Author-response table

| Reviewer item | Response | Change made (where) | Status |
|---|---|---|---|
| M1 No results | Agreed. Results cannot be written before the runs | None possible; run order documented (Phase IV README) | **Open** — needs Kaggle runs |
| M2 Calls matched, tokens not | Agreed; this is the paper's own confound in miniature | Protocol **v1.1 → v1.2** before any run: added exploratory board vs SC@15; `evaluate.py` now writes `tokens_per_item_a/b` for every comparison; §3.3 explains it; tests updated (46/46 pass) | **Done** (design); numbers pending |
| M3 Missing close oncology work | Agreed | Cited Kuerbanjiang et al. 2025 (full text checked: no matched budgets), CoMMa 2026 and MTBBench 2025; Introduction now names both closest studies and the difference | **Done** |
| M4 Primary n unknown | Agreed | Rule already in protocol (MDE reported); §3.1 keeps the [TO VERIFY] for n; abstract will label the analysis exploratory if n < ~200 | **Open** — needs MedMCQA build |
| M5 Title overreach | Partly agreed | Subtitle already limits scope ("…on Oncology Exam Questions"). Title kept for now; alternative recorded for the final decision | **Author decision pending** |
| m1 AI statement overclaim | Agreed | Reworded: metadata checked for all references; two statements from AI summaries marked | **Done** |
| m2 MDAgents SC baseline INFERRED | Agreed | Marked [TO VERIFY] in §2; MedAgentsBench claim also marked | **Done** (marking); reading Table 2 open |
| m3 Mixed option counts | Agreed | §3.1 sentence + per-source reporting | **Done** |
| m4 "Most report gains" | Agreed | "These systems report gains over their baselines, which in most cases make fewer model calls" | **Done** |
| m5 No data/ethics statement | Agreed | Added "Data availability and ethics" section | **Done** (URL [TO VERIFY]) |
| m6 MedMCQA floor | Agreed | §4 now names both floors (MedMCQA [TO VERIFY]) | **Done** (value pending) |
| m7 Seed reporting | Agreed | §4 sentence: seed 0 pre-registered as primary; others = sensitivity | **Done** |
| m8 IEEEtran length | Agreed | — | **Open** — compile on Overleaf |

## Changes outside the manuscript triggered by the review
| File | Change | Why |
|---|---|---|
| `configs/frozen_protocol.yaml` | v1.2: added `board_roles.final vs sc@15` (exploratory) | M2 |
| `scripts/evaluate.py` | Token-per-item columns in `comparisons.csv` | M2 |
| `tests/test_core.py` | Expect 3 exploratory comparisons | Protocol v1.2 |
| `paper/references.bib` | +3 verified entries (23 total) | M3 |
| `paper/bib_verification.md` | +3 rows | M3 |
| Lab_7 Prompt 04 matrix | First author of MedAgentsBench corrected to Shao | Found during bib verification |

## Decision-log entries (Prompt 16)
| ID | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|
| L-42 | 2026-10-24 | Protocol v1.2: add exploratory board vs SC@15 and report tokens with every comparison | Calls matched ≠ tokens matched (review M2); changed before any run | Git history; tests | — |
| L-43 | 2026-10-24 | Position the contribution against Kuerbanjiang et al. 2025 and Kim et al. 2025 | Closest oncology comparisons; neither matches budgets | Full text / PDF (VERIFIED) | Add to Prompt 04 novelty matrix as an addendum |
| L-44 | 2026-10-24 | Seek an independent human review of v0.2 | This review was self-review by the drafting AI | — | Ask supervisor / peer |
