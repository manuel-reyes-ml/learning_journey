---
description: Draft a production-grade GitHub Issue from a one-line goal. Outputs Markdown; does not create the Issue.
argument-hint: "[one-line goal]"
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(bash .github/scripts/*), Bash(gh issue list*), Bash(find *), Bash(ls *)
model: sonnet
context: fork
agent: Explore
background: false
disable-model-invocation: true
---

<!-- STUB. Instructions live once at .github/docs/prompts/commands/draft-issue.md and are
     shared with OpenCode. Edit the prompt body, not this file.
     Both lines below run at level 1. `!` substitution is single-pass, so shell inside
     the imported body would arrive as literal text (ADR-0001). All shell for this
     command is in .github/scripts/draft_issue_context.sh.
     UNVERIFIED on this harness: whether `$1` / `$ARGUMENTS` substitute BEFORE the `!`
     shell runs. Confirmed on OpenCode; probe before trusting the argument here. -->
 
!`bash ${CLAUDE_PROJECT_DIR}/.github/scripts/draft_issue_context.sh`
 
!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/draft-issue.md`
