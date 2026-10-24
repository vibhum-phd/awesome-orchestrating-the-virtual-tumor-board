# PROMPT 17 | Prepare reproducible GitHub documentation

**SAVE (as required by the assignment):** Public-ready research repository and reproduction instructions.

## Prompt as used
> Using my actual project files **[repository AITR_Lab02_Project at commit a398cff]**, environment **[AI workspace CPU, Python 3.13.16 / 3.11.17; target Kaggle 2×T4 — untested]**, dataset access/license **[MedQA MIT, MedMCQA MIT, MedQA 4-option CC-BY-4.0; Qwen2.5 Apache-2.0]** and commands I have genuinely executed **[CPU tests, data preparation, sanity checks, mock pipeline, LaTeX build; no GPU command]**, write a clear README with problem statement, setup, dataset preparation, baseline and experimental run commands, evaluation, reproduction of key figures, compute requirements, limitations, credits, license and citation. Mark unexecuted commands as [TEST REQUIRED] rather than pretending they work. Check that configuration files and dependency versions are included, that paths are realistic, and that no secrets, private data or restricted model weights are exposed. Add a minimum reproduction checklist for a second student.

## Files in this folder
- `README_repository.md` — the repository README (root `README.md`), every command labelled VERIFIED or [TEST REQUIRED]; 10-item reproduction checklist
- `repository_readiness_check.md` — command status table, 4 README errors found by a fresh-clone test and fixed, config/dependency check, secrets/data/weights scan, open items, decisions L-45–L-47
- `reproduction_log_fresh_clone.txt` — raw log of two fresh-clone runs (before and after the fixes)
- `requirements.txt`, `requirements-gpu.txt`, `frozen_protocol_v1.2.yaml`, `data_README.md`, `LICENSE`, `gitignore.txt` — the files the README refers to

## Status
README done and tested on CPU from a clean clone. GPU sections stay [TEST REQUIRED] until the Kaggle notebooks run. Repository URL [TO VERIFY] until pushed.
