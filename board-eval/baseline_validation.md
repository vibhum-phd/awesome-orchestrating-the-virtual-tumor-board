# Gate G2 — Baseline validation plan (to be filled with REAL outputs)

Nothing below is a result yet. Each check lists what to run, what would count as a pass, and where the
evidence goes. Mark each item VERIFIED / UNCERTAIN / NEEDS CORRECTION after running it.

## What "baseline" means here
The baselines are standard inference procedures (greedy CoT; self-consistency, Wang et al. 2023), run
with my own code on Qwen2.5-7B-Instruct. There is no single official implementation to replicate
number-for-number, so validation = (1) the pipeline measures what it claims and (2) the numbers are
in a plausible range relative to independent reports.

| # | Check | Command / evidence | Pass criterion | Status |
|---|---|---|---|---|
| V1 | Data integrity | notebook cell 4: sha256 + `manifest.json` | hash = `cfa75cbc…a3`; 1,273 items; 97 onc | VERIFIED in Claude workspace; re-check on Kaggle |
| V2 | Parser correctness | `pytest tests` (29 tests) | all pass | VERIFIED (CPU) |
| V3 | Parser on real model text | smoke test: compare `final` with the raw text for all 5 pilot items; then inspect every parse failure in the first real run | 0 mis-parses on manual reading; parse-fail ≤ 3% per method (else fix prompt/parser *on train items* and log) | TO RUN |
| V4 | External anchor (4-option MedQA, CoT) | `run_experiment.py --dataset medqa4_all --method cot --seed 0` → `evaluate.py` | Accuracy within a few points of independently reported Qwen2.5-7B MedQA figures (e.g., ~56.8% listed for "Qwen2.5 7B" in Table 1 of *O1 Replication Journey Part 3*, arXiv 2501.06458 — **INFERRED: variant, prompt and Instruct/base not confirmed; open the table yourself**). A large gap (>8 pp) → investigate prompt/chat template/parsing before going on. | TO RUN |
| V5 | Chance floor | 5-option: 20%, 4-option: 25% | every method clearly above chance | TO RUN |
| V6 | Self-consistency behaves like SC | `results.csv` sc@1…sc@15 | sc@1 ≈ CoT ± noise; accuracy non-decreasing on average with k (not guaranteed per item) | TO RUN |
| V7 | Seeds reproduce | rerun `cot` seed 0 on 20 items | identical outputs at T=0 (vLLM batching can cause tiny nondeterminism — record if it happens) | TO RUN |
| V8 | Call/token accounting | `results.csv` calls_per_item | cot 1, sc@9 9, board final 9 | VERIFIED with mock; re-check on real run |
| V9 | No test-set tuning | git history | prompts unchanged after first test-set run | ongoing |

## Deviations from published designs (fill in as they occur)
- Board is *inspired by* MedAgents/MDAgents, not a reproduction: fixed oncology roles (no expert recruitment step), no RAG, no report summariser.
- 5-option MedQA is used for experiments; 4-option only for V4.
