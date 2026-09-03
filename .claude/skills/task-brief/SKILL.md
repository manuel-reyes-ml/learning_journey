---
description: Generate a complete Agent Task Brief for a GitHub Issue number — Gate 1, no implementation.
argument-hint: "[issue-number]"
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(bash .github/scripts/*)
model: sonnet
context: fork
agent: Plan
background: false
disable-model-invocation: true
---

<!-- This file is a STUB. The instructions live once, at
     .github/docs/prompts/commands/task-brief.md, and are shared with OpenCode.
     Edit the prompt file, not this one. Only the settings above belong here.

     BOTH lines below run at level 1. That is deliberate: `!` substitution is
     single-pass, so shell written inside the imported body would arrive as
     literal text and never execute (verified on OpenCode 1.17.9, probe v4).
     The context script is the single source for that shell; the body is
     instructions only. -->

!`bash ${CLAUDE_PROJECT_DIR}/.github/scripts/task_brief_context.sh $1`

!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/task-brief.md`