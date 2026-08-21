---
description: Scouts current production-grade patterns and compares them to this codebase. Read-only, can fetch docs/the web. Use to find better, newer approaches. Invoke with @pattern-scout.
mode: subagent
model: opencode-go/kimi-k3
temperature: 0.2
permission:
  edit: deny
  webfetch: allow
  websearch: allow
  bash:
    "*": deny
    "git diff*": allow
    "grep *": allow
    "ls *": allow
    "find *": allow
---

{file:./.cursor/rules/ai-sdk-patterns.mdc}

<!-- Shared instructions. Edit .github/docs/prompts/agents/pattern-scout.md, not this file. -->

{file:./.github/docs/prompts/agents/pattern-scout.md}

> 🔒 **OpenCode note:** this agent reads source code AND uses cloud models + the web.
> For a finance/proprietary repo, switch `model` to `ollama/qwen3.5:9b` and set
> `webfetch`/`websearch` to `deny` before running.
