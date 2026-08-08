Review the current working state for production readiness.

1. Run `uv run ruff check src/ tests/` and report any issues
2. Run `uv run ruff format --check src/ tests/` and report anything unformatted
3. Run `uv run mypy src/` and report type errors
4. Run `uv run pytest tests/ -v --tb=short` and report failures
5. Run `uv lock --check` — report if `uv.lock` is stale against `pyproject.toml`
6. Run `git diff --stat` to see what changed

Then statically verify across every new or modified `.py` file:

**Code**
- `from __future__ import annotations` is the first line after the docstring
- Full type hints (PEP 604 `X | None`); public functions have NumPy-style docstrings
- Pydantic validates external/LLM data; the layer-boundary rule is respected
- No `print()` outside `scripts/`

**Logging — structlog, NOT the stdlib idiom**
- Log calls use **structlog kwargs**: `log.info("records_loaded", path=..., rows=...)`
- **Flag BOTH f-strings AND `%s`/`%d` interpolation of payload data.** The `%`-lazy-format
  idiom is correct for plain stdlib logging and **wrong in this codebase** — the event name
  is a stable `snake_case` key and all data travels as kwargs
- `configure_logging()` is called once at the entrypoint; no `basicConfig()` or
  `structlog.configure()` inside a library module
- `clear_contextvars()` is called before `bind_contextvars()` (no cross-run bleed)
- No prompt or completion bodies logged at INFO

**Config & secrets**
- All config goes through `settings` (pydantic-settings) — no raw `os.environ` / `os.getenv`
- Every credential is typed `SecretStr`, unwrapped only at the client constructor
- No hardcoded secrets or API keys, no PII in logs, no real participant data in fixtures

**Reliability**
- Retries use `stamina` with capped attempts AND total time, transient errors only
- No retry on `ValidationError` or auth failure; any retried write carries an idempotency key

**Packaging**
- `pyproject.toml` + committed `uv.lock`; no `requirements.txt`; no `pip install` in the Dockerfile

Summarize results as:
- ✅ Passing checks
- ❌ Failing checks with specific `file:line` references
- 🔧 Suggested fixes (one-liner each)

Do NOT fix anything — report only. I will decide what to address.
