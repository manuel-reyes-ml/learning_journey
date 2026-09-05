---
description: Generate a conventional-commits message for the currently staged changes. Does not commit.
agent: plan-cloud               # permissions from plan-cloud
model: opencode-go/minimax-m3   # but run on M3
subtask: true                   # keep it out of your context
---

<!-- Two level-1 `!` lines only. Shell lives in .github/scripts/commit_msg_context.sh; the body at
     .github/docs/prompts/commands/commit-msg.md is instructions-only. `!` substitution is
     single-pass, so shell written inside the imported body never executes (ADR-0001).
     Do not add ad-hoc `!` here — extend the script instead (ADR-0003). -->
 
!`bash .github/scripts/commit_msg_context.sh`
 
!`cat .github/docs/prompts/commands/commit-msg.md`