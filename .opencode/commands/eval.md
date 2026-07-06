---
description: Run the AI evaluation suite and report scores vs thresholds (RAG + agentic + GEval)
agent: eval-guardian
---

Run the AI evaluation suite and report quality scores.

!`deepeval test run tests/test_eval.py -v`

Report every metric the suite emits as `score vs threshold` with PASS/FAIL, grouped by family.
Metrics are defined in `tests/test_eval.py` — report the families this project actually uses.

**RAG / generation (all AI projects):**
- Answer Relevancy    target > 0.80
- Faithfulness        target > 0.85   (> 0.90 for AFC / Crucible — finance sensitivity)
- Hallucination       target < 0.15   (< 0.10 for AFC / Crucible)

**Agentic (AFC, Crucible — suite must supply `tools_called` / `expected_tools` at agent level):**
- Tool Correctness    target = 1.00   deterministic — every expected tool called, right selection + args
- Task Completion     target > 0.80   LLM-judged — agent resolved the multi-step goal

**Custom criteria — GEval (FormSense schema adherence, domain rules):**
- `GEval:<criterion>` target ≥ 0.85   (or the project's stated threshold)

Rules:
- For any metric below threshold, name the specific failing test case and its score.
- Report the judge model used. For finance/proprietary suites (AFC, Crucible) the judge must be
  **local Ollama** ($0, private) — flag it if a cloud judge ran on sensitive data.
- Tool Correctness is deterministic (no judge); Task Completion & GEval use the LLM judge.
- Conclude with **PASS** (all thresholds met) or **FAIL** (list failing metrics).
- Do **NOT** modify any files — report only.