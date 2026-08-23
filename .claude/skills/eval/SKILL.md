---
description: Run the AI evaluation suite and report scores against thresholds (RAG, agentic, GEval), and confirm the CI gate is real.
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(grep *), Bash(uv run deepeval:*), Bash(make eval)
context: fork
agent: eval-guardian
background: false
disable-model-invocation: true
---

<!-- This file is a STUB. The instructions live once, at
     .github/docs/prompts/commands/eval.md, and are shared with OpenCode.
     Edit the prompt file, not this one. Only the settings above belong here.
     The line below runs `cat` and pastes the file's text in before Claude reads
     it, so Claude receives the full instructions, not a pointer. -->

!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/eval.md`
