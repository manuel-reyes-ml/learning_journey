---
description: Generate a complete Agent Task Brief for a GitHub Issue number — Gate 1, no implementation.
argument-hint: "[issue-number]"
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(gh issue view:*), Bash(find *), Bash(ls *)
model: sonnet
context: fork
agent: Plan
background: false
disable-model-invocation: true
---

<!-- This file is a STUB. The instructions live once, at
     .github/docs/prompts/commands/task-brief.md, and are shared with OpenCode.
     Edit the prompt file, not this one. Only the settings above belong here.
     The line below runs `cat` and pastes the file's text in before Claude reads
     it, so Claude receives the full instructions, not a pointer. -->

!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/task-brief.md`
