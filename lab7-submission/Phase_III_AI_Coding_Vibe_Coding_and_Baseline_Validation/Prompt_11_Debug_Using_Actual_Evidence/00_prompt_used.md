# PROMPT 11 | Debug using actual evidence

**SAVE (as required by the assignment):** Corrected code, tested fix and documented debugging decision.

## Prompt as used (applied once per real failure; the log covers 12 cases)

> My code failed or behaved unexpectedly. Relevant code: **[file/function per case]**. Actual traceback or observed output: **[quoted per case, e.g. `AssertionError: assert 'A' == None`; `HTTPError HTTP Error 400: Bad Request`; v2 parser returning None for "Answer: C. Tell the attending…"]**. Expected behavior: **[per case]**. Determine the likely causes, separate confirmed evidence from hypotheses, and suggest the smallest safe correction with an explanation of each change. Provide a verification test and one relevant edge case; state whether earlier results may need to be rerun. Ask for more diagnostic information when needed. Do not claim to have run the code or generate imagined logs. Help me add this case to my AI-assistance/debugging log.

Placeholders filled: [CODE], [ACTUAL OUTPUT], [EXPECTED BEHAVIOR] — once per case.

## Files in this folder

- `debugging_log.md` — 12 real cases (summary table + detailed entries for the 5 that changed code), decisions L-28–L-29
- `parse_v2_vs_v3.txt` — actual output showing the parser v2 failure and the v3 behaviour
- `corrected_code/` — fixed `parse.py`, `backends.py`, `env_check.py` and the diff of the DBG-09 and DBG-10 fixes (env_check.py with the DBG-08 fix is a new file)
