---
description: Run the AI evaluation suite and report scores against thresholds (RAG, agentic, GEval), and confirm the CI gate is real.
argument-hint: "[optional]"
allowed-tools: Read, Grep, Glob, Bash(cat:*), Bash(bash .github/scripts/eval_context.sh:*), Bash(uv run deepeval:*), Bash(grep:*)
model: sonnet
context: fork
agent: eval-guardian
background: false
disable-model-invocation: true
---

<!-- STUB. Instructions live once at .github/docs/prompts/commands/eval.md and are
     shared with OpenCode. Edit the prompt body, not this file.
     NO CLAUDE_PROJECT_DIR ANYWHERE (no dollar-brace form) — DELIBERATE (ADR-0006). Claude Code statically
     analyses every `!` command and REFUSES any containing shell expansion
     ("Contains simple_expansion"), command substitution or brace expansion
     (anthropics/claude-code#43713, #11645). that variable in dollar-brace form is an expansion, so
     every stub that used it was refused before running. Relative paths only.
     Verified on this harness: expansion-free `!` DOES execute at level 1.
     `agent: Plan`, not Explore: this command judges output against project
     standards, and Explore deliberately skips CLAUDE.md to stay cheap (ADR-0004). -->
 
!`bash .github/scripts/eval_context.sh`
 
!`cat .github/docs/prompts/commands/eval.md`