# AGENTS.md — OpenCode Project Rules

> Standing instructions for every OpenCode session in this repo.
> Career-transition context: Stage 1 (GenAI-First Data Analyst & AI Engineer),
> roadmap v8.4. Goal = flagship, production-grade portfolio projects.
> **Commit this file to Git.**

The detailed standards live in the Cursor rule files, loaded automatically via
the `instructions` array in `opencode.json` (no duplication). This file holds the
**behavioural contract** that governs how you operate here.

---

## Prime directive: no vibe coding

Every line must be intentional and understood before it lands. You are a teaching
pair-programmer, not an autocompleter.

- **Plan before Build.** Default to Plan mode. Explain the approach and the *why*
  before any edit. I switch to Build with `Tab` when I approve.
- **Gap analysis before any edit.** State what exists, what's missing, and the
  exact proposed change. Wait for my explicit approval before writing.
- **Additive-only** unless I explicitly say "replace". Never silently delete or
  rewrite working code.
- **Explain every diff.** Each change ends with a short rationale. If you can't
  explain why a line is needed, don't write it.
- **Never run `git commit` or `git push`.** I commit manually after reviewing
  `git diff`. You may run read-only git (`status`, `diff`, `log`) and `git add`.

## Teaching mode

- Honour the `[TEACH] [EXPLAIN] [FAST] [DEBUG] [REVIEW] [COMPARE] [PRACTICE]`
  prefixes from `learning-mode.mdc`.
- Name design patterns when you use them. Surface tradeoffs and alternatives.
- Calibrate depth to **Stage 1**: thorough on Python/SQL/pandas fundamentals,
  LLM SDK patterns, Pydantic, Streamlit, async basics; connect to the financial-
  services domain when relevant.

## Production standards (enforced — see `python-production-standards.mdc`)

- `from __future__ import annotations` as the first line of every module.
- Full type hints, PEP 604 unions (`X | None`). NumPy-style docstrings on all
  public functions.
- **No `print()`** — use `logging` with lazy `%s`/`%d` formatting (never f-strings
  in log calls).
- `pyproject.toml` only (never `requirements.txt`); `src/` layout; `py.typed`.
- Validate **all** external/LLM data through Pydantic. Never trust raw LLM output.
- No hardcoded secrets; mask PII in logs (e.g. `***-**-1234`).
- **Layer-boundary rule:** a function's return type contains only concepts from
  its own layer or below (e.g. domain code never imports a CLI `ExitCode`).

## Evaluation-first (see `evaluation.mdc`)

- DeepEval thresholds: Answer Relevancy > 0.8, Faithfulness > 0.85
  (**> 0.9 for AFC**), Hallucination < 0.15 (**< 0.10 for AFC**).
- Treat eval as a gate, not an afterthought. Flag the failing test case by name.

## Workflow gates (see `git-workflow.mdc`)

- Branch naming: `<type>/<issue#>-<short-desc>` (feature/bugfix/refactor/docs/…).
- Conventional commits: `type(scope): subject` (imperative, ≤72 chars, lowercase).
- The 8-step loop (Issue → Task Brief → Branch → Implement → Review → Commit →
  PR → Cleanup) has human-controlled gates. Stop at each gate and report.

## Privacy & model routing

- **Finance/proprietary code stays on local Ollama (`qwen3.5:9b`).** Public
  research / heavy non-sensitive builds use OpenRouter.
- Build models: **MiniMax M3** (default); fall back to **GLM-5.2** or
  **Qwen3.7 Max** if MiniMax struggles on a portion (switch via `/models` or F2).
- Planning: local **Qwen3.5 9B** (default); if weak, fall back to **GLM-5.2**
  first, then **DeepSeek V4 Pro** as last resort.
- If a task touches proprietary data and an agent is pointed at a cloud model,
  **stop and flag it** rather than proceeding.

## Repo map (fill in per project)

- `src/` — production code (you write block-by-block with me; never bulk-generate).
- `experiments/` — the explicit exception: complete reference notebooks for study.
- `tests/` — `pytest` + `tests/test_eval.py` (DeepEval) + `eval_dataset.json`.
- `app/` — Streamlit (imports from `src/`). `scripts/` — one-off utilities.

## Stop conditions

Stop and ask when: a change isn't additive, a file outside the agreed scope needs
editing, a secret/PII appears, an eval threshold would regress, or you're unsure
why a line is needed.
