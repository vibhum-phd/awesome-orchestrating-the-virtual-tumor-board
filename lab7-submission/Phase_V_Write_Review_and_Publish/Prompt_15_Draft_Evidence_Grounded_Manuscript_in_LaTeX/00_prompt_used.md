# PROMPT 15 | Draft an evidence-grounded manuscript in LaTeX

**SAVE (as required by the assignment):** 6–10-page target manuscript, figures, .tex and verified .bib.

## Prompt as used

> Use only my VERIFIED problem brief **[Prompt 05 one-page brief]**, original references **[sources verified in paper/bib_verification.md]**, actual methodology **[protocol v1.1 + code]**, experimental settings **[Qwen2.5-7B-Instruct, vLLM, Kaggle 2×T4 — run logs pending]** and measured results **[NONE YET — Kaggle runs pending]**. Help me prepare an IEEE/ACM-style paper in Overleaf. First create a section outline and evidence checklist, then draft Related Work, Methodology, Experimental Setup, Results and Discussion, Limitations, Introduction and Conclusion, and write the Abstract last so it matches the final evidence. Mark missing facts [TO VERIFY]. Preserve distinctions between previously published methods, my experimental contribution and conjectures. Create BibTeX entries only from metadata I have verified. Flag inconsistencies between figures, tables, code and claims, and help me resolve LaTeX compilation errors.

Placeholders filled: [BRIEF], [SOURCES], [METHOD], [SETUP], [RESULTS] (honestly: none yet).

## Files in this folder

- `manuscript_outline_evidence_checklist_and_flags.md` — outline in writing order, claim→evidence checklist, published-vs-own distinctions, 8 inconsistencies found and resolved, what remains, decisions L-39–L-41
- `manuscript_draft_v0.1_RESULTS_PENDING.pdf` — compiled 5-page draft (no results)
- `paper/` — `main.tex`, `references.bib` (20 verified entries), `results_tables.tex` (PENDING shells), `bib_verification.md`, `figures/pipeline_paper.png` (+ .mmd)
- `make_paper_tables.py` — builds the results tables from `results/` only; refuses mock data
- `latex_build_log_summary.txt` — build result (5 pages, 0 BibTeX warnings)

## Status
Draft complete except everything that depends on results.
