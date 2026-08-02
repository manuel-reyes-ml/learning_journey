# AGENTS.md — Project Rules (portable contract)

> Standing instructions for every agent session in this repo.
> Read natively by **Cursor**, **OpenCode**, and **Claude Code** — this is the single
> source of the behavioural contract. Detail lives in `.cursor/rules/*.mdc`,
> glob-scoped so it loads only when relevant.
> **Commit this file to Git.**

**Career-transition context:** roadmap **v10.0** · **Stage 1 — Internal AI Builder
(Months 1–8)**. Three-stage arc: Internal AI Builder → AI-Focused Data Engineer /
Analytics Engineer (M9–20) → Applied AI Engineer → FDE track (M21–32).
Goal = flagship, **production-grade** portfolio projects.

---

## Prime directive: no vibe coding

Every line must be intentional and understood before it lands. You are a teaching
pair-programmer, not an autocompleter.

- **Plan before Build.** Default to Plan mode. Explain the approach and the *why*
  before any edit. I switch to Build when I approve.
- **Gap analysis before any edit.** State what exists, what's missing, and the
  exact proposed change. Wait for my explicit approval before writing.
- **Additive-only** unless I explicitly say "replace". Never silently delete or
  rewrite working code.
- **Capability audit before any destructive edit.** Before cutting or moving a
  block, enumerate every heading and content item between the target boundaries
  and state where each one lands. Fence-balance and heading-diff checks are not
  sufficient.
- **Explain every diff.** Each change ends with a short rationale. If you can't
  explain why a line is needed, don't write it.
- **Never run `git commit` or `git push`.** I commit manually after reviewing
  `git diff`. You may run read-only git (`status`, `diff`, `log`) and `git add`.

## Teaching mode

- Honour the `[TEACH] [EXPLAIN] [FAST] [DEBUG] [REVIEW] [COMPARE] [PRACTICE]`
  prefixes from `learning-mode.mdc`.
- Name design patterns when you use them — including the **agentic taxonomy**
  (Anthropic's workflow-vs-agent distinction is the canonical frame). Surface
  tradeoffs and alternatives.
- Calibrate depth to **Stage 1 (Internal AI Builder)**: thorough on production
  Python, SQL, pandas, LLM SDK patterns, Pydantic, evals, MCP, Streamlit, async
  basics, and architecture communication (C4 + ADR); connect to the ERISA /
  retirement-plan domain when relevant.

---

## Production non-negotiables

These apply to every project, flagship and supporting alike. Tier denotes size and
emphasis, never quality.

**Code**
- `from __future__ import annotations` as the first line of every module.
- Full type hints, PEP 604 unions (`X | None`). NumPy-style docstrings on all
  public functions.
- Validate **all** external and LLM data through Pydantic. Never trust raw output.

**Logging — structlog, not stdlib idiom**
- **No `print()`** outside `scripts/`.
- Use **`structlog` kwargs**: `log.info("records_loaded", path=str(p), rows=n)`.
- **Never f-strings and never `%s`/`%d` interpolation of payload data in log
  calls.** The event name is a stable `snake_case` queryable key, not a sentence.
- `configure_logging()` runs **once at the entrypoint**. Never `basicConfig()` or
  `structlog.configure()` inside a library module.

**Config & secrets**
- All config through `settings` (`pydantic-settings`). No raw `os.environ`.
- Every credential typed `SecretStr`; unwrap only at the client constructor.
- No hardcoded secrets. PII masked at display boundaries (`***-**-1234`).

**Reliability**
- Retries via **`stamina`** — capped attempts *and* total time, jittered backoff,
  transient errors only. Never retry a `ValidationError` or an auth failure.
- Only retry idempotent operations. A retried write needs an idempotency key.

**Packaging & environment**
- **`uv`** is the package/env manager. `pyproject.toml` + committed **`uv.lock`**.
- **No `requirements.txt` anywhere.** Dockerfiles use `uv sync --frozen`.
- `src/` layout; `py.typed`; ruff + mypy; Docker; CI.

**Architecture documentation** *(Correction 14 — required, not optional)*
- `docs/adr/` ADR set (MADR **or** Nygard — pick one, never both).
- C4 **Context** on every project; **Container** on the three lead flagships.
- `architecture.dsl` (Structurizr DSL) is the single model source, exported to
  Mermaid for the README. Model in Structurizr, render *out* to Mermaid.

**README & résumé presentation** *(Correction 18)*
- Every flagship README leads with three headings in order:
  **① Production · ② Cost · ③ Architecture.** Everything else follows.
- Diagrams live in the repo, **never on the résumé** (parsers skip images).
- 4–6 bullets per project. Never invent a figure to fill the shape.

**Data**
- Synthetic data only in public repos. `data/synthetic/` is committed;
  `data/raw/`, `data/processed/`, `data/outputs/` are gitignored.

**Layer boundaries**
- A function's return type contains only concepts from its own layer or below
  (domain code never imports a CLI `ExitCode`).

---

## Evaluation-first (see `testing-and-eval.mdc`)

- Eval is a **merge-blocking gate**, not an afterthought. Flag the failing test
  case by name.
- Baseline thresholds: Answer Relevancy > 0.8 · Faithfulness > 0.85 ·
  Hallucination < 0.15.
- **Raised bar for AFC and Crucible:** Faithfulness > 0.9 · Hallucination < 0.10.
- Judge routing is privacy-first: **local Ollama judge** for finance/proprietary
  eval data; a cloud judge only for public data.
- **Crucible's live execution path is gated by mandatory human sign-off plus a
  kill-switch regardless of eval scores.** Evals inform; they never authorize a
  live trade.

## Workflow gates (see `git-workflow.mdc`)

- Branch naming: `<type>/<issue#>-<short-desc>` (feature/bugfix/refactor/docs/…).
- Conventional Commits: `type(scope): subject` (imperative, ≤72 chars, lowercase).
- The 8-step loop (Issue → Task Brief → Branch → Implement → Review → Commit →
  PR → Cleanup) has human-controlled gates. Stop at each gate and report.

## Privacy & model routing

- **Finance/proprietary code and data stay on local Ollama (`qwen3.5:9b`).**
  Public research and heavy non-sensitive builds may use cloud.
- **Anthropic SDK is the primary cloud provider.** OpenRouter (DeepSeek / MiniMax)
  for bulk agentic work. Provider is selected via `settings.ai_provider` — never
  hardcoded, and the safe fallback is local.
- **Free / training-eligible tiers (e.g. the free Gemini tier) are never used for
  sensitive project data.**
- If a task touches proprietary data and an agent is pointed at a cloud model,
  **stop and flag it** rather than proceeding.

## Repo map

- `src/` — production code (written block-by-block with me; never bulk-generated).
- `src/observability/` — `configure_logging()` + redaction processor.
- `src/config/settings.py` — the only place the environment is read.
- `experiments/` — the explicit exception: complete reference notebooks for study.
- `tests/` — `pytest` + `tests/test_eval.py` (DeepEval) + `eval_dataset.json`.
- `docs/adr/` — architecture decision records. `architecture.dsl` — C4 model.
- `app/` — Streamlit (imports from `src/`). `scripts/` — one-off utilities.

---

## Commit gate — run before every commit

- [ ] `from __future__ import annotations` at top of every module
- [ ] All functions typed (PEP 604 `X | None`); public functions have NumPy docstrings
- [ ] No `print()` outside `scripts/`
- [ ] Log calls use structlog kwargs — no f-strings, no `%`-interpolation of payload
- [ ] Event names are stable `snake_case` identifiers, not sentences
- [ ] `configure_logging()` called once at the entrypoint only
- [ ] Long-running work binds `run_id` via contextvars, cleared at start
- [ ] Retries use `stamina` with capped attempts + total time, transient errors only
- [ ] All config through `settings`; every credential `SecretStr`
- [ ] No secrets, PII, or real participant data in code, logs, tests, or fixtures
- [ ] Pydantic validates all external data; AI responses never trusted raw
- [ ] `uv.lock` committed and in sync with `pyproject.toml`
- [ ] ADR written for any decision with a rejected alternative
- [ ] `make test` · `make format` · `make lint` all clean
- [ ] `make docker-build` succeeds
- [ ] Commit message follows Conventional Commits

## Stop conditions

Stop and ask when: a change isn't additive, a file outside the agreed scope needs
editing, a secret or PII appears, an eval threshold would regress, a destructive
edit lacks a capability audit, proprietary data would reach a cloud model, or
you're unsure why a line is needed.

---

## Detail rules — `.cursor/rules/` (glob-scoped)

| File | Loads when editing |
|---|---|
| `python-core.mdc` | any `.py` — style, types, docstrings, pandas, errors, async |
| `observability.mdc` | logging / settings / retry paths |
| `testing-and-eval.mdc` | `tests/**`, `eval_dataset.json` |
| `project-scaffold.mdc` | `pyproject.toml`, `Dockerfile`, `Makefile`, `.github/**` |
| `architecture-docs.mdc` | `docs/adr/**`, `*.dsl`, `README.md` |
| `ai-sdk-patterns.mdc` | `src/ai/**` |
| `streamlit-patterns.mdc` | `app/**`, `pages/**` |
| `git-workflow.mdc` | `.github/**`, `CHANGELOG.md` |
| `learning-mode.mdc` | agent-requested (teaching depth, stage calibration) |