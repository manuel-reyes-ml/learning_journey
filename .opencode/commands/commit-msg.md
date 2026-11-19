---
description: Generate a conventional-commits message for the currently staged changes. Does not commit.
agent: plan-cloud               # permissions from plan-cloud
model: opencode-go/minimax-m3#thinking   # but run on M3
subagent: true                   # V2: verify it stays out of your context
---

<!-- Two level-1 bang-backtick lines only. Shell lives in .github/scripts/commit_msg_context.sh; the body at
     .github/docs/prompts/commands/commit-msg.md is instructions-only. Bang-backtick substitution is
     single-pass, so shell written inside the imported body never executes (ADR-0001).
     Do not add ad-hoc bang-backtick lines here — extend the script instead (ADR-0003).
     NEVER put a bang right before a backtick anywhere in this comment: the harness runs
     that as shell, comments included (found 2026-11-19; guarded by
     scripts/tests/test_command_templates.py). -->

!`bash .github/scripts/commit_msg_context.sh`

!`cat .github/docs/prompts/commands/commit-msg.md`
