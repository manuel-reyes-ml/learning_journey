---
description: Draft a production-grade GitHub Issue from a one-line goal. Outputs Markdown; does not create the Issue.
argument-hint: "[one-line goal]"
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(find *), Bash(ls *)
model: sonnet
context: fork
agent: Explore
background: false
disable-model-invocation: true
---

<!-- This file is a STUB. The instructions live once, at
     .github/docs/prompts/commands/draft-issue.md, and are shared with OpenCode.
     Edit the prompt file, not this one. Only the settings above belong here.
     The line below runs `cat` and pastes the file's text in before Claude reads
     it, so Claude receives the full instructions, not a pointer. -->

!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/draft-issue.md`
