# PROMPT 04 | Check feasibility, novelty and resource access

**SAVE (as required by the assignment):** Novelty/feasibility matrix and go/no-go decision.

## Prompt as used

> My candidate study is **[a controlled comparison of a 4-specialist LLM tumor board against call-matched self-consistency, same open backbone (Qwen2.5-7B-Instruct), on oncology items from MedQA, with a generic-agent ablation]**. Develop a feasibility and novelty-verification plan. Provide scholarly search strings and specific categories of neighboring work to inspect, without inventing titles, DOIs or URLs. Create a matrix with columns: published method, VERIFIED contribution (with source), limitation, proposed difference and evidence still missing. Check whether the dataset, code, model weights, license and benchmark protocol are accessible; flag all unresolved availability claims. Estimate computational and time constraints for **[Kaggle 2×T4 free tier; Colab T4; GTX 1050 Ti 4 GB]** and **[4 weeks]**. Narrow the study to a viable experimental question and recommend a fallback if the preferred repository, weights or dataset are unavailable.

Placeholders filled: [IDEA], [HARDWARE], [WEEKS].
Tool: Claude (claude.ai project workspace, web search, Linux workspace without GPU).

## Files in this folder

- novelty_feasibility_matrix_and_go_no_go.md — search strings, novelty matrix, access/licence matrix, compute estimate, fallbacks, go/no-go
