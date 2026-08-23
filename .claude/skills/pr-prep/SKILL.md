---
description: Generate a pull request description for the current branch. Outputs Markdown; does not create the PR.
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(git diff:*), Bash(git log:*), Bash(git branch:*)
model: sonnet
context: fork
agent: Explore
background: false
disable-model-invocation: true
---

<!-- This file is a STUB. The instructions live once, at
     .github/docs/prompts/commands/pr-prep.md, and are shared with OpenCode.
     Edit the prompt file, not this one. Only the settings above belong here.
     The line below runs `cat` and pastes the file's text in before Claude reads
     it, so Claude receives the full instructions, not a pointer. -->

!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/pr-prep.md`
