---
description: Run the pytest suite and interpret the results, flagging fixture and hygiene gaps. Report only, no fixes.
agent: plan-cloud
model: opencode-go/glm-5.2
subtask: true
---

<!-- Two level-1 `!` lines only. Shell lives in .github/scripts/test_context.sh; the body at
     .github/docs/prompts/commands/test.md is instructions-only. `!` substitution is
     single-pass, so shell written inside the imported body never executes (ADR-0001).
     Do not add ad-hoc `!` here — extend the script instead (ADR-0003). -->
 
!`bash .github/scripts/test_context.sh`
 
!`cat .github/docs/prompts/commands/test.md`