# Research decision log — Phase V (Prompts 15–17), 24 Oct 2026

| ID | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|
| L-39 | 2026-10-24 | Results tables only from `make_paper_tables.py`; it refuses mock data | No hand-typed numbers | Script refusal shown (exit 1) in the fresh-clone log | Run on real results |
| L-40 | 2026-10-24 | Correct MedAgentsBench first author (Shao) and EvoMDT year (2025) | Source metadata | arXiv page; EvoMDT PDF | — |
| L-41 | 2026-10-24 | Keep two INFERRED literature claims flagged until read (MDAgents SC baseline; MedAgentsBench findings) | Came from AI summaries | `bib_verification.md` | Student reads both tables |
| L-42 | 2026-10-24 | Protocol v1.1 → v1.2: exploratory board vs SC@15; tokens per item with every comparison | Calls matched ≠ tokens matched (review M2); changed before any run | Git `4b36bad`; tests 46/46 | — |
| L-43 | 2026-10-24 | Position against Kuerbanjiang et al. 2025 and Kim et al. 2025; add CoMMa, MTBBench | Closest oncology work; neither matches budgets (full text / PDF VERIFIED) | `novelty_matrix_addendum_Prompt04.md` | — |
| L-44 | 2026-10-24 | Seek an independent human review of v0.2 | Prompt 16 review was AI self-review | — | Supervisor / peer |
| L-45 | 2026-10-24 | Every README command labelled VERIFIED or [TEST REQUIRED] | No GPU run has happened | `repository_readiness_check.md` §1 | Relabel after Kaggle |
| L-46 | 2026-10-24 | `requirements-gpu.txt` stays unpinned until notebook 01 runs | Untested pins would look verified | — | Pin from `pip_freeze.txt` |
| L-47 | 2026-10-24 | Test the README from a fresh clone | Found two README errors (R1, R2) | `reproduction_log_fresh_clone.txt` | Second student repeats on own machine |
