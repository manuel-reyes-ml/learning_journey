---
description: Draft a production-grade README from the repo and the flagship template. Outputs Markdown; does not write files.
agent: plan-cloud
model: opencode-go/minimax-m3
subtask: true
---

<!-- Two level-1 `!` lines only. Shell lives in .github/scripts/readme_context.sh; the body at
     .github/docs/prompts/commands/readme.md is instructions-only. `!` substitution is
     single-pass, so shell written inside the imported body never executes (ADR-0001).
     Do not add ad-hoc `!` here — extend the script instead (ADR-0003). -->
 
!`bash .github/scripts/readme_context.sh`
 
!`cat .github/docs/prompts/commands/readme.md`
