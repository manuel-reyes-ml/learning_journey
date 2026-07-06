Run the AI evaluation suite and report quality scores.

1. Run `deepeval test run tests/test_eval.py -v`
2. Report every metric the suite emits as score vs threshold, grouped by family
   (metrics are defined in `tests/test_eval.py` — report the families this project uses):

   RAG / generation (all AI projects):
   - Answer Relevancy (target: > 0.8)
   - Faithfulness (target: > 0.85, or > 0.9 for AFC / Crucible)
   - Hallucination (target: < 0.15, or < 0.10 for AFC / Crucible)

   Agentic (AFC, Crucible — suite must supply `tools_called` / `expected_tools` at agent level):
   - Tool Correctness (target: = 1.0 — deterministic; every expected tool called, right selection + args)
   - Task Completion (target: > 0.8 — LLM-judged; agent resolved the multi-step goal)

   Custom criteria — GEval (FormSense schema adherence, domain rules):
   - `GEval:<criterion>` (target: >= 0.85, or the project's stated threshold)

3. For any metric below threshold, flag it with the specific failing test case and its score
4. Report the judge model used. For finance/proprietary suites (AFC, Crucible) the judge must be
   local Ollama ($0, private) — flag if a cloud judge ran on sensitive data
5. Summarize: PASS (all metrics meet thresholds) or FAIL (list failing metrics)
6. Do NOT modify any files — report only