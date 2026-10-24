# Prompt 14 output — Pre-registered interpretation plan and Results/Discussion outline

Saved: 2026-10-24 · Labels: VERIFIED / INFERRED / UNKNOWN
Prompt 14 SAVE item: "Evidence-based Results and Discussion outline with limitations."

**There are no results yet, so nothing here interprets results.** This file fixes *in advance* how each possible outcome will be read. When the real `comparisons.csv`, `flip_rates.csv` and `results.csv` arrive, each slot marked ⟨…⟩ is filled from them and the matching row of the decision table is applied. A reading that does not appear in these tables needs an explicit note in the paper saying it was not planned.

## 1. Decision table per research question

### RQ1 — Specialist board (9 calls) vs SC@9
| Observed (primary set, seed 0) | Reading | Wording allowed |
|---|---|---|
| p < 0.05 and Δ ≥ +2 pp; same sign in seeds 1–2 | **Supported:** board structure adds accuracy beyond extra sampling, for this model and item type | "At equal calls, the board was ⟨Δ⟩ pp more accurate (95% CI ⟨lo, hi⟩)" |
| p < 0.05 and Δ ≤ −2 pp | **Contradicted:** sampling beats the board at equal cost | "Self-consistency was ⟨|Δ|⟩ pp more accurate at the same number of calls" |
| p < 0.05 but \|Δ\| < 2 pp | Statistically detectable but below the pre-set meaningful size | "A small difference (⟨Δ⟩ pp) below the 2-pp threshold" |
| p ≥ 0.05 | **Unresolved at this power** | "No difference was detected; with 80% power the test could detect only differences ≥ ⟨MDE⟩ pp (95% CI ⟨lo, hi⟩)". **Never** "the methods are equivalent" |
| Seed 0 significant, seeds 1–2 disagree in sign | Fragile | Report all three; do not claim |

### RQ2 — Specialist vs generic board (Holm-adjusted)
| Observed | Reading |
|---|---|
| Specialist > generic (p_Holm < 0.05, ≥ 2 pp) | Consistent with Kim et al. 2025 (roles help in discussion), now with an objective metric and an open 7B model |
| Generic ≥ specialist or not detected | Kim et al.'s role effect is **not reproduced** in this setting; consistent with Zheng et al. 2024 (personas do not help). Report the MDE |

### RQ3 — What discussion does
| Observed | Reading |
|---|---|
| Round-2 vote > round-1 vote (p_Holm < 0.05) | Discussion improves the board's vote |
| C→W rate CI below W→C rate CI | Discussion corrects more than it corrupts |
| C→W rate CI overlaps or exceeds W→C | **Error propagation** is as common as correction; contrasts with Kim et al.'s injected-error resistance (81–94%) |
| Chair overrides the final-round majority often and is usually wrong when it does | The chair adds noise; the round-2 vote is the better aggregator (exploratory) |

## 2. Alternative explanations to check before accepting any difference
| Explanation | Check (from real files) | If it holds |
|---|---|---|
| Unequal parse failures between arms | `parse_fail_rate` per variant in `results.csv` | Re-read failures; if one arm is penalised by format, report accuracy among parsed items as a sensitivity analysis |
| Unequal truncation (board texts longer) | `truncated_call_rate` | Same as above; consider a protocol change to `max_tokens` for **all** arms |
| Letter bias (gold "B" over-represented) | Prediction letter distribution per arm vs the 27.8% floor | Note it; exploratory option-shuffle follow-up |
| Chair just copies the majority | `chair.csv` override rate | The board then equals a 9-call vote; say so |
| Source heterogeneity (MedQA vignettes vs MedMCQA recall) | By-source rows in `results.csv` / `comparisons.csv` | Report the effect per source; do not generalise the pooled result |
| Seed noise | `seed_summary.csv` SD | Claims only if the direction holds across seeds |
| Pre-training contamination | Cannot be checked | Limits absolute accuracy, equal across arms; state it |
| Token budget, not call budget, drives the result | `api_tokens_per_item` per arm; position on the SC curve in the frontier figure | Report the token-matched reading next to the call-matched one |

## 3. Claims that will not be made whatever the numbers show
- Anything about real tumor-board decisions, patient outcomes, imaging, or clinical deployment.
- Generalisation to other models (only Qwen2.5-7B is tested).
- "Equivalence" from a non-significant test.
- Causal claims about *why* roles help or hurt beyond what the ablations isolate.

## 4. Results and Discussion outline (slots filled from real files only)
**4.1 Data and run integrity.** Item counts per source (⟨n_MedQA⟩ = 97 VERIFIED, ⟨n_MedMCQA⟩); leakage gate result; parse-failure and truncation rates per arm (Table 1); settings audit passed.
**4.2 Baseline behaviour.** CoT and SC@k accuracy vs the 27.8% floor and the 4-option anchor; SC curve (Figure 1).
**4.3 RQ1.** Table 1 row "specialist board vs SC@9": Δ, CI, p, MDE → reading from §1.
**4.4 RQ2 and RQ3a.** Table 2 (Holm family) → readings from §1.
**4.5 RQ3b.** Table 4 / Figure 2: flip rates with CIs; chair overrides.
**4.6 Cost.** Figure 1: accuracy vs API-equivalent tokens; wall-clock per item.
**4.7 Robustness.** Seeds (Table 3), by source, stem-only and human-audited subsets.
**Discussion.** (a) What the call-matched result says about earlier single-call comparisons (EvoMDT, Kim et al.). (b) Roles: agreement or disagreement with Kim et al. and Zheng et al. (c) Discussion as correction vs propagation. (d) Practical meaning for resource-limited settings, kept to exam accuracy and cost.
**Limitations.** Exam MCQs as a proxy; keyword-defined oncology scope; one 7B model; modest n (power stated); possible contamination; English-only; no retrieval, no images.

## 5. Follow-up experiments (max three, ranked by cost and information)
| Rank | Experiment | Cost | Information gained |
|---|---|---|---|
| 1 | Repeat the primary comparison with a second open model family of similar size | Medium (one more grid on the primary set) | Highest: whether the finding is model-specific |
| 2 | Option-order shuffle for SC@9 and the specialist board on the primary set | Low (two arms, one seed) | Separates reasoning from letter or position bias |
| 3 | Adaptive board (round 2 only when round 1 disagrees), call-matched (pathway C) | Medium | Practical efficiency; needs a new protocol version |

## 6. Decision-log entries (Prompt 14)

| ID | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|
| L-37 | 2026-10-24 | Pre-register the interpretation table before any result exists | Prevents turning nulls into positives after the fact | This file (dated, committed) | Apply to the real `comparisons.csv` |
| L-38 | 2026-10-24 | Check eight alternative explanations before accepting any difference | Parse, truncation, letter bias, chair copying, source mix, seed noise, contamination, tokens | §2 | Run checks on the real files |
