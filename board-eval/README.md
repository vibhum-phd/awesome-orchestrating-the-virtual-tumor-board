# Does the Virtual Tumor Board Need a Board?
### A call-matched evaluation of specialist multi-agent LLM deliberation on oncology exam questions

**Status (24 Oct 2026):** design, code, tests and a results-pending paper draft are complete. **No model results exist yet.** All GPU runs are prepared as Kaggle notebooks and have not been executed. Every command below is labelled:

- **[VERIFIED]** — run by us, output saved in this repository (path given)
- **[TEST REQUIRED]** — written and checked for syntax, but not yet run in the stated environment

Author: Vibhum Sharma (IIIT Allahabad). Course: AI Tools for Research, Lab 7.

---

## 1. Problem
Published LLM "tumor board" systems (EvoMDT, MedAgents, MDAgents, MDAT) report gains over single-model baselines, but the board usually makes more model calls than the baseline it beats. We ask whether the gain survives an **equal call budget**.

| Arm | Calls per item | What it is |
|---|---|---|
| CoT | 1 | One greedy chain-of-thought answer |
| SC@k | k (k = 1, 3, 5, 9, 15) | k sampled answers, plurality vote. **SC@9 is call-matched to the board** |
| Specialist board | 9 | 4 roles (medical, surgical, radiation oncologist, pathologist): round 1, round 2 with the others' views, greedy chair |
| Generic board | 9 | Same structure, roles replaced by identical generic agents (ablation) |

Model: Qwen2.5-7B-Instruct (Apache-2.0), same for every arm.

- **RQ1 (primary):** specialist board vs SC@9, exact McNemar, α = 0.05, 2-point practical threshold.
- **RQ2:** specialist vs generic board. **RQ3:** does discussion change answers (round-2 vs round-1 vote; correct→wrong and wrong→correct flips)?
- Secondary tests are Holm-corrected. Non-significant results are reported with the 95% CI and the minimum detectable effect, never as "no difference".

Everything is fixed in advance in `configs/frozen_protocol.yaml` (**v1.2**). Change history is in the file header and in `research_decisions.md`.

## 2. Repository layout
This folder is the handbook's suggested `AITR_Lab02_Project/` tree, kept as `board-eval/` inside the [orchestrating-the-virtual-tumor-board](..) repository. The prompt-by-prompt Lab 7 submission package is in [`../lab7-submission/`](../lab7-submission).
```
configs/frozen_protocol.yaml     pre-registered protocol v1.2 (model, sampling, datasets, comparisons, gates)
src/vtb/                         data.py (loader, oncology filter v1.0) · parse.py (answer parser v3)
                                 backends.py (vllm / hf / mock) · methods.py (cot, sc, board) · stats.py
scripts/
  prepare_data.py                MedQA test -> all items + oncology subset + audit files
  prepare_extra_data.py          MedMCQA-dev oncology, MedQA 4-option, 20 MedQA train pilot items (needs Hugging Face)
  dataset_sanity_checks.py       model-free checks: duplicates, option counts, letter floor
  leakage_checks.py              5-gram Jaccard overlap between two item files (gate)
  env_check.py                   environment report (GPU, packages, network) as JSON
  run_experiment.py              one (dataset, method, seed) cell -> results/raw/*.jsonl, resumable
  baseline_report.py             baseline validation numbers (floor, CoT, SC curve, determinism)
  evaluate.py                    integrity + settings audit, results.csv, comparisons.csv, flip rates, figures
  make_paper_tables.py           LaTeX tables from results/ only (refuses mock outputs)
notebooks/
  01_env_sanity_smoke_kaggle.ipynb   environment, data build, leakage gate, tests, smoke test, STOP
  02_baseline_kaggle.ipynb           CoT anchor, CoT + SC on oncology sets, 20-item rerun, baseline report, STOP
  03_main_grid_kaggle.ipynb          full grid; refuses to start without results/baseline/VALIDATED
tests/                           46 unit + end-to-end tests (mock backend)
paper/                           main.tex, references.bib (23 verified entries), bib_verification.md, figures/
data/                            see data/README.md (licences, hashes, what is committed)
docs/phase1 ... phase6/          per-prompt research records (Lab 7); phase5: fresh-clone log; phase6: AI provenance report
research_decisions.md            decision log L-01 ... L-51
```

## 3. Setup

### 3.1 CPU (analysis, data preparation, tests) — [VERIFIED]
```bash
git clone https://github.com/vibhum-phd/orchestrating-the-virtual-tumor-board.git   # [TO VERIFY] after the push
cd orchestrating-the-virtual-tumor-board/board-eval  # every command below runs from this folder
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q tests                         # expected: 45 passed, 1 skipped (the skipped test needs
                                                  # data/raw/medqa_test.jsonl; after §4 it gives 46 passed)
```
Verified on Python 3.13.16 and Python 3.11.17 (incl. a fresh clone, 24 Oct 2026: `docs/phase5/reproduction_log_fresh_clone.txt`) (Kaggle's version family), CPU only. Package versions used are listed in `requirements.txt` and `docs/py311_test_log.txt`.

### 3.2 GPU (model runs) — [TEST REQUIRED]
Kaggle notebook, accelerator **GPU T4 x2**, Internet **on**.
```bash
pip install -r requirements-gpu.txt               # vllm, datasets — deliberately unpinned until tested
python scripts/env_check.py --require-gpu --json results/env/env_check_kaggle.json
pip freeze > results/env/pip_freeze.txt           # then pin exact versions in requirements-gpu.txt
```
`env_check.py` itself is [VERIFIED] on CPU (`docs/phase3/Prompt_08_*/env_check_claude_workspace_cpu.json`); without a GPU, `--require-gpu` exits 1 as intended.

No API keys are needed. Qwen2.5-7B-Instruct is downloaded from Hugging Face by vLLM at run time; **no model weights are stored in this repository**.

## 4. Data
Licences and exact provenance: `data/README.md`. No patient data; all items are published exam-style questions.

| Set | Source (licence) | n | Role | Status |
|---|---|---|---|---|
| `medqa_onc` | MedQA-USMLE 5-option test, oncology filter v1.0 (MIT) | 97 | Primary, part 1 | [VERIFIED] built |
| `medmcqa_onc` | MedMCQA dev, same filter (MIT) | unknown | Primary, part 2 | [TEST REQUIRED] needs Hugging Face |
| `medqa_all` | MedQA 5-option test (MIT) | 1,273 | Secondary (power, onc vs general) | [VERIFIED] built |
| `medqa4_all` | MedQA 4-option, HF `GBaker/MedQA-USMLE-4-options` (CC-BY-4.0) | 1,273 | CoT anchor only | [TEST REQUIRED] |
| `pilot_train` | 20 MedQA train items | 20 | Prompt debugging only, never reported | [TEST REQUIRED] |

```bash
# MedQA (raw file is not committed). Source: copy of MedQA in gersteinlab/MedAgents      [VERIFIED]
git clone --depth 1 https://github.com/gersteinlab/MedAgents.git /tmp/MedAgents
mkdir -p data/raw && cp /tmp/MedAgents/datasets/MedQA/test.jsonl data/raw/medqa_test.jsonl
sha256sum data/raw/medqa_test.jsonl
#   must be cfa75cbcc53c29b023752b0a395ff49d8202121041392735ae44771a5ec734a3
python scripts/prepare_data.py --src data/raw/medqa_test.jsonl --out data/processed       # [VERIFIED] 1273 / 97
python scripts/dataset_sanity_checks.py .        # [VERIFIED] argument = repo root; writes scripts/dataset_sanity_checks_output.json

# MedMCQA, MedQA 4-option, pilot items                                                     [TEST REQUIRED]
python scripts/prepare_extra_data.py --out data/processed

# Leakage gate: must exit 0 before any run                                                 [TEST REQUIRED on Kaggle files]
python scripts/leakage_checks.py data/processed/medqa_train_pilot.jsonl data/processed/medqa_test_onc.jsonl
python scripts/leakage_checks.py data/processed/medmcqa_dev_onc.jsonl  data/processed/medqa_test_onc.jsonl
```
The processed MedQA files (`data/processed/*.jsonl`, `manifest.json`) are committed under the MedQA MIT licence (notice in `data/`). The keyword filter is checked by hand: fill `human_label` in `data/processed/onc_subset_human_audit.csv` (1 = oncology reasoning is central, 0 = incidental).

## 5. Runs
Run the notebooks in order on Kaggle. Each one ends at a **STOP** cell; check its output before going on.

| Step | Notebook / command | Produces | Status |
|---|---|---|---|
| 1 | `notebooks/01_env_sanity_smoke_kaggle.ipynb` | env JSON, pip freeze, data, leakage JSONs, 5-item smoke test | [TEST REQUIRED] |
| 2 | `notebooks/02_baseline_kaggle.ipynb` | `results/raw/` (CoT, SC), `results/rerun/`, `results/baseline/` | [TEST REQUIRED] |
| — | **Human check:** baseline acceptance criteria B1–B8 (`docs/phase3/Prompt_10_*/baseline_validation_report.md`), then `touch results/baseline/VALIDATED` | gate file | manual |
| 3 | `notebooks/03_main_grid_kaggle.ipynb` | full grid in `results/raw/`, then evaluation | [TEST REQUIRED] |

Single cells, if you prefer the command line:
```bash
# baseline                                                                                  [TEST REQUIRED]
python scripts/run_experiment.py --dataset medqa_onc --method cot --seed 0 --backend vllm
python scripts/run_experiment.py --dataset medqa_onc --method sc  --seed 0 --backend vllm
python scripts/run_experiment.py --dataset medqa_onc --method cot --seed 0 --backend vllm --limit 20 --out results/rerun
python scripts/baseline_report.py --raw results/raw --rerun results/rerun --out results/baseline

# main grid (order used in notebook 03: primary seed 0 -> medqa_all -> seeds 1-2)          [TEST REQUIRED]
for ds in medqa_onc medmcqa_onc; do for m in cot sc board_roles board_generic; do
  python scripts/run_experiment.py --dataset $ds --method $m --seed 0 --backend vllm; done; done
for m in cot sc board_roles board_generic; do
  python scripts/run_experiment.py --dataset medqa_all --method $m --seed 0 --backend vllm; done
for s in 1 2; do for ds in medqa_onc medmcqa_onc; do for m in cot sc board_roles board_generic; do
  python scripts/run_experiment.py --dataset $ds --method $m --seed $s --backend vllm; done; done; done
```
`run_experiment.py` is resumable: it skips items already written, so a Kaggle session that times out can be restarted with the same command.

**Plumbing check without a GPU** — [VERIFIED]: add `--backend mock` (and e.g. `--limit 5`). Mock outputs are random and watermarked SYNTHETIC; never report them. Example output: `docs/phase4/Prompt_13_*/SYNTHETIC_demo_outputs_mock_backend/`.

## 6. Evaluation and figures
```bash
python scripts/evaluate.py --raw results/raw --out results                                # [VERIFIED on mock; TEST REQUIRED on real runs]
python scripts/evaluate.py --raw results/raw --out results/sensitivity_audited \
       --restrict-ids data/processed/onc_subset_human_audit.csv                            # after the human audit
python scripts/make_paper_tables.py --results results --out paper/results_tables.tex       # refuses mock data
cd paper && latexmk -pdf main.tex                                                          # [VERIFIED] with pending tables
```
`evaluate.py` stops with an error if arms cover different items, mix code versions, or used different generation settings. It writes:

| File | Content |
|---|---|
| `results/results.csv` | accuracy, 95% CI, parse-fail and truncation rate, tokens, per arm × dataset × seed |
| `results/comparisons.csv` | every pre-registered comparison: Δ, CI, McNemar p, Holm p, MDE (80% power), tokens per item, decision text |
| `results/flip_rates.csv` | round 1 → round 2 correct→wrong / wrong→correct rates with item-cluster CIs |
| `results/figures/` | efficiency frontier (accuracy vs API-equivalent tokens per question, with the SC@k curve and each board) and the round-1 → round-2 flip matrix, PNG + PDF |

The paper's tables are generated from these files only; no number is typed by hand.

## 7. Compute
- Hardware: Kaggle free tier, 2 × NVIDIA T4 (16 GB each), fp16, tensor parallel 2.
- Estimated full grid: **7–19 GPU-hours** — INFERRED from call counts, not measured. Replace with the time measured in notebook 01's smoke test.
- Calls per item: CoT 1, SC 15 (one request, n = 15), each board 9.
- CPU part (tests, data, evaluation): under 1 minute on a laptop-class CPU [VERIFIED: tests 6.2 s].

## 8. Limitations
- Exam multiple-choice questions are a proxy; they are not tumor-board decisions on real patients. No images, pathology reports, guidelines or retrieval.
- Small primary set: with n = 97 alone the test detects only differences of about 12–15 points. MedMCQA is needed to reach ~6–8 points.
- Oncology scope is keyword-defined (filter v1.0); a human audit is pending.
- Public benchmarks may be in the model's pre-training data.
- One 7B open model family. Results may not transfer to larger or proprietary models.
- Calls are matched; tokens are not (the board reads other agents' texts). Tokens are reported for every comparison, plus an exploratory comparison against SC@15.
- Pooled set mixes 5-option (MedQA) and 4-option (MedMCQA) items; results are also reported by source.

## 9. Minimum reproduction checklist (for a second student)
Tick each item and note the date. Stop at the first failure and report it.

- [ ] 1. Clone the repository; `pip install -r requirements.txt`; `python -m pytest -q tests` → **45 passed, 1 skipped** (46 passed after step 2)
- [ ] 2. Download MedQA as in §4; `sha256sum` matches `cfa75cbc…a734a3`
- [ ] 3. `prepare_data.py` → `manifest.json` shows `n_all` 1273 and `n_onc_primary_stem_or_gold` 97; `git diff data/processed` shows no change
- [ ] 4. `python scripts/dataset_sanity_checks.py .` → majority-letter floor on MedQA-onc = **0.2784** (27/97; MedQA-all 0.2176)
- [ ] 5. Mock run: the 4 methods with `--dataset medqa_onc --seed 0 --backend mock --limit 5`, then `evaluate.py --raw results/raw --out results --pool medqa_onc` completes; `make_paper_tables.py` must **refuse** these outputs (exit 1). Delete `results/` afterwards
- [ ] 6. Kaggle notebook 01 passes every cell; save `env_check_kaggle.json` and `pip_freeze.txt`
- [ ] 7. Both leakage checks exit 0
- [ ] 8. Notebook 02: CoT on MedQA-onc is above 27.8%; parse failures ≤ 3%; the 20-item greedy rerun gives identical answers
- [ ] 9. Notebook 03 + `evaluate.py`: no integrity error; your `comparisons.csv` matches the authors' within sampling noise (same seeds → expect the same answers on greedy arms; sampled arms may differ slightly across vLLM versions)
- [ ] 10. `make_paper_tables.py` + `latexmk` rebuild the paper's tables from your results

## 10. AI assistance
The code, protocol and paper draft were written with an AI assistant (Claude). Every AI-written module was tested before use; errors found and fixed are in `docs/phase3/Prompt_11_*/debugging_log.md`, and decisions with their evidence are in `research_decisions.md`. Literature claims are labelled VERIFIED / INFERRED in `paper/bib_verification.md`.

## 11. Credits and licence
- MedQA: Jin et al. 2021 (MIT). MedMCQA: Pal et al. 2022 (MIT). MedQA 4-option HF copy: CC-BY-4.0. Raw MedQA copy obtained from the gersteinlab/MedAgents repository.
- Qwen2.5-7B-Instruct: Qwen team, Apache-2.0. vLLM: Kwon et al. 2023.
- Code in this repository: MIT (`LICENSE`). Dataset licences apply to the files in `data/`.

## 12. Citation
Paper in preparation; the draft is in `paper/` (results pending).
```bibtex
@misc{sharma2026vtbboard,
  author = {Sharma, Vibhum},
  title  = {Does the Virtual Tumor Board Need a Board? A Call-Matched Evaluation of
            Specialist Multi-Agent LLM Deliberation on Oncology Exam Questions},
  year   = {2026},
  note   = {Draft, results pending. Repository: https://github.com/vibhum-phd/orchestrating-the-virtual-tumor-board, folder board-eval/ [TO VERIFY]}
}
```
