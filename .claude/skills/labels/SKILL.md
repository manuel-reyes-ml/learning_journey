---
description: Create or update the standard GitHub label taxonomy for a repo and regenerate the label reference. WRITES TO GITHUB.
argument-hint: "[owner/repo — optional, defaults to current]"
allowed-tools: Read, Grep, Glob, Bash(cat:*), Bash(bash .github/scripts/labels_run.sh:*), Bash(gh label list:*), Bash(gh repo view:*)
model: sonnet
disable-model-invocation: true
---
 
<!-- STUB. Instructions live once at .github/docs/prompts/commands/labels.md and are
     shared with OpenCode. Edit the prompt body, not this file.
     NO CLAUDE_PROJECT_DIR ANYWHERE (no dollar-brace form) — DELIBERATE (ADR-0006). Claude Code statically
     analyses every `!` command and REFUSES any containing shell expansion
     ("Contains simple_expansion"), command substitution or brace expansion
     (anthropics/claude-code#43713, #11645). that variable in dollar-brace form is an expansion, so
     every stub that used it was refused before running. Relative paths only.
     Verified on this harness: expansion-free `!` DOES execute at level 1.
     Deliberately NOT `context: fork`: a side-effecting action belongs in the main
     conversation where it is visible, not in a background subagent. -->
 
!`bash .github/scripts/labels_run.sh`
 
!`cat .github/docs/prompts/commands/labels.md`
