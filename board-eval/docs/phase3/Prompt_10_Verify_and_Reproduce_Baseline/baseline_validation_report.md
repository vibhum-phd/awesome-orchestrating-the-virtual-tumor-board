# Prompt 10 output — Baseline validation report

Saved: 2026-10-24 · Status labels per item: **VERIFIED**, **UNCERTAIN**, **NEEDS CORRECTION**
Prompt 10 SAVE item: "Baseline reproduction/validation report, including discrepancies."

**Overall status: PARTIAL.**
- **Part A (implementation audit):** complete. It found one real defect, which is now fixed.
- **Part B (measured behaviour):** **waiting for the real baseline run** (`02_baseline_kaggle.ipynb`). The acceptance criteria are written down below *before* any number exists, so the result cannot be judged after the fact.
- **No board or comparison run** may start until Part B is complete.

Baselines audited: zero-shot CoT (Kojima et al. 2022, NeurIPS — VERIFIED proceedings page) and self-consistency (Wang et al. 2023, ICLR — VERIFIED from the arXiv PDF: "Published as a conference paper at ICLR 2023").

## Part A — Implementation audit against the original methodology

| # | Aspect | Original | Implementation (where) | Status |
|---|---|---|---|---|
| A1 | Preprocessing | Question + options as given | `format_question`: question, then options in letter order; no rewriting (`methods.py`) | VERIFIED (test `test_format_question_lists_options_in_order`) |
| A2 | Model ("architecture") | Any LLM; here one fixed backbone | Qwen2.5-7B-Instruct for every arm, read from the protocol (`frozen_protocol.yaml`) | VERIFIED (config) |
| A3 | CoT decoding | Greedy, zero-shot trigger "Let's think step by step" | Greedy (`temperature=0.0, top_p=1.0`, `methods.py` l.78–80); trigger reworded with a fixed answer line | VERIFIED; wording = acceptable adaptation (same in all arms) |
| A4 | SC sampling | T 0.5/0.7, top-k 40, 40 samples, majority vote, mean of 10 runs | T 0.7, top-p 0.95, 15 samples, plurality vote; 3 seeds (`methods.py` l.93–104) | VERIFIED; fewer samples and nucleus instead of top-k = acceptable adaptations (the paper's ablation also used p = 0.95), logged L-17 |
| A5 | SC aggregation | Unweighted majority vote over final answers | `majority_vote`: plurality over parsed answers, `None` ignored, ties → first seen (independent of the gold label) | VERIFIED (tests) |
| A6 | Random seeds | Not specified per call | Per-call seed = SHA-256(seed, item, tag); greedy calls are deterministic in principle | VERIFIED in code; vLLM batch determinism **UNCERTAIN** (check B6) |
| A7 | Metric | Accuracy | Exact letter match; unparseable = wrong; parse-fail rate reported (`evaluate.py` l.112–113) | VERIFIED |
| A8 | Data split | Test set of the benchmark | MedQA test (hash-checked); prompts debugged only on train items | VERIFIED (protocol, data manifest) |
| A9 | Benchmark protocol | MedQA accuracy as in MedAgents / MDAgents | Same file MedAgents evaluated on (5 options); 4-option variant only as an external anchor | VERIFIED |
| A10 | Output truncation | Not discussed | **Was not recorded.** A completion that hits `max_tokens` = 512 loses its "Answer:" line, becomes a parse failure, and could differ between arms unseen | **NEEDS CORRECTION → fixed 24 Oct**: `finish_reason` now stored per call, truncation rates reported by `baseline_report.py`; test `test_finish_reason_recorded` passes |
| A11 | Answer parser | — | v3 (24 Oct): last `Answer: X` wins; skips only "Answer: A" + lowercase word | VERIFIED on 21 parser test cases; behaviour on real text **UNCERTAIN** until B3 |
| A12 | Token accounting | — | SC counts the prompt once per sample ("API-equivalent"); wall-clock reported separately | VERIFIED; a reporting choice, stated in Methods |
| A13 | Evaluation comparisons | — | `evaluate.py` still holds the v1.0 comparison list | **NEEDS CORRECTION** before any comparison (L-21; Prompt 13). Does not affect the baseline numbers |

## Part B — Measured behaviour (to be filled from `baseline_outputs.zip`)
Acceptance criteria fixed on 24 Oct 2026, before any real output. A failed criterion means investigate, not discard.

| # | Check | Acceptance criterion | Source of the expectation | Measured | Status |
|---|---|---|---|---|---|
| B1 | CoT accuracy, MedQA 4-option test (anchor) | Within ±8 points of ≈ 57% | Table 1 of arXiv 2501.06458 lists 56.79% for "Qwen2.5 7B" on MedQA (read via an AI summary; Instruct vs base and option count not confirmed — **INFERRED**). A weak anchor: a miss means checking the chat template and parser, not proof of a bug | PENDING | — |
| B2 | CoT on MedQA-onc and MedMCQA-onc | MedQA-onc > 27.8% (majority-letter floor); MedMCQA-onc > its own floor (printed by the report) | `dataset_sanity_checks_output.json` (VERIFIED) | PENDING | — |
| B3 | Parse failures | ≤ 3% for CoT and per SC sample; every failure read by hand | Protocol gate | PENDING | — |
| B4 | Truncation | ≤ 2% of calls hit 512 tokens; otherwise raise `max_tokens` for **all** arms (logged change) | Instruction asks for ≤ 150 words | PENDING | — |
| B5 | SC@1 vs CoT | \|SC@1 − CoT\| ≤ 5 points | One sample at T = 0.7 should behave like greedy on average (INFERRED) | PENDING | — |
| B6 | SC curve | Accuracy at k = 1, 3, 5, 9 should not fall by more than 2 points at any step | Wang et al. 2023, Fig. 2: accuracy grows with the number of paths (VERIFIED) | PENDING | — |
| B7 | Determinism | Greedy CoT rerun on 20 items: ≥ 19/20 identical answers | Greedy decoding; small batch-order effects possible in vLLM | PENDING | — |
| B8 | Cost | Measured tokens per item and seconds per item recorded | Replaces the INFERRED compute estimate | PENDING | — |

## Part C — Discrepancies: acceptable adaptation vs invalidating change

| Difference | Acceptable? | Why |
|---|---|---|
| Reworded CoT trigger with a fixed answer line | Acceptable | Identical across every arm; needed for objective scoring |
| 15 samples instead of 40; 3 seeds instead of 10 runs | Acceptable | The study compares at 9 calls, not maximum SC accuracy; SC@15 is also reported |
| top-p 0.95 instead of top-k 40 | Acceptable | Used in the original paper's own robustness ablation |
| 5-option MedQA, while many papers report the 4-option variant | Acceptable if stated | The 4-option anchor (B1) links to published numbers |
| A different parser or `max_tokens` for one arm only | **Would invalidate** | Must be identical across arms; any fix is applied to all arms and every run is re-scored |
| Prompt tuning on test items | **Would invalidate** | Only train items are used for debugging |

## Part D — Additional checks required (exact steps)
1. Run `notebooks/01_env_sanity_smoke_kaggle.ipynb` → share `env_and_pilot_outputs.zip`.
2. Run `notebooks/02_baseline_kaggle.ipynb` → share `baseline_outputs.zip` (contains `results/baseline/baseline_report.md`).
3. Fill the "Measured" column of Part B from `baseline_report.md`; mark each row VERIFIED or NEEDS CORRECTION.
4. Read every unparseable or truncated answer (printed by notebook 02) and classify the cause (Prompt 11 log).
5. Open Table 1 of arXiv 2501.06458 yourself to confirm the anchor value and its variant (turns B1 from INFERRED into VERIFIED).
6. Only then fix `evaluate.py` (A13) and move to the comparison runs.

## Decision-log entries (Prompt 10)

| ID | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|
| L-25 | 2026-10-24 | Record `finish_reason` for every call; report truncation | Audit found truncation was invisible and could differ by arm | Code audit (VERIFIED); new test passes | Check B4 on the real run |
| L-26 | 2026-10-24 | Fix acceptance criteria B1–B8 before seeing any baseline output | Avoid judging the baseline after the fact | This report | Fill from `baseline_outputs.zip` |
| L-27 | 2026-10-24 | No comparison or board run until Part B is complete | Prompt 10: validate before testing extensions | — | Wait for Kaggle output |
