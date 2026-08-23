---
description: Draft a production-grade README from the repo and the flagship template. Outputs Markdown; does not write files.
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(find *), Bash(ls *), Bash(git log:*)
model: sonnet
context: fork
agent: Explore
background: false
disable-model-invocation: true
---

<!-- This file is a STUB. The instructions live once, at
     .github/docs/prompts/commands/readme.md, and are shared with OpenCode.
     Edit the prompt file, not this one. Only the settings above belong here.
     The line below runs `cat` and pastes the file's text in before Claude reads
     it, so Claude receives the full instructions, not a pointer. -->

!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/readme.md`
