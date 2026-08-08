Run the AI evaluation suite and report quality scores.

1. Run `uv run deepeval test run tests/test_eval.py -v`
2. Run `grep -rn "deepeval" .github/workflows/` to confirm the gate is actually wired.
   An eval suite with no CI job is an assertion, not a gate — report that as blocking.
3. Report every metric the suite emits as score vs threshold, grouped by family
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

4. For any metric below threshold, flag it with the specific failing test case and its score
5. Report the judge model used. For finance/proprietary suites (AFC, Crucible) the judge must be
   local Ollama ($0, private) — flag if a cloud judge ran on sensitive data
6. Report the labeled-set size; flag it if under 30 cases or missing adversarial / PII-probing inputs
7. Active portfolio is DataVault, PolicyPulse, Crucible (leads) plus FormSense and AFC
   (supporting). ODI and StreamSmart are backlog — note them as outside the active set,
   not as portfolio gates
8. On any Crucible run, state explicitly: eval scores never authorize a live trade. The live
   execution path is gated by mandatory human sign-off plus a kill-switch, independent of any metric
9. Summarize: PASS (all metrics meet thresholds) or FAIL (list failing metrics)
10. Do NOT modify any files — report only