---
description: Draft a production-grade GitHub Issue from a one-line goal (does not create it)
agent: plan-cloud
model: opencode-go/minimax-m3 
---

Draft a GitHub Issue for this goal: **$ARGUMENTS**

Reference material:
- Issue format: @.github/ISSUE_TEMPLATE/task.md
- Approved labels: @.github/docs/project_labels.md

Repository modules (to identify affected files):
!`find src -name '*.py' | head -100`

Existing decision records:
!`ls docs/adr 2>/dev/null || echo "no docs/adr yet"`

Write a complete Issue following the template, including:
- Context / problem statement
- Packs in scope (DE / ML / LLM-RAG / Agentic / none) — ticked, and matching what the
  eventual task brief and PR will carry
- Scope and non-scope
- Implementation plan: files to change/add — include `docs/adr/` and `architecture.dsl`
  where applicable
- **Decisions expected** — what has to be chosen and what the alternatives are. If a real
  alternative is likely to be rejected, mark that an **ADR is required** as part of the work.
- Acceptance criteria (explicit, testable checkboxes)
- Edge cases — including idempotency where data is touched
- Validation / smoke-test plan using the uv-native commands
  (`uv sync --frozen` · `uv run pytest -q` · `uv run ruff check` · `uv run mypy src/` ·
  `uv run deepeval test run tests/test_eval.py` if the project has eval gates)
- Data & security: synthetic data only, `SecretStr` credentials, config via `settings`,
  privacy-first provider routing
- Suggested labels — from `project_labels.md` ONLY — one sentence each on why
- Risks / impact

Also suggest a clear, outcome-focused Issue title in the template's
`[<area>] <concise outcome>` form — state what changes, not who might be impressed by it.

Output the final Issue body as one Markdown block I can paste into GitHub.
Do **NOT** create the Issue — I create it manually.