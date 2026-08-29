# Setting up Claude Code in your repo — step by step

Read this once top to bottom before you copy anything. It should take about 20 minutes
to install.

---

## Part 1 — The idea, in plain words

You have two AI coding tools that both need instructions:

- **OpenCode** (your main one) reads `.opencode/`
- **Claude Code** (the new one) reads `.claude/`

If you write the instructions twice, they slowly stop matching. One says "use Polars,"
the other still says "use pandas," and you don't notice until something goes wrong.

**So we write each instruction once, in a new folder, and both tools point at it.**

```
             .github/docs/prompts/          ← the instructions live HERE, once
                      ↓                ↓
        .opencode/ points at it    .claude/ points at it
```

That new folder — `.github/docs/prompts/` — is the only place you edit text. The files
in `.opencode/` and `.claude/` become tiny: just settings, plus one line saying "go read
the shared file."

### Two kinds of file, two ways of pointing

| Kind | What it is | How the pointing works |
|---|---|---|
| **Commands** (9 of them: `/review`, `/test`, `/eval`, …) | A saved prompt you trigger by typing `/name` | **Live pointer.** Both tools read the shared file every time. Edit the shared file, both tools change instantly. |
| **Agents** (6 of them: `security-auditor`, `docs-fix`, …) | A specialist with its own permissions | **Generated copy.** OpenCode uses a live pointer. Claude Code *can't* — so a small script writes the file for it. |

**Why the difference:** Claude Code has no way to pull in another file inside an agent
definition. Two open requests on Anthropic's GitHub ask for it (#5914, #6899); it isn't
there. So for agents we do what you already do with architecture diagrams: **keep one
source, run a command, and it writes the copy.** `make diagrams` regenerates Mermaid
from `architecture.dsl`. `make claude-agents` regenerates `.claude/agents/` from the
shared prompts. Same idea, same rule: **never hand-edit the generated file.**

A pre-commit hook catches you if you forget to regenerate. That's Step 7.

---

## Part 2 — What goes where

Here is your repo after the install. **Bold** = new folders.

```
your-repo/
│
├── AGENTS.md                    ← unchanged. Still the master rulebook.
├── CLAUDE.md                    ← NEW. Three lines. Points at AGENTS.md.
├── Makefile                     ← add 3 targets (Step 6)
├── .gitignore                   ← add 2 lines (Step 2)
├── .pre-commit-config.yaml      ← add 1 hook (Step 7)
│
├── .cursor/rules/*.mdc          ← unchanged. Your coding standards.
│
├── .github/
│   ├── docs/
│   │   ├── templates/           ← unchanged
│   │   ├── project_labels.md    ← unchanged
│   │   └── **prompts/**             ← NEW. The single source of truth.
│   │       ├── commands/        ← 9 files. The text of each /command.
│   │       └── agents/          ← 6 files + 5 small "delta" files.
│   ├── ISSUE_TEMPLATE/          ← unchanged
│   ├── workflows/               ← unchanged
│   └── scripts/                 ← unchanged
│
├── **scripts/**
│   └── build_claude_agents.py   ← NEW. Writes .claude/agents/ from the prompts.
│
├── .opencode/                   ← REPLACED with thin versions
│   ├── opencode.jsonc           ← unchanged, don't touch it
│   ├── agent/    (6 files)      ← now ~20 lines each instead of ~90
│   └── command/  (9 files)      ← now ~8 lines each instead of ~60
│
└── **.claude/**                     ← NEW. Everything Claude Code reads.
    ├── settings.json            ← permissions + the safety hook
    ├── settings.local.json      ← YOUR copy, gitignored (Step 3)
    ├── hooks/guard.py           ← the safety gate
    ├── rules/    (8 files)      ← point at your .cursor/rules/*.mdc
    ├── agents/   (5 files)      ← GENERATED — never edit by hand
    ├── skills/   (9 folders)    ← the /commands, thin stubs
    └── output-styles/learn.md   ← GENERATED — never edit by hand
```

### The `.github/` change explained

You are **adding one folder**: `.github/docs/prompts/`. Nothing existing in `.github/`
is moved, renamed or deleted. Your templates, workflows, label script and
`project_labels.md` all stay exactly where they are.

Why put it under `.github/`? Because that's already where your shared, agent-facing
reference material lives (`templates/`, `project_labels.md`), and your existing command
files already reach into it with `@.github/docs/templates/README_template.md`. It's the
neutral ground both tools already know about.

---

## Part 3 — Install it

### Step 0 — Install the extension

1. Open VS Code.
2. Press `Cmd+Shift+X`, search **Claude Code**, install the one published by **Anthropic**.
3. You need VS Code **1.94.0 or newer** (check with Help → About).
4. Click the Spark icon, sign in with your Claude account in the browser. **No API key
   needed** — your existing subscription covers it.

> The extension has its own built-in copy of Claude Code for the chat panel. If you also
> want to type `claude` in the VS Code terminal, that needs a separate CLI install. You
> don't need it for any of this.

### Step 1 — Copy the files in

From the folder I gave you, copy everything into your repo root, keeping the structure:

```bash
cd /path/to/your-repo

# the new shared source of truth
cp -r <download>/.github/docs/prompts .github/docs/

# the generator
mkdir -p scripts && cp <download>/scripts/build_claude_agents.py scripts/

# everything Claude Code reads
cp -r <download>/.claude .
cp <download>/CLAUDE.md .

# the thinned-out OpenCode files (this REPLACES your current ones —
# commit your working tree first so you can diff and revert)
cp -r <download>/.opencode/agent .opencode/
cp -r <download>/.opencode/command .opencode/

chmod +x .claude/hooks/guard.py
```

**Before you run that last pair of `cp` commands, commit whatever you have now.** They
overwrite your existing `.opencode/agent/` and `.opencode/command/` files. The
instructions inside them are not lost — they've moved to `.github/docs/prompts/` — but
you want a clean `git diff` to check that for yourself.

### Step 2 — Update `.gitignore`

Append the two lines from `.gitignore.additions`:

```
.claude/settings.local.json
CLAUDE.local.md
```

### Step 3 — Make your personal settings file

```bash
cp .claude/settings.local.json.example .claude/settings.local.json
```

This one is yours alone and never gets committed. `.claude/settings.json` (no `.local`)
**is** committed — that's the shared policy.

### Step 4 — Turn off Auto mode. Do not skip this.

On your plan, Claude Code starts new conversations in **Auto** mode, where a classifier
approves most actions instead of asking you. That is the opposite of your no-vibe-coding
rule.

`.claude/settings.json` already pins `"defaultMode": "plan"`. But there's a catch: **VS
Code reads its own mode setting from your User settings and ignores workspace settings**,
so the repo cannot pin it for you. Set it yourself, once:

1. `Cmd+,` → make sure you're on the **User** tab (not Workspace)
2. Search `claudeCode.initialPermissionMode`
3. Set it to **`plan`**
4. Search `claudeCode.allowDangerouslySkipPermissions` → confirm it is **off**

### Step 5 — Generate the agent files

```bash
python3 scripts/build_claude_agents.py
```

You should see six lines of `wrote …`. These files already exist in what I gave you, so
nothing should change — this is you confirming the script runs on your machine.

### Step 6 — Add the Makefile targets

Paste the contents of `Makefile.additions` at the end of your `Makefile`.
Makefiles need **real tab characters** for indentation — if you get
`missing separator`, your editor converted tabs to spaces.

Then:

```bash
make claude-verify
```

Four lines, all must say **PASS**. This is testing that the safety gate actually blocks
things. If any line says FAIL, stop and tell me before using Claude Code on the repo.

### Step 7 — Add the pre-commit hook

Paste the block from `.pre-commit-config.additions.yaml` under `repos:` in your
`.pre-commit-config.yaml`, then:

```bash
pre-commit install
pre-commit run claude-agents-check --all-files
```

This is what stops the generated agent files from drifting. If you edit a shared prompt
and forget to run `make claude-agents`, your commit fails with a message telling you to.

### Step 8 — Check it actually loaded

Open Claude Code in the repo and run these:

| Type this | You should see |
|---|---|
| `/context` | Under **Memory files**: `CLAUDE.md`, `AGENTS.md`, and your 8 rule files |
| `/permissions` | Mode is **plan**; the deny list is there |
| `/hooks` | `guard.py` registered under PreToolUse |
| `/` then scroll | The 9 skills: review, test, eval, commit-msg, … |
| `/review` | The **full text** of the review checklist, not a filename |

That last one is the important one. **It proves the extraction worked.** If `/review`
produces a short reply that mentions a file path instead of running the checklist, the
shared file isn't being pulled in — see Troubleshooting.

---

## Part 4 — How you actually use it day to day

**To change what a command says** → edit `.github/docs/prompts/commands/<name>.md`.
Nothing else. Both tools pick it up immediately.

**To change what an agent says** → edit `.github/docs/prompts/agents/<name>.md`, then
run `make claude-agents`. OpenCode picks it up immediately; the command updates Claude's
copy.

**To change an agent's permissions or model** → edit the `AGENTS` table near the top of
`scripts/build_claude_agents.py`, then `make claude-agents`.

**Never edit** anything in `.claude/agents/` or `.claude/output-styles/`. They carry a
`GENERATED FILE — DO NOT EDIT` banner. Your next `make claude-agents` silently
overwrites whatever you typed there.

### The one rule you must not break

**Do not open the proprietary 1099 / DataVault production repo in Claude Code.**

Claude Code can only talk to Anthropic's servers. There is no local-model option — no
Ollama, nothing. Your regulated work stays on OpenCode with the local model, exactly as
it is now. Claude Code is for the **public, synthetic-data-only** flagship repos.

`guard.py` blocks reads under `data/raw/`, `data/processed/`, `data/outputs/` and any
`.env` file as a backstop, but the real control is not opening the repo there at all.

---

## Part 5 — What is guaranteed, what to watch

Everything below was checked against Anthropic's current documentation, not from memory.

### Confirmed working

| Thing | Why it's certain |
|---|---|
| `CLAUDE.md` importing `AGENTS.md` with `@AGENTS.md` | Documented as the official way to share instructions with other agent tools. Imported files are expanded into context at launch. |
| `` !`cat …` `` inside a skill pulling in the shared body | Documented: the command runs and its output **replaces the placeholder before Claude sees the content**. Not a hint — a real paste. |
| `${CLAUDE_PROJECT_DIR}` in the `cat` path and in `allowed-tools` | Documented substitution in exactly those two places, so the path resolves no matter which folder you started in. |
| `.claude/rules/` with `paths:` frontmatter | Documented directory. Rules with `paths:` load only when Claude touches matching files. |
| `guard.py` blocking with exit code 2 | Documented: exit 2 blocks the tool call. It fires **before** any permission check and holds even in bypass mode. Tested 13/13 including the `git -C /path commit` escape. |
| Skills replacing commands | Documented: `.claude/commands/x.md` and `.claude/skills/x/SKILL.md` both make `/x`; the skill wins. |

### The one uncertain piece

**`@` imports inside `.claude/rules/*.md`.** The docs describe `@path` imports for
CLAUDE.md. Rules are loaded the same way, so it very probably works — but it is not
spelled out for rules specifically, and the failure would be *silent*.

**Check it in Step 8** with `/context`. If your `.mdc` content isn't showing up, the
guaranteed fallback is to import them straight from `CLAUDE.md` instead:

```markdown
@AGENTS.md
@.cursor/rules/python-core.mdc
@.cursor/rules/observability.mdc
@.cursor/rules/testing-and-eval.mdc
```

That definitely works. The cost is that all of them load every session instead of only
when relevant, which uses more context. Try the rules folder first.

### Known rough edges

- **Hooks fail silently.** If the gate seems inactive, run `claude --debug` — that's the
  only way to see hook errors.
- **Editing a skill takes effect immediately; editing an agent does not.** Agent files
  are read once at session start. Restart Claude Code after `make claude-agents`.
- **HTML comments in `CLAUDE.md` are stripped** before Claude sees them, so the
  maintainer notes in these files cost you nothing.
- **Every forked skill and subagent opens its own context window.** They draw on the
  same subscription allowance as claude.ai chat. Run `/usage` to see the breakdown per
  skill and agent.

---

## Part 6 — Troubleshooting

**`/review` replies with a file path instead of the checklist**
The `cat` didn't run. Check `.github/docs/prompts/commands/review.md` exists, and that
`Bash(cat *)` is still in the skill's `allowed-tools`. A failed `cat` aborts the whole
skill with `Shell command failed for pattern "..."` — that message is your clue.

**A skill doesn't appear when you type `/`**
Skill folder names become command names, so the folder must be `review/` with the file
named exactly `SKILL.md`. Run `claude --debug` to see frontmatter parse errors.

**Claude ignores a rule**
`/context` first — if the file isn't listed, Claude never saw it. Remember these files
are *context*, not enforcement. Anything that must never happen belongs in `guard.py`.

**`pre-commit` fails with "STALE"**
You edited a shared agent prompt without regenerating. Run `make claude-agents`,
`git add` the changed files, commit again. Working as designed.

**A tool gets blocked that shouldn't be**
Read the `BLOCKED by .claude/hooks/guard.py` message — it names the rule. If the rule is
wrong, edit the lists at the top of `guard.py`, then `make claude-verify`.

---

## Part 7 — Still outstanding

**Correction 42 is not written.** Your roadmap's CORRECTION 39 §9 currently records
Claude Code as declined. Until you record the reversal, this setup contradicts your own
source-of-truth file. The evidence for reversing is strong — the "$20/mo second harness"
ground is false, since the extension costs nothing on a subscription you already hold —
but recording it is your call, not mine.

**An ADR is owed** for the model ladder (haiku for mechanical work, sonnet for judgement,
opus for pattern-scout). The rejected alternative is flat sonnet everywhere. Right now
that choice is my preference with no record behind it.
