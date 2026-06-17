# `llm_api_smoke_test` — Test Suite

## Quick start

```bash
# 1. Install test dependencies (add to pyproject.toml [project.optional-dependencies])
pip install pytest pytest-asyncio pytest-cov

# 2. Run from the project root
pytest

# 3. With coverage report
pytest --cov=llm_api_smoke_test --cov-report=term-missing

# 4. Run just one file
pytest tests/test_config.py -v

# 5. Run by keyword
pytest -k "test_async" -v
```

## Files at a glance

| File | What it covers | Test count |
|---|---|---|
| `conftest.py` | Shared fixtures — env, settings, FakeSyncProvider, FakeAsyncProvider | (fixtures, not tests) |
| `test_config.py` | ProviderSettings, SmokeTestSettings, load_config | ~12 tests |
| `test_register.py` | DictInfo, ProviderList, register_class, live registry | ~13 tests |
| `test_runner.py` | run_smoke_tests() sync driver — happy + failure paths | ~9 tests |
| `test_batch_runner.py` | batch_smoke_test() async driver — happy + failure + concurrency cap | ~7 tests |
| `test_main.py` | ExitCode, LLMApiArgs, _build_parser, _validate_providers, _resolve_prompts, _build_providers | ~17 tests |
| `test_integration.py` | main() end-to-end — sync, async, failure-path exit codes | ~8 tests |

**Total: ~66 tests** covering every function/class without hitting the real Anthropic or Gemini APIs.

## Required pyproject.toml additions

Add these blocks to your `pyproject.toml` (the existing `[project]` block should already include `pydantic`, `pydantic-settings`, `structlog`, `anthropic`, `google-genai`, `httpx`, `aiolimiter`):

```toml
[project.optional-dependencies]
test = [
    "pytest>=7.4",
    "pytest-asyncio>=0.21",
    "pytest-cov>=4.1",
]

[tool.pytest.ini_options]
# Auto-mode runs every `async def test_*` in an event loop automatically.
# No @pytest.mark.asyncio needed on individual tests.
asyncio_mode = "auto"

# Where pytest searches for tests.
testpaths = ["tests"]

# Naming conventions — match Python's PEP 8.
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"

# Show slow tests so you can spot regression.
addopts = "--durations=10 -v"

# Coverage config (used by --cov=).
[tool.coverage.run]
source = ["llm_api_smoke_test"]
omit = ["tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

## Patterns demonstrated by these tests

| Pattern | Where | Why it matters |
|---|---|---|
| **conftest.py for shared fixtures** | `conftest.py` | Pytest auto-discovers; no explicit imports needed |
| **AAA structure (Arrange / Act / Assert)** | every test | Most readable test shape; recruiters expect it |
| **Fake objects via Protocol** | `FakeSyncProvider`, `FakeAsyncProvider` | No network, no API key, no flake — pure unit testing |
| **`monkeypatch.setenv`** | `valid_env` fixture | Safe env var manipulation, auto-restored |
| **`monkeypatch.setattr` / `setitem`** | `clean_registry`, `fake_registry` | Replace module state; auto-restored |
| **`@pytest.mark.parametrize`** | `test_rejects_placeholder_keys` | One test method covers N cases; each reported separately |
| **`pytest.raises(... match=...)`** | exception tests | Regex-matched messages, not just type |
| **`tmp_path` for file tests** | `test_reads_from_file` | Auto-cleaned temp dir, no manual housekeeping |
| **`pytestmark = pytest.mark.asyncio`** | `test_batch_runner.py` | Applies the marker to every test — less boilerplate |
| **Class-based test grouping** | every file | Namespaces test reports as a spec: `TestX::test_y` |
| **Fixture composition** | `settings` depends on `valid_env` | Pytest resolves the chain automatically |
| **Live registry tests** | `TestLiveRegistry` | Verify import-time side effects without mocking |
| **End-to-end via main(argv=...)** | `test_integration.py` | Tests the documented testability contract |

## What's NOT tested (and why)

| Not covered | Why |
|---|---|
| Real Anthropic / Gemini API calls | Costs money + slow + flaky.  Use `respx` (httpx mock library) when you need to test the actual HTTP layer. |
| `logger.py` config functions | The handlers attach to stdlib logging — testing them requires temporarily replacing handlers (verbose).  Add later if you find a logging bug. |
| `_compat.py` for the speller t-string code | Not in this package. |
| `cli_entry()` itself | It's a 2-line wrapper around `sys.exit(main())` — testing it just verifies sys.exit is called, which is trivial. |

## Next steps after green tests

1. **Add `pytest-cov` to CI** — fail the build on <80% coverage.
2. **Add `respx` and write provider HTTP tests** — verifies actual request shape against Anthropic/Gemini API contracts without spending tokens.
3. **Property-based tests via `hypothesis`** — fuzz `_validate_providers` with arbitrary strings to find edge cases the unit tests missed.

## Coach note

This suite intentionally avoids `pytest.mock` and `MagicMock`.  The fake-object pattern (real classes that satisfy the Protocol) is far more readable and lets the type checker help — `MagicMock` defeats both.

The single biggest test-quality lesson from this package: **define your fakes alongside your Protocols**.  The moment you have `LLMProvider` as a Protocol, you have a contract that a fake can satisfy structurally, no inheritance needed.  Same pattern carries to DataVault, PolicyPulse, FormSense.