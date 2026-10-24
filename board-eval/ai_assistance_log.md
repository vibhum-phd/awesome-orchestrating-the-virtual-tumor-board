# AI-assistance and verification log

Tool: Claude (Opus 5.5), claude.ai, with web search and a sandboxed Linux workspace (no GPU; Hugging Face blocked; GitHub reachable).
Only real events are recorded. Add your own entries (Kaggle runs, ChatGPT/Copilot use, manual fixes) in the same format.

| # | Date | Task | AI proposal | Human decision | Verification | Outcome |
|---|---|---|---|---|---|---|
| 1 | 2026-10-20 | Find gap | Proposed "multi-agent board vs call-matched single model" from memory of the field | Accepted only after checking it against *my* review and EvoMDT | Extracted text of my lit review PDF (Sec. 6–7) and EvoMDT PDF; searched EvoMDT text for baselines | Gap grounded in the review's own 4th gap; EvoMDT baselines confirmed single-pass (text-search level; I still need to read the figure) |
| 2 | 2026-10-20 | Verify related work | Cited MedAgents, MDAgents, Wang et al. 2024, Smit et al. 2023 | Keep, but cite only abstract-level claims until full texts are read | Web search to ACL Anthology / NeurIPS proceedings pages | Venues and code links VERIFIED; specific numbers not yet used |
| 3 | 2026-10-20 | Get data | Planned to load MedQA from Hugging Face | — | `curl` to huggingface.co returned proxy 403 | **AI limitation/environment failure.** Switched to the MedAgents GitHub copy; recorded sha256 so Kaggle copy can be checked |
| 4 | 2026-10-20 | Oncology filter | First keyword rule (v0.9) selected 121 items | Rejected v0.9 after reading every match | Printed match context for all 121 items | ~20 false inclusions (relatives' cancer, "neuroleptic malignant", TNF). v1.0 → 97 items. **Manual correction of AI-written code.** Human audit of 97 still pending |
| 5 | 2026-10-20 | Answer parser | First regex version | — | Unit test `Answer: A patient with…` | **Bug in AI-written code caught by test**: parsed as "A". Fixed; cost documented (D-08) |
| 6 | 2026-10-20 | Baseline anchor | Fetched arXiv 2501.06458; a summariser model reported 56.79% for "Qwen2.5 7B" on MedQA | Treat as INFERRED only | Not checked by a human yet | **Must open Table 1 personally** (Instruct vs base, 4 vs 5 options unstated) |
| 7 | 2026-10-20 | Figures | Generated evaluation plots | Added a "SYNTHETIC — MOCK" watermark to any figure made from the mock backend | Rendered and inspected PNGs | Prevents mock plots being mistaken for results |

| 8 | 2026-10-22 | Gap matrix from my review | Ranked 5 gaps; chose G4 | Scope set by me (P01–02 only); gap choice accepted, still to be reviewed | Review text searched | 5 errors found in my own Lab 4 review (Prompt 02) |
| 9 | 2026-10-23 | Novelty check | Narrowed claim after Kim et al. 2025 | Accepted; to be reviewed | Kim et al. full PDF | L-08. Kuerbanjiang et al. 2025 missed here, found on 24 Oct (Prompt 16) |
| 10 | 2026-10-24 | Parser v2 → v3 | v2 rejected "Answer: C. Tell…" | — | 5 new tests | **AI code bug caught by test** (DBG-09) |
| 11 | 2026-10-24 | env_check | HTTP 400 counted as unreachable | — | Contradicted by working git clone | **AI logic error** fixed (DBG-08) |
| 12 | 2026-10-24 | Truncation | Not recorded | — | Code review | `finish_reason` added (DBG-10) |
| 13 | 2026-10-24 | evaluate.py vs protocol | Still used v1.0 pairs | — | Code-vs-spec audit | Pairs now read from YAML (DBG-11) |
| 14 | 2026-10-24 | References | vLLM "29th"/"ACM" typed from memory; MedAgentsBench author "Tang" | — | Opened each source | **AI memory errors corrected** (`paper/bib_verification.md`) |
| 15 | 2026-10-24 | Paper self-review | 5 major / 8 minor concerns | Title left to me | One literature search (full text read) | Protocol v1.2 before any run; v0.2 |
| 16 | 2026-10-24 | README | Wrote run instructions | — | Two fresh-clone runs | 2 README errors fixed (R1, R2) |
| 17 | 2026-10-24 | Tool-use preference | Used web search/fetch while drafting the paper without asking | — | Audit | **Deviation disclosed** (Prompt 18) |

Full audit: `docs/phase6/Prompt_18_Audit_the_Human_AI_Collaboration/ai_provenance_and_integrity_report.md`.

## Open risks
- vLLM on Kaggle T4 not yet tested (UNKNOWN).
- Compute estimate is INFERRED from token assumptions, not measured.
- Model licence (Apache-2.0): checked on the model card (VERIFIED, protocol comment).
- 0/97 oncology items human-labelled; three tables (MDAgents T2, MedAgentsBench, arXiv 2501.06458 T1) still to be read by me.
