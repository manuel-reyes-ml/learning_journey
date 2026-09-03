Generate a complete Agent Task Brief for Issue #$1.

All context you need — the brief template, the Issue, its revision stamp, the modules
in scope, the existing ADRs, and any prior brief for this Issue — has already been
injected above this text by `.github/scripts/task_brief_context.sh`.

**Do not attempt to load any of it yourself.** This body contains no `!` blocks and no
`@` references by design: command-template substitution is single-pass, so a `!` or `@`
written here would arrive as literal text and silently never run. That is the defect
this structure exists to prevent — do not reintroduce it.

**First, check the context you were given.** If any block above is missing, empty, or
shows a line beginning `CONTEXT_ERROR`, **STOP and report which one**. Do not improvise
around missing context and do not try to fetch it another way.

The `BRIEF TEMPLATE` block above — not this file — defines the brief's section order,
headings and wording. This file defines only what goes *inside* each section. Follow the
template's structure exactly.

## Fill in every section of the template

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
- **Acceptance Criteria:** from the Issue + "no breaking changes" + "output compatible
  with downstream" + "`uv.lock` in sync if deps changed"
- **Edge Cases:** from the Issue + any found while reviewing the codebase; include
  idempotency (a retried write needs an idempotency key) where data is touched
- **Validation Commands:** the uv-native set —
  `uv sync --frozen` · `uv run python -c "import <package>"` · `uv run ruff check` ·
  `uv run ruff format --check` · `uv run mypy src/` · `uv run pytest -q` ·
  `uv run deepeval test run tests/test_eval.py` (if the project has eval gates)
- **Deliverable Summary** and **Stop Conditions:** keep the standard formats, including
  commit-gate status and the stop conditions for proprietary data reaching this harness
  and for a destructive edit without a capability audit

Every entry in **Files to Change** must correspond to a path that appeared in the
`MODULES IN SCOPE` block or is being newly created. Do not name a file you have not seen.

If a file not listed in the Issue appears to need changes, flag it explicitly.
If the Issue implies a decision with a real rejected alternative and no ADR is planned,
say so — that is a gap in the Issue, not something to silently add.

## Persist the brief

Write the completed brief to `.github/plans/issue-$1-task-brief.md`.

The file must open with exactly this frontmatter block, filled in:

```
---
issue: $1
issue_updated_at: <the revision stamp from the context above, verbatim>
branch: feature/$1-<short-description>
generated: <today's date, YYYY-MM-DD>
template: .github/docs/templates/task_brief.md
status: PROPOSAL
---
```

Rules governing the write — these are constraints, not suggestions:

1. **One file per Issue, deterministic name.** If the file already exists, overwrite it.
   Git history is the audit trail; do not create `-v2`, `-final`, or dated variants.
2. **Never set `status: APPROVED`.** The brief is written at `PROPOSAL` and stays there.
   Only I change that field, by hand. A brief still at `PROPOSAL` has not passed Gate 1
   and is not an execution contract.
3. **Staleness check.** If a prior brief appeared in the context and its
   `issue_updated_at` differs from the current revision stamp, state that at the top of
   your report — the Issue moved underneath the previous brief.
4. **This write is the Gate 1 deliverable, not implementation.** `.github/plans/` is the
   only path this command may write to. Any other write is out of scope — stop and report.
5. **If your harness denies the write, do not work around it.** Output the brief and say
   plainly that it was not persisted and why. Do not retry through a shell command, a
   different path, or a different agent.
6. **No proprietary or client data in the brief.** Synthetic or redacted only. If the
   Issue body contains real plan, participant or employer data, stop and report rather
   than copying it into a committed file.

Then output the brief in full for my review.

Do **NOT** start implementing — this is Gate 1.