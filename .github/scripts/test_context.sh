#!/usr/bin/env bash
# test_context.sh — context loader for /test. Read-only. See ADR-0001.
set -uo pipefail
echo "===== PYTEST RUN ====="
uv run pytest tests/ -v --tb=short 2>&1 || echo "(pytest exited non-zero — failures above are the payload, not a CONTEXT_ERROR)"
echo
echo "===== CONFTEST FIXTURES PRESENT ====="
grep -rn "_reset_structlog\|_no_retry_sleeps" tests/conftest.py 2>/dev/null \
  || echo "NEITHER _reset_structlog NOR _no_retry_sleeps FOUND in tests/conftest.py"
echo
echo "===== END CONTEXT ====="
