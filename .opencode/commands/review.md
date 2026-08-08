---
description: Production-readiness review of the working tree (report only, no fixes)
agent: plan
---

Review the current working state for production readiness. Report only.

Linting:
!`uv run ruff check src/ tests/`

Format check:
!`uv run ruff format --check src/ tests/`

Type checking:
!`uv run mypy src/`

Tests:
!`uv run pytest tests/ -v --tb=short`

Lock file in sync:
!`uv lock --check 2>&1 || echo "uv.lock is STALE — run 'uv lock'"`

Changed files:
!`git diff --stat`

Then statically verify across changed/new `.py` files:

**Code**
- `from __future__ import annotations` is the first line after the docstring
- All public functions have NumPy-style docstrings; full type hints (PEP 604 `X | None`)
- Pydantic validates external/LLM data; layer-boundary rule respected
- No `print()` outside `scripts/`

**Logging (structlog — NOT the stdlib idiom)**
- Log calls use **structlog kwargs**: `log.info("records_loaded", path=..., rows=...)`
- **No f-strings AND no `%s`/`%d` interpolation of payload data.** The `%`-lazy-format
  idiom is correct for plain stdlib logging and **wrong here** — flag both forms.
- Event names are stable `snake_case` identifiers, not sentences
- `configure_logging()` called once at the entrypoint; no `basicConfig()` or
  `structlog.configure()` inside a library module
- `clear_contextvars()` called before `bind_contextvars()` (no cross-run bleed)
- No prompt/completion bodies logged at INFO

**Config & secrets**
- All config through `settings` (pydantic-settings) — no raw `os.environ` / `os.getenv`
- Every credential typed `SecretStr`, unwrapped only at the client constructor
- No hardcoded secrets/API keys, no PII in logs, no real participant data in fixtures

**Reliability**
- Retries via `stamina` with capped attempts *and* total time, transient errors only
- No retry on `ValidationError` or auth failure; retried writes carry an idempotency key

**Packaging**
- `pyproject.toml` + committed `uv.lock`; no `requirements.txt`; no `pip install` in Dockerfile

Summarize as:
- ✅ Passing checks
- ❌ Failing checks with `file:line`
- 🔧 Suggested fix (one line each)

Do **NOT** fix anything — I decide what to address.
