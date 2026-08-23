---
description: Production-readiness review of the working tree — lint, format, types, tests, lock sync, then a static standards audit. Report only, no fixes.
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(uv run:*), Bash(uv lock:*), Bash(git diff:*), Bash(git status:*)
model: sonnet
context: fork
agent: Explore
background: false
disable-model-invocation: true
---

<!-- This file is a STUB. The instructions live once, at
     .github/docs/prompts/commands/review.md, and are shared with OpenCode.
     Edit the prompt file, not this one. Only the settings above belong here.
     The line below runs `cat` and pastes the file's text in before Claude reads
     it, so Claude receives the full instructions, not a pointer. -->

!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/review.md`
