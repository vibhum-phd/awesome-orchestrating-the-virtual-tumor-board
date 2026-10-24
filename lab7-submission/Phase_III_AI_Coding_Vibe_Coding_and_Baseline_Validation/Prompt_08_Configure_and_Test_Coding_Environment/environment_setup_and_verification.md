# Prompt 08 output — Environment setup and verification log

Saved: 2026-10-24 · Labels: VERIFIED / INFERRED / UNKNOWN / [TEST REQUIRED]
Prompt 08 SAVE item: "Environment verification log and structured project repository."

**Status:** the environment test exists and was **run for real in the AI's CPU workspace** (log in this folder). The target environment (Kaggle 2×T4) has **not** been tested yet. Following the prompt, work stops here until the Kaggle console output from `01_env_sanity_smoke_kaggle.ipynb` is shared.

## 1. Target environment and libraries

| Component | Proposed | How compatibility is checked (not assumed) | Status |
|---|---|---|---|
| Hardware | Kaggle GPU T4 ×2 (16 GB each), 12-h sessions | `nvidia-smi`; `env_check.py --require-gpu` needs compute capability ≥ 7.0 (vLLM docs list T4) | [TEST REQUIRED] |
| Python | Kaggle default (3.10–3.12 expected) | `env_check.py` prints it; vLLM docs require 3.9–3.12 (v0.9.0 docs, VERIFIED) | [TEST REQUIRED] |
| Inference engine | vLLM, unpinned until tested | Cell 3 installs, `env_check.py` imports it, cell 9 runs a real generation | [TEST REQUIRED] |
| Model | Qwen/Qwen2.5-7B-Instruct, fp16, tensor-parallel 2 | Cell 9 loads it and generates; fallback 3B in protocol | [TEST REQUIRED] |
| Data libs | `datasets` (Hugging Face) | Cell 6 builds MedMCQA and the 4-option anchor | [TEST REQUIRED] |
| Analysis libs | numpy ≥ 1.26, pandas ≥ 2.1, scipy ≥ 1.11, matplotlib ≥ 3.8, PyYAML ≥ 6.0, pytest ≥ 7.4 | Tested here with numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, matplotlib 3.11.2, PyYAML 6.0.3, pytest 9.1.1 on Python 3.13.16 | VERIFIED (CPU) |
| Local GTX 1050 Ti (4 GB) | Not used for 7B inference | Cannot hold a 7B fp16 model; fine for the CPU test suite | — |

Version pinning rule: `requirements-gpu.txt` stays unpinned until cells 5–9 pass on Kaggle; then the exact versions from `results/env/pip_freeze.txt` are written into it and committed.

## 2. Installation commands (Kaggle)
```bash
pip install -r requirements.txt          # analysis + tests
pip install datasets vllm                 # GPU inference [TEST REQUIRED]
pip freeze > results/env/pip_freeze.txt   # record what actually installed
```

## 3. GPU / system diagnostics
`nvidia-smi` (raw) and `python scripts/env_check.py --require-gpu --json results/env/env_check_kaggle.json`.
**Expected output type:** a JSON object with `python, platform, cpu_count, ram_gb, disk_free_gb, packages{}, cuda{available, devices[], capabilities[]}, vllm_import, data{medqa_sha256_ok, n_all, n_onc}, seed_check, network{}, problems[]`. Exit code 0 = no blocking problem.

## 4. Dataset access procedure
1. MedQA test: `git clone gersteinlab/MedAgents` → copy `datasets/MedQA/test.jsonl` → `prepare_data.py`; the sha256 must equal `cfa75cbc…a3`.
2. MedMCQA dev, MedQA 4-option, pilot train items: `prepare_extra_data.py` (needs Hugging Face; prints split sizes, `cop` base and oncology n).
3. Gate: `leakage_checks.py` must exit 0 for pilot-vs-test and MedMCQA-onc-vs-MedQA-onc.

## 5. Random-seed controls
- Every call's seed = SHA-256(run seed | item_id | arm/round/role) → `SamplingParams(seed=…)` (vLLM) or `torch.manual_seed` (HF backend).
- Greedy calls (CoT, chair) use temperature 0.
- Bootstrap uses `numpy.random.default_rng(20261020)`.
- `env_check.py` confirms numpy RNG repeatability; a 20-item rerun checks vLLM determinism in Prompt 10.

## 6. Repository structure (tracked files, VERIFIED with `git ls-files`)
```
README.md  LICENSE  .gitignore  requirements.txt  requirements-gpu.txt
research_decisions.md  baseline_validation.md  ai_assistance_log.md
configs/frozen_protocol.yaml                     protocol v1.1
data/README.md  data/NOTICE_*_LICENSE.txt        data access + licences (raw data not committed)
data/processed/{manifest.json, onc_filter_audit.csv, onc_subset_human_audit.csv, *.jsonl}
notebooks/01_env_sanity_smoke_kaggle.ipynb       this prompt's Kaggle notebook
scripts/{prepare_data, prepare_extra_data, leakage_checks, dataset_sanity_checks, env_check,
         run_experiment, evaluate}.py
src/vtb/{data, parse, backends, methods, stats}.py
tests/test_core.py
results/  paper/  docs/
```

## 7. The environment test and its real output here
`environment_test_log_claude_workspace_cpu.txt` and `env_check_claude_workspace_cpu.json` (VERIFIED, run 24 Oct 2026):
- Python 3.13.16, 2 CPUs, about 7 GB RAM, no torch, no vLLM, no GPU.
- MedQA hash **matches**; 1,273 items, 97 oncology items.
- numpy seeds repeat.
- GitHub reachable; **Hugging Face not reachable**.
- `--require-gpu` exits 1, which is the correct answer for this machine.
- 29/29 unit tests pass.

This proves the test itself works. It says nothing about Kaggle.

## 8. Failure diagnostics

| Symptom | Likely cause | What to do |
|---|---|---|
| `cuda.available: false` on Kaggle | Accelerator not set to GPU | Settings → Accelerator → GPU T4 x2, restart |
| `vllm_import: failed …` after install | vLLM wheel built for a different torch/CUDA | Check `pip_freeze.txt`; try a vLLM version matching Kaggle's torch, or use the HF fallback (3b) |
| `medqa_sha256_ok: false` | Different MedQA copy | Stop; do not continue with a different file |
| Hugging Face errors in cell 6 | Internet off, or rate limit | Enable Internet; retry; if MedMCQA still fails apply the protocol fallback (MedQA-onc only) |
| Leakage gate exit 1 | Overlapping items | Drop flagged pilot items or keep one copy; log a decision |
| CUDA out of memory loading 7B | Both GPUs not used, or other processes | Confirm `tensor_parallel_size: 2`; otherwise the AWQ / 3B fallback (logged protocol change) |
| Many `parsed: None` in cell 9 | Output format differs from the parser rule | Inspect the texts; fix on train items only (Prompt 11) |

## 9. STOP — what to share next
Run `notebooks/01_env_sanity_smoke_kaggle.ipynb` on Kaggle and share `env_and_pilot_outputs.zip` (or the printed output of cells 2, 3, 5, 6, 7 and 9). Nothing after this prompt is run on real model output until then.

## 10. Decision-log entries (Prompt 08)

| ID | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|
| L-22 | 2026-10-24 | Add `scripts/env_check.py` and gate the Kaggle notebook on it | Prompt 08 needs a real, repeatable environment test | Ran here (VERIFIED) | Run on Kaggle |
| L-23 | 2026-10-24 | Keep `requirements-gpu.txt` unpinned until Kaggle passes | vLLM/torch/CUDA compatibility untested | — | Pin from `pip_freeze.txt` |
| L-24 | 2026-10-24 | Fix `env_check.reachable()`: HTTP error = host reachable | First run reported GitHub unreachable because of an HTTP 400 to HEAD | Diagnosed with a direct urllib call (VERIFIED) | Logged in Prompt 11 |
