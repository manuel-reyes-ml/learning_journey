@AGENTS.md

## Claude Code — harness-specific addenda

`AGENTS.md` above is the single behavioural contract, shared verbatim with OpenCode.
Everything below applies **only** to Claude Code and does not duplicate it.

### Provider reality — read this before starting a session

Claude Code routes to **Anthropic only** (or Bedrock / Vertex / Foundry). There is
**no local-model path**. The `settings.ai_provider` privacy routing that governs the
*projects* has no equivalent in this *harness*.

**Stop conditions (binding, additive to the AGENTS.md set):**

- **Never open the proprietary 1099 / DataVault production repo in Claude Code.**
  That work stays on OpenCode + local Ollama. `guard.py` blocks reads under
  `data/raw/`, `data/processed/` and `data/outputs/` as a backstop, but the real
  control is not opening the repo here at all.
- Public flagship repos are in scope: they are **synthetic-data-only** per
  CORRECTION 41 §3, so the repository boundary — not the model — is the control.
- If a task would put a real participant record, client identifier or production
  figure in front of this harness, **stop and say so** rather than proceeding.

### Permission posture — do not rely on the default

On Pro/Max/Team plans Claude Code starts new conversations in **Auto** mode, where a
classifier reviews actions instead of asking. That is incompatible with the
no-vibe-coding invariant.

- `.claude/settings.json` pins `permissions.defaultMode: "plan"`.
- VS Code reads `initialPermissionMode` from **user** settings and ignores workspace
  values, so also set it in your VS Code *User* settings, not the workspace file.
- Leave `allowDangerouslySkipPermissions` at `false`. Permanently.
- Plan → review → Manual is the loop. `Edit automatically` and `Auto` are not used
  in this repo.

### Where enforcement actually lives

A rule written here is **context, not configuration** — Claude reads it and tries to
follow it. Anything that must not happen is enforced in `.claude/hooks/guard.py`
(PreToolUse), which fires before any permission-mode check and holds even under
`bypassPermissions`. That is the harness-level restatement of CORRECTION 39 §11:
a prohibition in a prompt is persuasion; a hook is architecture.

`guard.py` blocks: `git commit` · `git push` · `git reset --hard` · `gh pr create` ·
`gh pr merge` · reads of `.env*` and `roadmap.html` · writes under `data/raw|processed|outputs`.
It normalises `git -C <path>` and `git -c k=v` first — the documented bypass.

### Session hygiene

- **Start on a clean tree.** Carried over from CORRECTION 39 §6: `git diff` review is
  the gate, and it stops being trustworthy the moment agent edits mix with your own
  uncommitted work.
- `/usage` breaks consumption down per skill, subagent and MCP server. Forked skills
  and subagents each get their own context window, so a subagent-heavy session costs
  materially more of the same subscription window that claude.ai chat draws on.
- Run `/memory` if a rule is not being honoured — it shows which instruction files
  actually loaded, in what order.

### Model ladder used in this repo

| Tier | Model | Used for |
|---|---|---|
| Mechanical | `haiku` | commit messages, label runs — deterministic shape, no judgement |
| Judgement | `sonnet` | reviews, audits, doc drift, issue and brief drafting |
| Architecture | `opus` | pattern-scout only — research plus a standard-change recommendation |

This ladder is a **decision with a rejected alternative** (flat `sonnet` everywhere)
and is owed an ADR. The reasoning mirrors CORRECTION 39 §7: the output that every
later step depends on gets the stronger model; volume is low enough that the cheaper
tier buys nothing.
