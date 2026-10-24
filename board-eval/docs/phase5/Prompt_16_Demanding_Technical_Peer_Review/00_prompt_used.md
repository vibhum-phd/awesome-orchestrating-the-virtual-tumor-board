# PROMPT 16 | Conduct a demanding technical peer review

**SAVE (as required by the assignment):** Peer-review report and manuscript revision log.

## Prompt as used
> Review my draft manuscript **[manuscript_draft_v0.1_RESULTS_PENDING.pdf, Prompt 15]** as a critical technical reviewer. Assess significance, literature coverage, contribution validity, technical correctness, data leakage, fair baselines, experimental design, robustness of conclusions, reproducibility, figure/table accuracy, citation traceability and clarity. Separate MAJOR and MINOR concerns, give section/page locations, explain why each concern matters and propose one concrete remedy or experiment. Identify unsupported novelty and performance claims. Do not default to praise, invent missing literature or treat a fluent manuscript as scientifically sound. Return a prioritized revision checklist and an author-response table.

## Files in this folder
- `peer_review_report.md` — 5 MAJOR (M1–M5) and 8 MINOR (m1–m8) concerns with location, why it matters and remedy; unsupported-claims check; correctness/leakage/fairness/reproducibility checks; prioritised checklist
- `revision_log_and_author_response.md` — author-response table (what changed, where, status), changes outside the manuscript, decisions L-42–L-44
- `manuscript_draft_v0.2_RESULTS_PENDING.pdf` — revised draft (5 pages, 23 references, 0 BibTeX warnings)
- `paper_v0.2/` — revised `main.tex`, `references.bib`, `bib_verification.md`, `results_tables.tex` (PENDING), figures
- `frozen_protocol_v1.2.yaml` — protocol after the M2 change (made before any run)
- `novelty_matrix_addendum_Prompt04.md` — the missed close study (Kuerbanjiang et al. 2025) added to the Prompt 04 matrix

## Honesty note
The reviewer and the author here are the same AI system. This is a self-review. It found real gaps (M2, M3, m1), but it is not a substitute for an independent human review (L-44). The one literature search added for M3 was verified at source; nothing was invented.

## Status
9 of 13 concerns fixed in v0.2. Open: M1 and M4 (need Kaggle results), M5 (title decision), m8 (Overleaf compile), independent human review.
