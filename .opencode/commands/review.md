---
description: Production-readiness review of the working tree (report only, no fixes)
agent: plan
---

Review the current working state for production readiness. Report only.

Linting:
!`ruff check src/ tests/`

Type checking:
!`mypy src/`

Tests:
!`pytest tests/ -v --tb=short`

Changed files:
!`git diff --stat`

Then statically verify across changed/new `.py` files:
- `from __future__ import annotations` is the first line after the docstring
- Logger calls use lazy `%s`/`%d` formatting (no f-strings in logging)
- All public functions have NumPy-style docstrings
- No `print()`, no hardcoded secrets/API keys, no PII in logs
- Pydantic validates external/LLM data; layer-boundary rule respected

Summarize as:
- ✅ Passing checks
- ❌ Failing checks with `file:line`
- 🔧 Suggested fix (one line each)

Do **NOT** fix anything — I decide what to address.
