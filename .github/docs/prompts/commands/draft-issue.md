Draft a GitHub Issue for this goal: **$ARGUMENTS**

All context you need has already been injected above this text by
`.github/scripts/draft_issue_context.sh`.

**Do not attempt to load any of it yourself.** This body contains no `!` blocks and no
`@` references by design: command-template substitution is single-pass, so either would
arrive as literal text and silently never run (ADR-0001).

**Check the context first.** If a block above is missing, empty, or shows a line
beginning `CONTEXT_ERROR`, **STOP and report which one**. Do not infer, reconstruct, or
reason from the rules files in place of the missing output.

The `ISSUE TEMPLATE` block defines the structure; follow it exactly. The `APPROVED
LABELS` block is the **only** permitted source of labels — if it reports
`CONTEXT_ERROR`, suggest no labels and say the reference is missing. Never invent a
label name.

Write a complete Issue following the template, including:
- Context / problem statement
- Packs in scope (DE / ML / LLM-RAG / Agentic / none) — ticked, and matching what the
  eventual task brief and PR will carry
- Scope and non-scope
- Implementation plan: files to change/add — include `docs/adr/` and `architecture.dsl`
  where applicable. Every path must appear in the `REPOSITORY MODULES` block or be
  newly created; do not name a file you have not seen.
- **Decisions expected** — what has to be chosen and what the alternatives are. If a
  real alternative is likely to be rejected, mark that an **ADR is required** as part of
  the work.
- Acceptance criteria (explicit, testable checkboxes)
- Edge cases — including idempotency where data is touched
- Validation / smoke-test plan using the uv-native commands
  (`uv sync --frozen` · `uv run pytest -q` · `uv run ruff check` · `uv run mypy src/` ·
  `uv run deepeval test run tests/test_eval.py` if the project has eval gates)
- Data & security: synthetic data only, `SecretStr` credentials, config via `settings`,
  privacy-first provider routing
- Suggested labels — from the `APPROVED LABELS` block ONLY — one sentence each on why
- Risks / impact

Check the `OPEN ISSUES` block and flag any existing Issue that overlaps this goal
rather than drafting a duplicate.

Also suggest a clear, outcome-focused Issue title in the template's
`[<area>] <concise outcome>` form — state what changes, not who might be impressed by it.

Output the final Issue body as one Markdown block I can paste into GitHub.
Do **NOT** create the Issue — I create it manually.