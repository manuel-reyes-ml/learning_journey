---
description: Runs the AI evaluation suite and reports scores vs thresholds — RAG, agentic, GEval; stricter 0.90 faithfulness for AFC/Crucible. Read + eval commands only, no edits. Invoke with @eval-guardian.
mode: subagent
model: opencode-go/kimi-k3
temperature: 0.0
permission:
  edit: deny
  webfetch: deny
  bash:
    "*": deny
    "deepeval *": allow
    "uv run deepeval*": allow
    "uv run pytest*": allow
    "pytest*": allow
    "make eval": allow
    "make test": allow
    "git diff*": allow
---

{file:./.cursor/rules/testing-and-eval.mdc}

<!-- Shared instructions. Edit .github/docs/prompts/agents/eval-guardian.md, not this file. -->

{file:./.github/docs/prompts/agents/eval-guardian.md}
