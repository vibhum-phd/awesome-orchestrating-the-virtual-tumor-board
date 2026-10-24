# PROMPT 09 | Vibe-code one baseline module at a time

**SAVE (as required by the assignment):** Working baseline plus code understanding and prompt-to-code log.

## Prompt as used

> You are my AI pair programmer. I am reproducing **[zero-shot chain-of-thought (Kojima et al. 2022) and self-consistency (Wang et al. 2023) with Qwen2.5-7B-Instruct]** for **[MedQA-USMLE oncology subset (and MedMCQA oncology subset)]** to produce **[per-item predictions (JSONL) and accuracy]**. Work in short cycles: (1) specify the module and assumptions, (2) generate minimal executable code, (3) explain the logic and input/output shapes, (4) supply a unit/sanity test, and (5) wait for my genuine execution output before continuing. Implement data loading/validation, preprocessing, baseline model or algorithm, training/processing, evaluation, saving predictions and basic plots. Prefer official reference implementations when licensing permits, and record any deliberate deviations. Do not present pseudocode as runnable code, rewrite unrelated modules, or claim successful execution without logs.

Placeholders filled: [PUBLISHED BASELINE], [DATASET], [OUTPUT].
Tool: Claude (Linux workspace, CPU only). Genuine execution in this folder = CPU unit tests with a mock model; real-model execution is [TEST REQUIRED] on Kaggle.

## Files in this folder

- `baseline_modules_and_prompt_to_code_log.md` — six cycles (spec, logic, I/O shapes, tests, genuine output), deviations, prompt-to-code log
- `test_logs/` — real pytest output for each cycle + full suite (41/41) + the baseline report run on SYNTHETIC mock outputs
- `code_snapshot/` — the code at this prompt (`vtb/` package, runner, report script, tests, `02_baseline_kaggle.ipynb`)
