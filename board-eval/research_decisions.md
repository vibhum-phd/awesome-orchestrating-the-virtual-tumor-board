# Research decisions log

Format: ID · date · decision · reason · evidence (label) · next action.
Labels: VERIFIED / INFERRED / UNKNOWN. Add a row for every protocol change; never edit old rows.

| ID | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|
| D-01 | 2026-10-20 | Stay in the review's area; target the 4th research gap (thin independent validation of multi-agent tumor-board systems). | Required continuity; gap is computationally testable without patient data. | Lit review PDF Sec. 6 & 7 (VERIFIED, text extracted and read). | — |
| D-02 | 2026-10-20 | Question = board vs **call-matched** self-consistency, not board vs single call. | EvoMDT compares only to single-pass models, so gains are confounded with 9× more inference. | EvoMDT PDF results + methods text: baselines Llama3-70B, Claude-3, Med-PaLM 2; no "self-consistency" string in text (VERIFIED by text search; **confirm by reading Fig. 2 and Methods yourself**). Conflicting general evidence: Wang et al. 2024 (ACL), Smit et al. 2023, Wunderlich et al. 2026 (ACL-SRW) — abstracts VERIFIED. | Check MDAgents & CoMMa tables for SC baselines (UNKNOWN). |
| D-03 | 2026-10-20 | Data: MedQA-USMLE 5-option test from the MedAgents GitHub copy; sha256 `cfa75cbc…a3`. | Hugging Face is blocked in the Claude workspace (HTTP 403 via proxy); GitHub works. Same file is what MedAgents evaluated on. | 1,273 items, 5 options each, gold distribution A273/B277/C252/D269/E202 (VERIFIED by execution). MedQA repo licence MIT (VERIFIED, LICENSE file). | On Kaggle, hash check in notebook cell 4. |
| D-04 | 2026-10-20 | Oncology filter v0.9 (keywords in stem or gold answer) → **v1.0** adds: drop sentences about relatives, drop negated mentions, drop non-oncology phrases (neuroleptic malignant syndrome, TNF, malignant hyperthermia/hypertension). n: 121 → **97**. | Reading all 121 v0.9 matches showed ~20 items included only via a relative's cancer ("father died of lung cancer") or false phrases; these are not oncology vignettes. Change made **before any model output existed**. | Match-context listing of all 121 items (VERIFIED, reviewed in session). Known cost: a few genuine items lost (e.g., Lynch-syndrome family-history item). | Human audit of the 97 (`data/processed/onc_subset_human_audit.csv`) → pre-registered sensitivity analysis (`evaluate.py --restrict-ids`). |
| D-05 | 2026-10-20 | Add MedMCQA-dev oncology subset (same filter + topic_name), pooled with MedQA-onc for the primary test. | n = 97 alone gives low power for a paired test. MedMCQA is Indian-exam material (links to review gap 5, LMIC representation); EvoMDT also used a MedMCQA cancer subset. | MedMCQA repo licence MIT (VERIFIED). HF id `openlifescienceai/medmcqa`, `cop` base, n — **UNKNOWN** until built on Kaggle. | Paste `prepare_extra_data.py` output here. |
| D-06 | 2026-10-20 | Backbone Qwen2.5-7B-Instruct, fp16, vLLM, 2×T4. Fallback Qwen2.5-3B-Instruct. | Open weights → reproducible, no API cost, fits free Kaggle. | Licence Apache-2.0 (INFERRED from memory — **verify on model card**). vLLM-on-T4 compatibility UNKNOWN. | Smoke test. |
| D-07 | 2026-10-20 | Board design: 4 roles (medical, surgical, radiation oncologist; pathologist), 2 rounds, greedy chair = 9 calls. SC draws 15 samples and is scored at k = 1,3,5,9,15. | Mirrors MDT composition in the reviewed literature; 9 calls makes SC@9 the call-matched control; SC curve allows token-matched reading too. | Design choice (INFERRED as reasonable; not a reproduction of MedAgents/MDAgents). | — |
| D-08 | 2026-10-20 | Answer parser: letter must stand alone after "Answer:". | Unit test showed "Answer: A patient with…" parsed as A (bug in first version). | tests/test_core.py (VERIFIED by execution). Cost: "Answer: B because…" → parse failure; rate reported per method. | Inspect parse failures in smoke test. |
| D-09 | 2026-10-20 | Freeze: `configs/frozen_protocol.yaml` v1.0. Primary metric, primary comparison, test, threshold, seeds and datasets fixed before any real run. | Prevents choosing the comparison after seeing results. | — | Any change after the first non-pilot run → new row + protocol v1.1. |

## Phase I log — Prompts 01–02 (submitted 22 Oct 2026)

| ID | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|
| L-01 | 2026-10-20 | Stay in VTB area; convert Lab 4 review | Continuity rule (assignment §2) | Assignment PDF (VERIFIED) | Summarise review scope |
| L-02 | 2026-10-20 | Evidence base = Lab 4 review (24 papers), not AI-generated Lab 1 paper | Lab 1 was an audit of AI-written citations | Review text extracted (VERIFIED) | Extract gaps |
| L-03 | 2026-10-22 | Treat review's internal cross-references as unreliable | Text cites "Section 9", "6.4", "5.2"; review is numbered 1–9 | Review text (VERIFIED) | Fix before reuse |
| L-04 | 2026-10-22 | Rank gaps on significance, resources, feasibility | Free Kaggle/Colab T4, GTX 1050 Ti, ~4 weeks, no patient data | Own constraints (VERIFIED) | Score five gaps |
| L-05 | 2026-10-22 | Provisionally select G4 (score 9); G1 as secondary analysis | Top of ranking | Gap matrix (INFERRED until novelty check) | Prompt 03/04: MDAgents/CoMMa baseline check |

Saved Phase I outputs:
- Review scope (Prompt 01) → `docs/phase1/prompt01_review_scope.md`
- Gap matrix, ranking and evidence ledger (Prompt 02) → `docs/phase1/prompt02_gap_matrix.md`
  (G1 complexity, G2 instability, G3 country transfer, G4 multi-agent fair comparison, G5 multimodal)
Review errors found: EvoMDT datasets called "oncology" (MedQA is general); first author of iScience 2025 is Xiaodong Wang, not "D. Wang"; Lukac 2023 cited but not in reference list; abstract 60–>90% vs Table 1 ~56–87% inconsistent; EvoMDT ties Med-PaLM 2 on MedQuAD (0.63).

## Phase I log — Prompts 03–04 (23 Oct 2026)

| ID | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|
| L-06 | 2026-10-23 | Do not reproduce EvoMDT or Han et al. | Code unreachable/absent; API-only backbone; private data | Access matrix (VERIFIED / UNKNOWN as marked) | — |
| L-07 | 2026-10-23 | Choose study B (controlled comparison) on MedQA oncology items | Only option with a baseline I control that fits free GPUs | Prompt 03 output B | Kaggle smoke test |
| L-08 | 2026-10-23 | Narrow claim to call matching, public data, open 7B model, error flips | Kim et al. 2025 already tested roles and discussion in oncology | Kim et al. PDF text (VERIFIED) | Read their Appendix B myself |
| L-09 | 2026-10-23 | Re-implement; do not copy MedAgents, MDAgents or Kim et al. code | Their repos have no licence | Repo file lists (VERIFIED) | Cite as design references |
| L-10 | 2026-10-23 | Conditional GO with listed conditions and fallbacks | All required data and weights openly licensed | Access matrix | Prompts 05–06 |

Saved Phase I outputs (Prompts 03–04):
- Literature-to-experiment map + mandatory bridge (Prompt 03) → `docs/phase1/prompt03_literature_to_experiment_bridge.md` (+ `prompt03_bridge.png`)
- Novelty/feasibility matrix + go/no-go (Prompt 04) → `docs/phase1/prompt04_novelty_feasibility_go_nogo.md`

## Phase I log — Prompt 05 (24 Oct 2026)

| ID | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|
| L-11 | 2026-10-24 | Three RQs: board vs SC@9 (primary), role ablation, discussion effects; exploratory complexity/efficiency analyses | Covers G4 directly and G1 at no extra compute | Prompts 02–04 | Freeze in Prompt 07 |
| L-12 | 2026-10-24 | Two-sided tests; no directional hypotheses for RQ1/RQ2 | Prior evidence points both ways | Kim 2025 vs Wang 2024 / Smit 2023 | — |
| L-13 | 2026-10-24 | Primary set = pooled oncology (MedQA + MedMCQA); MedQA-only as pre-specified fallback | n = 97 detects only ≈ 12–15-point effects | Power simulation (VERIFIED run; assumed inputs) | Build MedMCQA subset on Kaggle |
| L-14 | 2026-10-24 | Report nulls against the minimum detectable effect and the CI | Avoid "no difference" over-claims | Power table | Write into frozen protocol |
| L-15 | 2026-10-24 | Prompt 05 brief supersedes `research_brief_G1.md` (20 Oct) | Old brief predates Kim et al. 2025 | Prompt 04 | Exclude old brief from submissions |

Saved: `docs/phase1/prompt05_research_questions_and_success_criteria.md`, `docs/phase1/research_brief_one_page.pdf`

## Phase II log — Prompts 06–07 (24 Oct 2026)

See `docs/phase2/research_decisions_phase_II.md` (L-16 to L-21). Protocol frozen at v1.1 (`configs/frozen_protocol.yaml`).

## Phase III log — Prompts 08–11 (24 Oct 2026)

See `docs/phase3/research_decisions_phase_III.md` (L-22 to L-29).

## Phase IV log — Prompts 12–14 (24 Oct 2026)

See `docs/phase4/research_decisions_phase_IV.md` (L-30 to L-38).

## Phase V log — Prompts 15–17 (24 Oct 2026)

See `docs/phase5/research_decisions_phase_V.md` (L-39 to L-47). Protocol now v1.2 (L-42, before any run).

## Phase VI log — Prompt 18 (24 Oct 2026)

See `docs/phase6/research_decisions_phase_VI.md` (L-48 to L-51) and the provenance report in `docs/phase6/`.
