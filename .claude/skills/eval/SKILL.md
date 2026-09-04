---
description: Run the AI evaluation suite and report scores against thresholds (RAG, agentic, GEval), and confirm the CI gate is real.
argument-hint: "[optional]"
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(bash .github/scripts/*), Bash(uv run deepeval*), Bash(grep *)
model: sonnet
context: fork
agent: eval-guardian
background: false
disable-model-invocation: true
---

<!-- STUB. Instructions live once at .github/docs/prompts/commands/eval.md and are
     shared with OpenCode. Edit the prompt body, not this file.
     Both lines below run at level 1. `!` substitution is single-pass, so shell inside
     the imported body would arrive as literal text (ADR-0001). All shell for this
     command is in .github/scripts/eval_context.sh.
     UNVERIFIED on this harness: whether `$1` / `$ARGUMENTS` substitute BEFORE the `!`
     shell runs. Confirmed on OpenCode; probe before trusting the argument here. -->
 
!`bash ${CLAUDE_PROJECT_DIR}/.github/scripts/eval_context.sh`
 
!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/eval.md`