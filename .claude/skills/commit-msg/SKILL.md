---
description: Generate a conventional-commits message for the currently staged changes. Does not commit.
argument-hint: "[optional scope hint]"
allowed-tools: Read, Bash(cat *), Bash(git diff:*), Bash(git status:*), Bash(git log:*)
model: haiku
context: fork
agent: Explore
background: false
disable-model-invocation: true
---

<!-- This file is a STUB. The instructions live once, at
     .github/docs/prompts/commands/commit-msg.md, and are shared with OpenCode.
     Edit the prompt file, not this one. Only the settings above belong here.
     The line below runs `cat` and pastes the file's text in before Claude reads
     it, so Claude receives the full instructions, not a pointer. -->

!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/commit-msg.md`
