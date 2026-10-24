# Prompt 05 output — Research problem, questions and success criteria

Saved: 2026-10-24 · Tool: Claude · Labels: VERIFIED / INFERRED / UNKNOWN
Prompt 05 SAVE item: "One-page problem brief with questions and measurable outcomes."
(The one-page brief itself is `research_brief_one_page.pdf` in this folder; this file holds the full working.)

## Inputs to this prompt
- **[GAP]** G4 from the Prompt 02 gap matrix: multi-agent tumor-board claims lack an independent, fair comparison (review Sec. 7, fourth gap; Sec. 6 "new failure surfaces … not yet well characterized").
- **[IDEA]** Study B from Prompt 03: a controlled comparison on MedQA oncology items with one fixed open model, narrowed in Prompt 04 after Kim et al. 2025.
- **[SOURCES]** EvoMDT (Liu et al. 2026, PDF read); Kim et al. 2025, MLHC (PDF read); MDAgents (Kim et al. 2024, NeurIPS; abstract and repo verified, Table 2 via AI summary); Wang et al. 2024, ACL (abstract); Smit et al. 2023 (abstract); Zheng et al. 2024, EMNLP Findings (title/abstract).

## 1. Research problem (one sentence)
Multi-agent "virtual tumor board" LLM systems are reported to beat single models, but the published comparisons do not hold the backbone model and the inference budget fixed, so it is unknown whether specialist deliberation — rather than simply spending more model calls — produces the gain, particularly for small open models that a resource-limited centre could run.

## 2. Research questions

### RQ1 (primary) — Does the board beat equal-budget sampling?
With Qwen2.5-7B-Instruct fixed, is a 4-specialist tumor board (2 rounds + chair = 9 calls) more accurate than self-consistency with 9 samples on oncology exam questions?

| Element | Specification |
|---|---|
| Input data | Pooled oncology set: MedQA-USMLE 5-option test, oncology subset (n = 97, filter v1.0, VERIFIED) + MedMCQA dev oncology subset (n UNKNOWN until built). If MedMCQA cannot be obtained, MedQA oncology alone (pre-specified fallback). |
| Comparator | Self-consistency @9 (call-matched). Reference only: greedy CoT (1 call). |
| Independent variable | Inference method (board vs SC@9) |
| Dependent variable | Item correct / incorrect (exact letter match; unparseable answer = incorrect) |
| Held constant | Model and weights, answer instruction, temperature 0.7, top-p 0.95, max tokens, item set, seeds |
| Metric (higher = better) | Accuracy; paired difference with 95% item-bootstrap CI |
| Test | Exact two-sided McNemar, α = 0.05 |
| Decision rule | Board better: p < 0.05 **and** difference ≥ +2 points. SC better: p < 0.05 and ≤ −2 points. Otherwise: "no difference detected", reported together with the CI and the minimum detectable effect (Section 4). |
| Hypothesis | H0: board accuracy = SC@9 accuracy (two-sided). The literature is split, so no directional hypothesis: Kim et al. 2025 favour boards; Wang et al. 2024, Smit et al. 2023 and the MDAgents CoT-SC baseline suggest sampling is competitive. |
| My expectation | No meaningful advantage for the board at equal calls. |
| Observation that would contradict me | Board ≥ 2 points above SC@9 with p < 0.05 on the pooled set and the same sign in each seed. |

### RQ2 — Do specialist roles matter inside the board?
Does replacing the four oncology specialists with four identical generic-physician agents, in the same 9-call pipeline, change accuracy?

| Element | Specification |
|---|---|
| Input data | Same pooled oncology set |
| Comparator | Generic-agent board (identical prompts except the system role) |
| Independent variable | Role assignment (specialist vs generic) |
| Dependent variable / metric | Item correctness / accuracy, paired difference with CI |
| Test | Exact McNemar; Holm correction across the secondary family (RQ2, RQ3a and board vs CoT) |
| Hypothesis | H0: no difference (two-sided). Kim et al. 2025 found roles help in discussion (Group Chat) but not in voting; Zheng et al. 2024 found personas do not help single models. |
| Contradicting observation | For Kim et al.'s finding: generic ≥ specialist board. For the persona finding: specialist board clearly better (Holm-adjusted p < 0.05, ≥ 2 points). |

### RQ3 — What does discussion do to individual answers?
(a) Does the round-2 vote differ in accuracy from the round-1 vote? (b) How often does a member change a correct answer to a wrong one (error propagation) versus a wrong answer to a correct one (correction)?

| Element | Specification |
|---|---|
| Input data | Board transcripts (round-1 and round-2 member answers, chair answer) |
| Comparator | Round-1 independent vote (same board, before discussion) |
| Dependent variables | (a) item correctness of each vote; (b) per-member transitions C→C, W→C, C→W, W→W |
| Metric | (a) accuracy difference + exact McNemar; (b) C→W rate among initially correct answers, W→C rate among initially wrong answers, with 95% CIs by item-cluster bootstrap |
| Hypothesis | Descriptive for (b); H0 for (a) as in RQ1 |
| Contradicting observation | Kim et al. report discussion corrects injected errors 81–94% of the time (VERIFIED, PDF). Contradicted here if the C→W rate is not clearly smaller than the W→C rate. |

### Exploratory analyses (no hypothesis, reported as exploratory)
- Accuracy stratified by round-1 board agreement (4/4, 3/4, ≤ 2/4) as a complexity proxy (links to gap G1).
- Accuracy vs API-equivalent tokens and wall-clock time (efficiency frontier).
- Variation across 3 seeds.

## 3. Contribution — intended vs already demonstrated

| Already demonstrated by others (not claimed) | Intended contribution of this study |
|---|---|
| Multi-agent methods beat a single CoT call (MDAgents 2024; Kim et al. 2025) | Comparison at an **equal call budget** with the **same backbone** |
| Specialist roles help in discussion-based boards, judged by an LLM on 31 private head-and-neck cases (Kim et al. 2025) | Role ablation repeated with an **objective exact-match metric** on **public** oncology items |
| Self-consistency is a strong baseline on medical QA with GPT-4-class models (MDAgents Table 2, INFERRED; Smit et al. 2023) | Evidence for a **small open 7B model** runnable on free GPUs |
| Discussion corrects deliberately injected errors (Kim et al. 2025) | Rates of **spontaneous** correct→wrong and wrong→correct changes |

Not claimed: a new architecture; clinical validity; anything about real tumor-board decisions, imaging or patient outcomes; results for other models.

## 4. Flags on overbroad or underpowered questions
- **Overbroad (rejected):** "Do multi-agent systems improve oncology decision-making?" Exam MCQs are a proxy, not tumor-board decisions. RQ1 is limited to "accuracy on oncology exam items for this model".
- **Overbroad (rejected):** "Do roles matter?" in general. RQ2 is limited to this 9-call pipeline and backbone.
- **Underpowered — must be stated in advance.** Simulated power of the two-sided exact McNemar test (α = 0.05), assuming 15–25% of items are discordant (assumption, not measured):

| Paired items (n) | Difference detectable with ≈ 80% power |
|---|---|
| 97 (MedQA oncology only) | ≈ 12–15 points |
| 200 | ≈ 8–10 points |
| 400 | ≈ 6–8 points |
| 1,273 (full MedQA) | ≈ 4–5 points |

Script and raw output: `power_mcnemar.py`, `power_mcnemar_results.csv` (VERIFIED by execution; the inputs are assumptions). Consequences:
1. The primary set must be the **pooled** oncology set; MedQA oncology alone can only detect large effects.
2. The 2-point "meaningful" threshold is below what the study can detect. A null result will be reported as "no difference larger than about X points", using the CI — never as "no difference".
3. Full MedQA (n = 1,273) stays as a secondary set to show whether any effect is oncology-specific.

## 5. Decision-log entries (Prompt 05)

| ID | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|
| L-11 | 2026-10-24 | Three RQs: board vs SC@9 (primary), role ablation, discussion effects; exploratory complexity/efficiency analyses | Covers G4 directly and G1 at no extra compute | Prompts 02–04 | Freeze in Prompt 07 |
| L-12 | 2026-10-24 | Two-sided tests and no directional hypotheses for RQ1/RQ2 | Prior evidence points both ways | Kim 2025 vs Wang 2024 / Smit 2023 | — |
| L-13 | 2026-10-24 | Primary set = pooled oncology (MedQA + MedMCQA); MedQA-only as pre-specified fallback | n = 97 detects only ≈ 12–15-point effects | Power simulation (VERIFIED run; assumed inputs) | Build MedMCQA subset on Kaggle (Prompt 06) |
| L-14 | 2026-10-24 | Report nulls against the minimum detectable effect and CI | Avoid "no difference" over-claims | Power table | Write into the frozen protocol |
| L-15 | 2026-10-24 | This brief supersedes `research_brief_G1.md` (20 Oct) | That brief predates the Kim et al. 2025 finding | Prompt 04 | Remove the old brief from the submission set |
