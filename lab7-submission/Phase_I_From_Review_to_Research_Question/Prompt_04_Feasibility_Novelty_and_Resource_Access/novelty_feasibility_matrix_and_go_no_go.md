# Prompt 04 output — Novelty/feasibility matrix and go/no-go decision

Saved: 2026-10-23 · Tool: Claude · Labels: VERIFIED / INFERRED / UNKNOWN
Prompt 04 SAVE item: "Novelty/feasibility matrix and go/no-go decision."

## Prompt as used
> My candidate study is **[a controlled comparison of a 4-specialist LLM tumor board against call-matched self-consistency, same open backbone (Qwen2.5-7B-Instruct), on oncology items from MedQA, with a generic-agent ablation]**. Develop a feasibility and novelty-verification plan. Provide scholarly search strings and specific categories of neighboring work to inspect, without inventing titles, DOIs or URLs. Create a matrix with columns: published method, VERIFIED contribution (with source), limitation, proposed difference and evidence still missing. Check whether the dataset, code, model weights, license and benchmark protocol are accessible; flag all unresolved availability claims. Estimate computational and time constraints for **[Kaggle 2×T4 free tier; Colab T4; GTX 1050 Ti 4 GB]** and **[4 weeks]**. Narrow the study to a viable experimental question and recommend a fallback if the preferred repository, weights or dataset are unavailable.

## A. Search strings and neighbouring work (searches actually run 20–23 Oct 2026)

| # | Search string | Category | Relevant hit |
|---|---|---|---|
| S1 | ("multi-agent" OR "agent teams") AND ("tumor board" OR "multidisciplinary team") AND (LLM OR "large language model") | Oncology MDT simulations | Kim et al. 2025 (MLHC); Kuerbanjiang et al. 2025; Zhang et al. 2025 (GI oncology); CoMMa 2026 |
| S2 | "multi-agent debate" AND ("self-consistency" OR "majority voting") AND ("compute" OR "budget" OR "cost") | Compute-matched test-time scaling | Wunderlich et al. 2026 (ACL SRW); Smit et al. 2023 |
| S3 | "multi-agent" AND medical AND (MedQA OR benchmark) AND (CoT-SC OR baseline) | Medical multi-agent frameworks | MDAgents 2024; MedAgents 2024; MedAgentsBench 2025 |
| S4 | (persona OR "role prompting" OR "role specialization") AND LLM AND (ablation OR "does not improve") | Role/persona effects | Zheng et al. 2024 (EMNLP Findings) |
| S5 | "Are multi-agent discussions the key" / "single agent" strong prompt | Single agent vs discussion | Wang et al. 2024 (ACL) |
| S6 | "consensus matrix" oncology MDT | Consensus aggregation | Han et al. 2025 (arXiv) |

Not yet searched: conformity / error propagation in LLM discussions; other studies' oncology subsets of MedQA; "cited by" for Kim et al. 2025.

## B. Novelty matrix

The broad question "is multi-agent better than self-consistency" is already studied, with mixed answers, and Kim et al. 2025 already ran an oncology role ablation. The defensible difference: strict call matching, public data with an objective metric, an open 7B model, spontaneous error propagation.

| Published method | Contribution (source, label) | Limitation | My proposed difference | Evidence still missing |
|---|---|---|---|---|
| EvoMDT, Liu et al. 2026 | MedQA 0.86 vs Llama3-70B 0.76, Claude-3 0.79; backbone DeepSeek V3/R1 (PDF, VERIFIED) | Baselines use other models, single pass; code link unreachable | Same backbone for every arm; equal call budget | Fig. 2 not checked for a DeepSeek-only baseline |
| Kim et al. 2025, MLHC (head & neck MDT) | Generic roles hurt Group Chat (win 25.8% vs 53.5%, p<0.001) but not Majority Vote (ns); adding discussion to voting helps; GPT-4o + Gemma-27B, MedGemma-27B, o4-mini (PDF text, VERIFIED) | 31 private single-centre cases; LLM-as-judge pairwise wins; call counts differ; code has no licence | Public oncology MCQs, exact accuracy; call-matched; 7B open model; correct→wrong flips without injected errors | Whether their discussion gain survives call matching |
| MDAgents, Kim et al. 2024, NeurIPS | CoT-SC baseline on the same GPT-4 backbone: MedQA CoT-SC 83.9, MedAgents 79.1, MDAgents 88.7; API calls reported for 3 configs only (AI summary of PDF, INFERRED) | Closed model; calls not matched; no oncology subset | Oncology; matched calls; open model | My own reading of Table 2 |
| MedAgentsBench, Shao et al. 2025 (corrected 24 Oct 2026: first author is Shao, not Tang) | MedAgents and MDAgents average below CoT-SC on HARD subset with GPT-4o; no matched-cost comparison (AI summary, INFERRED) | No oncology focus; GPT-4o only for agent methods | Matched calls; oncology | My own reading |
| Wang et al. 2024, ACL | Strong single-agent prompt ≈ best discussion; discussion wins only without demonstrations (abstract, VERIFIED) | General reasoning, no medical roles | Oncology roles; zero-shot | — |
| Smit et al. 2023 | Debate does not reliably beat self-consistency (abstract v3, VERIFIED) | Closed models | Open 7B; oncology | — |
| Zheng et al. 2024, EMNLP Findings | Personas in system prompts do not improve performance (title, VERIFIED) | Not multi-agent | Roles inside a board | Full-text check |
| Han et al. 2025, arXiv | 87.5% vs 83.8% for an unnamed strongest baseline (abstract, VERIFIED) | Baseline/LLMs unnamed; no code | — (not reproducible) | Full text |

**Claim I can defend:** an independent, call-matched, public-benchmark replication of the specialist-board idea with a small open model — a course-level contribution, not a new method.

## C. Access and licence matrix

| Resource | Source | Licence | Access status |
|---|---|---|---|
| MedQA test, 5 options (1,273) | Jin et al. 2021, github.com/jind11/MedQA | MIT (VERIFIED) | Downloaded via MedAgents GitHub copy; sha256 recorded; 97 oncology items built (VERIFIED) |
| MedMCQA dev | Pal et al. 2022, github.com/medmcqa/medmcqa; HF openlifescienceai/medmcqa | MIT (VERIFIED) | HF blocked from AI workspace; download untested (UNKNOWN) |
| Qwen2.5-7B-Instruct | huggingface.co/Qwen/Qwen2.5-7B-Instruct | Apache-2.0 (model card, VERIFIED) | Kaggle download untested (UNKNOWN) |
| vLLM | docs.vllm.ai | Open source | T4 supported, compute capability ≥ 7.0 (docs v0.9.0, VERIFIED); Kaggle install untested (UNKNOWN) |
| Baseline code | Own implementation | MIT | Unit tests pass with mock model (VERIFIED); no real run yet |
| Reference code | MedAgents, MDAgents, Kim et al. 2025 | **No licence file** (VERIFIED) | Read and cite only |
| EvoMDT code | Link in paper | — | Could not be opened (UNKNOWN) |
| Benchmark protocol | Exact-match MCQ accuracy (as in MedAgents, MDAgents) | — | Standard; no private test server |

## D. Compute, narrowed question, fallbacks

| Run | Items × seeds | Calls/item | Generated tokens (~250/call) | GPU-hours, 2×T4 |
|---|---|---|---|---|
| Minimum: MedQA oncology | 97 × 3 = 291 | 34 (CoT 1 + SC 15 + board 9 + generic 9) | ~2.5 M | ~1–3 |
| + MedMCQA oncology | n unknown × 3 | 34 | unknown | scales with n |
| + full MedQA (power set) | 1,273 × 1 | 34 | ~10.8 M | ~4–12 |

Assumptions (INFERRED): 250 output tokens/call (cap 512); 500–1,500 generated tokens/s for 7B fp16 batched on 2×T4; prompt processing up to 2×. Kaggle sessions 12 h; weekly quota unpublished, commonly ~30 h (INFERRED). GTX 1050 Ti (4 GB) cannot hold 7B fp16 → CPU tests only.

**Narrowed RQ:** with Qwen2.5-7B-Instruct fixed, on MedQA oncology items, does a 4-specialist tumor board (9 calls) beat self-consistency with 9 samples? Secondary: does replacing specialists with generic agents change board accuracy; how often does round-2 discussion turn a correct member wrong?

| If this fails | Fallback |
|---|---|
| vLLM fails on Kaggle T4 | HF transformers on one T4; MedQA oncology, 1 seed |
| 7B too slow / OOM | Qwen2.5-3B-Instruct (logged protocol change) |
| MedMCQA unavailable | MedQA oncology + full MedQA as power set |
| GPU quota runs out | Drop full MedQA, then seeds 3 → 1 |
| Accuracy near chance (20%) | Debug prompt/parser on MedQA **train** items only |

## Go/no-go decision

**GO, conditionally**, for study B with the narrowed claim. Modest novelty: extends Kim et al. 2025 and MDAgents.

| Condition | Kills or changes the plan if… |
|---|---|
| Kaggle smoke test (5 pilot items) runs end to end | vLLM and HF fallback both fail → 3B model |
| Parse failures ≤ 3% per method on pilot items | Higher → fix prompt on train items first |
| CoT accuracy on MedQA oncology clearly above 20% | Near chance → no-go for 7B; reassess |
| I confirm (Kim 2025, MDAgents Table 2) no call-matched oncology comparison exists | One exists → reframe as pure replication (pathway A) |
| Measured GPU-hours fit quota | Over budget → fallbacks in order above |
