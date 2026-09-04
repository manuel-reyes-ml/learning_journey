---
description: Production-readiness review of the working tree — lint, format, types, tests, lock sync, then a static standards audit. Report only, no fixes.
agent: plan-cloud
model: opencode-go/kimi-k3
subtask: true
---

<!-- Two level-1 `!` lines only. Shell lives in .github/scripts/review_context.sh; the body at
     .github/docs/prompts/commands/review.md is instructions-only. `!` substitution is
     single-pass, so shell written inside the imported body never executes (ADR-0001).
     Do not add ad-hoc `!` here — extend the script instead (ADR-0003). -->
 
!`bash .github/scripts/review_context.sh`
 
!`cat .github/docs/prompts/commands/review.md`