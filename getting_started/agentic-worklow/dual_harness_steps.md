# Dual-Harness Development Workflow — Step by Step

## From Issue to Merged PR — Claude Code plans and reviews, OpenCode builds

**Author:** Manuel Reyes
**Version:** 2.0
**Date:** August 30, 2026
**Replaces:** `cursor_workflow.md` v1.0 (April 06, 2026)
**Applies to:** All flagship and supporting portfolio projects — PolicyPulse, DataVault / 1099 Data Platform, Crucible, PostCheck, FormSense, AFC
**Aligned with:** Roadmap v10.0 — CORRECTIONS 39, 40, 41; ADR-001 §5a; `python-core.md`, `git-workflow.md`, `architecture-docs.md`

> ⚠️ **GOVERNANCE STATUS — READ FIRST.**
> This document describes a topology that **supersedes CORRECTION 39 §1 and §9**. The
> reversing correction (**CORRECTION 42**) is **not yet written**. Until it is, this file
> is a *proposal of record*, not ratified canon. `roadmap.html` remains the single source
> of truth and wins on any conflict. Do not propagate this file to the project scope
> documents until Correction 42 is signed off.

> **This file:** the step-by-step workflow only — §3 harness roles and §3.2 trial
> procedure (used in Step 3), §4 Steps 0–7, §5 control gates, §6 daily cycle.
> **Analysis and rationale** (§0–§2, §3.1, §3.3, §4-R, §7–§13) are in `dual_harness_analysis.md`.
> Section numbers are unchanged from the single-file v2.0, so every `§` reference
> resolves in one file or the other.

---

## 3. Harness roles — when to use each

| Role | Where | Trigger | Use for | Can it write? |
|------|-------|---------|---------|---------------|
| **Claude Code — plan** | VS Code | `Shift+Tab` → Plan, or `/plan` | Architecture, scope, Issue drafting, Task Brief authoring | ❌ No |
| **Claude Code — review** | VS Code | Fresh session on a dirty tree | Diff review against the Issue and brief | ❌ No |
| **OpenCode — `build`** | Cursor terminal | Default build agent | Multi-file refactors; gates **after** the write via `git diff` | ✅ **Sole writer** |
| **OpenCode — `build-gated`** | Cursor terminal | Explicit selection | Unfamiliar libraries, single-file work; gates **before** each write | ✅ **Sole writer** |
| **OpenCode — `build-hard`** *(trial, Nov 2026)* | Cursor terminal | Explicit selection | Hard multi-file tasks, run side by side with `build` (§3.2) | ✅ **Sole writer** |
| **Claude (browser project)** | claude.ai | — | Roadmap governance, corrections, cross-project strategy | ❌ No repo access |

### `build` vs `build-gated` — the selection rule (CORRECTION 39 §6, restated)

**Neither is universally correct.** Pre-write gating suits unfamiliar libraries and
single-file work, where the slowdown *is* the value. It is **wrong for large multi-file
refactors** — the S2 Polars ingestion rewrite is the named case — because per-edit
approval hides the whole-change picture, and long prompt chains produce reflex approval:
**a gate that feels real but is not.**

**Precondition binding on both:** start every session on a clean tree.

### 3.2 `build-hard` trial — GLM-5.3 vs the GLM-5.2 default (Nov 2026)

`build-hard` has the **same permissions as `build`**; only the model differs (GLM-5.3).
The built-in `general` and `explore` helpers are pinned to GLM-5.2, so both agents
delegate to identical helpers. That keeps the model the only variable.

**Run each hard task twice, isolated:**

```bash
git switch main && git pull                      # clean, current tree
git worktree add -b trial/<issue>-build      ../lj-build      HEAD
git worktree add -b trial/<issue>-build-hard ../lj-build-hard HEAD
# OpenCode in ../lj-build → Tab to `build`;  OpenCode in ../lj-build-hard → Tab to `build-hard`
# Same prompt in both: "Execute the task brief at <path>…"
```

Two worktrees mean two working trees, so the two agents never write to the same files
and each `git diff` shows exactly one model's work.

**Log per task** (one row each):

| Issue | Agent | Model in footer | Checks pass first try? (`make test` / `make lint` / mypy) | Review fixes you made | Minutes | Go usage % (Console) |
|---|---|---|---|---|---|---|

**Fairness rules:** same brief, same starting commit, same effort setting. Don't compare a
session that hit context compaction against one that didn't; note it and rerun.

**⚠️ Confirm the model before every run.** In OpenCode 2.x the session keeps its own model:
a model picked by hand for an agent beats that agent's configured `model`, and Tab
restores each agent's last-used model. Read the footer (`Build-Hard · GLM-5.3`). If it
shows anything else, pick the right model with `/models` first. A run on the wrong model
doesn't count. Example from 18 Nov: the footer read `Plan-Cloud · DeepSeek V4.1 Flash` because that
model had been picked by hand. The footer was right; the config's `model` was not what ran.

**Decide after ~10 hard tasks:** keep `build-hard` only if it needs **clearly fewer review
fixes** than `build` and the shared Go pool holds; otherwise remove the agent. Record the
result as a roadmap correction. Clean up with `git worktree remove ../lj-build` (and
`../lj-build-hard`) once each comparison is reviewed.

---

## 4. Step-by-step workflow

### 4.0 🔑 This document names commands. It does not contain prompts.

**The prompt bodies live once, in `.github/docs/prompts/`.** OpenCode reads them via
live `@` imports; Claude Code reads them via `` !`cat` `` stubs; `build_claude_agents.py`
regenerates the Claude Code side and `claude-agents-check` enforces it at the commit
boundary.

So: every step below names a `/command`, states what it reads, and says which gate it
satisfies. **To change what a step does, edit the body in `.github/docs/prompts/` —
never this file.**

*Why prompts are referenced, not pasted → `dual_harness_analysis.md` §4-R.*

---

### Step 0 — Draft the Issue (Claude Code, plan mode)

**Goal:** a GitHub Issue that is explicit and testable, in the repo's standard format.

Open VS Code, start Claude Code, confirm the mode indicator reads **Plan**.

```
/draft-issue <one-sentence goal>
```

**Reads:** `@.github/ISSUE_TEMPLATE/task.md` · `@.github/docs/project_labels.md` ·
`find src -name '*.py'` · `ls docs/adr`
**Emits:** a full Issue body — context, packs in scope, scope/non-scope, implementation
plan, **decisions expected** (with ADR-required flag where an alternative gets rejected),
testable acceptance criteria, edge cases incl. idempotency, uv-native validation plan,
data-and-security line, suggested labels with one-sentence justifications, risks.
**Does not create the Issue.** You paste it.

**Alternative — Claude (browser project)** for issues needing roadmap-level strategic
alignment across the four flagships. Claude Code sees the repo; browser Claude sees the
portfolio. Pick on which context the issue actually needs.

**Outcome:** paste into GitHub. Apply the suggested labels. **This is Gate 0.**

---

### Step 1 — Generate the Task Brief (Claude Code, plan mode)

**Goal:** convert the approved Issue into a precise execution contract that OpenCode
follows without inheriting any of the planning conversation.

```
/task-brief XX
```

**Reads:** `gh issue view XX` · `@.github/docs/templates/task_brief.md` · `find src tests`
· `ls docs/adr`
**Emits:** metadata with branch name and ticked packs · objective · **all nine hard
constraints verbatim** · files-to-change table incl. `docs/adr/000N-….md` and
`architecture.dsl` where applicable · ordered execution steps each ending "STOP and
report diff" · acceptance criteria · edge cases incl. idempotency · the uv-native
validation set · deliverable summary and stop conditions.
**Ends with: "Do NOT start implementing — this is Gate 1."**

⚠️ **`task-brief.md` line 6 currently points at
`@.github/docs/templates/cursor_task_brief.md`, which does not exist.** The file on disk
is `task_brief.md`. **This command is broken right now** — see §12.

**Non-interactive route** — for generating the artifact in one shot without a session:

```bash
claude -p --permission-mode plan \
  "$(cat .github/docs/templates/task_brief.md) — fill this out for Issue #XX" \
  > .github/plans/issue-XX-task-brief.md
```

⚠️ **§11-Q3: verify this once before relying on it.** The `-p` + `--permission-mode plan`
combination outputting the plan to stdout with no approval dialog is reported by a
secondary source, not confirmed against first-party docs. Note also that `claude -p`
**never shows the workspace-trust dialog**, which changes which project configuration
loads — read the trust table in the permissions docs before making this the default path.

**Review the brief before proceeding.** Right files? Right order? Testable criteria?
Would you actually run those validation commands? Edit it directly if not — this is your
last chance to correct scope before code is written. **This is Gate 1.**

*Why the brief-on-disk is load-bearing → `dual_harness_analysis.md` §4-R.*

---

### Step 2 — Pre-implementation checkpoint

```bash
git checkout main
git pull origin main
git checkout -b feature/XX-short-description

git status -sb          # MUST be clean
```

If the agent produces something you don't want, `git checkout .` returns you here
instantly.

---

### 🚦 Gate 1.5 — Harness switch (NEW in v2.0)

**Run this every time control passes between harnesses. Both directions. No exceptions.**

```bash
git status --porcelain          # planning → building: MUST be empty
```

**The rule:** the outgoing harness's session is closed before the incoming harness's
session is opened. Never two live sessions on one tree.

Concretely:

| Transition | Precondition |
|-----------|--------------|
| Plan → Build | Claude Code session closed; `git status --porcelain` empty |
| Build → Review | OpenCode session **closed or idle**; diff is complete and stable |
| Review → Build (fixes) | Claude Code session closed; findings written down outside the harness |

*Why Build → Review still needs this gate → `dual_harness_analysis.md` §4-R.*

---

### Step 3 — Build (OpenCode — sole writer)

**Goal:** ~90% of the code changes, following the brief step by step.

Open Cursor. OpenCode runs in the **integrated terminal** — detection relies on terminal
environment variables, so an external terminal will not work (CORRECTION 39 §1).

Select `build` or `build-gated` per §3 — or, during the trial, run `build` and `build-hard` side by side per §3.2.

```
Execute the task brief at <path>. Follow the execution steps in order.
Stop after each step and report what changed. Do NOT commit or push.
```

This is the one place a typed instruction is correct rather than a command: the brief
*is* the prompt, and it was authored in Step 1 and ratified by you at Gate 1.

**After each stop point:**

```bash
git status -sb
git diff
git diff --stat
```

**Validation per the brief:**

```bash
make test
make lint
```

**If it goes wrong:**

```bash
git checkout . && git clean -fd          # back to the Step 2 checkpoint
git checkout -- src/ai/guardrails.py     # or one file
```

**This is Gate 2 — repeated at every stop point.**

---

### Step 4 — Cross-harness review (Claude Code — fresh session, read-only)

**Goal:** find what the builder cannot find about its own work.

*The self-review rule this step satisfies → `dual_harness_analysis.md` §4-R.*

**Procedure:**

1. Close or idle OpenCode. Run **Gate 1.5**.
2. Open Claude Code in VS Code. **Start a new session** — do not resume, do not
   `/compact`, do not reuse the planning session.
3. Confirm read-only posture is active (`/permissions`).
4. Invoke:

```
/review
```

**Runs, via `!` injection:** `ruff check` · `ruff format --check` · `mypy src/` ·
`pytest -v` · `uv lock --check` · `git diff --stat`
**Then statically verifies:** `from __future__ import annotations` placement · NumPy
docstrings and PEP 604 hints · Pydantic at trust boundaries · **structlog kwargs with
NO f-string and NO `%s`/`%d` interpolation of payload data** · stable `snake_case` event
names · `configure_logging()` once at entrypoint · `clear_contextvars()` before
`bind_contextvars()` · no bodies at INFO · `settings` not `os.environ` · `SecretStr`
credentials · `stamina` with capped attempts *and* total time, idempotency keys on
retried writes · `pyproject.toml` + `uv.lock`, no `requirements.txt`.
**Emits:** ✅ passing · ❌ failing with `file:line` · 🔧 one-line fix each.
**Ends with: "Do NOT fix anything — I decide what to address."**

For the security and privacy pass, `security-auditor` covers the same ground with a
disclosure lens and a 🔴/🟡/🟢 severity split — run it on any diff touching logging,
config, fixtures or provider routing.

⚠️ **Forked review returns a summary, not the raw findings.** With `context: fork`, only
the subagent's final message comes back. For six of the nine that is pure gain; for
`/review` it is the compaction problem one layer down — **a reviewer that silently drops
three of eleven findings has made a Gate 3 decision that belongs to you.** The
✅/❌/🔧 contract in `review.md` must therefore be treated as a **hard return format,
every finding, no editorial filtering** — not a formatting suggestion. See §11-Q4d.

*The residual weakness (planner = reviewer) and its mitigations → `dual_harness_analysis.md` §4-R.*

**Apply fixes in OpenCode** (Gate 1.5 in the other direction first), then review again.
**This is Gate 3.**

---

### Step 5 — Commit (YOU — manually)

```bash
git add -p                    # interactive, hunk by hunk — never blind `git add .`
```

Then `/commit-msg` — it reads the full staged diff and the file-level summary, enforces
conventional-commits types and scopes, requires a **content-mapping in the body when the
diff relocates or deletes content** (git won't detect a rename when one file becomes
several), applies the deposition test to the message itself, flags a staged decision with
a rejected alternative and no ADR, and suppresses the `Co-Authored-By` trailer. Review
it, then commit yourself:

```bash
git commit -m "feat(guardrails): add PII leak scanner for AI responses

Regex-based scanner for SSN, phone, email patterns.
Runs on every AI response before display.
Tests cover detection, edge cases, and false positives.

Refs #12"
```

**Rules:** one logical change per commit · read the generated message before using it ·
`conventional-pre-commit` will reject a non-conforming message at the `commit-msg` stage
(CORRECTION 21 Tier C), so a malformed message fails locally, not in review.

**This is Gates 4 and 5.**

---

### Step 6 — Push and PR

```bash
git push -u origin feature/XX-short-description
```

`/pr-prep` — reads `@.github/pull_request_template.md` and
`@.github/docs/project_labels.md`, diffs `main...HEAD`, lists branch commits, checks
whether `docs/adr`, `architecture.dsl`, `docs/diagrams` or `README.md` changed, and emits
the PR body in the template's exact section order. **Packs ticked must match the Issue
and the brief — a mismatch is flagged, not guessed.** Validation results are left as
`<TODO: paste output>` rather than invented. **Does not create the PR.**

**This is Gate 6 — the last one. Push is always manual.**

---

### Step 7 — Post-merge cleanup

```bash
git checkout main
git pull origin main
git branch -d feature/XX-short-description
```

---

### 4.8 Greenfield vs. existing codebase — when does work need an Issue?

**Yes, greenfield work gets Issues too. The unit is the deliverable, not the file.**

**Granularity rule — one Issue per deliverable that has its own acceptance criteria and
could ship as one reviewable PR.** Derive them from
`@.github/docs/FLAGSHIP_CHECKLIST.md`, which is already the definition-of-done bar.

| ✅ One Issue | ❌ Not an Issue |
|---|---|
| "Scaffold repo to production standard: `pyproject.toml` + uv, ruff, mypy, pre-commit Tier A, CI, `src/` layout" | One Issue per config file |
| "Add `settings` + structlog observability layer with PII-redaction processor" | "Create `logging.py`" |
| "First vertical slice: ingest → validate → write, with tests" | "Add a function" |
| "Wire the eval harness and make it merge-blocking in CI" | Renaming a variable |

Roughly **4–8 Issues to first working slice**, not thirty. If you cannot write testable
acceptance criteria for it, it is not an Issue — it is a step inside one.

**Exempt from the cycle entirely:** exploratory spikes on a throwaway branch, and
debugging (§10, item 2 — the split is wrong where the state is a hunch rather than an
artifact). Spike freely, then throw it away and open the Issue for the real thing.

#### ⚠️ Both commands degrade on an empty repo

`draft-issue` runs `find src -name '*.py' | head -100` and `task-brief` runs
`find src tests -name '*.py' | head -100`. **On a repo with no `src/` yet, both return
nothing** — so "modules in scope" comes back empty and the Files-to-Change table has
nothing to build from. The commands still work; they just cannot infer.

**On greenfield, supply the intended layout yourself** in the `/draft-issue` argument, and
read the resulting table as **files to *create*** rather than files to change. Everything
else in the template — decisions expected, acceptance criteria, edge cases, the uv-native
validation set — applies unchanged and is where the value is anyway.

*Why greenfield work gets Issues (scaffold Issue → ADR) → `dual_harness_analysis.md` §4-R.*

---

## 5. Control gates

| Gate | What | Who | When |
|------|------|-----|------|
| **0** | Issue approval | YOU | Before any planning |
| **1** | Task Brief approval | YOU | Before any code is written |
| **1.5** | 🆕 **Harness switch — clean tree** | YOU | **Every** transition between harnesses, both directions |
| **2** | Diff review | YOU | After every OpenCode stop point |
| **3** | Cross-harness review findings | YOU | You decide which findings to act on |
| **4** | Staging | YOU | `git add -p`, hunk by hunk |
| **5** | Commit message | YOU | Reviewed before committing |
| **6** | Push + PR | YOU | Manual `git push` after all gates pass |

**No agent crosses a gate. Gates 0–6 are human. Gate 1.5 is a shell command.**

---

## 6. Daily cycle

```
┌──────────────────────────────────────────────────────────────────────┐
│  DUAL-HARNESS WORKFLOW — DAILY CYCLE                                 │
│  🧠 = Claude Code / VS Code (read-only)   🔨 = OpenCode / Cursor      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  0. ISSUE     🧠 plan mode · issue_template + project_labels          │
│               → paste into GitHub                        [GATE 0]     │
│                                                                       │
│  1. BRIEF     🧠 plan mode · task_brief template                      │
│               → save .github/plans/issue-XX-task-brief.md [GATE 1]    │
│                                                                       │
│  2. BRANCH    git checkout -b feature/XX-description                  │
│               git status -sb → clean                                  │
│                                                                       │
│  ── SWITCH ── close 🧠 · git status --porcelain empty     [GATE 1.5]  │
│                                                                       │
│  3. BUILD     🔨 build | build-gated · execute the brief              │
│               NO commits · stop each step · git diff      [GATE 2]    │
│               make test && make lint                                  │
│                                                                       │
│  ── SWITCH ── idle 🔨 · diff complete and stable          [GATE 1.5]  │
│                                                                       │
│  4. REVIEW    🧠 FRESH session · read-only · vs Issue + brief         │
│               findings only, no fixes                     [GATE 3]    │
│               (fixes → back through GATE 1.5 → step 3)                │
│                                                                       │
│  5. COMMIT    git add -p → /commit-msg → review → commit  [GATES 4-5] │
│               YOU commit. YOU own the history.                        │
│                                                                       │
│  6. PR        git push → /pr-prep → paste into GitHub     [GATE 6]    │
│                                                                       │
│  7. CLEAN     merge → git branch -d → next issue                      │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```
