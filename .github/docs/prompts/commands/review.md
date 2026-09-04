Review the current working state for production readiness. Report only.

All context you need has already been injected above this text by
`.github/scripts/review_context.sh`.

**Do not attempt to load any of it yourself.** This body contains no `!` blocks and no
`@` references by design: command-template substitution is single-pass, so either would
arrive as literal text and silently never run (ADR-0001).

**Check the context first.** If a block above is missing, empty, or shows a line
beginning `CONTEXT_ERROR`, **STOP and report which one**. Do not infer, reconstruct, or
reason from the rules files in place of the missing output.

The context blocks give you `RUFF CHECK`, `RUFF FORMAT CHECK`, `MYPY`, `PYTEST`,
`UV.LOCK IN SYNC`, `CHANGED FILES`, and the full source of every changed or new `.py`
file. Report from those blocks only.

**If the changed-files source block reports `CONTEXT_ERROR`, STOP.** A
production-readiness verdict with no source in context is a fabrication, and this
command's output is used to decide what ships.

Then statically verify across the `.py` sources provided:

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

Every finding must cite `file:line` from a source block you were given. A finding you
cannot cite is not a finding — omit it.

Summarize as:
- Passing checks
- Failing checks with `file:line`
- Suggested fix (one line each)

Do **NOT** fix anything — I decide what to address.