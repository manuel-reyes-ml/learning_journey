---
description: Create or update the standard GitHub label taxonomy for a repo and regenerate the label reference. WRITES TO GITHUB.
argument-hint: "[owner/repo — optional, defaults to current]"
allowed-tools: Read, Bash(cat *), Bash(bash .github/scripts/setup-labels.sh:*), Bash(gh repo view:*), Bash(head *)
model: haiku
disable-model-invocation: true
---

<!-- This file is a STUB. The instructions live once, at
     .github/docs/prompts/commands/labels.md, and are shared with OpenCode.
     Edit the prompt file, not this one. Only the settings above belong here.
     The line below runs `cat` and pastes the file's text in before Claude reads
     it, so Claude receives the full instructions, not a pointer. -->

!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/labels.md`
