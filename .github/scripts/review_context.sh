#!/usr/bin/env bash
# review_context.sh — context loader for /review. Read-only. See ADR-0001.
set -uo pipefail
run() { echo "===== $1 ====="; shift; "$@" 2>&1 || echo "(non-zero exit — findings above are the payload)"; echo; }

run "RUFF CHECK"        uv run ruff check src/ tests/
run "RUFF FORMAT CHECK" uv run ruff format --check src/ tests/
run "MYPY"              uv run mypy src/
run "PYTEST"            uv run pytest tests/ -v --tb=short

echo "===== UV.LOCK IN SYNC ====="
uv lock --check 2>&1 || echo "uv.lock is STALE — run 'uv lock'"
echo
echo "===== CHANGED FILES ====="
git diff --stat 2>&1 || echo "CONTEXT_ERROR: git diff failed. STOP and report."
echo
echo "===== CHANGED/NEW PYTHON FILES (full source for static review) ====="
files=$(git diff --name-only --diff-filter=ACMR -- '*.py' 2>/dev/null; git ls-files --others --exclude-standard -- '*.py' 2>/dev/null)
if [[ -z "${files// }" ]]; then
  echo "CONTEXT_ERROR: no changed or new .py files found. The static checks below"
  echo "have nothing to run against — STOP and report rather than reviewing from memory."
else
  for f in $files; do
    [[ -r "$f" ]] || continue
    echo "----- BEGIN $f -----"; cat "$f"; echo "----- END $f -----"; echo
  done
fi
echo "===== END CONTEXT ====="
