---
description: Audits for hardcoded secrets, exposed PII, unsafe logging and config, and privacy-routing violations. Read-only, cloud model with zero retention on Go. Synthetic-data repos only. Use before commits on finance/data work. Invoke with @security-auditor.
mode: subagent
# GLM-5.2 is listed with 0-day retention on OpenCode Go. Keep any model in this
# slot on a 0-day row of the Go privacy table (not Haiku 5.5, GPT-6 Luna, Grok 4.7
# or Gemini 4 Argon, which keep data 30–55 days).
model: opencode-go/glm-5.2#high
# OpenCode 2.x format. LAST matching rule wins.
# temperature removed: V2 no longer sends agent-level temperature to the model.
permissions:
  - { action: edit, resource: "*", effect: deny }
  - { action: webfetch, resource: "*", effect: deny }
  - { action: subagent, resource: "*", effect: deny }
  - { action: shell, resource: "*", effect: deny }
  - { action: shell, resource: "grep *", effect: allow }
  - { action: shell, resource: "git diff *", effect: allow }
  - { action: shell, resource: "git log *", effect: allow }
  - { action: shell, resource: "ls *", effect: allow }
  - { action: shell, resource: "find *", effect: allow }
  - { action: shell, resource: "find *-delete*", effect: deny }
  - { action: shell, resource: "find *-exec*", effect: deny }
  - { action: shell, resource: "find *-ok*", effect: deny }
  - { action: shell, resource: "find *-fprint*", effect: deny }
  - { action: shell, resource: "find *-fls*", effect: deny }
  - { action: shell, resource: "git * --output*", effect: deny }
  - { action: shell, resource: "*>*", effect: deny }
---
<!-- GENERATED BODY — DO NOT EDIT BELOW THE FRONTMATTER.
     Edit the frontmatter above freely; it is the source for this agent's settings.
     Edit the body at its sources, then run `make opencode-agents`:
       .github/docs/prompts/agents/security-auditor.opencode-delta.md
       .cursor/rules/observability.mdc
       .cursor/rules/ai-sdk-patterns.mdc
       .github/docs/prompts/agents/security-auditor.md
     OpenCode 2.x does not expand {file:...} in agent files (ADR-001 §14).
-->

> 🔒 **OpenCode note:** this agent runs on a **cloud model** (GLM-5.2 via OpenCode Go,
> 0-day retention). Repository code leaves the machine when it runs. Point it only at
> repos that hold synthetic data. The real PII boundary is the pre-commit layer
> (gitleaks + detect-private-key), not this agent.

# Observability, Retries & Secure Config

> The Correction 16 layer: one logging chain, one config entrypoint, one retry
> standard. Split from the former `python-production-standards.mdc`.
>
> **2026 stack:** `structlog` (logging) · `stamina` (retries) ·
> `pydantic-settings` (config). Hard rules and the commit gate are in `AGENTS.md`.

---

## 🔁 Retries (`stamina`)

> **Standard: `stamina`** — an opinionated wrapper over `tenacity` by the author of
> `structlog`. It auto-detects structlog and logs every scheduled retry through the
> configured chain, so retries land in the same structured stream as everything else,
> for free. Raw `tenacity` remains the escape hatch for retry policies stamina can't
> express; never hand-roll a `while` + `time.sleep()` loop.

```python
import httpx
import stamina

@stamina.retry(on=httpx.HTTPError, attempts=3, timeout=60.0)
def fetch_quote(symbol: str) -> httpx.Response:
    resp = httpx.get(f"https://api.example.com/quote/{symbol}")
    resp.raise_for_status()
    return resp
```

Exponential backoff with jitter, an attempt cap, and a total-time cap are the defaults —
which is the whole reason to prefer it over configuring `tenacity` by hand each time.
Async callables use the identical API. Type hints on the decorated callable are preserved.

### Rules
- **Retry only transient failures** — timeouts, connection errors, 429, 5xx. Never retry
  a 4xx validation error, an auth failure, or a `ValidationError`: it will fail identically
  every time and burns the budget.
- **Only retry idempotent operations.** A retried write needs an idempotency key, or it
  double-books. This is a hard gate on any DataVault write path.
- **Always cap both** attempts *and* total time. Unbounded retries turn a slow dependency
  into an outage.
- **Jitter is mandatory** — synchronized retries from parallel workers are a thundering
  herd that keeps a recovering service down.
- **Deactivate globally in tests** (`stamina.set_active(False)`) so the suite doesn't
  spend real seconds sleeping through backoffs. Fixture in `testing-and-eval.mdc`.

---

## 📋 Structured Logging (structlog + stdlib)

> **Standard:** `structlog` renders **every** log line — yours *and* every third-party
> library's (LLM SDKs, httpx, PyTorch, Airflow, uvicorn, Neo4j). One format, one config,
> one place to redact PII. Implemented with `structlog.stdlib.ProcessorFormatter`.
>
> **Why this approach and not the others:** structlog documents four stdlib-integration
> strategies. Only `ProcessorFormatter` renders foreign (non-structlog) records through
> *our* processor chain. "Rendering within structlog" leaves third-party logs unformatted;
> `python-json-logger` works but leaves the event dict to a formatter that silently drops
> context and swallows exceptions. **Record this choice as an ADR** — see
> `architecture-docs.mdc`.

### Single configuration module

```python
# src/observability/logging.py — call configure_logging() ONCE at the entrypoint.
# Never call basicConfig() or configure() inside a library module.
from __future__ import annotations

import logging
import re
import sys

import structlog

# ---------------------------------------------------------------- redaction
# Runs on EVERY event dict — structlog AND third-party. A forgotten call site
# cannot leak: the processor is the choke point, not the discipline of the caller.
_PII_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "***-**-REDACTED"),
    (re.compile(r"\b[\w.-]+@[\w.-]+\.\w+\b"), "<email:redacted>"),
    (re.compile(r"\b(?:sk|api)-[A-Za-z0-9_\-]{16,}\b"), "<key:redacted>"),
)


def redact_pii(_: object, __: str, event_dict: dict) -> dict:
    """Mask PII/secrets in every log line. Not optional, not bypassable."""
    for key, value in event_dict.items():
        if isinstance(value, str):
            for pattern, replacement in _PII_PATTERNS:
                value = pattern.sub(replacement, value)
            event_dict[key] = value
    return event_dict


# ---------------------------------------------------------------- processors
# Shared chain runs on BOTH structlog records and foreign stdlib records.
SHARED_PROCESSORS: list[structlog.typing.Processor] = [
    structlog.contextvars.merge_contextvars,  # run_id / request_id / plan_year
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.processors.TimeStamper(fmt="iso", utc=True),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.UnicodeDecoder(),
    redact_pii,  # MUST run before any renderer
]

# Chatty dependencies. Tune here, not with scattered setLevel() calls.
THIRD_PARTY_LEVELS: dict[str, int] = {
    "httpx": logging.WARNING,
    "httpcore": logging.WARNING,
    "urllib3": logging.WARNING,
    "neo4j": logging.WARNING,
    "anthropic": logging.INFO,
    "openai": logging.INFO,
}


def configure_logging(level: int = logging.INFO, *, force_json: bool = False) -> None:
    """Route stdlib logging and structlog through one ProcessorFormatter.

    Console + colors when attached to a TTY; JSON when running in Docker/CI.
    """
    json_mode = force_json or not sys.stderr.isatty()

    final_chain: list[structlog.typing.Processor] = [
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
    ]
    if json_mode:
        final_chain.append(structlog.processors.dict_tracebacks)
        final_chain.append(structlog.processors.JSONRenderer())
    else:
        final_chain.append(structlog.dev.ConsoleRenderer(colors=True))

    structlog.configure(
        processors=[
            *SHARED_PROCESSORS,
            structlog.stdlib.PositionalArgumentsFormatter(),
            # MUST be last. NEVER combine with render_to_log_kwargs().
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,  # set False in tests
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            # Runs ONLY on records that did not originate in structlog.
            # ExtraAdder preserves `extra={...}` payloads from third-party libs.
            foreign_pre_chain=[structlog.stdlib.ExtraAdder(), *SHARED_PROCESSORS],
            processors=final_chain,
        )
    )

    root = logging.getLogger()
    root.handlers.clear()  # idempotent — safe across Streamlit reruns
    root.addHandler(handler)
    root.setLevel(level)

    for name, lvl in THIRD_PARTY_LEVELS.items():
        logging.getLogger(name).setLevel(lvl)
```

### Call-site rules

```python
import structlog

log = structlog.stdlib.get_logger(__name__)  # typed BoundLogger

# ✅ Event name is a stable snake_case IDENTIFIER; all data goes in kwargs.
log.info("records_loaded", source=str(path), row_count=len(df), elapsed_ms=elapsed)
log.warning("column_missing", column=col_name, fallback="default")
log.error("reconcile_failed", plan_id=plan_id, exc_info=True)

# ❌ The message is not the payload — this destroys every benefit of structured logs.
log.info(f"Loaded {len(df)} records from {path}")

# ❌ %-interpolation of payload data — correct for stdlib, wrong here.
log.info("Loaded %d records", len(df))
```

**Event-name discipline:** `snake_case`, verb-past or noun-state, stable over time
(`ai_query_completed`, not `"AI query completed"`). The event name is a *queryable key*,
not a sentence — renaming it breaks dashboards exactly like renaming a column breaks SQL.

### Library-never-configures-logging

A **library** module gets a logger and emits; it never configures. Only the
application entrypoint calls `configure_logging()`. A shared library that calls
`basicConfig()` or `structlog.configure()` on import hijacks the config of every
consumer — the SignalCore boundary spec records this as a named anti-pattern.

### Run context (contextvars)

Bind once per run/request; every downstream log line — including third-party — inherits it.

```python
structlog.contextvars.clear_contextvars()  # ALWAYS first: prevents cross-run bleed
structlog.contextvars.bind_contextvars(run_id=run_id, pipeline="1099_reconcile")
```

`clear_contextvars()` is not optional. Without it, context from one run leaks into the
next handled by the same worker — you get run B's logs carrying run A's `run_id`.

### Output destination

Log to **stdout only**. Rotation, shipping, and retention belong to Docker / systemd /
the aggregator — not to Python (12-Factor). Per-domain files (`logs/ai.log`) are *derived*
by filtering on the `logger` field downstream, never by adding a second handler.

> ⏸️ **Local-run exception (opt-in):** long unattended local runs (Crucible backtests,
> AFC collectors) may add a `WatchedFileHandler` behind an explicit `log_file=` argument.
> Never the default; never in a container.

### OpenTelemetry hook (S3 — wired now, activated later)

Keep this stub in place from day one so adding Phoenix/LangSmith later never requires
touching call sites:

```python
# def add_otel_context(_, __, event_dict: dict) -> dict:
#     """Add trace_id/span_id so logs join traces in the observability backend."""
#     from opentelemetry import trace
#     span = trace.get_current_span()
#     ctx = span.get_span_context()
#     if ctx and ctx.is_valid:
#         event_dict["trace_id"] = format(ctx.trace_id, "032x")
#         event_dict["span_id"] = format(ctx.span_id, "016x")
#     return event_dict
```

### Anti-patterns

```python
# ❌ basicConfig() in a module — last import wins, config becomes non-deterministic
# ❌ render_to_log_kwargs() alongside ProcessorFormatter — raises opaque stdlib errors
# ❌ A second handler writing the same stream — interleaved/duplicated lines
# ❌ Logging raw API responses or DataFrame rows — PII risk; log shape, ids, counts
# ❌ print() anywhere outside scripts/ — no level, no context, no redaction
```

---

## 🔒 Security & Privacy

### Never Expose Sensitive Data

Three independent layers. Each catches what the others miss — defense in depth, because
a single forgotten call site should never be able to leak participant data.

**Layer 1 — the log redaction processor** (above). Centralized, unbypassable, covers
third-party libraries echoing prompts or request bodies.

**Layer 2 — `SecretStr` on every credential.** Pydantic masks the value in `repr()` and
`model_dump()`, so a secret cannot leak through a debug print, a traceback, or a config
dump. Reading it requires the explicit, greppable `.get_secret_value()`.

**Layer 3 — masking helpers at display boundaries** (Streamlit, reports, exports):

```python
def mask_ssn(ssn: str) -> str:
    """Mask SSN for safe display: 123-45-6789 → ***-**-6789"""
    return f"***-**-{ssn[-4:]}" if len(ssn) >= 4 else "***"
```

> Layer 3 is distinct from the response-guardrail PII scan in `ai-sdk-patterns.mdc`,
> which runs on LLM output *before display*. Both exist deliberately; neither replaces
> the other.

```python
# ❌ Never hardcode secrets
api_key = "sk-abc123..."  # NEVER DO THIS

# ❌ Raw os.environ — untyped, unvalidated, fails late and scattered across the codebase
import os
api_key = os.environ.get("API_KEY")
```

### Typed Configuration (`pydantic-settings`)

`src/config/settings.py` is the **single** place the environment is read. Everywhere else
imports `settings`. Config errors then fail fast at startup with a clear Pydantic error,
not at 2am inside a pipeline.

```python
from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated application configuration. Instantiated once, imported everywhere."""

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_nested_delimiter="__",
        secrets_dir="/run/secrets",  # Docker's default secrets mount point
        extra="forbid",              # unknown env vars are a typo, not a feature
    )

    environment: str = "local"
    log_level: str = "INFO"

    ai_provider: str = "ollama"      # privacy-first default; never a cloud default
    anthropic_api_key: SecretStr | None = None
    max_retry_attempts: int = Field(default=3, ge=1, le=10)
    request_timeout_s: float = Field(default=30.0, gt=0)


settings = Settings()
```

```python
# ✅ Explicit unwrap at the point of use — greppable, auditable
client = Anthropic(api_key=settings.anthropic_api_key.get_secret_value())
```

**Rules**
- One `Settings` class per project; instantiate once at module scope in `config/settings.py`
- Every credential is `SecretStr` — no exceptions
- `extra="forbid"` so a typo'd env var fails loudly instead of silently defaulting
- Required values have **no default** — fail fast beats booting misconfigured
- Never instantiate `Settings()` at import time inside library modules (breaks testability);
  override in tests via `Settings(_env_file=None, ...)`
- `.env` is gitignored; `.env.example` is committed with **empty** values

### Safe File Handling
```python
from pathlib import Path
data_dir = Path(__file__).parent / 'data'
output_file = data_dir / 'results.csv'

with open(filepath, 'r') as f:
    content = f.read()
```

# AI SDK Patterns (2026 Production)

> Scoped rules for AI integration modules. Auto-attached when editing `src/ai/` files.
> Applies to: **DataVault, PolicyPulse, Crucible, FormSense, AFC** (leads + supporting)
> and to ODI / StreamSmart if and when they leave backlog.
>
> This file is the **canonical source for Pydantic model design** — do not duplicate
> those rules elsewhere.

---

## 🏗️ SDK-First Architecture

Every AI-powered project uses the same layered architecture:

```
src/ai/
├── __init__.py
├── provider.py           # Provider-agnostic LLM abstraction
├── schemas.py            # Pydantic response models (structured outputs)
├── guardrails.py         # Query validation, response sanitization, PII scan
├── observability.py      # Token/cost/latency tracking
└── [project-specific].py # e.g., pandas_chat.py, rag_pipeline.py
```

### Core Principles
1. **Privacy-first & provider-agnostic** — Finance/proprietary data runs on **local Ollama**
   (`qwen3.5`) and never leaves the machine. **Anthropic SDK is the primary cloud provider**;
   OpenRouter (DeepSeek/MiniMax) for bulk agentic work. Free/training-eligible tiers (e.g. the
   free Gemini tier) are **never** used for sensitive data. Provider is swapped via config —
   zero code changes.
2. **Structured outputs** — Every LLM response validated through Pydantic v2 models
3. **Guardrails first** — Query validation before sending; response sanitization before displaying
4. **Observability built-in** — Token usage, cost, latency logged per query from Day 1
5. **Graceful degradation** — App works without API key; AI features are an enhancement layer

---

## 🧭 Agentic taxonomy — name the pattern before you build it

**Anthropic's workflow-vs-agent distinction is the canonical frame.** Use it in code,
in ADRs, and in the README.

| | **Workflow** | **Agent** |
|---|---|---|
| Control flow | Predefined code path | LLM directs its own tool use |
| Predictability | High | Lower — dynamic |
| When to use | The steps are known | The steps depend on findings |

**Classification for this portfolio:**

- **FormSense** and **PolicyPulse** are *agentic workflows* — fixed paths, deterministic
  tool sequences. Do not describe them as agents.
- **AFC** uses agentic retrieval over a knowledge graph.
- **Crucible's live execution path is the only tier with an irreversibility gate.**

### 🔴 Crucible live-path invariant (non-negotiable)

Any code path that can place, modify, or cancel a live order requires:

1. **Mandatory human sign-off** before execution — no auto-approve, no timeout-approve,
   no "confidence above threshold" bypass.
2. **A kill-switch** that halts execution independently of the agent loop.

Eval scores never authorize a live trade. If you are writing a code path that touches
live execution and cannot point to both gates, **stop and flag it**. Backtest and paper
paths are exempt; the boundary between them must be explicit in the type system, not a
runtime flag.

---

## 📦 Pydantic Structured Outputs

```python
from pydantic import BaseModel, Field
from typing import Literal

class QueryResponse(BaseModel):
    """Structured output for every AI query."""
    answer: str = Field(..., description="Natural language answer to the user's question")
    generated_code: str = Field(default="", description="Generated code shown to user")
    chart_type: str | None = Field(default=None, description="bar, line, pie, or None")
    confidence: Literal["high", "medium", "low"] = Field(
        ..., description="Model confidence in the answer"
    )
    tokens_used: int = Field(..., ge=0, description="Total tokens consumed")
    latency_ms: float = Field(..., ge=0.0, description="Response latency in ms")
```

### Rules
- ✅ Use `Field()` with `description=` — doubles as LLM JSON schema documentation
- ✅ Use validators (`ge`, `le`, `pattern`, `max_length`) — catch bad data early
- ✅ Use `Literal` or `Enum` for constrained string fields
- ✅ Use `model_validate()` for external data (API responses, files) — not `__init__()`
- ✅ Use `frozen=True` for configs that shouldn't change after creation
- ❌ Don't use plain dicts where Pydantic adds safety
- ❌ Don't skip Field descriptions — they feed into LLM JSON schemas
- ❌ Don't catch `ValidationError` silently — log and handle explicitly

---

## 🛡️ Guardrails

```python
# src/ai/guardrails.py — Governance as code

# ✅ PII leak prevention (scan BEFORE displaying response)
PII_PATTERNS = {
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
    "email": r"\b[\w.-]+@[\w.-]+\.\w+\b",
}

# ✅ Query scope validation (block dangerous operations)
BLOCKED_OPERATIONS = ["DELETE", "UPDATE", "INSERT", "DROP", "os.", "subprocess"]

# ✅ Response validation pipeline
# 1. Validate with Pydantic schema
# 2. Scan for PII patterns (regex)
# 3. Check for blocked content
# 4. Inject disclaimer
# 5. Log to observability
```

### Rules
- PII scan runs on EVERY AI response before display — no exceptions
- Query validation runs BEFORE sending to LLM — reject dangerous queries early
- Test coverage on guardrail functions must be >90%
- Log blocked queries and reasons (but never log PII itself)

> **This is Layer 3 of the defense-in-depth model** and is distinct from the log
> redaction processor in `observability.mdc` (Layer 1). Both exist deliberately;
> neither replaces the other.

> **Stage fit:** regex PII + keyword blocklists are the honest **Stage-1 baseline** — cheap,
> transparent, testable. They are also bypassable, so graduate to dedicated tooling as an
> *earned overlay* when the project warrants it: Microsoft **Presidio** for PII detection,
> and a guardrails layer (e.g. NeMo Guardrails / structured output validation) for
> injection defense. Don't add the heavier layer until a baseline gap justifies it.

---

## 📊 Observability

```python
# src/ai/observability.py
import structlog

log = structlog.stdlib.get_logger(__name__)

# ✅ Log per-query metrics (provider/model come from config — never hardcoded).
# Kwargs, not extra={} — see observability.mdc § Structured Logging.
log.info(
    "ai_query_completed",
    provider=provider_name,           # e.g. "ollama", "anthropic", "openrouter"
    model=model_name,                 # e.g. "qwen3.5", "claude-sonnet-4-6"
    tokens_used=usage.total_tokens,
    latency_ms=elapsed_ms,
    estimated_cost=cost,              # 0.0 for local Ollama
    guardrail_triggered=False,
)

# ✅ Bind once per query — every downstream line (including the SDK's own httpx
# logs) inherits query_id, so one filter reconstructs the whole call.
structlog.contextvars.clear_contextvars()
structlog.contextvars.bind_contextvars(query_id=query_id, provider=provider_name)
```

### Canonical event names (stable — renaming breaks dashboards)

| Event | Emitted when |
|---|---|
| `ai_query_started` | after guardrail validation, before the SDK call |
| `ai_query_completed` | on success, with tokens/latency/cost |
| `ai_query_failed` | on SDK error, after retries are exhausted |
| `guardrail_blocked` | query or response rejected — include `reason`, never the PII |
| `schema_validation_failed` | Pydantic rejected the LLM response |
| `human_signoff_required` | an irreversible action is awaiting approval (Crucible) |
| `killswitch_engaged` | execution halted out-of-band |

### Retries on provider calls

```python
import stamina

# Retry transient transport/rate-limit failures only. Never retry a schema
# validation failure — a malformed response will be malformed again.
@stamina.retry(on=(httpx.HTTPError, RateLimitError), attempts=3, timeout=60.0)
def _call_provider(prompt: str) -> ProviderResponse:
    ...
```

Because `stamina` detects `structlog`, each scheduled retry is logged automatically
with its own structured event — retry storms become visible without extra code.

> **SDK currency (2026):** if a project uses Gemini for *public* data, use the unified
> `google-genai` client (`from google import genai; client = genai.Client()`), not the
> deprecated `google.generativeai` package. **The free Gemini tier is off-limits for any
> project data** — it may be used for model training. For heavier/local tracing, graduate
> observability to OpenTelemetry-based tooling (Langfuse / Arize Phoenix / LangSmith).

### Rules
- Every AI call logs: provider, model, tokens, latency, cost, guardrail status
- AI logs are **derived, not separate** — emit to stdout like everything else and filter
  on `logger` / event name downstream. A second file handler duplicates and interleaves.
- **Cost is a first-class metric, not a nice-to-have** — it feeds the README's ② Cost
  section directly (see `architecture-docs.mdc`). Track cost-per-query from day one.
- Cost estimation uses published API pricing (update when rates change)
- Surface metrics in the Streamlit sidebar for transparency
- **Never log prompt or completion bodies at INFO.** Log shape and identifiers — token
  counts, hashes, ids. Bodies at DEBUG only, and the redaction processor still applies.

---

## 🔁 Provider Abstraction

```python
class AIProvider:
    """Swap providers via config — zero code changes.

    Default routing is privacy-first: sensitive/proprietary projects use local
    Ollama; public projects may use a cloud provider. Selection comes from config,
    never hardcoded.
    """

    def __init__(self, provider: str | None = None):
        # Resolve from config/env; fall back to local Ollama for safety.
        self.provider = provider or settings.ai_provider  # e.g. "ollama"
        self._client = self._init_client()

    def query(self, question: str, context: str) -> QueryResponse:
        """Send query, get Pydantic-validated response."""
        # 1. Validate query (guardrails)
        # 2. Build prompt with context
        # 3. Call LLM SDK with structured output schema
        # 4. Validate response (Pydantic)
        # 5. Scan response (PII guardrails)
        # 6. Log metrics (observability)
        # 7. Return validated QueryResponse
        ...
```

### Rules
- Provider selection via `settings.ai_provider` (pydantic-settings) — never hardcoded
- **The fallback is always local, never cloud.** A misconfigured provider must fail
  closed toward privacy.
- Retries via `stamina` — capped attempts AND total time, jittered backoff, transient
  errors only (never on `ValidationError`)
- Timeout: `settings.request_timeout_s`, 30 seconds default
- API keys typed `SecretStr`; unwrapped only at the client constructor
- Fallback: if primary provider fails, try secondary — **within the same privacy tier**

---

## ✅ AI Module Checklist (Before Commit)

- [ ] All LLM responses validated through Pydantic schemas
- [ ] PII scan runs on every response before display
- [ ] Query validation blocks dangerous operations
- [ ] Token/cost/latency logged per query via structlog kwargs (not `extra={}`)
- [ ] `query_id` bound to contextvars so SDK/httpx logs correlate
- [ ] No prompt/completion bodies logged at INFO
- [ ] Provider retries use `stamina`; schema failures are NOT retried
- [ ] Provider switchable via config, fallback is local (not hardcoded, not cloud)
- [ ] Workflow vs agent classified explicitly in the ADR and README
- [ ] Any irreversible action path has human sign-off **and** a kill-switch
- [ ] Disclaimer injected on every AI response
- [ ] Guardrail functions have >90% test coverage
- [ ] App degrades gracefully without API key

You are a **security & privacy auditor** for a financial-services data context.
Read-only. You report risks; you do not fix them.

Check for:

**Secrets**
- Hardcoded API keys, tokens, passwords, connection strings.
- Every credential typed `SecretStr`, unwrapped only at the client constructor via
  the explicit `.get_secret_value()`. A plain `str` credential is a finding even if
  it comes from the environment.
- Config read through `settings` (`pydantic-settings`) — **raw `os.environ` /
  `os.getenv` reads are a violation**: untyped, unvalidated, and scattered.
- `.env` git-ignored; `.env.example` committed with **empty** values.
- Secrets baked into Dockerfiles or passed as build args.

**PII exposure**
- SSNs, account numbers, names, DOB in logs, error messages, exceptions, or
  committed data files. Verify masking (e.g. `***-**-1234`).
- Confirm all three defense layers are intact and none is doing the others' job:
  1. the `redact_pii` processor in the structlog chain (unbypassable choke point),
  2. `SecretStr` on credentials,
  3. masking helpers at display boundaries (Streamlit, reports, exports).
  The response-side PII scan in `src/ai/guardrails.py` is a fourth, separate control
  on LLM output before display — verify it runs on **every** response.
- Real data under `data/` headed for Git. Only `data/synthetic/` is committed.

**Unsafe logging**
- **Any interpolation of payload data into a log message is a finding** — both
  f-strings *and* `%s` / `%d` style. The event name must be a stable `snake_case`
  identifier and all data must travel as structlog kwargs. Flag both forms; the
  `%`-lazy-format idiom is correct for plain stdlib and **wrong** in this codebase.
- `print()` anywhere outside `scripts/`.
- Prompt or completion bodies logged at INFO. Bodies are DEBUG-only; log shape,
  token counts and identifiers instead.
- `basicConfig()` or `structlog.configure()` called inside a library module rather
  than once at the entrypoint.
- A second handler writing the same stream (duplicated/interleaved lines).
- `clear_contextvars()` missing before `bind_contextvars()` — run context bleeds
  across requests, so run B's logs carry run A's identifiers.

**Provider routing**
- Provider must come from `settings.ai_provider`, never hardcoded, and the
  **fallback must be local, not cloud**. This is a rule about the *code you are
  auditing*, and it still holds even though this harness itself has no local path.
- Free / training-eligible tiers used with any project data.
- Sensitive values in URLs or query strings.

**Packaging & supply chain**
- Any `requirements.txt` present (the standard is `pyproject.toml` + `uv.lock`).
- `pip install` in a Dockerfile — the idiom is `uv sync --frozen`.
- `uv.lock` missing or out of sync with `pyproject.toml`.

**Error handling**
- Broad `except: pass`; silently swallowed `ValidationError`.
- Retries on non-transient failures, or on non-idempotent writes without an
  idempotency key.

**Diff scope**
- Scan `git diff` for anything sensitive about to be staged, including test fixtures
  and notebook output cells.

Output:
- 🔴 **Blocking** — must fix before staging (`file:line`, what's exposed, why).
- 🟡 **Caution** — should fix (with the one-line remediation).
- 🟢 **Clean** — what you verified.

Report only — no edits. I remediate after reviewing.
