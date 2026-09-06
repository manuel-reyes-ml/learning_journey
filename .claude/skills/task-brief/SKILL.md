---
description: Generate a complete Agent Task Brief for a GitHub Issue number — Gate 1, no implementation.
argument-hint: "[issue-number]"
allowed-tools: Read, Grep, Glob, Write, Bash(cat *), Bash(bash .github/scripts/*)
model: sonnet
disable-model-invocation: true
---

<!-- This file is a STUB. The instructions live once, at
     .github/docs/prompts/commands/task-brief.md, and are shared with OpenCode.
     Edit the prompt file, not this one. Only the settings above belong here.
     BOTH lines below run at level 1. That is deliberate: `!` substitution is
     single-pass, so shell written inside the imported body would arrive as
     literal text and never execute (verified on OpenCode 1.17.9, probe v4).
     The context script is the single source for that shell; the body is
     instructions only. See ADR-0001.
     NO `context: fork` AND NO `agent:` — DELIBERATE (ADR-0005).
     This command must WRITE the brief to .github/plans/. Both built-in read-only
     subagents (Plan, Explore) make that impossible, and `agent: general-purpose`
     depends on a field reported as ignored when a skill runs via the Skill tool
     (anthropics/claude-code#17283, #49559) — which fails OPEN to a wider tool pool.
     Running unforked puts the boundary in .claude/settings.json instead, where it is
     deterministic and versioned. Same reasoning as the `labels` skill: a consequential
     action belongs in the main conversation where it is visible.
     REQUIRED companion setting in .claude/settings.json:
         { "permissions": { "allow": ["Write(.github/plans/**)"] } }
     Without it the write prompts on every run. -->
 
!`bash ${CLAUDE_PROJECT_DIR}/.github/scripts/task_brief_context.sh $1`
 
!`cat ${CLAUDE_PROJECT_DIR}/.github/docs/prompts/commands/task-brief.md`