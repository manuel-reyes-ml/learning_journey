Generate a complete Agent Task Brief for Issue #$1.

Issue details:
!`gh issue view $1`

Issue revision stamp:
!`gh issue view $1 --json updatedAt --jq .updatedAt`

Modules in scope:
!`find src tests -name '*.py' | head -100`

Existing decision records:
!`ls docs/adr 2>/dev/null || echo "no docs/adr yet"`

Prior brief for this Issue, if one exists:
!`cat .github/plans/issue-$1-task-brief.md 2>/dev/null || echo "no prior brief"`

## Read the template before writing anything

**Read `.github/docs/templates/task_brief.md` in full, with the Read tool, now.**

That file — not this one — defines the brief's section order, headings and wording.
This file defines only what goes *inside* each section. A brief written without the
template read is not a brief; it is an improvisation that will drift from every other
brief in `.github/plans/`.

Do **not** assume the template arrived via an `@` reference. This prompt body is
imported into the harness command file (`@` on OpenCode, `cat` on Claude Code), and
nested `@`/`!` references inside an imported body are **not** re-expanded. Read the
template by path, explicitly, with the tool.

If the template cannot be read, **STOP and report**. Do not improvise a structure.

**Same check on the context blocks above:** if any of them shows the literal command
instead of its output, the expansion did not run. Re-run it yourself with the tools you
have and say that you did. If you are not permitted to run it, **STOP** — do not write a
brief from missing Issue context.

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

If a file not listed in the Issue appears to need changes, flag it explicitly.
If the Issue implies a decision with a real rejected alternative and no ADR is planned,
say so — that is a gap in the Issue, not something to silently add.

## Persist the brief

Write the completed brief to `.github/plans/issue-$1-task-brief.md`.

The file must open with exactly this frontmatter block, filled in:

```
---
issue: $1
issue_updated_at: <the revision stamp printed above, verbatim>
branch: feature/$1-<short-description>
generated: <today's date, YYYY-MM-DD>
template: .github/docs/templates/task_brief.md
status: PROPOSAL
---
```

Rules governing the write — these are constraints, not suggestions:

1. **One file per Issue, deterministic name.** If `.github/plans/issue-$1-task-brief.md`
   already exists, overwrite it. Git history is the audit trail; do not create `-v2`,
   `-final`, or dated variants.
2. **Never set `status: APPROVED`.** The brief is written at `PROPOSAL` and stays there.
   Only I change that field, by hand. A brief still at `PROPOSAL` has not passed Gate 1
   and is not an execution contract.
3. **Staleness check.** If a prior brief was printed above and its `issue_updated_at`
   differs from the current revision stamp, state that explicitly at the top of your
   report — the Issue moved underneath the previous brief.
4. **This write is the Gate 1 deliverable, not implementation.** `.github/plans/` is the
   only path this command may write to. Any other write is out of scope — stop and report.
5. **If your harness denies the write, do not work around it.** Output the brief and
   state plainly that it was not persisted and why. Do not retry through a shell command,
   a different path, or a different agent.
6. **No proprietary or client data in the brief.** Same standard as the repository:
   synthetic or redacted only. If the Issue body contains real plan, participant or
   employer data, stop and report rather than copying it into a committed file.

Then output the brief in full for my review.

Do **NOT** start implementing — this is Gate 1.