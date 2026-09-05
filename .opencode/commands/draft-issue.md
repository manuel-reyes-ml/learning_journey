---
description: Draft a production-grade GitHub Issue from a one-line goal. Outputs Markdown; does not create the Issue.
agent: plan-cloud
model: opencode-go/minimax-m3
subtask: true
---

<!-- Two level-1 `!` lines only. Shell lives in .github/scripts/draft_issue_context.sh; the body at
     .github/docs/prompts/commands/draft-issue.md is instructions-only. `!` substitution is
     single-pass, so shell written inside the imported body never executes (ADR-0001).
     Do not add ad-hoc `!` here — extend the script instead (ADR-0003). -->
 
!`bash .github/scripts/draft_issue_context.sh`
 
!`cat .github/docs/prompts/commands/draft-issue.md`