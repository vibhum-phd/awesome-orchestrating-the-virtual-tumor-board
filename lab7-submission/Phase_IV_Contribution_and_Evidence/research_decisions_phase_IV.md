# Research decisions log — Phase IV (Prompts 12–14)

Continues L-01 to L-29. Labels: VERIFIED / INFERRED / UNKNOWN.

| ID | Prompt | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|---|
| L-30 | 13 | 2026-10-24 | Read comparison pairs from the protocol; Holm only in the secondary family | Code/protocol mismatch (DBG-11) | `test_protocol_pairs_parsed_from_yaml` | DBG-11 closed |
| L-31 | 13 | 2026-10-24 | Report exact 80%-power MDE with every non-significant result | Null-reporting rule (L-14) | Exact power vs simulation (VERIFIED) | — |
| L-32 | 13 | 2026-10-24 | Refuse evaluation if arms cover different items or used different settings | Paired design; fair comparators | `test_unpaired_arms_fail_integrity` | — |
| L-33 | 13 | 2026-10-24 | Flip-rate CIs by item-cluster bootstrap | Members within an item are not independent | `test_cluster_bootstrap_rate` | — |
| L-34 | 12 | 2026-10-24 | Provisionally choose pathway B; re-confirm after baseline Part B | Code exists and is tested; call-matched; free ablations | Prompt 12 §2 | Re-confirm after `baseline_outputs.zip` |
| L-35 | 12 | 2026-10-24 | Pathway C (adaptive discussion) not run in this study | Not pre-registered; needs its own control | Prompt 12 §2 | Future work |
| L-36 | 12 | 2026-10-24 | Notebook 03 gated on baseline sign-off and leakage gate | Validate before comparing | Notebook gate cell | — |
| L-37 | 14 | 2026-10-24 | Pre-register the interpretation table before any result | Prevent post-hoc framing | Prompt 14 file (committed) | Apply to real files |
| L-38 | 14 | 2026-10-24 | Check eight alternative explanations before accepting a difference | Parse, truncation, letter bias, chair copying, source mix, seed noise, contamination, tokens | Prompt 14 §2 | Run on real files |
