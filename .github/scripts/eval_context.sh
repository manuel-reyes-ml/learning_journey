#!/usr/bin/env bash
# eval_context.sh — context loader for /eval. Read-only. See ADR-0001.
#
# A fabricated PASS on an eval gate propagates into README claims and the
# flagship checklist. Every block below is mandatory: the body STOPS if any
# is missing rather than inferring a verdict.
set -uo pipefail
echo "===== DEEPEVAL RUN ====="
if uv run deepeval test run tests/test_eval.py -v 2>&1; then :; else
  echo "(deepeval exited non-zero — failures above are the payload)"
fi
echo
echo "===== EVAL SUITE SOURCE (metric + threshold definitions) ====="
if [[ -r tests/test_eval.py ]]; then
  cat tests/test_eval.py
else
  echo "CONTEXT_ERROR: tests/test_eval.py not readable. STOP and report."
fi
echo
echo "===== CI EVAL GATE WIRED? ====="
grep -rn "deepeval" .github/workflows/ 2>/dev/null \
  || echo "NO CI EVAL JOB FOUND — report as blocking"
echo
echo "===== END CONTEXT ====="
