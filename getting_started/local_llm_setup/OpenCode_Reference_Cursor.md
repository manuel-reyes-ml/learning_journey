# OpenCode — Commands, Tips & Configuration Reference

**Focus:** Using OpenCode inside **Cursor** (as the integrated-terminal extension), with model-agnostic providers (local Ollama + OpenRouter).
**Compiled:** June 2026 · Aligned to a Cursor-primary, learning-while-building, "no vibe coding" workflow.
**Version:** 1.1 (June 22, 2026)

> 📝 **Changelog v1.1:** + §7 Plan & Build modes (Tab to switch, per-mode model config) · + §9 model-ID format + routing/performance notes (incl. the DeepSeek-V4-Pro slowness fix) · + F2 model-cycling · + 404-slug / slow-agent / Claude-auth troubleshooting rows · cleaned up some broken markdown. v1.0 = original.

> ⚠️ OpenCode ships fast and command names/keybinds can change between versions. Treat **opencode.ai/docs** as the source of truth, and inside the TUI use **`/help`** or **`Ctrl+p`** (command palette) to see exactly what your installed build supports.

---

## 1. Mental model (how it behaves in Cursor)

OpenCode is an open-source, terminal-first AI coding agent. The Cursor/VS Code extension is essentially a **bridge that runs the OpenCode CLI inside the editor's integrated terminal** with workspace awareness — it is *not* a separate sidebar panel. So "using OpenCode in Cursor" = the OpenCode TUI running in a terminal pane, editing the same files Cursor has open.

Key consequences:

- OpenCode is its **own agent** (own plan/build modes, own model/providers). It does **not** use Cursor's agent or credits.
- Edits land on **disk**, so they appear in Cursor's editor and in `git diff` regardless of which surface you used.
- It's **model-agnostic + BYOK**: point it at free local models (Ollama) or any API (OpenRouter, Anthropic, etc.).

---

## 2. Install & update

**CLI (the engine):**

```bash
# Homebrew (Apple Silicon installs to /opt/homebrew/bin)
brew install opencode          # or: brew upgrade opencode  (keep current for security fixes)

# Official install script (auto-detects platform)
curl -fsSL https://opencode.ai/install | bash

# npm (needs Node 18+)
npm i -g opencode-ai@latest
```

**Extension in Cursor (separate from VS Code!):** Cursor keeps its *own* extension list, so installing in VS Code does **not** install it in Cursor. Do one of:

- Cursor → Extensions (`Cmd+Shift+X`) → search `opencode` (publisher **sst-dev**) → Install.
- Terminal: `cursor --install-extension sst-dev.opencode`
- Or download the `.vsix` from OpenCode's GitHub releases → Extensions → "⋯" → **Install from VSIX**.
- Or simply run `opencode` in Cursor's integrated terminal — it auto-installs the companion extension.

> The path difference (`opencode` in `/opt/homebrew/bin`, `cursor` in `/usr/local/bin`) is normal — different installers. Both just need to be on `PATH`.

---

## 3. Launching inside Cursor

1. Open your project folder in Cursor (`File → Open Folder`). OpenCode scopes everything to this directory.
2. Open the integrated terminal (`` Ctrl+` ``).
3. Start it any of these ways:

| Method | Action |
| ------------------------------------------ | ------------------------------------------------------- |
| Type `opencode` in the integrated terminal | Launches the TUI with workspace context (most reliable) |
| **`Cmd+Shift+Esc`** (Mac) | New OpenCode session (extension shortcut) |
| `Cmd+Shift+P` → "opencode" | Run the launch command from the palette |
| `Cmd+K Cmd+O` | Opens OpenCode in an editor group (default-bindable) |

**If `Cmd+Shift+Esc` does nothing:** the extension likely isn't installed *in Cursor* (only VS Code). Confirm via `Cmd+Shift+P` → type "opencode" — if no commands appear, install it in Cursor (section 2), then reload. The CLI working in the terminal does **not** prove the extension is active.

**If `opencode: command not found`:** the binary isn't on that shell's PATH — run `which opencode`; if empty, fully quit and reopen Cursor so it picks up the installer's PATH entry.

---

## 4. Cursor coexistence & context sharing

**Avoid two agents fighting:** OpenCode and Cursor's native agent can both run in one window. Use whichever you invoke. If you want OpenCode to be the *sole* agent during a session (no accidental Cursor AI / credit burn), disable Cursor's AI in settings:

```jsonc
// Cursor settings.json
"chat.disableAIFeatures": true,
"chat.agent.enabled": false,
"inlineChat.affordance": "off",
"terminal.integrated.suggest.enabled": false
```

Toggle these back on when you want Cursor's Tab autocomplete (its real strength).

**Context awareness (extension):**

- Automatically shares your **current tab / selection** with OpenCode.
- Set `EDITOR="cursor --wait"` so `/editor` and `/export` open in Cursor and block until you close the tab.

---

## 5. Referencing files (precise context control)

| Want | Do this |
| ---------------------------- | ------------------------------------------------------------------------------------ |
| Attach a whole file | Type `@` then the path → pick from autocomplete (e.g. `@src/strategies/momentum.py`) |
| Several files | Chain multiple `@` mentions in one prompt |
| A specific line range | In Cursor, **select the lines → `Cmd+Option+K`** → inserts `@File#L37-42` |
| Add a file from the explorer | Right-click the file → context-menu "add to OpenCode prompt" |
| A frequently-used directory | Configure a named **reference**, then `@alias` (root) or `@alias/` (search inside) |

Notes: `@` autocomplete is **`.gitignore`-aware** (ignored files won't appear). You don't *have* to reference — the agent reads files on its own — but `@` lets you pin exactly what's in context (good for controlled, low-noise prompts and lower token cost).

---

## 6. Slash commands (built-ins)

Type `/` in the TUI. Run `/help` or `Ctrl+p` for the full list in your build.

| Command | Aliases | Purpose |
| --------------------- | ---------------------- | --------------------------------------------------- |
| `/help` | | Show the help dialog |
| `/init` | | Guided **AGENTS.md** setup (project context) |
| `/new` | `/clear` | Start a fresh session |
| `/sessions` | `/resume`, `/continue` | List & switch between past sessions |
| `/undo` | | Revert last message **and file changes** (uses Git) |
| `/redo` | | Redo a previously undone message |
| `/compact` | | Summarize/compact the conversation to free context |
| `/models` | | List & pick the active model |
| `/connect` | | Add a provider + API key |
| `/share` · `/unshare` | | Create/stop a public share link (`opncd.ai/s/<id>`) |
| `/editor` | | Open the prompt in your `$EDITOR` |
| `/export` | | Export the conversation to Markdown |
| `/themes` | | List/switch themes |
| `/exit` | `/quit`, `/q` | Exit cleanly (saves session history) |

**Input patterns:**

- `@file` → attach file context (see section 5).
- `!command` → run a shell command; its output is added to the prompt as context (e.g. `!git diff --staged`).

---

## 7. Plan & Build modes (the non-vibecode core)

OpenCode has two built-in primary modes, and switching is how you enforce "review before it touches code":

| Mode | Tools | Use it for |
|---|---|---|
| **Plan** | **Read-only** — cannot modify files (can only write a plan to `.opencode/plans/*.md`) | Explore the codebase, have it explain its approach step-by-step, agree on the change *before* any edit |
| **Build** | Full tools (read, write, edit, bash) | Implement the agreed change, with each edit shown as a diff you approve |

**Switch with `Tab`** (and `Shift+Tab` to cycle back). The active mode shows in the status bar. Other handy keys: **`F2` / `Shift+F2`** cycle through recently-used models; the **leader key is `Ctrl+x`** (press it, release, then the next key — e.g. `Ctrl+x` then `n` = new session); use **`Shift+Enter`** (or `Ctrl+J`) for newlines.

**The disciplined loop:** start in **Plan** → read the plan → `Tab` to **Build** → approve each diff → review `git diff` → commit manually. Plan mode is one gate, per-edit approval another, your commit the last — exactly your control-gate workflow.

**Pin a different model per mode** (this is the fix for slow planning — see §9). In `opencode.json`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "plan":  { "model": "ollama/qwen3.5:9b" },          // fast/cheap for planning
    "build": { "model": "openrouter/qwen/qwen3.7-max" }  // stronger for implementation
  }
}
```
> Older docs use a top-level `"mode"` key (now deprecated in favor of `"agent"`) — both set per-mode models; verify against `opencode.ai/docs/modes`.

---

## 8. Sessions (persistence & resuming)

Sessions are **saved to disk automatically** and scoped per project — quitting loses nothing.

**Resume:**

```bash
opencode --continue            # -c : jump back into the most recent session
opencode --session <ses_id>    # -s : open a specific session
opencode --session <id> --fork # branch off a previous session
```

Inside the TUI: `/sessions` (or `/resume`) to pick from a list; `/new` for a clean slate.

**See everything / fix "missing" sessions:**

```bash
opencode session list                 # ALL sessions: ids, project paths, timestamps
opencode session resume <ses_id>      # reliably reopen by id
```

> Known quirk: the TUI `/sessions` picker only shows roughly the **last 30 days**, so older sessions can look gone. `opencode session list` still shows them. Set `OPENCODE_DISABLE_PRUNE=true` to protect old session data from pruning.

**Clean loop:** work → `/exit` → later `opencode -c` to resume exactly where you stopped.

---

## 9. Providers, models & routing (Ollama + OpenRouter)

OpenCode is model-agnostic with **bring-your-own-key** (or free local). Credentials live in `~/.local/share/opencode/auth.json`.

**Reliable command path:**

```bash
opencode auth login                    # interactive: pick a provider, paste key
opencode auth login --provider openrouter
opencode models                        # list available models
opencode --model openrouter/z-ai/glm-5.2   # model form is provider/model
```

In the TUI: `/connect` to add a provider+key, `/models` to switch models live, `F2` to cycle recent ones.

**Model-ID format in OpenCode:**

| Source | Format | Example |
|---|---|---|
| OpenRouter | `openrouter/` + the OpenRouter slug | `openrouter/anthropic/claude-opus-4.8`, `openrouter/qwen/qwen3.7-max`, `openrouter/deepseek/deepseek-v4-pro` |
| Local Ollama | `ollama/` + the tag | `ollama/qwen3.5:9b`, `ollama/qwen2.5-coder:7b` |

> Always keep the **`vendor/` prefix** inside OpenRouter slugs — `claude-sonnet-4.6` 404s; `anthropic/claude-sonnet-4.6` works.

**Local Ollama (free, private)** — run a model first (`ollama run qwen2.5-coder:7b`), then configure OpenCode to point at the local OpenAI-compatible endpoint. Representative `opencode.json` (verify keys against `opencode.ai/docs/providers`):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "options": { "baseURL": "http://localhost:11434/v1" },
      "models": { "qwen2.5-coder:7b": {}, "qwen3.5:9b": {} }
    }
  }
}
```

**⚡ Performance & routing (read this if OpenCode feels slow):**
- **Heavy reasoning models can be slow in OpenCode**, especially in **Plan mode** (the most reasoning-heavy phase). DeepSeek V4 Pro is the usual culprit: long time-to-first-token, and OpenCode's ai-sdk doesn't handle DeepSeek's thinking-content stream cleanly. It can look frozen, then dump output.
- **Fix:** use a **fast model for Plan, a stronger model for Build** (§7 per-mode config). Good planners: `ollama/qwen3.5:9b` (no network), `openrouter/deepseek/deepseek-v4-flash`, or `openrouter/z-ai/glm-5.2`.
- **OpenRouter variability:** it farms requests to whichever host is free, some slow. Try the throughput variant (`…:nitro`) or set provider routing to sort by throughput / exclude slow providers in OpenRouter settings.
- **Smoother heavy models in OpenCode:** `z-ai/glm-5.2` and `qwen/qwen3.7-max` tend to run more cleanly than `deepseek-v4-pro` here.

**Quick routing** (see the separate Routing Cheat-Sheet for slugs): plan → fast/cheap · build → strong open model · learning/private → local Ollama · hardest 20% → escalate to Claude.

> **Privacy split for you:** keep finance/proprietary work on **local Ollama** (free, on-device); route heavier build tasks to **GLM-5.2 / Qwen3.7 Max via OpenRouter**. Note: OpenCode may still call its cloud to generate session *titles* even with local models — fine for most work, worth knowing for fully air-gapped use.
> **Claude in OpenCode = API key only.** Since Jan 2026 Anthropic blocked OpenCode from using Claude Pro/Max consumer logins, so reach Claude via an **OpenRouter or Anthropic API key**, not your subscription.

---

## 10. Custom commands (repeatable prompts)

Define reusable prompts as markdown in `.opencode/commands/` (check them into Git for repeatable, team-shareable workflows). Invoke with `/name`.

```markdown
---
description: Run the test suite with coverage and propose fixes
agent: build
model: openrouter/z-ai/glm-5.2
---
Run the full test suite with coverage. Focus on failing tests in @$ARGUMENTS and suggest minimal fixes.
```

Placeholders/patterns: `$ARGUMENTS` (and positional `$1`, `$2`…), `@file` to inject files, `!cmd` to inject shell output. Set `subtask: true` to force a subagent so it doesn't pollute your main context.

---

## 11. Custom agents & project context

- **AGENTS.md** (run `/init` to scaffold): your project's standing instructions — the place to encode your standards (no vibe coding, layer-boundary rule, `%s`/`%d` lazy logging, eval-first, etc.) so the agent follows them automatically. Analogous to your Cursor `.mdc` rules. **Commit it to Git** so the context is shared and versioned.
- **Custom agents:** `opencode agent create` walks you through a custom **system prompt + permissions** (anything you don't allow is denied in the agent's frontmatter). Great for a constrained "learning-mode" or "review-only" agent. Built-in primary agents include **Build** and **Plan**; subagents like **Explore** (fast read-only codebase search) can be `@`-mentioned.

---

## 12. Configuration files at a glance

| File | Scope | Configures |
| ---------------------------------------- | ------------------------------------- | ---------------------------------------------------------------------------- |
| `opencode.json` | project root or `~/.config/opencode/` | providers, models, **per-mode/agent models**, permissions, runtime/server |
| `tui.json` / `tui.jsonc` | TUI | theme, keybinds, diff style, attention (sounds/notifications), scroll, mouse |
| `AGENTS.md` | project | standing instructions/context for the agent |
| `.opencode/commands/*.md` | project | custom slash commands |
| `.opencode/agents/*.md` · `.opencode/modes/*.md` | project | custom agents / modes |
| `auth.json` (`~/.local/share/opencode/`) | global | provider credentials |

**Useful `tui.json`:**

```jsonc
{
  "$schema": "https://opencode.ai/tui.json",
  "theme": "opencode",
  "keybinds": { "leader": "ctrl+x", "command_list": "ctrl+p" },
  "diff_style": "auto",
  "attention": { "enabled": true, "notifications": true, "sound": true }
}
```

**Keybinds:** the **leader** key defaults to `Ctrl+x` — many shortcuts are leader-prefixed (e.g. `Ctrl+x` then `n` = new session). The command palette is `Ctrl+p`; **`Tab`** switches Plan/Build mode; **`F2`** cycles models. Disable any binding by setting it to `"none"`. Custom path via `OPENCODE_TUI_CONFIG`.

**Env vars worth knowing:** `OPENCODE_DISABLE_PRUNE=true` (keep old sessions), `OPENCODE_TUI_CONFIG` (custom TUI config), `OPENCODE_SERVER_PASSWORD` (auth for `serve`/`web`).

---

## 13. CLI quick reference

```bash
opencode                         # start TUI in current dir
opencode -c                      # continue last session
opencode -s <id> [--fork]        # open/branch a specific session
opencode -m provider/model       # set model for this run
opencode models                  # list available models
opencode run "<prompt>" [-c] [-s <id>] [-m ...]   # non-interactive / scripting / CI
opencode session list|resume|delete              # manage sessions
opencode auth login [--provider <name>]          # credentials
opencode agent create                            # new custom agent
opencode serve [--port 4096]                     # headless API server
opencode web   [--port 4096 --hostname 0.0.0.0]  # browser UI
opencode attach http://host:4096 [--dir <p>]     # attach to a running server
opencode --version | --help
```

---

## 14. Workflow tips (tailored)

- **Plan before Build** (§7). Start in Plan mode (read-only) so it explains its approach; `Tab` to Build; approve each diff. Your `git diff` is the final control gate — fits your manual-commit discipline.
- **Split the model by mode:** fast/cheap for Plan, strong for Build (§9) — this alone fixes most "OpenCode feels slow" complaints.
- **Encode your standards once** in `AGENTS.md` (and a custom "learning-mode" agent) so every session teaches and explains instead of vibe-coding.
- **Control context & cost** with `/compact` on long sessions and `@`/line-range references instead of dumping whole files — especially on API models.
- **Right tool per task:** local Ollama (free, private) for practice/finance; OpenRouter (GLM-5.2 / Qwen3.7 Max) for heavy builds; keep Cursor's Tab for autocomplete.
- **Resume, don't restart:** `opencode -c` + `OPENCODE_DISABLE_PRUNE=true`.
- **Check custom commands into Git** for repeatable project workflows.
- **Stay updated** (`brew upgrade opencode`) — an older RCE bug (CVE-2026-22812) was patched in v1.1.10; keep current.

---

## 15. Troubleshooting

| Symptom | Cause / Fix |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `Cmd+Shift+Esc` does nothing | Extension not installed in Cursor (only VS Code) → install in Cursor, reload |
| `opencode: command not found` | Not on PATH → `which opencode`; quit & reopen Cursor to refresh PATH |
| No OpenCode commands in palette | Extension inactive in Cursor → reinstall/enable it |
| **Agent very slow / long pause before any output** | Heavy reasoning model (e.g. DeepSeek V4 Pro) in Plan mode → set Plan to a fast model (§7/§9) or `F2` to switch; try OpenRouter `…:nitro` / throughput routing |
| **Model returns 404 / "model not found"** | Missing `vendor/` prefix → use `anthropic/claude-sonnet-4.6` (or `openrouter/anthropic/claude-sonnet-4.6`), not `claude-sonnet-4.6` |
| **Claude won't authenticate via Claude Pro** | Since Jan 2026 OpenCode can't use the consumer subscription → use an OpenRouter or Anthropic **API key** instead |
| Old sessions missing in `/sessions` | TUI shows ~30 days only → use `opencode session list`; set `OPENCODE_DISABLE_PRUNE=true` |
| `Shift+Enter` won't make a newline | Known integrated-terminal keybind issue → add a `workbench.action.terminal.sendSequence` binding for `shift+enter` in `keybindings.json` (or use `Ctrl+J`) |
| Two agents responding at once | Disable Cursor AI features (section 4) during OpenCode sessions |

---

## 16. Sources

opencode.ai/docs (CLI, TUI, **Modes**, **Agents**, Commands, References, IDE, Providers) · DeepWiki sst/opencode VS Code extension · CodeReaper "Using OpenCode with VSCode" · Warp & NxCode OpenCode setup guides · Educative "Plan Mode vs Build Mode" · CodeSignal / OpenCode School session lessons · explainx.ai slash-command reference · ComputingForGeeks CLI cheat sheet · OpenCode GitHub issues (#16733 sessions, #14810 keybinds, #2129 line ranges). Re-verify command names/keybinds against `opencode.ai/docs` and `/help` before relying on them.