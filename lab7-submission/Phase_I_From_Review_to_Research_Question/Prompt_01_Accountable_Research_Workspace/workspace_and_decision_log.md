# Prompt 01 output — Workspace and decision log

Saved: 2026-10-22 (reorganised into Lab_7 on 2026-10-24) · Labels: VERIFIED / INFERRED / UNKNOWN

## Workspace
A git repository following the structure in §9 of the assignment, first committed on 20 Oct 2026 (VERIFIED: `git log`). The Lab_7 folder you are reading holds the per-prompt outputs; the code repository is kept separately.

```
AITR_Lab02_Project/
  README.md                 research question + reproducibility
  research_decisions.md     decisions → reasons → evidence → next action
  ai_assistance_log.md      prompts, AI proposals, human checks
  configs/ data/ notebooks/ src/ scripts/ results/ paper/   (used from Phase II onward)
```

## Decision log — format
Every entry has: ID · date · decision · reason · evidence (with label) · next action. Entries are never edited after the fact; a change gets a new entry. The full Phase I log is `../research_decisions_phase_I.md`.

## Entries made at this prompt

| ID | Date | Decision | Reason | Evidence (label) | Next action |
|---|---|---|---|---|---|
| L-01 | 2026-10-20 | Stay in the virtual-tumor-board area and convert the Lab 4 review | Continuity rule (assignment §2) | Assignment PDF (VERIFIED) | Summarise review scope |
| L-02 | 2026-10-20 | Evidence base = Lab 4 review (24 papers), not the AI-generated Lab 1 paper | Lab 1 was an audit of AI-written citations | Review text extracted (VERIFIED) | Extract gaps |
| L-03 | 2026-10-22 | Treat the review's internal cross-references as unreliable | Text cites "Section 9", "6.4", "5.2"; review is numbered 1–9 | Review text (VERIFIED) | Fix before reusing text |
