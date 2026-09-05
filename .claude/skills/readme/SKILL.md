---
description: Draft a production-grade README from the repo and the flagship template. Outputs Markdown; does not write files.
argument-hint: "[optional]"
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(bash .github/scripts/*), Bash(git log*), Bash(find *), Bash(ls *), Bash(head *)
model: sonnet
context: fork
agent: Explore
background: false
disable-model-invocation: true
---

<!-- STUB. Instructions live once at .github/docs/prompts/commands/readme.md and are
     shared with OpenCode. Edit the prompt body, not this file.
     Both lines below run at level 1. `!` substitution is single-pass, so shell inside
     the imported body would arrive as literal text (ADR-0001). All shell for this
     command is in .github/scripts/readme_context.sh.
     UNVERIFIED on this harness: whether `$1` / `$ARGUMENTS` substitute BEFORE the `!`
     shell runs. Confirmed on OpenCode; probe before trusting the argument here. -->
 
!`bash ${CLAUDE_PROJECT_DIR}/.github/scripts/readme_context.sh`
 
!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/readme.md`
