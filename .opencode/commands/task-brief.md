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

Fill in every section of the template:
- **Metadata:** Issue #$1, branch `feature/$1-<short-description>`, today's date
- **Objective:** one paragraph from the Issue context
- **Hard Constraints:** keep the 5 standard constraints (no commits, minimal
  additive changes, gap-analysis-first, explain every diff, stop at each gate)
- **Files to Change:** table of exact paths, change type, reason per file
- **Execution Steps:** ordered, each ending with "STOP and report diff"
- **Acceptance Criteria:** from the Issue + "no breaking changes" + "output
  compatible with downstream"
- **Edge Cases:** from the Issue + any found while reviewing the codebase
- **Validation Commands:** `python -m compileall`, `pytest`, `make lint`, `make eval`
- **Deliverable Summary** and **Stop Conditions:** keep the standard formats

If a file not listed in the Issue appears to need changes, flag it explicitly.
Output the brief for my review. Do **NOT** start implementing — this is Gate 1.
