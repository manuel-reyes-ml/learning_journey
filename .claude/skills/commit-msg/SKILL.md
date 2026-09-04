---
description: Generate a conventional-commits message for the currently staged changes. Does not commit.
argument-hint: "[optional scope hint]"
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(bash .github/scripts/*), Bash(git diff*), Bash(git log*)
model: haiku
context: fork
agent: Explore
background: false
disable-model-invocation: true
---

<!-- STUB. Instructions live once at .github/docs/prompts/commands/commit-msg.md and are
     shared with OpenCode. Edit the prompt body, not this file.
     Both lines below run at level 1. `!` substitution is single-pass, so shell inside
     the imported body would arrive as literal text (ADR-0001). All shell for this
     command is in .github/scripts/commit_msg_context.sh.
     UNVERIFIED on this harness: whether `$1` / `$ARGUMENTS` substitute BEFORE the `!`
     shell runs. Confirmed on OpenCode; probe before trusting the argument here. -->
 
!`bash ${CLAUDE_PROJECT_DIR}/.github/scripts/commit_msg_context.sh`
 
!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/commit-msg.md`