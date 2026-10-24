# Prompt 13 output — Evaluation code, audit procedure and request for real files

Saved: 2026-10-24 · Labels: VERIFIED / INFERRED / UNKNOWN
Prompt 13 SAVE item: "Metrics script, actual result CSV, tables and research figures."

**Status:** the metrics script is finished and tested: 46/46 tests pass, including four new tests of the protocol-v1.1 logic.
**There is no actual result CSV yet**, because no real model run exists (see Phase III). The `SYNTHETIC_demo_outputs_mock_backend/` folder shows the format only. Interpretation waits for the real files listed in §6.

## 1. What `evaluate.py` checks before computing any metric
In order; the script stops with a non-zero exit if any **FAIL** appears.

| Check | How | Failure means |
|---|---|---|
| ID alignment | Every `item_id` in a run must exist in the dataset file | Wrong file or corrupted run |
| Label alignment | Gold letter in each record must equal the dataset file's gold | Data or code mismatch |
| Duplicates | No `item_id` twice within a run | Resume bug |
| Coverage | Share of the dataset each run covers is printed | Partial run (allowed only if all arms match) |
| **Pairing** (new) | All arms for a dataset/seed/model must cover the **same** items | Comparisons would be unpaired → refused (test `test_unpaired_arms_fail_integrity`) |
| Protocol version | One version per run and across runs | Mixed protocols → refused |
| **Comparator settings** (new) | `run_meta.jsonl`: same generation settings and model for every run | Arms not comparable → refused |
| Missing values | Unparseable answers kept as `None`, scored wrong, reported as `parse_fail_rate` | — |
| **Truncation** (new) | Share of calls that hit `max_tokens`, per variant (`truncated_call_rate`) | Unequal truncation between arms is flagged for discussion |
| Metric direction | Recorded in `integrity_report.json`: accuracy, higher is better | — |

## 2. Comparisons — exactly the frozen protocol
Pairs are read from `configs/frozen_protocol.yaml`, not typed into the code. This fixes DBG-11 / L-21: the code had kept the v1.0 list.
- **PRIMARY:** specialist board (final) vs SC@9. Exact McNemar; decision rule p < 0.05 **and** |Δ| ≥ 2 points.
- **Secondary (Holm-adjusted as one family):** specialist vs generic board; round-2 vote vs round-1 vote; specialist board vs CoT.
- **Exploratory (no correction, prefixed "EXPLORATORY"):** board final vs round-1 vote; generic board vs SC@9.
- **Non-significant results** print the minimum difference the test could detect with 80% power. This is computed exactly from n and the observed share of discordant items (`mde80_pp`, new function `mde_80`), so a null can never be written as "no difference". Example wording: *"not detected; with 80% power this test detects only differences ≥ 18.0 pp; 95% CI −15.5 to 9.3 pp"*.
- Uncertainty: 95% item-bootstrap CIs (10,000 resamples, seed 20261020) for every accuracy and every paired difference.
- Multiple runs: `seed_summary.csv` gives mean, SD, min and max across seeds per variant. The primary analysis remains seed 0 (protocol).
- RQ3b: `flip_rates.csv` gives the C→W rate (among initially correct member answers) and W→C rate (among initially wrong), with CIs from resampling **items**, because four members of one item are not independent.
- Pooled and by-source: the oncology sources are evaluated separately and pooled (`--pool medqa_onc,medmcqa_onc`, as in the protocol).

The exact power calculation was checked against the Prompt 05 simulation: n = 97, 15% discordance, 10-point difference → 0.68 exact vs 0.69 simulated (test `test_power_matches_simulation_and_edges`, VERIFIED).

## 3. Outputs (all traceable to raw JSONL)
`integrity_report.json` · `results.csv` (accuracy, CI, parse-fail, truncation, calls, API-equivalent tokens, wall-clock per variant) · `comparisons.csv` · `flip_rates.csv` · `flips.csv` · `chair.csv` · `stratified.csv` · `seed_summary.csv` · `figures/frontier__*.png|pdf` (accuracy vs tokens) · `figures/flips__*.png|pdf`.
Figures made from mock outputs are automatically watermarked "SYNTHETIC — MOCK BACKEND". Real-run figures carry no watermark.

## 4. How to audit for leakage
1. `leakage_checks.py` (Prompt 06) must have exited 0 for pilot-vs-test and MedMCQA-onc vs MedQA-onc **before** the runs (protocol gate). Keep its JSON output with the results.
2. Confirm in git history that no prompt, parser or setting changed after the first test-set run (`git log -- src/ configs/`). If one did, protocol §13 applies: re-score all arms and report it.
3. Confirm that pilot items (`medqa_train_pilot.jsonl`) never appear in `results/raw/` (`evaluate.py` would also flag unknown IDs).
4. Pre-training contamination cannot be audited here. It is reported as a limitation, and it applies equally to all arms.

## 5. How to audit for incompatible comparator settings
1. `integrity_report.json` must contain "generation settings identical across N run records" and no FAIL lines.
2. `results.csv`: `calls_per_item` must be 1 (CoT), k (SC@k) and 9 (both boards' final). Anything else means a pipeline change.
3. `truncated_call_rate` and `parse_fail_rate` should be similar across arms. A large gap is an explanation to test before any claim (Prompt 14).
4. All runs must share the same `protocol_version` (checked automatically).

## 6. Files required before any interpretation (please share)
From the Kaggle runs (notebook 03, Prompt 12):
- `results/raw/*.jsonl` and `results/raw/run_meta.jsonl` for: CoT, SC, specialist board and generic board × MedQA-onc and MedMCQA-onc × seeds 0, 1, 2 (+ MedQA-all seed 0)
- `results/env/leak_*.json` (leakage gate output)
- `results/env/pip_freeze.txt`, `results/env/env_check_kaggle.json`
- The git commit hash used for the runs

Then: `python scripts/evaluate.py --raw results/raw --out results` → read `integrity_report.json` first → then Prompt 14.

## 7. Decision-log entries (Prompt 13)

| ID | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|
| L-30 | 2026-10-24 | Read comparison pairs from the protocol file; Holm only in the secondary family | Code/protocol mismatch (DBG-11) | `test_protocol_pairs_parsed_from_yaml` | Closed DBG-11 |
| L-31 | 2026-10-24 | Report exact 80%-power MDE with every non-significant result | Protocol null-reporting rule (L-14) | Exact power vs simulation (VERIFIED) | — |
| L-32 | 2026-10-24 | Refuse evaluation if arms cover different items or used different settings | Paired design; fair comparators | `test_unpaired_arms_fail_integrity` | — |
| L-33 | 2026-10-24 | Flip-rate CIs by item-cluster bootstrap | Members within an item are not independent | `test_cluster_bootstrap_rate` | — |
