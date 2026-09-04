---
description: Create or update the standard GitHub label taxonomy for a repo and regenerate the label reference. WRITES TO GITHUB.
agent: build
model: opencode-go/minimax-m3
subtask: true
---

<!-- Two level-1 `!` lines only. Shell lives in .github/scripts/labels_run.sh; the body at
     .github/docs/prompts/commands/labels.md is instructions-only. `!` substitution is
     single-pass, so shell written inside the imported body never executes (ADR-0001).
     Do not add ad-hoc `!` here — extend the script instead (ADR-0003).
     AGENT CHOICE: the GitHub write happens in the level-1 script, before any agent
     exists. The agent only reads the result and reports, so it is deliberately the
     READ-ONLY plan-cloud, not build. -->
 
!`bash .github/scripts/labels_run.sh $ARGUMENTS`
 
!`cat .github/docs/prompts/commands/labels.md`