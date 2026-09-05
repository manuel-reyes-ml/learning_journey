---
description: Generate a pull request description for the current branch. Outputs Markdown; does not create the PR.
agent: plan-cloud
model: opencode-go/minimax-m3
subtask: true
---

<!-- Two level-1 `!` lines only. Shell lives in .github/scripts/pr_prep_context.sh; the body at
     .github/docs/prompts/commands/pr-prep.md is instructions-only. `!` substitution is
     single-pass, so shell written inside the imported body never executes (ADR-0001).
     Do not add ad-hoc `!` here — extend the script instead (ADR-0003). -->
 
!`bash .github/scripts/pr_prep_context.sh $1`
 
!`cat .github/docs/prompts/commands/pr-prep.md`