Generate a complete Cursor Agent Task Brief for the Issue number provided after this command.

Usage: `/task-brief 12` (where 12 is the GitHub Issue number)

1. Read `.github/docs/templates/cursor_task_brief.md` for the required Task Brief format
2. Fetch the Issue details: run `gh issue view <number>` to get scope, acceptance criteria, and context
3. Review all modules in `src/` and `tests/` to identify the exact files that need to change
4. Run `ls docs/adr` to see which decisions are already recorded
5. Fill in every section of the template:

   - **Metadata:** Issue number, branch name (`feature/<number>-<short-description>`),
     today's date, and packs ticked to match the Issue
   - **Objective:** One paragraph from the Issue context
   - **Hard Constraints:** Keep all **9** standard constraints verbatim — no commits or
     pushes · additive-first · gap-analysis-before-edit plus a capability audit on any
     destructive edit · no behavior change outside scope · the production standard
     (structlog kwargs, `settings`, `stamina`, uv + `uv.lock`) · testable changes ·
     no secrets or real client data · propose-and-pause autonomy limit · an ADR where a
     real alternative is rejected
   - **Files to Change:** Table with exact file paths, change type, and reason for each.
     Include `docs/adr/000N-....md` if this task involves a decision with a real rejected
     alternative, and `architecture.dsl` if containers or boundaries change
   - **Execution Steps:** Ordered steps with specific edits, each ending with "STOP and report diff"
   - **Acceptance Criteria:** Copy from Issue + add "no breaking changes", "output compatible
     with downstream", and "`uv.lock` in sync if deps changed"
   - **Edge Cases:** From the Issue + any you discover from reviewing the codebase. Include
     idempotency where data is touched — a retried write needs an idempotency key
   - **Validation Commands:** the uv-native set — `uv sync --frozen`,
     `uv run python -c "import <package>"`, `uv run ruff check src/ tests/`,
     `uv run ruff format --check src/ tests/`, `uv run mypy src/`, `uv run pytest -q`,
     and `uv run deepeval test run tests/test_eval.py` if the project has eval gates
   - **Deliverable Summary:** Keep the standard **7-item** format (what changed · files
     changed · key logic decisions · what to review in `git diff` · validation commands ·
     pack-specific results · commit-gate status)
   - **Stop Conditions:** Keep the standard **7** stop conditions, including proprietary data
     reaching a cloud model and a destructive edit without a capability audit

6. If any file not listed in the Issue appears to need changes, flag it explicitly
7. If the Issue implies a decision with a real rejected alternative and no ADR is planned,
   say so — that is a gap in the Issue, not something to silently add
8. Save the completed brief to `.cursor/plans/issue-<number>-task-brief.md`
9. Output the brief so I can review and approve before implementation begins
10. Do NOT start implementing — brief review is Gate 1