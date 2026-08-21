---
description: Audits for hardcoded secrets, exposed PII, unsafe logging and config, and privacy-routing violations. Read-only, local model. Use before commits on finance/data work. Invoke with @security-auditor.
mode: subagent
model: opencode-go/glm-5.2
temperature: 0.0
permission:
  edit: deny
  webfetch: deny
  bash:
    "*": deny
    "grep *": allow
    "git diff*": allow
    "git log*": allow
    "ls *": allow
    "find *": allow
---

{file:./.cursor/rules/observability.mdc}

{file:./.cursor/rules/ai-sdk-patterns.mdc}

<!-- Shared instructions. Edit .github/docs/prompts/agents/security-auditor.md, not this file. -->

{file:./.github/docs/prompts/agents/security-auditor.md}

> 🔒 **OpenCode note:** this agent runs on a **local model** — proprietary code never
> leaves the machine. That guarantee is why it is safe to point at a regulated repo.
