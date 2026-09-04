Report the AI evaluation suite results and quality scores.

All context you need has already been injected above this text by
`.github/scripts/eval_context.sh`.

**Do not attempt to load any of it yourself.** This body contains no `!` blocks and no
`@` references by design: command-template substitution is single-pass, so either would
arrive as literal text and silently never run (ADR-0001).

**Check the context first.** If a block above is missing, empty, or shows a line
beginning `CONTEXT_ERROR`, **STOP and report which one**. Do not infer, reconstruct, or
reason from the rules files in place of the missing output.

**This command emits a PASS/FAIL verdict on an eval gate.** A fabricated PASS
propagates into README claims and the flagship checklist. If the `DEEPEVAL RUN` block
is absent, empty, or errored, **STOP and report FAIL — no verdict possible**. Never
infer scores from the thresholds listed below; those are targets, not results.

Report every metric the suite emits as `score vs threshold` with PASS/FAIL, grouped by
family. Metric definitions are in the `EVAL SUITE SOURCE` block — report only the
families this project actually uses.

**RAG / generation (all AI projects):**
- Answer Relevancy    target > 0.80
- Faithfulness        target > 0.85   (> 0.90 for AFC / Crucible — finance sensitivity)
- Hallucination       target < 0.15   (< 0.10 for AFC / Crucible)

**Agentic (AFC, Crucible — suite must supply `tools_called` / `expected_tools`):**
- Tool Correctness    target = 1.00   deterministic — every expected tool called, right selection + args
- Task Completion     target > 0.80   LLM-judged — agent resolved the multi-step goal

**Custom criteria — GEval (FormSense schema adherence, domain rules):**
- `GEval:<criterion>` target >= 0.85   (or the project's stated threshold)

Rules:
- For any metric below threshold, name the specific failing test case and its score.
- Report the judge model the suite configures, read from the `EVAL SUITE SOURCE` block.
  For finance/proprietary suites (AFC, Crucible) the configured judge must be **local
  Ollama** — flag it if a cloud judge is wired up for sensitive data.
- Tool Correctness is deterministic (no judge); Task Completion & GEval use the LLM judge.
- Report the labeled-set size; flag it if under 30 cases or missing adversarial /
  PII-probing inputs.
- The `CI EVAL GATE WIRED?` block tells you whether this is a gate or an assertion.
  Report `NO CI EVAL JOB FOUND` as blocking.
- Active portfolio is DataVault, PolicyPulse, Crucible (leads) + FormSense, AFC
  (supporting), and PostCheck. **ODI and StreamSmart are backlog** — note them as
  outside the active set, not as portfolio gates.
- **On any Crucible run, state explicitly:** eval scores never authorize a live trade.
  The live path is gated by mandatory human sign-off plus a kill-switch, independent of
  any metric.
- Conclude with **PASS** (all thresholds met) or **FAIL** (list failing metrics).
- Do **NOT** modify any files — report only.