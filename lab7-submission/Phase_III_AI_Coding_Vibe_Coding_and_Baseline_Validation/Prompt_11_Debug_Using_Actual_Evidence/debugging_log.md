# Prompt 11 output — Debugging log (actual evidence only)

Saved: 2026-10-24 · Labels: CONFIRMED (shown by real output) / HYPOTHESIS (not yet shown)
Prompt 11 SAVE item: "Corrected code, tested fix and documented debugging decision."

Every case below happened in this project, and the "actual output" column quotes it. **No real-model run exists yet**, so there is no model-output bug here. Those will be added after the Kaggle runs, using the same format. Cases are newest first.

## Summary

| ID | Date | Area | Symptom (actual) | Fix | Tested | Rerun needed? |
|---|---|---|---|---|---|---|
| DBG-12 | 24 Oct | Data | MedMCQA README split table: Valid 6,150 / Test 4,183 — conflicts with other sources | Measure on Kaggle; not fixed in code | — | No (nothing run) |
| DBG-11 | 24 Oct | Evaluation | `evaluate.py` still compares the 4 v1.0 pairs; protocol v1.1 names 3 | **Open** — fix in Prompt 13 | — | No (nothing evaluated) |
| DBG-10 | 24 Oct | Backend | Truncated completions not recorded | `finish_reason` stored and reported | `test_finish_reason_recorded` | No |
| DBG-09 | 24 Oct | Parser | v2 returns `None` for "Answer: C. Tell the attending…" | Parser v3 | 5 new cases; 42/42 pass | No (no real outputs) |
| DBG-08 | 24 Oct | Env test | `env_check.py` reported GitHub unreachable | HTTP error = reachable | Re-run shows `github: true` | No |
| DBG-07 | 24 Oct | LaTeX | `! LaTeX Error: File 'lmodern.sty' not found.` | Use `mathptmx` | PDF builds, 1 page | No |
| DBG-06 | 23 Oct | Literature tooling | Fetching Kim et al. 2025 PDF returned "[binary data]" | Download with curl, extract with pdfplumber | 31 pages extracted | No |
| DBG-05 | 23 Oct | Repo access | `git clone …/KesselZ/EvoMDT` → `fatal: could not read Username` | None possible; recorded UNKNOWN | — | No |
| DBG-04 | 20 Oct | Runner | `DeprecationWarning: datetime.datetime.utcnow() is deprecated` | `datetime.now(timezone.utc)` | Warning gone | No |
| DBG-03 | 20 Oct | Data access | `curl: (56) CONNECT tunnel failed, response 403` (Hugging Face) | Use the GitHub copy of MedQA; hash recorded | Hash re-checked 24 Oct | No |
| DBG-02 | 20 Oct | Oncology filter | v0.9 selected 121 items incl. "His father died of lung cancer", "Neuroleptic malignant syndrome", "Tumor necrosis factor-α" | Filter v1.0 | 5 filter tests; 97 items | Data rebuilt before any model run |
| DBG-01 | 20 Oct | Parser | `AssertionError: assert 'A' == None` for "Answer: A patient with … so D" | Parser v2 | Test passes | No |

## Detailed entries (the five that changed code behaviour)

### DBG-09 — Parser v2 rejects normal answers with trailing text
- **Relevant code:** `src/vtb/parse.py`, `_ANSWER_TAG` v2 (required the letter to be the last thing on its line).
- **Actual output** (v2 from the committed HEAD vs v3 from the working tree, run 24 Oct; raw file `parse_v2_vs_v3.txt`):

| Last line | v2 | v3 |
|---|---|---|
| `Answer: C. Tell the attending he cannot fail to disclose t…` | None | C |
| `Answer: B because the drug cross-links DNA` | None | B |
| `Answer: A patient with this finding most likely has D` | None | None |
| `Answer: C` | C | C |
| `Answer: Cisplatin` | None | None |

- **Expected:** a letter followed by punctuation or option text is the answer. "A" followed by a lowercase word is the article, so it is not.
- **Cause (CONFIRMED by the table):** the v2 fix for DBG-01 was too broad. It removed every case with trailing text.
- **Hypothesis (not yet shown):** Qwen2.5-7B will often write "Answer: X. <option text>". Only the pilot run can show how often.
- **Smallest safe correction:** v3 accepts the letter unless it runs into another letter ("Cisplatin"). It skips only "A" + space + lowercase word.
- **Verification test + edge case:** 5 new parser cases, including the edge case "Answer: A patient\nAnswer: D" → D. Full suite 42/42.
- **Earlier results to rerun:** none; no real outputs exist. If a later parser change happens after real runs, every arm is re-scored from the stored texts (protocol §13).

### DBG-10 — Truncation was invisible
- **Relevant code:** `backends.py` `Completion`; `methods.py` `_tok`, `_sum_tokens`.
- **Actual evidence:** code audit in Prompt 10 (A10). `Completion` had no field for why generation stopped.
- **Expected:** every call records whether it hit `max_tokens`.
- **Cause (CONFIRMED by reading the code):** the field was never stored. **Hypothesis:** board members may hit 512 tokens more often than CoT, which would create unequal parse failures.
- **Correction:** `finish_reason` added (vLLM's own value; HF backend: "length" if the token count reached `max_tokens`); `n_truncated` summed per record; `baseline_report.py` reports truncation rates.
- **Test:** `test_finish_reason_recorded` (mock returns "stop"). The real vLLM value is [TEST REQUIRED] in notebook 01.
- **Rerun:** none needed.

### DBG-08 — Environment test said GitHub was unreachable
- **Actual output:** first run `"network": {"huggingface": false, "github": false}`, although `git clone` from GitHub had worked. Direct check: `HTTPError HTTP Error 400: Bad Request`.
- **Cause (CONFIRMED):** GitHub answered the HEAD request with 400, and `reachable()` counted every exception as "unreachable". The proxy certificate was a hypothesis, and it was ruled out.
- **Correction:** `urllib.error.HTTPError` counts as reachable; only connection, TLS or proxy failures count as unreachable.
- **Test:** re-run → `"github": true`, `"huggingface": false` (correct for this workspace).
- **Rerun:** the environment log was regenerated (the saved log is the corrected run).

### DBG-02 — Oncology filter included non-oncology items
- **Actual output:** listing of all 121 v0.9 matches, e.g. "…His mother died of lung cancer at age 68…", gold "Neuroleptic malignant syndrome", gold "Tumor necrosis factor-α".
- **Cause (CONFIRMED):** keyword matching ignored who had the cancer, negation ("rule out cancer") and fixed phrases.
- **Correction:** filter v1.0 drops sentences about relatives, negated mentions and three non-oncology phrases → 97 items.
- **Tests:** `test_filter_excludes_relative_history`, `…_negated_and_phrases`, `…_gold_only`, `test_distractor_alone_does_not_include`.
- **Known cost:** a few true oncology items are lost (e.g. a Lynch-syndrome family-history item). A human audit file and a sensitivity analysis are planned.
- **Rerun:** the data subset was rebuilt before any model output existed.

### DBG-01 — "Answer: A patient…" parsed as option A
- **Actual output:** `AssertionError: assert 'A' == None` where `'A' = extract_answer('Answer: A patient with ... so D', [...])`.
- **Cause (CONFIRMED):** the v1 regex accepted any capital letter after "Answer:".
- **Correction:** v2 (later refined in DBG-09).
- **Rerun:** none.

## How future (real-run) bugs will be logged
Same fields: relevant code, actual traceback or output, expected behaviour, confirmed cause vs hypotheses, smallest correction, verification test + one edge case, which runs must be re-scored or rerun. Fixes found on test outputs are applied to every arm and reported (protocol §13).

## Decision-log entries (Prompt 11)

| ID | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|
| L-28 | 2026-10-24 | Adopt parser v3 before any real output | v2 rejected common answer formats | `parse_v2_vs_v3.txt` (CONFIRMED) | Check parse-fail rate on the pilot (B3) |
| L-29 | 2026-10-24 | Keep DBG-11 open until Prompt 13; block comparisons until fixed | Protocol/code mismatch | Code read | Fix in Prompt 13 |
