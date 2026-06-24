# OpenCode Setup — Install & Usage

Scaffold for using OpenCode inside Cursor with local Ollama (planning/private) +
OpenRouter GLM-5.2 (build). Aligned to roadmap v8.4, Stage 1. Verified against
opencode.ai/docs (Jun 2026).

## 1. Where files go

Copy into your project root, preserving structure:

```
your-repo/
├── AGENTS.md                      # standing rules (commit to Git)
├── opencode.json                  # rename from opencode.jsonc, OR keep .jsonc
└── .opencode/
    ├── agents/
    │   ├── learn.md               # primary  — teaching mode (Tab to switch)
    │   ├── docs-sync.md           # subagent — docs vs codebase (read-only)  @docs-sync
    │   ├── docs-fix.md            # subagent — edits doc files directly       @docs-fix
    │   ├── pattern-scout.md       # subagent — production patterns @pattern-scout
    │   ├── eval-guardian.md       # subagent — eval thresholds     @eval-guardian
    │   └── security-auditor.md    # subagent — secrets/PII         @security-auditor
    └── commands/
        ├── commit-msg.md  draft-issue.md  task-brief.md  review.md
        ├── test.md        eval.md         pr-prep.md
```

> The `instructions` array in `opencode.json` reuses your existing
> `.cursor/rules/*.mdc` — they are combined with `AGENTS.md` automatically.
> No duplication. Adjust the paths if your rules live elsewhere.

## 2. One-time provider setup

```bash
brew upgrade opencode                 # stay current (security)
ollama pull qwen3.5:9b                 # if not already pulled; check: ollama list
opencode auth login --provider openrouter   # paste key (stored in auth.json)
```

Then in the TUI run `/models` and confirm these appear:
- `ollama/qwen3.5:9b` (plan); fallbacks `openrouter/z-ai/glm-5.2` then
  `openrouter/deepseek/deepseek-v4-pro` (in that order)
- `openrouter/minimax/minimax-m3` (build default), plus `openrouter/z-ai/glm-5.2`
  and `openrouter/qwen/qwen3.7-max` (build alternates)

Switch models mid-session with **F2** (cycle recent) or `/models` (pick): reach for
a build alternate when MiniMax struggles on a portion. If local planning is weak,
fall back to **GLM-5.2** first, then **DeepSeek V4 Pro** as last resort. Heads-up:
V4 Pro can be slow / look frozen in Plan mode (reasoning-MoE + ai-sdk thinking-
stream) — that's expected, not a hang.

If Plan-mode tool calls misbehave on the 9B, raise Ollama context (start 16k):
`OLLAMA_CONTEXT_LENGTH=16384 ollama serve` (or set `num_ctx` in a Modelfile).

## 3. How to add a custom agent (two ways)

**Markdown file (preferred — modular, like your .mdc):**
create `.opencode/agents/<name>.md`; the filename becomes the agent name.

```markdown
---
description: What it does and when to use it   # required
mode: subagent            # primary | subagent | all
model: ollama/qwen3.5:9b  # optional; subagents inherit caller's model if omitted
temperature: 0.1
permission:               # preferred over the deprecated `tools:` field
  edit: deny              # allow | ask | deny
  bash:
    "*": deny             # last matching rule wins — put "*" first
    "git diff*": allow
  webfetch: deny
---

System prompt goes here (the body).
```

**Interactive:** `opencode agent create` walks you through scope, prompt, and
permissions, then writes the markdown file. List them with `opencode agent list`.

Permission keys you'll use most: `edit` (gates write/edit/apply_patch), `bash`,
`read`, `webfetch`, `websearch`, `task`. Values: `allow` / `ask` / `deny`;
`bash` also takes `"pattern": action` maps.

## 4. The disciplined loop (your non-vibecode gates)

1. Start in **Plan** (local qwen3.5:9b) → it explains the approach. Gate 1.
2. `/task-brief <issue#>` for a full brief if working from an Issue.
3. `Tab` → **Build** (MiniMax M3; F2 → GLM-5.2 / Qwen3.7 Max if it struggles).
   Edits apply directly (`edit: allow`); your gate is the `git diff` review. Gate 2.
4. `/review` then `/test` (and `/eval` for AI work). Gate 3.
5. `/commit-msg` → review → **you** `git commit` manually. Gate 4.
6. `/pr-prep` → review → **you** open the PR.

Agents never run `git commit`/`git push` (denied in config).

## 5. When to reach for which agent

- Stuck on a concept / want to understand before building → **learn** (`Tab`).
- READMEs/docstrings drifted from code → `@docs-sync` (report) or `@docs-fix` (apply doc edits).
- "Is there a better, current way to do this?" → `@pattern-scout`.
- Check AFC/eval thresholds → `@eval-guardian` (or `/eval`).
- Before committing finance/data work → `@security-auditor`.

## 6. Privacy

Finance/proprietary stays on local Ollama. `small_model` is pinned local so even
session titles don't hit the cloud. `pattern-scout` uses cloud + web — for a
proprietary repo, switch its model to `ollama/qwen3.5:9b` and deny webfetch/
websearch first (noted in the file).
