---
description: Generate a complete Agent Task Brief for a GitHub Issue number — Gate 1, no implementation.
agent: plan-cloud
model: opencode-go/minimax-m3
---

<!-- Two level-1 `!` lines only. Shell lives in .github/scripts/task_brief_context.sh; the body at
     .github/docs/prompts/commands/task-brief.md is instructions-only. `!` substitution is
     single-pass, so shell written inside the imported body never executes (ADR-0001).
     Do not add ad-hoc `!` here — extend the script instead (ADR-0003). -->
 
!`bash .github/scripts/task_brief_context.sh $1`
 
!`cat .github/docs/prompts/commands/task-brief.md`