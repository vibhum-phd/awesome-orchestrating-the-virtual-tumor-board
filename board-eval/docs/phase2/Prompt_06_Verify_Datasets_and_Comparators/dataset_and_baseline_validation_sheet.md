# Prompt 06 output — Dataset and baseline validation sheet

Saved: 2026-10-24 · Tool: Claude · Labels: VERIFIED / INFERRED / UNKNOWN
Prompt 06 SAVE item: "Dataset and baseline validation sheet."

## 1. Recommendation (summary)

| Role | Dataset | Why |
|---|---|---|
| **Primary** | Pooled oncology set: MedQA-USMLE 5-option test, oncology subset (n = 97) + MedMCQA dev, oncology subset (n UNKNOWN) | Public, licensed, objective answers; pooling needed for power (Prompt 05) |
| Secondary | MedQA-USMLE 5-option full test (n = 1,273) | Power, and whether any effect is oncology-specific |
| Baseline anchor | MedQA-USMLE 4-option test (n = 1,273, HF copy) | The variant most published numbers use; external check of the CoT baseline |
| Prompt/parser debugging only | 20 random MedQA **train** items | Keeps all prompt tuning off test items |

Baselines: **B1 greedy zero-shot CoT** (simplest credible baseline) and **B2 self-consistency** voted at k = 1, 3, 5, 9, 15, where SC@9 is the call-matched comparator. Ablation comparator: the same board with generic agents.

## 2. Datasets — source, structure, protocol, licence, compute, pitfalls

| | MedQA-USMLE (5-option) | MedMCQA (dev) | MedQA-USMLE (4-option, HF) |
|---|---|---|---|
| Official source to verify | Jin et al. 2021; github.com/jind11/MedQA (data on Google Drive linked from README) | Pal et al. 2022; github.com/medmcqa/medmcqa; HF `openlifescienceai/medmcqa` | HF `GBaker/MedQA-USMLE-4-options` |
| Copy actually used | `datasets/MedQA/test.jsonl` from github.com/gersteinlab/MedAgents (same file MedAgents evaluated on) | To be downloaded on Kaggle | To be downloaded on Kaggle |
| File structure | JSONL: `question`, `options{A..E}`, `answer`, `answer_idx`, `meta_info` (step1 / step2&3) (VERIFIED, parsed) | JSON: `id, question, opa–opd, cop, choice_type, exp, subject_name, topic_name` (official README, VERIFIED) | `question, options, answer_idx, meta_info` (dataset card, INFERRED) |
| Size | 1,273 test items; 679 Step 1 / 594 Step 2&3 (VERIFIED) | README table: Train 182,822 · Valid 6,150 · Test 4,183 (VERIFIED as printed). Other sources quote dev = 4,183, so which split has which size is **UNCERTAIN** — measured on Kaggle | 1,273 test (INFERRED) |
| Label convention | Letter in `answer_idx` (VERIFIED) | `cop` is 1-based in the original JSON (README example `"cop":1` = A; official `dataset.py` does `cop - 1`, VERIFIED). HF copy may be 0-based → script infers the base from the value range and stops if ambiguous | Letter |
| Benchmark protocol | Exact-match accuracy on the chosen option (as in MedAgents, MDAgents) | Same; dev split used because test labels are not public (INFERRED — confirm on Kaggle) | Same |
| Licence | MIT (LICENSE file, VERIFIED) | MIT (LICENSE file, VERIFIED) | CC-BY-4.0 (dataset card, VERIFIED on 20 Oct) |
| Compute | Inference only; ~110-word stems (median 114 words, VERIFIED) | Inference only; short stems (README max 135 tokens in the valid split) | Same as 5-option |
| Pitfalls | Two test items share one study abstract (5-gram Jaccard 0.78, different answers; not leakage; neither in the oncology subset — VERIFIED). Gold letters unevenly spread (see §4) | Mostly short recall questions, unlike MedQA's case vignettes: **report results by source as well as pooled**. Some items are multi-choice → keep `choice_type == single` only. Repeated questions → de-duplicate by content hash | Different option count → never pool with the 5-option set |

## 3. Baselines and comparators — original method vs this study

| | Original method | This study | Deviation and why acceptable |
|---|---|---|---|
| B1 zero-shot CoT | Kojima et al. 2022, NeurIPS: adds "Let's think step by step" (VERIFIED, proceedings page) | One greedy call; instruction "Reason through the case step by step, concisely … Answer: <letter>" | Wording differs and a fixed answer format is added for reliable parsing. The same instruction is used in every arm, so the comparison stays fair |
| B2 self-consistency | Wang et al. 2023, ICLR: sample reasoning paths, majority vote; T = 0.5 or 0.7 with top-k 40; 40 samples; 10 runs (VERIFIED, arXiv PDF) | T = 0.7, top-p 0.95, 15 samples, majority vote at k = 1, 3, 5, 9, 15; 3 seeds | Fewer samples (compute) and nucleus instead of top-k (the paper's robustness ablation used p = 0.95/0.9). SC@9 is chosen to match the board's 9 calls, not to maximise SC |
| Comparator: generic board | Kim et al. 2025 "w/o recruit" condition: all agents get a generic "medical expert" role (VERIFIED, PDF) | Same 9-call pipeline, 4 identical generic-physician agents | Matches Kim et al.'s ablation idea inside our pipeline |
| Trivial floors (computed, no model) | — | Oncology subset: always answer "B" = **27.8%**; always pick longest option = 20.6%; chance = 20% (VERIFIED, `dataset_sanity_checks_output.json`) | Any method must clearly beat **27.8%**, not 20%, before its result is interpretable |

**Simplest credible baseline:** B1, greedy zero-shot CoT with Qwen2.5-7B-Instruct on the oncology subset. It needs one call per item and validates the prompt, parser and serving stack before anything else runs.

## 4. Evaluation design (zero-shot inference study)
- **No training, so no train/validation/test split is created.** Every arm sees the same frozen item set. The test items are scored once per seed under the frozen protocol (Prompt 07).
- **Prompt and parser development** uses only the 20 MedQA train items. A prompt change after the first test-set run is a protocol change and must be logged.
- **Seeds:** 3 seeds for the oncology sets, 1 for full MedQA. Seeds are derived per item and arm, so arms do not share random draws by accident.
- **Unit of analysis:** the item. All comparisons are paired on the same items (McNemar, paired bootstrap).

## 5. Leakage and validity risks

| Risk | Applies? | Handling |
|---|---|---|
| Item overlap between debug (train) items and test items | Possible; MedQA train file not yet obtained (UNKNOWN) | `leakage_checks.py` pilot vs test on Kaggle; drop any flagged pilot item |
| Overlap between MedQA and MedMCQA items | Unlikely (different exams), UNKNOWN | `leakage_checks.py` MedMCQA-onc vs MedQA-onc; keep one copy |
| Pre-training contamination (Qwen saw MedQA/MedMCQA) | Possible, UNKNOWN | Cannot be removed. It inflates absolute accuracy, not the paired difference between arms; stated as a limitation |
| Subset selection uses the gold answer text (filter rule "stem or gold") | Yes, by design | Same items for every arm, so no bias between arms; absolute accuracy may differ from "all oncology"; sensitivity analysis on the stem-only rule (74 items) |
| Letter bias (gold "B" over-represented in the oncology subset: 27/97) | Yes (VERIFIED) | Report the 27.8% floor; exploratory option-shuffle check if time allows |
| Test-set tuning | Must not happen | Frozen protocol + git history (Prompt 07) |
| Patient / subject / document / time leakage | Not applicable: no patient records, no training | — |

Self-test of the checker (VERIFIED, `leakage_checks_selftest_output.txt`): oncology subset vs full test flags exactly the 97 identical items; full test vs itself flags one pair (the shared-abstract pair above).

## 6. Independent-verification checklist (before Phase III runs)
- [ ] Kaggle: sha256 of `medqa_test.jsonl` = `cfa75cbc…a3`
- [ ] Kaggle: `prepare_extra_data.py` prints MedMCQA split sizes, `cop` distribution and oncology n — compare with the README table
- [ ] Open the MedMCQA HF dataset card: licence, splits, whether test labels are hidden
- [ ] Open the `GBaker/MedQA-USMLE-4-options` card: licence and size
- [ ] Run `leakage_checks.py` for pilot vs test and MedMCQA-onc vs MedQA-onc; both must exit 0
- [ ] Read 10 random MedMCQA oncology items to see whether the filter picks oncology questions
- [ ] Hand-label the 97 MedQA oncology items (`onc_subset_human_audit.csv`)

## 7. Decision-log entries (Prompt 06)

| ID | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|
| L-16 | 2026-10-24 | Floor for "above chance" = 27.8% (majority letter), not 20% | Gold letter B over-represented in the oncology subset | `dataset_sanity_checks_output.json` (VERIFIED) | Update go/no-go and protocol |
| L-17 | 2026-10-24 | Record SC deviations (15 samples, top-p 0.95) from Wang et al. 2023 | Compute; SC@9 is a call-matched control, not a maximised SC | Wang et al. 2023 PDF (VERIFIED) | Report in Methods |
| L-18 | 2026-10-24 | Report results by source (MedQA, MedMCQA) as well as pooled | The two item types differ (vignettes vs short recall) | MedMCQA README; MedQA lengths (VERIFIED) | Add to protocol tables |
| L-19 | 2026-10-24 | Gate the runs on `leakage_checks.py` passing | Train/test and cross-dataset overlap are UNKNOWN | Self-test (VERIFIED) | Kaggle notebook cell |
