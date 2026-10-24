# Prompt 09 output — Baseline built one module at a time, with prompt-to-code log

Saved: 2026-10-24 · Labels: VERIFIED / INFERRED / UNKNOWN / [TEST REQUIRED]
Prompt 09 SAVE item: "Working baseline plus code understanding and prompt-to-code log."

**Baseline being reproduced:** zero-shot chain-of-thought (Kojima et al. 2022) and self-consistency (Wang et al. 2023) on MedQA oncology items, producing per-item predictions (JSONL).
**What "working" means here:** every module runs and passes its tests on CPU with a mock model (VERIFIED, logs in `test_logs/`). The real model run is **[TEST REQUIRED]**: `02_baseline_kaggle.ipynb` produces it, and Prompt 10 waits for its output. No accuracy number in this folder comes from a real model.

## Short-cycle log (spec → code → logic and shapes → test → genuine output)

### Cycle 1 — Data loading and validation (`src/vtb/data.py`, `scripts/prepare_data.py`)
- **Spec / assumptions:** MedQA JSONL rows have `question`, `options`, `answer_idx`; the gold letter must be one of the options; no duplicate questions; item IDs must not depend on file order.
- **Logic:** `load_medqa_jsonl` validates each row and raises `ValueError` on a missing key, a bad gold letter or a duplicate. `item_id` = first 12 hex characters of SHA-1(question). The oncology filter (v1.0) is in the same file.
- **Shapes:** file → `list[Item]`; `Item = {item_id: str[12], question: str, options: dict[letter→str] (5 for MedQA), answer_idx: letter, meta: dict}`; `prepare_data.py` writes `medqa_test_all.jsonl` (1,273), `medqa_test_onc.jsonl` (97), `onc_filter_audit.csv`, `manifest.json`.
- **Tests:** `test_loader_rejects_bad_rows`, `test_loader_shapes_on_real_file`, `test_processed_onc_subset_integrity`; filter tests in `test_core.py`.
- **Genuine output:** `test_logs/cycle1_data.txt`, `cycle1b_oncology_filter.txt` (all pass); `prepare_data.py` on the real file printed 1,273 → 97 (VERIFIED, 20 Oct).

### Cycle 2 — Prompt construction and answer parsing (`src/vtb/methods.py`, `src/vtb/parse.py`)
- **Spec / assumptions:** one fixed answer instruction for every arm; options listed in letter order; the answer is read from an explicit `Answer: X` line. An unparseable answer counts as wrong and is reported.
- **Logic:** `format_question` → "Question: … Options: A. … B. …". `extract_answer`: the last `Answer: X` tag wins; then `\boxed{X}`; then a bare letter on the last line; else `None`. Parser v3 (24 Oct) skips only "Answer: A" + lowercase word (the article), see Prompt 11. `derive_seed` = SHA-256(seed | item | tag).
- **Shapes:** `Item` → prompt string; completion text → letter or `None`; list of letters → plurality letter (ties broken by first appearance).
- **Tests:** 22 parser and vote cases (`test_extract_answer[...]`, `test_majority_vote_ties_and_none`), `test_format_question_lists_options_in_order`, `test_derive_seed_deterministic_and_tag_specific`.
- **Genuine output:** `test_logs/cycle2_prompt_and_parser.txt`, `cycle2b_parser.txt` (all pass).

### Cycle 3 — Model backend (`src/vtb/backends.py`)
- **Spec / assumptions:** one interface, `generate(list[Request]) → list[list[Completion]]`, so the methods never know which engine runs. vLLM for real runs, HF transformers as fallback, a mock for tests only.
- **Logic:** `VLLMBackend` applies the model's chat template and passes per-request `SamplingParams(n, temperature, top_p, max_tokens, seed)`. `MockBackend` returns synthetic "Answer: X" texts and must never be reported.
- **Shapes:** `Request{messages[list of {role, content}], n, temperature, top_p, max_tokens, seed}` → `n` × `Completion{text, prompt_tokens, completion_tokens}`.
- **Tests:** `test_mock_backend_shapes`. **vLLM path: [TEST REQUIRED]** (notebook 01, cell 9).
- **Genuine output:** `test_logs/cycle3_backend.txt` (pass).

### Cycle 4 — Baseline algorithms (`run_cot`, `run_sc` in `src/vtb/methods.py`)
- **Spec / assumptions:** CoT = 1 greedy call (T = 0). SC = 15 samples at T = 0.7, top-p 0.95 in one request (`n = 15`). The stored `final` = vote over the first 9 samples (the call-matched SC@9); other k are recomputed later from the stored samples.
- **Logic:** both build the same system + user messages, call the backend in one batch, parse every sample and record tokens.
- **Shapes:** `list[Item]` → `list[record]`; CoT record `{item_id, gold, method:'cot', calls:1, final, samples[1], prompt_tokens, completion_tokens}`; SC record `{…, method:'sc', calls:15, k_max:15, samples[15]}`.
- **Tests:** `test_cot_record_shape`, `test_sc_record_shape_and_vote`, `test_cot_is_reproducible`.
- **Genuine output:** `test_logs/cycle4_cot_sc.txt` (pass).

### Cycle 5 — Runner, saving predictions, evaluation, stats (`scripts/run_experiment.py`, `scripts/evaluate.py`, `src/vtb/stats.py`)
- **Spec / assumptions:** one file per (dataset, method, model, seed); resumable; run metadata recorded (argv, versions, GPU, timing). Evaluation checks ID/label alignment before computing anything.
- **Logic:** chunks of items → method → append JSONL → `run_meta.jsonl`. `evaluate.py` runs integrity checks (duplicates, unknown IDs, gold mismatch, mixed protocol versions) and stops if any fails. Exact McNemar via a binomial test; paired bootstrap; Holm.
- **Shapes:** JSONL records → `results.csv` (one row per dataset × seed × variant), `comparisons.csv`, figures.
- **Tests:** `test_mcnemar_hand_computed` (hand-computed p = 0.375), `test_holm`, `test_paired_bootstrap_identical_is_zero`, `test_end_to_end_mock` (also checks that resuming does not duplicate records).
- **Genuine output:** `test_logs/cycle5_runner_eval_stats.txt` (pass).

### Cycle 6 — Baseline-only report and basic table (`scripts/baseline_report.py`)
- **Spec:** numbers only, from raw files; rows from the mock model are tagged SYNTHETIC.
- **Output:** n, majority-letter floor, CoT accuracy + CI, parse-fail rate, SC@k, SC@1 − CoT, determinism on a 20-item rerun.
- **Genuine output:** `test_logs/cycle6_baseline_report_on_SYNTHETIC_mock_outputs.md`. This proves the script runs. Its accuracies are fake by construction.

**Full suite:** 41 / 41 tests pass (`test_logs/full_suite.txt`, VERIFIED).

## Deliberate deviations from the published baselines
| Item | Original | Here | Reason |
|---|---|---|---|
| CoT trigger | "Let's think step by step" (Kojima et al. 2022) | "Reason through the case step by step, concisely … Answer: <letter>" | Fixed answer format for parsing; identical across arms |
| SC sampling | T 0.5/0.7, top-k 40, 40 samples, 10 runs (Wang et al. 2023) | T 0.7, top-p 0.95, 15 samples, 3 seeds | Compute; SC@9 is a call-matched control |
| Few-shot | Not used by either baseline in zero-shot form | Zero-shot | Same |

No official reference implementation is reused: the published code (MedAgents, MDAgents, Kim et al. 2025) has no licence (Prompt 04, L-09).

## Prompt-to-code log (what was asked, what the AI produced, what was checked)
| Date | Request to the AI | Code produced / changed | Check | Result |
|---|---|---|---|---|
| 20 Oct | Build data pipeline with a frozen oncology filter | `data.py`, `prepare_data.py` | Ran on the real MedQA file; read all 121 v0.9 matches | Filter refined to v1.0 (97 items) before any model output |
| 20 Oct | Answer parser + vote | `parse.py` v1 | Unit test | Bug: "Answer: A patient" → A; fixed (v2) |
| 20 Oct | Backends + CoT/SC/board methods | `backends.py`, `methods.py` | Mock end-to-end test | Pass |
| 20 Oct | Runner and evaluator | `run_experiment.py`, `evaluate.py`, `stats.py` | Hand-computed McNemar; mock end-to-end | Pass |
| 24 Oct | Review the parser for realistic outputs | `parse.py` v3 + 5 new tests | Tests | "Answer: C. Tell…" now parsed; 41/41 pass |
| 24 Oct | Module-level tests for the baseline | `tests/test_baseline_modules.py` | Run | 8 new tests pass |
| 24 Oct | Baseline report and Kaggle notebook | `baseline_report.py`, `02_baseline_kaggle.ipynb` | Report run on mock output | Works; real run [TEST REQUIRED] |

## What is still needed (genuine execution)
Run `notebooks/01_env_sanity_smoke_kaggle.ipynb`, then `notebooks/02_baseline_kaggle.ipynb`, and share `baseline_outputs.zip`. Prompt 10 is completed from that.
