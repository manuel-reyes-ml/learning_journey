---
description: Create or update the standard GitHub label taxonomy for a repo and regenerate the label reference. WRITES TO GITHUB.
agent: plan-cloud
model: opencode-go/minimax-m3#thinking
subagent: true
---

<!-- Two level-1 bang-backtick lines only. Shell lives in .github/scripts/labels_run.sh; the body at
     .github/docs/prompts/commands/labels.md is instructions-only. Bang-backtick substitution is
     single-pass, so shell written inside the imported body never executes (ADR-0001).
     Do not add ad-hoc bang-backtick lines here — extend the script instead (ADR-0003).
     AGENT CHOICE: the GitHub write happens in the level-1 script, before any
     agent exists. The agent only reads the result and reports, so it is
     deliberately the READ-ONLY plan-cloud, not build.
     NEVER put a bang right before a backtick anywhere in this comment: the harness runs
     that as shell, comments included (found 2026-11-19; guarded by
     scripts/tests/test_command_templates.py). -->

!`bash .github/scripts/labels_run.sh $ARGUMENTS`

!`cat .github/docs/prompts/commands/labels.md`
