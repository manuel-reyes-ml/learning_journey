---
description: Generate a complete Agent Task Brief for a GitHub Issue number — Gate 1, no implementation.
argument-hint: "[issue-number]"
allowed-tools: Read, Grep, Glob, Write, Bash(cat:*), Bash(bash .github/scripts/task_brief_context.sh:*)
model: sonnet
disable-model-invocation: true
---

<!-- STUB. Instructions live once at .github/docs/prompts/commands/task-brief.md and are
     shared with OpenCode. Edit the prompt body, not this file.

     NO CLAUDE_PROJECT_DIR ANYWHERE (no dollar-brace form) — DELIBERATE (ADR-0006). Claude Code statically
     analyses every `!` command and REFUSES any containing shell expansion
     ("Contains simple_expansion"), command substitution or brace expansion
     (anthropics/claude-code#43713, #11645). that variable in dollar-brace form is an expansion, so
     every stub that used it was refused before running. Relative paths only.

     Verified on this harness: expansion-free `!` DOES execute at level 1.

     NO `context: fork` AND NO `agent:` — DELIBERATE (ADR-0005). This command WRITES the
     brief to .github/plans/. Plan and Explore are both read-only, and `agent:` is
     reported as ignored when a skill runs via the Skill tool (#17283, #49559), failing
     OPEN to a wider tool pool. Unforked puts the boundary in .claude/settings.json:
         { "permissions": { "allow": ["Write(.github/plans/**)"] } }
     Verified: that write succeeds silently.

     THE ARGUMENT CANNOT GO IN THE `!` LINE — it would be an expansion and be refused.
     The body is loaded by `!`; the context script is invoked by YOU, below. -->

!`cat .github/docs/prompts/commands/task-brief.md`

---

**Before anything else**, run this with your Bash tool, replacing `<N>` with the Issue
number this command was invoked with (on this harness the argument arrives as a separate
`ARGUMENTS:` line rather than interpolated into the text above — read it from there):

    bash .github/scripts/task_brief_context.sh <N>

Its output is the context the instructions above refer to. If you cannot determine the
Issue number, **STOP and report** — do not guess one and do not run the script bare.