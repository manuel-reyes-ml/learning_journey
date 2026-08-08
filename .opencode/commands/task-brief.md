---
description: Generate a Task Brief for a GitHub Issue number — Gate 1, no implementation
agent: plan
---

Generate a complete Agent Task Brief for Issue #$1.

Issue details:
!`gh issue view $1`

Task Brief format: @.github/docs/templates/cursor_task_brief.md

Modules in scope:
!`find src tests -name '*.py' | head -100`

Existing decision records:
!`ls docs/adr 2>/dev/null || echo "no docs/adr yet"`

Fill in every section of the template:
- **Metadata:** Issue #$1, branch `feature/$1-<short-description>`, today's date,
  packs ticked to match the Issue
- **Objective:** one paragraph from the Issue context
- **Hard Constraints:** keep all **9** standard constraints verbatim (no commits/pushes ·
  additive-first · gap-analysis-before-edit + capability audit on destructive edits ·
  no out-of-scope behavior change · the production standard (structlog kwargs, `settings`,
  `stamina`, uv/`uv.lock`) · testable changes · no secrets or real client data ·
  propose-and-pause autonomy limit · ADR required where an alternative is rejected)
- **Files to Change:** table of exact paths, change type, reason per file — include
  `docs/adr/000N-….md` if this task involves a decision with a real rejected alternative,
  and `architecture.dsl` if containers or boundaries change
- **Execution Steps:** ordered, each ending with "STOP and report diff"
- **Acceptance Criteria:** from the Issue + "no breaking changes" + "output
  compatible with downstream" + "`uv.lock` in sync if deps changed"
- **Edge Cases:** from the Issue + any found while reviewing the codebase; include
  idempotency (a retried write needs an idempotency key) where data is touched
- **Validation Commands:** the uv-native set —
  `uv sync --frozen` · `uv run python -c "import <package>"` · `uv run ruff check` ·
  `uv run ruff format --check` · `uv run mypy src/` · `uv run pytest -q` ·
  `uv run deepeval test run tests/test_eval.py` (if the project has eval gates)
- **Deliverable Summary** and **Stop Conditions:** keep the standard formats, including
  commit-gate status and the stop conditions for proprietary data reaching a cloud model
  and for a destructive edit without a capability audit

If a file not listed in the Issue appears to need changes, flag it explicitly.
If the Issue implies a decision with a real rejected alternative and no ADR is planned,
say so — that is a gap in the Issue, not something to silently add.

Output the brief for my review. Do **NOT** start implementing — this is Gate 1.