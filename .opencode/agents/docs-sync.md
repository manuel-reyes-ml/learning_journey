---
description: Reviews documentation against the actual codebase to find drift, including ADRs, C4 diagrams and README structure. Read-only. Invoke with @docs-sync.
mode: subagent
model: opencode-go/minimax-m3
temperature: 0.1
permission:
  edit: deny
  webfetch: deny
  bash:
    "*": deny
    "git diff*": allow
    "git log*": allow
    "grep *": allow
    "ls *": allow
    "find *": allow
---

{file:./.cursor/rules/architecture-docs.mdc}

<!-- Shared instructions. Edit .github/docs/prompts/agents/docs-sync.md, not this file. -->

{file:./.github/docs/prompts/agents/docs-sync.md}
