# llm-api-smoke-test

> Verify your Anthropic and Gemini API keys with a single round trip each — a production-grade smoke test in under a second.

[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Typed](https://img.shields.io/badge/typing-strict-brightgreen.svg)](https://peps.python.org/pep-0561/)
[![Ruff](https://img.shields.io/badge/lint-ruff-orange.svg)](https://github.com/astral-sh/ruff)

A tiny CLI that answers one question fast: **are my LLM API keys actually working?** Instead of discovering a bad key 30 seconds into a long pipeline, run one short prompt against each provider and get an immediate, structured answer.

This is a deliberately small project built to demonstrate production Python patterns at the smallest possible scale — Pydantic-validated config, Protocol-based provider abstraction, sync **and** async execution paths, structured logging, and a fully typed, fully tested codebase.

---

## Why this exists

A broken API key is one of the most common — and most annoying — failures in any LLM application. The error usually surfaces late: deep inside a batch job, halfway through a deployment, or in CI after everything else has already run. `llm-api-smoke-test` moves that failure to the front:

- **Fail fast** — placeholder keys and missing env vars are caught at startup, before any network call.
- **Fail clearly** — a non-zero exit code per the documented `ExitCode` table, plus structured NDJSON logs.
- **Fail safely** — API keys are wrapped in Pydantic `SecretStr`, so they're redacted in every log line, repr, and traceback.

Drop it into CI as a pre-flight check, or run it locally whenever you rotate keys.

---

## Features

- **Two providers out of the box** — Anthropic (Claude) and Google Gemini, each behind a clean adapter.
- **Sync and async execution** — sequential round-trips for simple checks, or a concurrent batch runner with semaphore + leaky-bucket rate limiting for higher throughput.
- **Three ways to pass prompts** — space-separated list, repeated flag (git/docker style), or a prompts file.
- **Secret-safe by construction** — keys never appear in logs, output, or tracebacks.
- **Structured logging** — NDJSON output queryable with `jq`, DuckDB, or any log aggregator.
- **Fully typed** — `pyright --strict` clean, ships a `py.typed` marker (PEP 561).
- **Extensible** — add a new provider with a single decorated class; no changes to the runner or CLI.

---

## Installation

Requires **Python 3.12+**.

```bash
# Clone the repo
git clone https://github.com/manuel-reyes-ml/learning_journey.git
cd learning_journey

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows

# Editable install with dev tooling (tests, lint, type-check)
pip install -e ".[dev]"
```

After installation, the `llm-api-smoke-test` command is available on your shell.

---

## Configuration

Credentials are read from environment variables (or a `.env` file in the working directory). Only the two API keys are required; model identifiers have sensible defaults.

| Variable | Required | Default |
|---|:---:|---|
| `ANTHROPIC_API_KEY` | ✅ | — |
| `GEMINI_API_KEY` | ✅ | — |
| `ANTHROPIC_MODEL` | ❌ | `claude-sonnet-4-6` |
| `GEMINI_MODEL` | ❌ | `gemini-2.5-flash` |

Create a `.env` file:

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-your-real-key
GEMINI_API_KEY=AIza-your-real-key
```

> **Note:** Real environment variables take precedence over `.env` entries. Keys are validated at startup — an empty or placeholder value (`your-key-here`, `changeme`, etc.) is rejected immediately with a clear error.

---

## Usage

```bash
# Run all registered providers with the default prompt
llm-api-smoke-test anthropic gemini

# Test a single provider
llm-api-smoke-test anthropic

# Custom prompts (space-separated)
llm-api-smoke-test anthropic --prompts "what is 2+2" "say hello"

# Custom prompts (repeated flag — robust for prompts with special characters)
llm-api-smoke-test anthropic --prompt "first prompt" --prompt "second prompt"

# Prompts from a file (one per line; lines starting with '#' are comments)
llm-api-smoke-test anthropic --prompts-file prompts.txt

# Async batch mode — concurrency + rate-limit caps
llm-api-smoke-test anthropic gemini --async

# Verbose (DEBUG-level) logging
llm-api-smoke-test anthropic --verbose

# Console-only — disable the rotating log file
llm-api-smoke-test anthropic --no-log-file
```

You can also run it as a module:

```bash
python -m llm_api_smoke_test anthropic gemini
```

### Prompt input modes

The three prompt flags are **mutually exclusive** — argparse rejects any combination of them.

| Flag | Best for | Example |
|---|---|---|
| `--prompts A B C` | 1–3 short prompts, scripted use | `--prompts "hi" "bye"` |
| `--prompt A --prompt B` | Prompts with special characters, interactive use | `--prompt "say: hi, ok?"` |
| `--prompts-file FILE` | Many prompts, version-controlled with code | `--prompts-file prompts.txt` |

---

## Exit codes

The CLI follows POSIX conventions so it composes cleanly in shell pipelines and CI gates.

| Code | Name | Meaning |
|:---:|---|---|
| `0` | `SUCCESS` | Every provider returned a response. |
| `1` | `CONFIG_ERROR` | Missing env var, placeholder key, or unknown provider name. |
| `2` | `PROVIDER_ERROR` | At least one provider's call raised. Returned even if others succeeded. |
| `130` | `KEYBOARD_INTERRUPT` | Interrupted with Ctrl-C. |

> **Why fail on _any_ provider error rather than all?** This is a smoke test — its job is to surface a broken credential immediately. A partial failure means at least one key is wrong, and CI should catch that before anything downstream runs.

Use it as a CI gate:

```bash
llm-api-smoke-test anthropic gemini || exit 1
```

---

## Architecture

The package follows a strict dependency hierarchy — lower layers never import from higher ones.

```
config.py        Pydantic settings + SecretStr (no internal imports)
    │
register.py      Plugin registry: ProviderList, DictInfo, register_class
    │
providers.py     LLMProvider / AsyncLLMProvider Protocols + concrete adapters
    │            (registers itself into the registry at import time)
    ├── runner.py          sync driver — run_smoke_tests()
    ├── batch_runner.py    async driver — batch_smoke_test()
    └── logger.py          structlog-on-stdlib, NDJSON output
            │
        __main__.py        composition root — CLI parse → dispatch → exit code
```

### How a run flows

1. **`__main__.py`** parses arguments into a typed, frozen `LLMApiArgs`.
2. Logging is configured (structlog + stdlib, NDJSON to disk).
3. `SmokeTestSettings` loads and validates credentials from the environment.
4. Provider names are validated against the registry, then instantiated — picking the **sync** or **async** variant based on the `--async` flag.
5. The chosen runner executes: `run_smoke_tests()` (sequential) or `batch_smoke_test()` (concurrent, rate-limited).
6. Results are summarised; the appropriate `ExitCode` is returned.

### Project layout

```
llm-api-smoke-test/
├── src/
│   └── llm_api_smoke_test/
│       ├── __init__.py          # NullHandler logging + version
│       ├── __main__.py          # CLI composition root + entry points
│       ├── config.py            # Pydantic settings, SecretStr, validators
│       ├── register.py          # Plugin registry (sync/async dual-registration)
│       ├── providers.py         # Protocols + Anthropic/Gemini adapters
│       ├── runner.py            # Synchronous driver
│       ├── batch_runner.py      # Async driver (semaphore + rate limiter)
│       ├── logger.py            # structlog + NDJSON configuration
│       └── py.typed             # PEP 561 typed-package marker
├── tests/                       # ~66 tests across 7 modules
├── pyproject.toml
├── LICENSE
└── README.md
```

---

## Extending: add a new provider

Adding a third provider (say, OpenAI) requires **one decorated class per variant** — no changes to the runner, CLI, or registry.

```python
from llm_api_smoke_test.register import register_class
from llm_api_smoke_test.providers import SmokeTestResult
from llm_api_smoke_test.config import ProviderSettings


@register_class("openai", "sync", "OpenAI sync LLM provider")
class OpenAIProvider:
    def __init__(self, settings: ProviderSettings) -> None:
        import openai
        self._client = openai.OpenAI(api_key=settings.api_key.get_secret_value())
        self._settings = settings

    def smoke_test(self, prompt: str) -> SmokeTestResult:
        # ... call the API, build and return a SmokeTestResult ...
        ...
```

The class satisfies the `LLMProvider` Protocol structurally — no inheritance needed. The decorator registers it under the key `"openai"`, and it's immediately available to the CLI: `llm-api-smoke-test openai`.

---

## Development

```bash
# Run the test suite
pytest

# With coverage
pytest --cov=llm_api_smoke_test --cov-report=term-missing

# Lint and format
ruff check src tests
ruff format src tests

# Type-check (strict)
pyright
```

### Test suite

~66 tests across 7 modules, using **fake provider objects** (classes that satisfy the Protocol) rather than mocks — no real API calls, no flake, no spent tokens.

| File | Covers |
|---|---|
| `test_config.py` | Pydantic settings, secret redaction, placeholder rejection |
| `test_register.py` | Registry mechanics, sync/async dual-registration |
| `test_runner.py` | Sync driver — success + failure paths |
| `test_batch_runner.py` | Async driver + concurrency-cap verification |
| `test_main.py` | CLI parsing, prompt resolution, provider validation |
| `test_integration.py` | End-to-end `main()` → exit code |

---

## Design notes

A few decisions worth calling out, since this project exists partly to demonstrate them:

- **Protocol over ABC** — providers conform to a structural interface, so a fake test double or a third-party class can satisfy the contract without inheriting from anything.
- **`SecretStr` everywhere** — API keys are wrapped at the config boundary, so they can't leak into logs or tracebacks even by accident.
- **Frozen dataclasses + `dataclasses.replace`** — the registry is immutable; updates produce new instances rather than mutating shared state.
- **Sync and async share a Protocol** — the same registry key resolves to either a blocking or concurrent adapter, selected at dispatch time.
- **No retry logic, by design** — a smoke test should surface a broken key _immediately_, not mask it behind exponential backoff. Retry belongs in the production workloads downstream, not here.
- **Layer-boundary exception handling** — domain functions raise standard exceptions; only the CLI layer translates them into exit codes.

---

## License

[MIT](LICENSE) © Manuel Reyes

---

<sub>Built as a learning artifact for a GenAI-engineering career transition — production-grade patterns at the smallest honest scale.</sub>