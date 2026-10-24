# Phase III — AI coding, vibe coding and baseline validation (Prompts 08–11)

Status: **done as far as possible without a GPU; STOPPED at the points the prompts require real output.**
The AI workspace has no GPU and cannot reach Hugging Face, so no model was run. Every number from a model is
either PENDING or comes from the mock backend and is labelled SYNTHETIC.

| Prompt | Folder | SAVE item | State |
|---|---|---|---|
| 08 | `Prompt_08_Configure_and_Test_Coding_Environment/` | Environment verification log and structured repository | Test written and **run for real on CPU**; Kaggle run **[TEST REQUIRED]** — STOP |
| 09 | `Prompt_09_Vibe_Code_Baseline_Module_by_Module/` | Working baseline + code understanding + prompt-to-code log | 6 cycles, 42/42 tests pass (real logs); real-model run [TEST REQUIRED] |
| 10 | `Prompt_10_Verify_and_Reproduce_Baseline/` | Baseline validation report incl. discrepancies | Audit complete (1 defect found and fixed); measured part PENDING with pre-set acceptance criteria |
| 11 | `Prompt_11_Debug_Using_Actual_Evidence/` | Corrected code, tested fix, debugging decision | 12 real cases logged; fixes tested |

Phase-level file: `research_decisions_phase_III.md` (L-22 to L-29).

## What you need to run (in this order)
1. `notebooks/01_env_sanity_smoke_kaggle.ipynb` on Kaggle (GPU T4 x2, Internet on) → share `env_and_pilot_outputs.zip`.
2. `notebooks/02_baseline_kaggle.ipynb` → share `baseline_outputs.zip`.
Then Prompt 10 Part B is filled in, DBG-11 is fixed, and the comparison runs can start.
