---
description: Run the pytest suite and interpret the results, flagging fixture and hygiene gaps. Report only, no fixes.
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(uv run pytest:*), Bash(make test)
model: sonnet
context: fork
agent: Explore
background: false
disable-model-invocation: true
---

<!-- This file is a STUB. The instructions live once, at
     .github/docs/prompts/commands/test.md, and are shared with OpenCode.
     Edit the prompt file, not this one. Only the settings above belong here.
     The line below runs `cat` and pastes the file's text in before Claude reads
     it, so Claude receives the full instructions, not a pointer. -->

!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/test.md`
