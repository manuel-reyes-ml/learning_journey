---
description: Create or update the standard GitHub label taxonomy for a repo and regenerate the label reference. WRITES TO GITHUB.
argument-hint: "[owner/repo — optional, defaults to current]"
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(bash .github/scripts/*), Bash(gh label list*), Bash(bash .github/scripts/*)
model: haiku
disable-model-invocation: true
---

<!-- STUB. Instructions live once at .github/docs/prompts/commands/labels.md and are
     shared with OpenCode. Edit the prompt body, not this file.
     Both lines below run at level 1. `!` substitution is single-pass, so shell inside
     the imported body would arrive as literal text (ADR-0001). All shell for this
     command is in .github/scripts/labels_run.sh.
     UNVERIFIED on this harness: whether `$1` / `$ARGUMENTS` substitute BEFORE the `!`
     shell runs. Confirmed on OpenCode; probe before trusting the argument here. -->
<!-- Deliberately NOT `context: fork`: a side-effecting action belongs in the main
     conversation where it is visible, not in a background subagent. -->
 
!`bash ${CLAUDE_PROJECT_DIR}/.github/scripts/labels_run.sh $ARGUMENTS`
 
!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/labels.md`
