---
description: Generate a pull request description for the current branch. Outputs Markdown; does not create the PR.
argument-hint: "[optional]"
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(bash .github/scripts/*), Bash(git diff*), Bash(git log*), Bash(git rev-parse*)
model: sonnet
context: fork
agent: Explore
background: false
disable-model-invocation: true
---

<!-- STUB. Instructions live once at .github/docs/prompts/commands/pr-prep.md and are
     shared with OpenCode. Edit the prompt body, not this file.
     Both lines below run at level 1. `!` substitution is single-pass, so shell inside
     the imported body would arrive as literal text (ADR-0001). All shell for this
     command is in .github/scripts/pr_prep_context.sh.
     UNVERIFIED on this harness: whether `$1` / `$ARGUMENTS` substitute BEFORE the `!`
     shell runs. Confirmed on OpenCode; probe before trusting the argument here. -->
 
!`bash ${CLAUDE_PROJECT_DIR}/.github/scripts/pr_prep_context.sh $1`

!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/pr-prep.md`