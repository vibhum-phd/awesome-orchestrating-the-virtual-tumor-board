# Bibliography verification (paper/references.bib)

Every entry was opened at its source by the AI during this project (23–24 Oct 2026). Nothing comes from memory alone. "Claim used" = what the paper cites it for.

| Key | Source opened | Metadata checked | Claim used in the paper | Claim support |
|---|---|---|---|---|
| liu2025evomdt | Full PDF (project file) | Authors, journal, DOI, year as the article's own "Cite this article as" line (2025) | MedQA 0.86 vs 0.76/0.79; DeepSeek V3/R1 backbone | VERIFIED in PDF text |
| kim2025mlhc | Full PDF (PMLR) + mlanthology | Authors, PMLR 298, pages 1–31 | Roles help Group Chat, not Majority Vote; 31 private cases; LLM judge; unequal calls | VERIFIED in PDF text |
| kim2024mdagents | mlanthology + NeurIPS abstract page | Authors, DOI | Adaptive solo/group structure; includes a self-consistency baseline | Abstract VERIFIED; table numbers not used in the paper |
| tang2024medagents | ACL Anthology page | Authors, pages 599–621, DOI | Five-stage role-playing discussion | Abstract VERIFIED |
| shao2025medagentsbench | arXiv abstract page (current version) | Authors (first author **Shao**, not Tang), current title | Agent frameworks do not consistently beat strong reasoning models; overhead | AI summary of the HTML version (INFERRED) — read before submission |
| han2025consensus | arXiv abstract | Authors, ID | Consensus matrix with RL | Abstract VERIFIED |
| wang2024rethinking | ACL Anthology | Authors, pages, DOI | Strong single agent ≈ discussion | Abstract VERIFIED |
| smit2023mad | arXiv abstract v3 | Authors, title of v3 | Debate does not reliably beat self-consistency | Abstract VERIFIED (v3 wording) |
| wunderlich2026pareto | ACL Anthology (2026.acl-srw.1) | Authors, pages 1–14 | Small gains of debate over SC at equal compute (MMLU-Pro, BBH) | Abstract VERIFIED |
| wang2023selfconsistency | arXiv PDF | Authors, ICLR 2023 line | Majority vote over sampled paths; settings | VERIFIED in PDF text |
| wei2022cot | mlanthology / NeurIPS | Authors | Chain-of-thought prompting | Title-level |
| kojima2022zeroshot | NeurIPS proceedings page | Authors | Zero-shot CoT trigger | Abstract VERIFIED |
| zheng2024personas | ACL Anthology | Authors, pages, DOI | Personas do not improve performance | Title/abstract VERIFIED |
| jin2021medqa | dspace.mit.edu record | Authors, journal, vol/issue, article 6421, DOI | Dataset | — |
| pal2022medmcqa | PMLR v174 page | Authors, pages 248–260 | Dataset | — |
| qwen2025qwen25 | arXiv abstract | Author line, ID | Model | — |
| kwon2023vllm | arXiv abstract (comment "SOSP 2023") | Authors | Serving engine | — |
| mcnemar1947 | Springer DOI + RePEc | Vol 12(2), pp. 153–157, DOI | Test | — |
| holm1979 | Wikipedia citation (JSTOR 4615733) | Vol 6(2), pp. 65–70 | Correction | — |
| park2024fidelity | Full PDF (project file) | Journal, vol, pages, DOI | 86.96% concordance, 322 patients | VERIFIED in PDF text |
| kuerbanjiang2025mdat | medRxiv full text (added in v0.2) | Title, 5 authors, DOI | Agent team beat baselines incl. universal self-consistency and debate; no matched call/token budgets reported | VERIFIED in full text |
| wu2026comma | arXiv abstract (added in v0.2) | Title, 12 authors, ID | Contribution-aware aggregation over partitioned data | Abstract VERIFIED |
| vasilev2025mtbbench | arXiv abstract (added in v0.2) | Title, 8 authors, "Accepted to NeurIPS 2025" | Multimodal longitudinal MTB benchmark | Abstract VERIFIED; NeurIPS track name not confirmed |

## Corrections found while verifying (vs earlier Lab 7 files)
- MedAgentsBench was called "Tang et al. 2025" in Prompt 04/05 files; the first author is **Yanjun Shao**, and the arXiv record now shows a new title.
- EvoMDT is "2026" in the Lab 4 review, but the article's own citation line says **2025** (copyright line 2026).
- An earlier draft of the vLLM entry said "29th Symposium" and then "ACM Symposium" from memory; both were removed because the source only says "SOSP 2023".
