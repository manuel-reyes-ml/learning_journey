---
description: Run the AI evaluation suite and report scores vs thresholds (RAG + agentic + GEval)
agent: eval-guardian
---

Run the AI evaluation suite and report quality scores.

!`uv run deepeval test run tests/test_eval.py -v`

Confirm the gate is wired (an eval suite with no CI job is an assertion, not a gate):
!`grep -rn "deepeval" .github/workflows/ 2>/dev/null || echo "NO CI EVAL JOB FOUND — report as blocking"`

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
- Report the labeled-set size; flag it if under 30 cases or missing adversarial / PII-probing inputs.
- Active portfolio is DataVault, PolicyPulse, Crucible (leads) + FormSense, AFC (supporting).
  **ODI and StreamSmart are backlog** — note them as outside the active set, not as portfolio gates.
- **On any Crucible run, state explicitly:** eval scores never authorize a live trade. The live
  path is gated by mandatory human sign-off plus a kill-switch, independent of any metric.
- Conclude with **PASS** (all thresholds met) or **FAIL** (list failing metrics).
- Do **NOT** modify any files — report only.