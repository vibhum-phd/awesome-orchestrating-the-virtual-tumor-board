# Prompt 16 output — Critical technical peer review of manuscript draft v0.1

Reviewed: `manuscript_draft_v0.1_RESULTS_PENDING.pdf` (5 pages, 24 Oct 2026).
**Reviewer independence:** this review was written by the same AI that drafted the paper, so it is a self-review, which is the weakest kind. One new literature check was run for it (§2, M3). Before submission, a human reviewer (supervisor or peer) should read v0.2 cold.

**Overall assessment.** The design is careful: a call-matched comparison, a pre-registered protocol, MDE reporting and integrity gates. The paper is honest about scope. But it **cannot be evaluated as research yet**: it contains no results, and two design and coverage problems should be fixed before the runs, not after. **Recommendation as it stands: major revision.**

## 1. Significance and contribution
The question is narrow but useful. It tests whether published board gains survive an equal call budget. The contribution is correctly framed as a controlled comparison, not a new method. The value depends entirely on the results and on whether the call-matched angle is genuinely untested (see M3).

## 2. MAJOR concerns

| ID | Concern | Location | Why it matters | Remedy / experiment |
|---|---|---|---|---|
| M1 | **No results.** Every claim about RQ1–RQ3 is pending | §5–6, Abstract, Conclusion | Nothing can be accepted or rejected | Run notebooks 01→02→03; generate tables; write §5–6 from the pre-registered decision table |
| M2 | **Calls are matched, tokens are not.** Round-2 prompts carry three other members' texts and the chair reads four, so a 9-call board likely uses many more input tokens than SC@9 | §3.2, §3.3, Limitations | A board "win" at 9 calls could still be a compute win. The paper's own thesis is about confounded budgets | Pre-register (before any run) an extra comparison of board vs SC@15 as the higher-budget SC, and report tokens per item next to every comparison. If tokens are still unequal, say which arm had more |
| M3 | **Related work misses close oncology studies.** Kuerbanjiang et al. (medRxiv 2025) compare a multi-agent gynecologic-oncology team with six baselines, including universal self-consistency and multi-agent debate, on 182 cases and 3 LLMs. CoMMa (2026) and MTBBench (NeurIPS 2025) are not cited either | §2 | A reviewer will ask why the closest SC-vs-board oncology comparison is missing | Cite all three (metadata verified for this review). Checked in their full text: Kuerbanjiang et al. do **not** report matched calls or tokens for the baselines (cost given only for their own system), so the call-matched contribution still holds and should be stated against them explicitly |
| M4 | **Primary set size unknown.** The design relies on MedMCQA to reach adequate power; if its oncology subset is small, the primary test detects only very large effects | §3.1, Limitations | Underpowered nulls are uninformative | State the realised n and its MDE in §3.1; if n_total < ~200, label the primary analysis exploratory in the abstract |
| M5 | **Construct validity of the title.** "Does the virtual tumor board need a board?" invites a clinical reading; the evidence is exam MCQs | Title, Abstract | Overreach | Keep the scope words in the subtitle (already) and repeat "exam questions" in the first sentence of the conclusion. Consider "Do LLM tumor-board agents beat sampling at equal cost?" |

## 3. MINOR concerns

| ID | Concern | Location | Remedy |
|---|---|---|---|
| m1 | AI statement says "Every citation was checked against its source", but two literature claims (MDAgents' SC baseline; MedAgentsBench findings) come from AI summaries | AI statement; §2 | Reword: metadata of every reference checked; two claims marked for verification |
| m2 | "MDAgents … includes a self-consistency baseline" is INFERRED | §2 | Mark [TO VERIFY] until Table 2 is read |
| m3 | Pooled set mixes 5-option (MedQA) and 4-option (MedMCQA) items with different chance levels | §3.1 | Say so and point to by-source results (already in the protocol) |
| m4 | "Most report gains over single-call baselines" generalises from three papers | §2 | "These systems report gains …" |
| m5 | No data-availability or ethics statement | end matter | Add: public benchmarks, licences, no human subjects or patient data |
| m6 | The 27.8% floor is MedQA-specific; MedMCQA needs its own floor | §4 | State both floors |
| m7 | Seeds 1–2 are run but only seed 0 is primary; readers may expect averages | §3.3 | One sentence: seed 0 is pre-registered as primary; seeds are reported as sensitivity |
| m8 | Final length and layout unknown under IEEEtran (local build used the fallback class) | — | Compile on Overleaf before submission |

## 4. Unsupported novelty or performance claims found
- None about performance: there are no performance numbers of this study in the draft.
- Novelty: the contribution list does not say "first", which is correct. After M3 it should name Kuerbanjiang et al. and Kim et al. as the closest work and say exactly what differs (call matching, public items, objective metric, small open model).

## 5. Checks on technical correctness, leakage, fairness, reproducibility
- **Statistics:** exact McNemar, Holm within one pre-declared family, paired bootstrap, MDE from exact power. Appropriate for paired binary outcomes. The flip-rate CIs resample items. Correct.
- **Leakage:** debug items from train only; overlap checker gate; contamination stated. Adequate.
- **Fair baselines:** same model, prompt format, sampling, parser; truncation and parse-failure reported per arm. Fair, except the token imbalance (M2).
- **Reproducibility:** protocol, seeds, code, tests (46/46 on Python 3.11 and 3.13) are present. Repository URL and pinned GPU versions are missing.
- **Figures and tables:** generated, not typed; mock data refused. Figure 1 legible after revision.
- **Citations:** 20/20 references have verified metadata (`bib_verification.md`).

## 6. Prioritised revision checklist
1. [ ] (M2) Add the higher-budget SC comparison to the protocol **before** any run; report tokens per item with every comparison
2. [ ] (M3) Add Kuerbanjiang et al., CoMMa and MTBBench to Related Work and position the contribution against them
3. [ ] (m1, m2) Correct the AI statement; mark the MDAgents claim [TO VERIFY]
4. [ ] (m3, m5, m6, m7) Mixed option counts, data/ethics statement, both floors, seed sentence
5. [ ] (m4) Soften the generalisation in Related Work
6. [ ] (M1, M4) Run the experiments; fill §5–6, the abstract and the conclusion; state the realised n and MDE
7. [ ] (M5, m8) Title decision; compile on Overleaf; check page count (6–10)
8. [ ] Independent human review of v0.2

## 7. Author-response table
See `revision_log_and_author_response.md` (what was changed, where, and what remains open).
