---
description: Updates documentation files directly (markdown, README, CHANGELOG, docs/). Edits docs ONLY, never code, never ADRs, never generated diagrams. The writable counterpart to docs-sync. Invoke with @docs-fix.
mode: subagent
model: opencode-go/minimax-m3
temperature: 0.1
permission:
  webfetch: deny
  bash:
    "*": deny
    "git diff*": allow
    "git log*": allow
    "grep *": allow
    "ls *": allow
    "find *": allow
  edit:
    "*": deny
    "*.md": allow
    "**/*.md": allow
    "*.mdx": allow
    "**/*.mdx": allow
    "README*": allow
    "**/README*": allow
    "CHANGELOG*": allow
    "**/CHANGELOG*": allow
    "docs/**": allow
    ".github/**": deny
    ".opencode/**": deny
    ".cursor/**": deny
    ".claude/**": deny
    "docs/adr/**": deny
    "**/architecture.dsl": deny
    "docs/diagrams/**": deny
---

{file:./.cursor/rules/architecture-docs.mdc}

{file:./.cursor/rules/git-workflow.mdc}

<!-- Shared instructions. Edit .github/docs/prompts/agents/docs-fix.md, not this file. -->

{file:./.github/docs/prompts/agents/docs-fix.md}

> 🔒 **OpenCode note:** your write boundary is enforced by the `permission.edit` path map
> in the frontmatter above — it is architecture, not persuasion.
