# Research decisions log — Phase I (Prompts 01–05)

Student: Vibhum Sharma (T32) · Course: AI Tools for Research (Lab 7)
Format: ID · date · decision · reason · evidence (label) · next action. Labels: VERIFIED / INFERRED / UNKNOWN.

| ID | Prompt | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|---|
| L-01 | 01 | 2026-10-20 | Stay in VTB area; convert Lab 4 review | Continuity rule (assignment §2) | Assignment PDF (VERIFIED) | Summarise review scope |
| L-02 | 01 | 2026-10-20 | Evidence base = Lab 4 review (24 papers), not AI-generated Lab 1 paper | Lab 1 was an audit of AI-written citations | Review text extracted (VERIFIED) | Extract gaps |
| L-03 | 01 | 2026-10-22 | Treat review's internal cross-references as unreliable | Text cites "Section 9", "6.4", "5.2"; review numbered 1–9 | Review text (VERIFIED) | Fix before reuse |
| L-04 | 02 | 2026-10-22 | Rank gaps on significance, resources, feasibility | Free Kaggle/Colab T4, GTX 1050 Ti, ~4 weeks, no patient data | Own constraints (VERIFIED) | Score five gaps |
| L-05 | 02 | 2026-10-22 | Provisionally select G4 (score 9); G1 as secondary analysis | Top of ranking | Gap matrix (INFERRED until novelty check) | Novelty check (Prompts 03–04) |
| L-06 | 03 | 2026-10-23 | Do not reproduce EvoMDT or Han et al. | Code unreachable/absent; API-only backbone; private data | Access matrix (VERIFIED / UNKNOWN as marked) | — |
| L-07 | 03 | 2026-10-23 | Choose study B (controlled comparison) on MedQA oncology items | Only option with a baseline I control that fits free GPUs | Prompt 03 output B | Kaggle smoke test |
| L-08 | 04 | 2026-10-23 | Narrow claim to call matching, public data, open 7B model, error flips | Kim et al. 2025 already tested roles and discussion in oncology | Kim et al. PDF text (VERIFIED) | Read their Appendix B myself |
| L-09 | 04 | 2026-10-23 | Re-implement; do not copy MedAgents, MDAgents or Kim et al. code | Their repos have no licence | Repo file lists (VERIFIED) | Cite as design references |
| L-10 | 04 | 2026-10-23 | Conditional GO with listed conditions and fallbacks | All required data and weights openly licensed | Access matrix | Prompts 05–06 |
| L-11 | 05 | 2026-10-24 | Three RQs: board vs SC@9 (primary), role ablation, discussion effects; exploratory complexity/efficiency analyses | Covers G4 directly and G1 at no extra compute | Prompts 02–04 | Freeze in Prompt 07 |
| L-12 | 05 | 2026-10-24 | Two-sided tests; no directional hypotheses for RQ1/RQ2 | Prior evidence points both ways | Kim 2025 vs Wang 2024 / Smit 2023 | — |
| L-13 | 05 | 2026-10-24 | Primary set = pooled oncology (MedQA + MedMCQA); MedQA-only as pre-specified fallback | n = 97 detects only ≈ 12–15-point effects | Power simulation (VERIFIED run; assumed inputs) | Build MedMCQA subset on Kaggle (Prompt 06) |
| L-14 | 05 | 2026-10-24 | Report nulls against the minimum detectable effect and the CI | Avoid "no difference" over-claims | Power table | Write into the frozen protocol (Prompt 07) |
| L-15 | 05 | 2026-10-24 | The Prompt 05 brief supersedes `research_brief_G1.md` (20 Oct) | That brief predates the Kim et al. 2025 finding | Prompt 04 | Exclude the old brief from submissions |
