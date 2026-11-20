---
description: Generate a complete Agent Task Brief for a GitHub Issue number — Gate 1, no implementation.
agent: plan-cloud
model: opencode-go/minimax-m3#thinking
---

<!-- Two level-1 bang-backtick lines only. Shell lives in .github/scripts/task_brief_context.sh; the body at
     .github/docs/prompts/commands/task-brief.md is instructions-only. Bang-backtick substitution is
     single-pass, so shell written inside the imported body never executes (ADR-0001).
     Do not add ad-hoc bang-backtick lines here — extend the script instead (ADR-0003).
     NEVER put a bang right before a backtick anywhere in this comment: the harness runs
     that as shell, comments included (found 2026-11-19; guarded by
     scripts/tests/test_command_templates.py). -->

!`bash .github/scripts/task_brief_context.sh $1`

!`cat .github/docs/prompts/commands/task-brief.md`
