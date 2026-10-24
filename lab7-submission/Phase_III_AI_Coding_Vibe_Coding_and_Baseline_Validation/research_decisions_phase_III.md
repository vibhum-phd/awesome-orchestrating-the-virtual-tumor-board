# Research decisions log — Phase III (Prompts 08–11)

Continues L-01 to L-21. Labels: VERIFIED / INFERRED / UNKNOWN.

| ID | Prompt | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|---|
| L-22 | 08 | 2026-10-24 | Add `scripts/env_check.py`; gate the Kaggle notebook on it | Prompt 08 needs a real, repeatable environment test | Ran in AI workspace (VERIFIED) | Run on Kaggle |
| L-23 | 08 | 2026-10-24 | Keep `requirements-gpu.txt` unpinned until Kaggle passes | vLLM/torch/CUDA compatibility untested | — | Pin from `pip_freeze.txt` |
| L-24 | 08 | 2026-10-24 | HTTP error status = host reachable in `env_check` | False "GitHub unreachable" (DBG-08) | Direct urllib check (VERIFIED) | — |
| L-25 | 10 | 2026-10-24 | Record `finish_reason`; report truncation | Truncation invisible, could differ by arm (DBG-10) | Code audit; new test | Check B4 on real run |
| L-26 | 10 | 2026-10-24 | Acceptance criteria B1–B8 fixed before any baseline output | Avoid post-hoc judgement | `baseline_validation_report.md` | Fill from `baseline_outputs.zip` |
| L-27 | 10 | 2026-10-24 | No comparison/board run until baseline Part B is complete | Validate before extending | — | Wait for Kaggle output |
| L-28 | 11 | 2026-10-24 | Adopt parser v3 before any real output | v2 rejected common formats (DBG-09) | `parse_v2_vs_v3.txt` | Pilot parse-fail rate |
| L-29 | 11 | 2026-10-24 | Keep DBG-11 open; block comparisons until `evaluate.py` matches protocol v1.1 | Protocol/code mismatch | Code read | Fix in Prompt 13 |
