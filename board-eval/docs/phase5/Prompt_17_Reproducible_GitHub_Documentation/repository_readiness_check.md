# Prompt 17 output — Repository readiness check and reproduction instructions

Date: 2026-10-24 · Repository commit checked: `a398cff` (+ README note on the sanity-check output file)
Deliverable: `README.md` (public-ready, in this folder and at the repo root).

## 1. Command status (what was genuinely executed)
| Command | Where run | Status | Evidence |
|---|---|---|---|
| `pip install -r requirements.txt`; `pytest -q tests` | AI workspace, Python 3.13.16 and 3.11.17, two fresh clones | VERIFIED: 45 passed + 1 skipped, 46 after raw data | `reproduction_log_fresh_clone.txt` |
| MedQA `git clone` + `sha256sum` | fresh clone | VERIFIED: hash matches | same |
| `prepare_data.py` | fresh clone | VERIFIED: 1273 / 97, committed files unchanged | same |
| `dataset_sanity_checks.py .` | fresh clone | VERIFIED: floors 0.2176 / 0.2784 | same |
| `run_experiment.py --backend mock` (4 methods) + `evaluate.py` | fresh clone | VERIFIED (plumbing only; outputs SYNTHETIC) | same |
| `make_paper_tables.py` on mock results | fresh clone | VERIFIED: refuses, exit 1 | same |
| `latexmk -pdf main.tex` | AI workspace | VERIFIED: 5 pages, 0 BibTeX warnings (fallback class) | Prompt 15/16 build logs |
| `env_check.py` | AI workspace CPU | VERIFIED; `--require-gpu` exits 1 without GPU | Phase III Prompt 08 |
| `leakage_checks.py` | AI workspace self-test only | VERIFIED as self-test; real gate [TEST REQUIRED] | Phase II Prompt 06 |
| `pip install -r requirements-gpu.txt`, `prepare_extra_data.py`, all `--backend vllm` runs, notebooks 01–03, `evaluate.py` on real outputs | Kaggle 2×T4 | **[TEST REQUIRED]** — never run | — |

## 2. Errors the reproduction test found in the README (fixed)
| # | README said | What happened | Fix |
|---|---|---|---|
| R1 | `dataset_sanity_checks.py data/processed` | FileNotFoundError: the script takes the repo root | Command changed to `dataset_sanity_checks.py .` |
| R2 | "expected: 46 passed" after install | 45 passed, 1 skipped — one test needs the raw MedQA file, which is not committed | Expected count stated as 45 + 1 skipped, 46 after §4 |
| R3 | (not in README) | sanity script writes `scripts/dataset_sanity_checks_output.json` into the tree | Mentioned in the README |
| R4 | (my log) | first log showed `exit=0` for the refusal because `$?` came from `tail` | Re-checked directly: exit 1; recorded in the log |

These were found only by running the README from a clean clone. Writing it was not enough.

## 3. Configuration and dependencies
| Item | Present | Note |
|---|---|---|
| `configs/frozen_protocol.yaml` v1.2 | yes | model, sampling, datasets, comparisons, gates, seeds |
| `requirements.txt` (CPU) | yes | floors + versions actually tested (3.13 in the file header; 3.11 in `docs/py311_test_log.txt`) |
| `requirements-gpu.txt` | yes, **unpinned** | Deliberate: pinning untested versions would be a false claim. Pin from `pip_freeze.txt` after notebook 01 |
| Seeds | yes | run seeds 0/1/2; per-call seed = SHA-256(seed, item, role); bootstrap seed 20261020 |
| Data hashes | yes | MedQA sha256 in `data/README.md` and `manifest.json` |
| Paths | relative to repo root everywhere; Kaggle paths only inside notebooks (`/kaggle/working`) | checked by the fresh clone in a different directory |

## 4. Secrets, private data and weights scan
| Check | Command / method | Result |
|---|---|---|
| Tokens / keys (HF, OpenAI-style, GitHub, AWS, private keys, `password=`, `api_key=`) | `grep -rInE` over the tree, `.git` excluded | none |
| Email addresses | regex scan | none |
| Model weights (`*.safetensors`, `*.bin`, `*.gguf`, `*.pt`) | `find` | none |
| Files > 2 MB | `find -size +2M` | none (largest: `medqa_test_all.jsonl`, 1.3 MB) |
| Local paths | grep for `/home/claude`, `/tmp/claude-0`, `/root/`, Windows paths | LaTeX build files (now git-ignored) and one raw self-test log (`leakage_checks_selftest_output.txt`) containing the AI workspace path. Kept unaltered because it is a raw log; it reveals nothing private |
| Patient / private data | by design | none: public exam questions only |
| Redistribution | MedQA and MedMCQA are MIT (notices in `data/`); the raw MedQA file is not committed, processed MedQA files are | consistent with the licence |
| Restricted model | Qwen2.5-7B-Instruct is Apache-2.0 and downloaded at run time | nothing restricted is stored |

## 5. Still open before the repository is public
- Push to GitHub and replace `<repository-url>` / `[TO VERIFY]` in README and paper.
- Fold into `orchestrating-the-virtual-tumor-board` if that remains the plan.
- Pin GPU versions after notebook 01; replace the INFERRED compute estimate with measured time.
- A second person should run checklist items 1–5 on their own machine (the test above was run by the AI in its workspace, not by a second student).

## 6. Decision-log entries (Prompt 17)
| ID | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|
| L-45 | 2026-10-24 | Every README command carries VERIFIED or [TEST REQUIRED] | Prompt 17 rule; no GPU run has happened | Section 1 | Update labels after Kaggle |
| L-46 | 2026-10-24 | Keep `requirements-gpu.txt` unpinned until notebook 01 runs | Untested pins would look like a verified environment | — | Pin from `pip_freeze.txt` |
| L-47 | 2026-10-24 | Test the README from a fresh clone, not only by reading it | Found errors R1–R2 | `reproduction_log_fresh_clone.txt` | Second student repeats on own machine |
