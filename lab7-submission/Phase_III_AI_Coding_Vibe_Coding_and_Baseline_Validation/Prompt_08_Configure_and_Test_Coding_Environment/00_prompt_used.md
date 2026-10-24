# PROMPT 08 | Configure and test the coding environment

**SAVE (as required by the assignment):** Environment verification log and structured project repository.

## Prompt as used

> Act as my research software engineer. Set up **[KAGGLE GPU (2×T4); local CPU for tests]** for **[zero-shot LLM inference with Qwen2.5-7B-Instruct: greedy CoT, self-consistency, and a 4-agent tumor-board pipeline]** using **[vLLM, Hugging Face datasets, numpy, pandas, scipy, matplotlib, PyYAML, pytest]**. Propose dependency versions and show how to check their compatibility instead of claiming untested compatibility. Provide installation commands, GPU/system diagnostics, dataset access procedures, project directories, random-seed controls and a clean repository structure (README, src, notebooks, configs, scripts, results, paper, requirements). Write a small executable environment test, state its expected output type and list failure diagnostics. Stop after this test and ask me to share the actual console output before proceeding.

Placeholders filled: [GOOGLE COLAB/LOCAL/INSTITUTIONAL GPU], [METHOD], [LIBRARIES].
Tool: Claude (Linux workspace, CPU only, no Hugging Face access).

## Files in this folder

- `environment_setup_and_verification.md` — versions + compatibility checks, install commands, diagnostics, data access, seed controls, repo structure, failure-diagnostics table, STOP point
- `env_check.py` — the executable environment test
- `environment_test_log_claude_workspace_cpu.txt`, `env_check_claude_workspace_cpu.json` — **real output** of the test in the AI's CPU workspace (not the GPU target)
- `01_env_sanity_smoke_kaggle.ipynb` — the Kaggle notebook to run next (stops after the smoke test)
- `requirements.txt`, `requirements-gpu.txt` — dependencies (GPU file unpinned until tested)

## Status
STOPPED as the prompt requires: waiting for the Kaggle console output.
