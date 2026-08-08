Draft a GitHub Issue for the goal described after this command.

Usage: `/draft-issue Add PII scanning for AI response guardrails`

1. Read `.github/ISSUE_TEMPLATE/task.md` for the required Issue format
2. Read `.github/docs/project_labels.md` for approved labels
3. Review all modules in `src/` to identify affected files globally
4. Run `ls docs/adr` to see which decisions are already recorded
5. Write a complete GitHub Issue following the template, including:

   - Context / problem statement
   - Packs in scope (DE / ML / LLM-RAG / Agentic / none) — ticked, and matching what the
     eventual task brief and PR will carry
   - Scope and non-scope
   - Implementation plan: files to change or add — include `docs/adr/` and `architecture.dsl`
     where applicable
   - **Decisions expected** — what has to be chosen and what the alternatives are. If a real
     alternative is likely to be rejected, mark that an ADR is required as part of the work
   - Acceptance criteria (checkboxes — explicit and testable)
   - Implementation notes (likely files and functions to change)
   - Edge cases — including idempotency where data is touched
   - Validation / smoke test plan using the uv-native commands: `uv sync --frozen`,
     `uv run pytest -q`, `uv run ruff check src/ tests/`, `uv run mypy src/`, and
     `uv run deepeval test run tests/test_eval.py` if the project has eval gates
   - Data & security: synthetic data only, `SecretStr` credentials, config via `settings`,
     privacy-first provider routing
   - Suggested labels from `.github/docs/project_labels.md` only — explain each choice
   - Risks / impact

6. Suggest a clear, outcome-focused Issue title in the template's `[<area>] <concise outcome>`
   form — state what changes, not who might be impressed by it
7. Output the final Issue body as a Markdown block I can copy and paste into GitHub
8. Do NOT create the Issue — I will create it manually