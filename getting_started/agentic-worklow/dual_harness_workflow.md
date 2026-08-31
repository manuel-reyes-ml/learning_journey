# Dual-Harness Development Workflow

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

---

## 0. What changed from v1.0

| | v1.0 (April 2026) | v2.0 (August 2026) |
|---|---|---|
| **Harnesses** | One — Cursor Agent | Two — Claude Code (VS Code) + OpenCode (Cursor) |
| **Planning** | Cursor Plan Mode | Claude Code plan mode, Opus 5 |
| **Building** | Cursor Agent Mode | OpenCode `build` / `build-gated`, build ladder |
| **Review** | Cursor Chat Mode — *same agent that wrote the code* | Claude Code, **fresh session, read-only, Sonnet 5** |
| **Write permission** | Implicit | **Explicit and exclusive — one writer, ever** |
| **Enforcement** | Prompt instructions ("do NOT commit") | `permissions.deny` + `guard.py` PreToolUse hook |
| **Gates** | 0–6 | 0–6 **plus Gate 1.5 (harness switch)** |
| **Plan artifacts** | `.cursor/plans/` | `.github/plans/` — harness-neutral, repo-tracked ⚠️ *pending path audit* |
| **Stale items** | `black` in `format.sh`; 6 `.mdc` rules; Roadmap v8.2 | Corrected — see §12 |

Everything not listed above is **carried forward unchanged**. The gate model, the
template hierarchy, the no-vibe-coding rule and manual commits are all v1.0 material
that survived the harness change intact — which is the point: **the harness changed,
the governance did not.**

---

## 1. The governing ruling — one writer, one reader

### 1.1 Topology

| Phase | Harness | Editor | Permission | Model | Output artifact |
|-------|---------|--------|-----------|-------|-----------------|
| **Plan** | Claude Code | VS Code | **read-only** | Opus 5 | Issue body · filled Task Brief |
| **Build** | OpenCode | Cursor | **sole writer** | build ladder (GLM-5.2 et al.) | Working-tree diff |
| **Review** | Claude Code | VS Code | **read-only, fresh session** | Sonnet 5 | Findings list — no fixes |
| **Commit / Push / PR** | — | — | **human only** | — | Git history |

**Read this table as a permission table, not a task table.** The phase names are
descriptive; the permission column is the ruling.

### 1.2 The invariant

> **Exactly one process may write to the working tree, and it is OpenCode.
> Claude Code never writes. The human commits.**

This is not a preference. CORRECTION 39 §6 already binds every build gate to a
**clean tree** precondition — without it, `git diff` mixes agent edits with uncommitted
work and diff review stops being trustworthy. Two concurrent writers destroy that
precondition directly, and the failure is silent:

- Uncommitted file writes from one agent are **visible to the other agent's reads**, so
  the second agent reasons over a half-written file and produces a correct-looking diff
  against wrong input.
- Concurrent staging operations target the same `.git/index` and corrupt it.
- The loser's changes disappear **without an error message**; you find out when the
  tests fail an hour later.

There is no coordination protocol that fixes this. The fix is exclusivity.

### 1.3 What enforces it

Per the Claude Code permissions documentation, **permission rules are enforced by
Claude Code itself, not by the model** — instructions in a prompt or in `CLAUDE.md`
shape what Claude *tries* to do, but do not change what Claude Code *allows*.

This is CORRECTION 39 §11's architecture-vs-persuasion distinction, restated by the
vendor. Apply it here:

| Layer | Mechanism | Status |
|-------|-----------|--------|
| ❌ Prompt text ("do not edit files") | — | **Persuasion.** Not a boundary. |
| ⚠️ `defaultMode: "plan"` | Session mode | **Soft.** Toggleable mid-session; see §11-Q1. |
| ✅ `permissions.deny` | Settings file | **Architecture.** Deny → ask → allow; deny always wins. |
| ✅ `guard.py` PreToolUse hook | Shell hook, exit code 2 | **Architecture.** Runs before the permission prompt. |

**Reviewer/planner posture — `.claude/settings.json`:**

```jsonc
{
  "permissions": {
    "defaultMode": "plan",
    "deny": [
      "Edit",                      // bare tool name → removed from Claude's context entirely
      "Write",                     //   "
      "NotebookEdit",              //   " — NOT covered by a Read deny rule; must be named
      "Bash(git add *)",
      "Bash(git commit *)",
      "Bash(git push *)",
      "Bash(ruff format *)",       // formatter mutates source
      "Bash(ruff check --fix *)",  // --fix mutates source
      "Read(.env)",
      "Read(**/*.key)"
    ],
    "disableBypassPermissionsMode": "disable",
    "disableAutoMode": "disable"
  }
}
```

Four documented behaviours this configuration relies on, recorded because each is
load-bearing and none is obvious:

1. **Deny → ask → allow.** First match in that order wins; rule specificity does not
   change the order. A deny rule **cannot carry allowlist exceptions**.
2. **A bare tool name in `deny` removes the tool from context entirely** — Claude never
   sees `Edit` at all, rather than seeing it and being blocked. This is strictly
   stronger than a path-scoped deny.
3. **`Edit` rules cover all built-in file-editing tools — except `NotebookEdit`.** A
   `Read` deny also blocks Edit and Write on the same path, but not NotebookEdit. Given
   five notebook-bearing repos (CORRECTION 21 Tier B), `NotebookEdit` must be named
   explicitly. Path rules written against `Write`, `NotebookEdit`, `Glob` or `MultiEdit`
   are **accepted and never consulted** — use `Edit(path)` and `Read(path)` only.
4. **Deny beats every scope, including managed settings and CLI flags.** If a tool is
   denied at any level, no other level can allow it. `disableBypassPermissionsMode` set
   in your own settings locks *you* out of bypass mode — a self-imposed hard floor,
   which is the correct posture for a governance model whose whole value is that you
   cannot talk yourself past a gate at 11 p.m.

`guard.py` remains in place and is **not redundant**. PreToolUse hooks run *before* the
permission prompt, and a hook exiting with code 2 stops the call before permission rules
are evaluated at all. It also covers the gap in §1.4, which deny rules cannot.

**Historical note, recorded because it explains why the hook is not optional:** a filed
Claude Code issue reported that `settings.json` deny rules — for Read, Edit, Write,
whole tools, and Bash commands — were **not enforced at all** in one release, and the
recommended workaround was precisely a PreToolUse hook. Whether that has been fixed in
the installed version is **§11-Q2: verify before relying on deny alone.**

### 1.4 ⚠️ Recorded gap — `Edit` deny is not a complete write boundary while Bash is live

Read and Edit deny rules apply to Claude's built-in file tools and to file commands
Claude Code recognises inside Bash (`cat`, `head`, `tail`, `sed`). **They do not apply
to arbitrary subprocesses that open files themselves** — a Python or Node script that
writes to disk is invisible to them.

Consequence: `python -c "open('src/x.py','w').write(...)"` routes around a full
`Edit`/`Write`/`NotebookEdit` deny. The review harness needs Bash to run `pytest`,
`mypy` and `ruff check`, so Bash cannot simply be denied.

**This gap is logged as outstanding work, not claimed as closed** — the same treatment
CORRECTION 41 §4 gave the `gitleaks` SSN gap. Three candidate remedies, none adopted yet:

- **`guard.py` inspects Bash payloads** for write vectors (`>`, `>>`, `open(...,'w')`,
  `Path.write_*`, `shutil.copy`) and exits 2. Cheapest; consistent with the existing hook.
- **OS-level sandboxing.** Restricts the Bash tool's filesystem access for the command
  and its child processes. Strongest; largest configuration surface.
- **Accept it, and rely on the real invariant** — see below.

**The honest formulation of the invariant, which narrows the gap considerably:**

> The rule is not *"no bytes are written."* It is ***`git status` stays clean.***

`pytest` writing `.pytest_cache/`, `ruff` writing its cache, `mypy` writing
`.mypy_cache/` — all gitignored, all harmless, none of which break diff review. What
breaks diff review is a **tracked source file changing under the reviewer**. Gate 1.5
(§4) checks exactly that, and checks it at the boundary where it matters.

### 1.5 Model allocation

| Step | Model | Reasoning |
|------|-------|-----------|
| **Plan** | Opus 5 (Claude Code) | CORRECTION 39 §7's own logic: plan output is the architecture every later build depends on, **a bad plan propagates silently where a bad diff does not**, and plan volume (~80–120 calls/mo) is low enough that a cheaper model buys nothing. That reasoning selects the *best available* model for the lowest-volume, highest-leverage step. |
| **Build** | Build ladder in `opencode.jsonc` | Unchanged. Flat-capped OpenCode Go absorbs the token volume. |
| **Review** | Sonnet 5 (Claude Code) | Review is **per-diff and therefore high-volume**, the opposite economics from planning. Opus 5 consumes the subscription cap several times faster than Sonnet for equivalent work. |

**⚠️ Budget reality — record it, do not discover it.** On Pro, Sonnet and Opus draw from
a **single shared pool**, and that pool is shared across Claude Code, Claude.ai chat and
Cowork. Roadmap-governance sessions in the browser therefore draw from the same budget
as Opus planning. Independent practitioner guidance lands on exactly the allocation
above: default to Sonnet, save Opus for planning, one scoped task per session, clear
between tasks.

**Cross-family review comes free with the topology.** Building on GLM-5.2 and reviewing
on Sonnet 5 puts the writer and the reviewer in **different training distributions** —
the condition the adversarial-review literature says is required for genuine
independence. This is a property of the split, not something that had to be engineered.

### 1.6 Which falsifier fired — for CORRECTION 42

CORRECTION 39 §9 declined Claude Code and wrote **one** falsifier: revisit if OpenCode's
speed penalty (~78% longer on identical tasks) costs more than $20/mo of the 25 hrs/week
budget.

**That falsifier has not fired, and should be retained.** This topology keeps the entire
build loop in OpenCode, so the speed penalty is unchanged — and the head-to-head figure
cuts *for* OpenCode as builder: the extra time came from OpenCode running full test
suites and safety checks by default, and it produced **29% more tests**. OpenCode also
spawns LSP servers and feeds compiler diagnostics back to the model after every edit, so
a type error introduced on one turn is corrected on the next. That is the *understand-
every-line* invariant enforced by mechanism.

**What fired instead was §9's stated *reason*, on a ground the falsifier did not
anticipate:** "a second **$20/mo** harness could not be justified against a $10 flat
subscription already covering the work." The roadmap toolkit table already carries
**Claude Pro at $20/mo as committed spend**, and Claude Code is included in it. The
marginal cost of the second harness is **$0**, not $20. The premise was false, not the
logic.

**CORRECTION 42 should therefore record:**
1. §9 overturned on **cost-premise correction**, not on the speed falsifier.
2. The speed falsifier **retained, unfired**, and still governing.
3. **Net recurring spend unchanged from CORRECTION 41** (−$10/mo vs pre-39 baseline).
4. **§10's decline of the Claude Code desktop GUI STANDS** — "writes to disk with no
   pre-write diff review." This topology uses the VS Code extension, read-only. The
   decline is untouched and its reasoning is *reinforced* by §1.3.
5. **A new falsifier for this ruling** (every standing ruling needs one): revert to a
   single harness if the review harness's false-positive rate (§10) makes the review
   step net-negative on the 25 hrs/week budget, or if Anthropic's shared-pool economics
   make Opus planning unaffordable at Pro tier without a Max upgrade.

---

## 2. Guiding principles — carried forward from v1.0, unchanged

### Source-of-truth hierarchy

1. **GitHub Issue** = contract (scope + acceptance criteria + validation)
2. **Task Brief** = execution plan derived from the Issue
3. **Code changes** = must satisfy the brief's acceptance criteria and validation plan

### Templates are mandatory inputs

When generating or reviewing Issues, PRs, task briefs or labels, **both harnesses** must
read and follow:

- `.github/templates/issue_template.md` — Issue format and required sections
- `.github/templates/project_labels.md` — approved labels + definitions/usage
- `.github/templates/pull_request_template.md` — PR body format + required sections
- `.github/templates/task_brief.md` — agent execution contract ⚠️ *renamed from
  `cursor_task_brief.md`; harness-neutral. See §12.*

These live in `.github/templates/` in every repo and are version-controlled. Every
Issue, PR, task brief and label conforms to these templates — no exceptions.

### The "no vibe coding" rule

- **YOU commit. YOU push. YOU create the PR.**
- Both harnesses generate commit messages, PR descriptions and review summaries — you
  approve them.
- Every diff is reviewed by you before it leaves your machine.
- OpenCode may run terminal commands (tests, linting) but **never** `git commit` or
  `git push`. Claude Code cannot run them at all — denied in `settings.json` (§1.3).

### Why manual commits beat agent commits

| Agent commits | Manual commits |
|---------------|----------------|
| "Surprise" changes in history | Every commit tells YOUR story |
| Hard to revert cleanly | Clean atomic commits you understand |
| Breaks "no vibe coding" | Forces you to review every diff |
| Recruiters see AI-generated history | Recruiters see professional commit hygiene |

---

## 3. Harness roles — when to use each

| Role | Where | Trigger | Use for | Can it write? |
|------|-------|---------|---------|---------------|
| **Claude Code — plan** | VS Code | `Shift+Tab` → Plan, or `/plan` | Architecture, scope, Issue drafting, Task Brief authoring | ❌ No |
| **Claude Code — review** | VS Code | Fresh session on a dirty tree | Diff review against the Issue and brief | ❌ No |
| **OpenCode — `build`** | Cursor terminal | Default build agent | Multi-file refactors; gates **after** the write via `git diff` | ✅ **Sole writer** |
| **OpenCode — `build-gated`** | Cursor terminal | Explicit selection | Unfamiliar libraries, single-file work; gates **before** each write | ✅ **Sole writer** |
| **Claude (browser project)** | claude.ai | — | Roadmap governance, corrections, cross-project strategy | ❌ No repo access |

### `build` vs `build-gated` — the selection rule (CORRECTION 39 §6, restated)

**Neither is universally correct.** Pre-write gating suits unfamiliar libraries and
single-file work, where the slowdown *is* the value. It is **wrong for large multi-file
refactors** — the S2 Polars ingestion rewrite is the named case — because per-edit
approval hides the whole-change picture, and long prompt chains produce reflex approval:
**a gate that feels real but is not.**

**Precondition binding on both:** start every session on a clean tree.

---

## 4. Step-by-step workflow

### Step 0 — Draft the Issue (Claude Code, plan mode)

**Goal:** a GitHub Issue that is explicit and testable, in the repo's standard format.

Open VS Code, start Claude Code, confirm the mode indicator reads **Plan**.

```
Read .github/templates/issue_template.md and .github/templates/project_labels.md.

Draft a GitHub Issue for: [one-sentence goal].

Review every module in src/ to identify affected files globally.
Include explicit acceptance criteria as checkboxes, and a validation/smoke-test
plan with commands and expected outcomes.
Recommend labels from project_labels.md ONLY — one sentence of justification each.

Output the final Issue body as Markdown, ready to paste into GitHub.
```

**Alternative — Claude (browser project)** for issues needing roadmap-level strategic
alignment across the four flagships. Claude Code sees the repo; browser Claude sees the
portfolio. Pick on which context the issue actually needs.

**Outcome:** paste into GitHub. Apply the suggested labels. **This is Gate 0.**

---

### Step 1 — Generate the Task Brief (Claude Code, plan mode)

**Goal:** convert the approved Issue into a precise execution contract that OpenCode
follows without inheriting any of the planning conversation.

```
Read .github/templates/task_brief.md.

Generate a complete Task Brief for Issue #XX.
Review all modules in src/ and tests/ to identify the exact files to change.
Fill in every section: objective, files to change, execution steps with stop points,
acceptance criteria, edge cases, validation commands.
Enforce: no commits, no pushes, minimal incremental changes.

Write the brief as a Markdown code block. I will save it to
.github/plans/issue-XX-task-brief.md myself.
```

**Non-interactive route** — for generating the artifact in one shot without a session:

```bash
claude -p --permission-mode plan \
  "$(cat .github/templates/task_brief.md) — fill this out for Issue #XX" \
  > .github/plans/issue-XX-task-brief.md
```

⚠️ **§11-Q3: verify this once before relying on it.** The `-p` + `--permission-mode plan`
combination outputting the plan to stdout with no approval dialog is reported by a
secondary source, not confirmed against first-party docs. Note also that `claude -p`
**never shows the workspace-trust dialog**, which changes which project configuration
loads — read the trust table in the permissions docs before making this the default path.

#### 🔑 Why the brief-on-disk is the load-bearing artifact

The standard objection to planning in one tool and building in another is context loss.
**Your workflow already paid that cost in v1.0, and that is what makes this topology
nearly free for you where it is expensive for others.**

An independent 2026 write-up on agent harnesses describes your architecture almost
verbatim: the output of the planning conversation is not more conversation but a **spec
file written to disk and handed to Cursor or Claude Code for execution** — and it exists
precisely because the planning and execution stages must not share memory implicitly.
If they did, the executing agent would inherit whatever the planner happened to be
thinking about at the moment of handoff, **including the dead ends and half-formed ideas
that got walked back three messages earlier.**

The same distinction, put more sharply elsewhere: a handoff is **boundary-aligned,
deliberate, inspectable, diffable and on disk**, where the alternative — auto-compaction
under token pressure — is lossy in an uncontrolled way, invisible, unversioned, and does
not survive to reach a different agent.

**The Task Brief is not overhead you tolerate for the sake of the split. It is the
mechanism that makes the split safe.**

**Review the brief before proceeding.** Right files? Right order? Testable criteria?
Would you actually run those validation commands? Edit it directly if not — this is your
last chance to correct scope before code is written. **This is Gate 1.**

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

**Why the Build → Review direction still needs a gate even though the reviewer cannot
write:** the reviewer reasons over a diff. If OpenCode is still mid-edit, the reviewer
reads a partially written file and produces confident findings against input that no
longer exists thirty seconds later. **Read-only does not mean concurrency-safe.**

---

### Step 3 — Build (OpenCode — sole writer)

**Goal:** ~90% of the code changes, following the brief step by step.

Open Cursor. OpenCode runs in the **integrated terminal** — detection relies on terminal
environment variables, so an external terminal will not work (CORRECTION 39 §1).

Select `build` or `build-gated` per §3.

```
Execute the task brief in .github/plans/issue-XX-task-brief.md.
Follow the execution steps in order. Stop after each step and report what changed.
Do NOT commit or push.
```

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

#### The rule this step exists to satisfy

**The model that wrote the code must not review it.** The evidence is consistent across
independent 2026 sources:

- LLMs measurably **favour their own output** under self-review, which makes the writing
  agent a weak checker for its own incorrect diff.
- A single-context reviewer **shares the generator's assumptions, training biases and
  blind spots**; the same model that rationalised a shortcut during implementation will
  rationalise it again during review.
- The sharpest version: **self-review is least reliable on incorrect code — which is the
  only code review exists to catch.**
- The reviewer must start in a **fresh context**, because build-phase conversation
  history contaminates the review. On any retry, spawn a new session; anchoring bias
  affects models as it does humans.

**Procedure:**

1. Close or idle OpenCode. Run **Gate 1.5**.
2. Open Claude Code in VS Code. **Start a new session** — do not resume, do not
   `/compact`, do not reuse the planning session.
3. Confirm read-only posture is active (`/permissions`).
4. Invoke:

```
Review the diff on this branch against BOTH:
  1. GitHub Issue #XX — the contract
  2. .github/plans/issue-XX-task-brief.md — the execution plan

Check for:
- Correctness and the edge cases named in the Issue
- Repo conventions: type hints, NumPy docstrings, structlog %s/%d lazy formatting
- `from __future__ import annotations` in every new module
- Polars idiom violations per python-core.md — pandas signatures against Polars objects
- Test coverage gaps against the acceptance criteria
- Anything real in a fixture. Synthetic data only.

You are explicitly licensed to conclude that THE PLAN ITSELF WAS WRONG.
Do not propose scope expansion. Do NOT fix anything — report only.

Output: ✅ passing · ❌ failing with file:line · 🔧 one-line suggested fix each.
```

#### ⚠️ The residual weakness, stated rather than hidden

Claude Code both **authors the plan and reviews against it**. That reintroduces
self-review one level up: a reviewer grading "did OpenCode follow my plan" instead of
"is this correct." Three mitigations, all active:

1. **The review is anchored to the Issue, not only the brief.** The Issue is the Gate 0
   artifact and is human-approved.
2. **You are Gate 1.** The brief was ratified by a human before the build began. The
   reviewer is not checking an unreviewed plan; it is checking against a contract you signed.
3. **The reviewer is explicitly licensed to reject the plan.** Written into the prompt above.

A fourth mitigation exists and is **declined for now**: pinning the reviewer to a
non-Anthropic model would remove the shared-family bias entirely, but the only harness
that can host it is OpenCode — the writer's harness — which would put review back in the
same context as build and trade a smaller bias for a larger one. **Falsifier:** adopt a
third read-only harness only if the review step is measurably missing defects that
OpenCode's LSP loop already catches.

**Apply fixes in OpenCode** (Gate 1.5 in the other direction first), then review again.
**This is Gate 3.**

---

### Step 5 — Commit (YOU — manually)

```bash
git add -p                    # interactive, hunk by hunk — never blind `git add .`
```

Generate the message with `/commit-msg` in **either** harness (both read the same prompt
body — see §8.3), then review it and commit yourself:

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

Invoke `/pr-prep`. It reads `pull_request_template.md` and `project_labels.md`, diffs
`main...HEAD`, reads the Issue from the commit footers, and outputs a paste-ready PR body
with `Closes #XX` and label suggestions.

**This is Gate 6 — the last one. Push is always manual.**

---

### Step 7 — Post-merge cleanup

```bash
git checkout main
git pull origin main
git branch -d feature/XX-short-description
```

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

---

## 7. Repository layout — the dual tree

```
repo-root/
├── AGENTS.md                          # ⭐ SHARED governance — both harnesses read this
├── opencode.jsonc                     # canonical location = repo root (ADR-001 §5a)
│
├── .claude/                           # Claude Code — PLAN + REVIEW, read-only
│   ├── settings.json                  # permission policy (§1.3) — COMMITTED
│   ├── settings.local.json            # machine-local overrides — GITIGNORED
│   ├── agents/                        # subagents (generated — see below)
│   │   ├── docs-fix.md                # ⚠️ WRITER — see §8.2
│   │   ├── docs-sync.md               # ⚠️ WRITER — see §8.2
│   │   ├── eval-guardian.md
│   │   ├── pattern-scout.md
│   │   └── security-auditor.md
│   ├── commands/                      # ⚠️ PROPOSED: was skills/ — see §8.1
│   │   ├── commit-msg.md              # !`cat` stubs → .github/docs/prompts/
│   │   ├── draft-issue.md
│   │   ├── eval.md
│   │   ├── labels.md
│   │   ├── pr-prep.md
│   │   ├── readme.md
│   │   ├── review.md
│   │   ├── task-brief.md
│   │   └── test.md
│   ├── hooks/
│   │   └── guard.py                   # PreToolUse — commit gate, secrets, PII, write vectors
│   ├── output-styles/
│   │   └── learn.md                   # ⚠️ requires write access — see §9
│   └── rules/
│       ├── ai-sdk-patterns.md
│       ├── architecture-docs.md
│       ├── git-workflow.md
│       ├── observability.md
│       ├── project-scaffold.md
│       ├── python-core.md
│       ├── streamlit-patterns.md
│       └── testing-and-eval.md
│
├── .opencode/                         # OpenCode — BUILD, sole writer
│   ├── agents/
│   │   ├── docs-fix.md
│   │   ├── docs-sync.md
│   │   ├── eval-guardian.md
│   │   ├── learn.md
│   │   ├── pattern-scout.md
│   │   └── security-auditor.md
│   └── commands/                      # @ live imports → .github/docs/prompts/
│       ├── commit-msg.md   draft-issue.md   eval.md      labels.md
│       ├── pr-prep.md      readme.md        review.md    task-brief.md
│       └── test.md
│
├── .github/
│   ├── docs/prompts/                  # ⭐ SINGLE SOURCE — prompt bodies live here once
│   ├── templates/
│   │   ├── issue_template.md
│   │   ├── project_labels.md
│   │   ├── pull_request_template.md
│   │   └── task_brief.md              # ⚠️ renamed from cursor_task_brief.md
│   ├── plans/                         # ⚠️ PROPOSED: was .cursor/plans/ — see §12
│   │   └── issue-XX-task-brief.md
│   └── workflows/ci.yml               # authoritative gate — hooks are a strict subset
│
├── scripts/
│   └── build_claude_agents.py         # generator — Claude Code has no native subagent import
├── .pre-commit-config.yaml            # Tier A/B/C per CORRECTION 21
└── docs/adr/                          # Nygard template
```

**Note on `.cursor/`:** with OpenCode hosted in Cursor's integrated terminal and Cursor
on Hobby tier (CORRECTION 40), `.cursor/rules/`, `.cursor/commands/` and `.cursor/hooks/`
are **no longer part of the workflow**. Removal is a separate change requiring its own
capability audit — **not performed here.**

---

## 8. Commands, skills, agents

### 8.1 ⚠️ Ruling proposed — `.claude/skills/` → `.claude/commands/`

Your screenshot shows the nine workflow prompts under `.claude/skills/` (directories),
where OpenCode has them under `.opencode/commands/` (files). That asymmetry matters:

**Skills auto-invoke based on context. Slash commands require you to type something first.**

In a workflow whose entire value is explicit gates, **auto-invocation is a gate leak**.
An auto-fired `/commit-msg` or `/pr-prep` is a prompt you never typed, arriving at a
moment you did not choose. Worse, in a read-only harness a `pr-prep` skill that fires
during a *review* session is producing a PR body for a diff you have not yet approved.

**Proposal:** move the nine to `.claude/commands/` (manual invocation). Reserve
`.claude/skills/` for genuine auto-loading domain knowledge — a Polars-idiom skill, an
ERISA-fixture skill — where firing unbidden is the feature, not the bug.

**Two things to verify first (§11-Q4):** Claude Code ships **built-in** `/review` and
`/code-review`, so your custom `review` may shadow or be shadowed by one of them; and one
source reports that a 2026 release **merged the skills and commands concepts**, which
would soften or void this ruling entirely. **Settle by observation — run `/review` once
in each location and read what actually loads.**

### 8.2 ⚠️ Two agents are writers and must be handled

`.claude/agents/` currently mirrors `.opencode/agents/`. Under a read-only Claude Code,
two of the five contradict the posture:

| Agent | Claude Code disposition |
|-------|------------------------|
| `docs-fix` | ❌ **Writer.** Deny it, or convert to propose-a-patch-don't-apply. |
| `docs-sync` | ❌ **Writer.** Same. |
| `eval-guardian` | ✅ Read-only — keep |
| `pattern-scout` | ✅ Read-only — keep |
| `security-auditor` | ✅ Read-only — keep |

Deny is architectural and cheap — `Agent(AgentName)` rules are documented:

```jsonc
"deny": ["Agent(docs-fix)", "Agent(docs-sync)"]
```

**Do not delete the files.** `build_claude_agents.py` generates them from the shared
source; deleting the output while the source stands guarantees drift on the next run.
**Deny at the permission layer, keep the file, and record the reason** — declined
options are logged with rationale, not silently omitted.

The same rules also gate model tier: `Agent(model:opus)` matches subagent calls that
request the Opus tier, which is a usable lever for the **model-ladder ADR** still on the
horizon.

### 8.3 Shared prompt bodies — the drift risk this topology introduces

Current architecture (unchanged and correct): bodies live once in
`.github/docs/prompts/`; OpenCode uses live `@` imports; Claude Code commands use
`` !`cat` `` stubs. `build_claude_agents.py` regenerates the Claude Code side;
`claude-agents-check` enforces it at the commit boundary.

**What v2.0 breaks:** the `review` prompt is no longer harness-neutral. The OpenCode
version reviews its own work in-context; the Claude Code version reviews a foreign diff
from a cold start against the Issue. **Same name, different contract.**

**Proposed split:**

| Prompt | Shared body? |
|--------|-------------|
| `draft-issue` · `task-brief` · `pr-prep` · `labels` · `readme` · `commit-msg` | ✅ Shared — harness-neutral |
| `test` · `eval` | ✅ Shared — both just run and report |
| `review` | ❌ **Split** — `review-build.md` (OpenCode, in-context) / `review-cross.md` (Claude Code, cold, vs Issue) |

Single-source-no-drift is preserved: **one body per contract**, not one body per name.

---

## 9. Declined, with falsifiers

**🚫 Git worktrees for parallel agents.** The dominant isolation primitive for
concurrent agents, natively supported by Claude Code and Cursor, and it genuinely solves
the §1.2 failure mode. **Declined:** the one-writer rule makes it unnecessary at a
single-developer, one-feature-at-a-time cadence, and it adds a directory layer, per-tree
environment setup and duplicated `node_modules`/`.venv` for no gain. Practitioners also
warn that worktrees defer conflicts to merge rather than removing them, and that
lockfile churn from two agents adding dependencies is miserable to resolve by hand.
**Falsifier:** adopt the moment two feature branches must genuinely progress in parallel
— e.g. DataVault Track A and Track B running concurrently in Week 12.

**🚫 Claude Code as builder.** Faster on identical tasks and better-integrated. Declined
because OpenCode's LSP diagnostic loop and default full-test-suite runs are the mechanism
that enforces *understand every line*, and because the build ladder is absorbed by a flat
$10/mo cap where Claude Code build volume would draw on the shared Pro pool that Opus
planning needs. **Falsifier:** the CORRECTION 39 §9 speed falsifier, retained verbatim.

**🚫 Claude Code desktop GUI.** Unchanged from CORRECTION 39 §10 — writes to disk with
no pre-write diff review. **The decline stands and this document reinforces it.**

**🚫 A third read-only harness for cross-vendor review.** See §4. **Falsifier:** review
demonstrably missing defects the LSP loop already catches.

**⏸️ `learn.md` output style — deferred, not declined.** CORRECTION 39 §9 named it as
the only native mechanisation of the conceptual-inquiry pattern found in the survey: it
inserts `TODO(human)` markers asking you to implement the strategic pieces. **It
requires write access, which this topology denies.** For now, accept the loss — OpenCode's
`build-gated` enforces the same invariant by configuration, which was §9's own argument.
**Falsifier / future option:** carve a narrow *learning lane* — a dedicated branch,
single-file scope, Claude Code temporarily granted `Edit`, OpenCode closed, Gate 1.5 on
both sides. Adopt only if a Stage 2 module proves `build-gated` is not producing the same
conceptual engagement. **Do not carve it pre-emptively** — an exception that exists
before it is needed is an exception that gets used when it is not.

---

## 10. Counter-evidence, recorded

Recorded because it cuts against this ruling, in keeping with the governance model.

**1. External LLM reviewers over-flag.** Research reports that LLM reviewers
**systematically flag correct code as non-compliant**, and that adding explanation
requirements **worsens** the false-positive rate. Mitigations, both already in place:
the review prompt is report-only, never fix; and findings are advisory input to Gate 3,
where you decide. **Track the false-positive rate for the first week** — that number is
the evidence CORRECTION 42's falsifier should be written against.

**2. Handoff is wrong for some work.** A chain of handoffs is wrong for **exploratory
debugging where the state is a hunch rather than an artifact**, for plans short enough
that context accumulation never bites, and for tightly coupled units where the boundary
is artificial. **Consequence: debugging sessions are exempt from this workflow.** Stay in
one harness, no brief, no cross-harness review. The split is for planned work against an
Issue.

**3. Handoff loops are the number-one multi-agent failure mode** — agent A passes to B,
B to C, C back to A, with context loss compounding at every transfer because nobody owns
the task. **This topology is not exposed to it:** the chain is linear, terminates at a
human at every gate, and the human owns the task throughout. Recorded so the exemption
is deliberate rather than lucky.

---

## 11. Open questions — settle by observation, not assumption

Same discipline as CORRECTION 39 §13. Each of these has a one-command answer; none
should be resolved by reasoning.

**Q1 — Is plan mode a boundary or a suggestion?** Sources conflict. One vendor-adjacent
guide describes it as structurally incapable of making changes; a code-level analysis of
the implementation reports that the file-writing tools **remain present**, that a prompt
is injected reminding the agent it is read-only, and that there is **no other
enforcement** visible. **Test:** in plan mode, with the §1.3 denies temporarily removed,
ask Claude Code to write a file. Record the result. **Until answered, treat plan mode as
convenience and `permissions.deny` as the boundary.**

**Q2 — Are deny rules actually enforced in the installed version?** A filed issue
reported total non-enforcement in one release. **Test:** with `"deny": ["Edit"]` active,
ask for an edit. If it succeeds, `guard.py` is the *only* boundary and must be hardened
before this workflow is used.

**Q3 — Does `claude -p --permission-mode plan` emit the plan to stdout?** §4 Step 1.
**Test:** run it once, redirect to a file, inspect.

**Q4 — `.claude/skills/` vs `.claude/commands/` in the installed version.** §8.1. Also:
does a custom `review` shadow the built-in `/review`, or the reverse?

**Q5 — Does the `` !`cat` `` stub expansion in a Claude Code command respect the active
permission mode?** This is the direct analogue of CORRECTION 39 §13's unresolved question
about OpenCode's `` !`shell` `` expansion, and it has the same shape: if expansion respects
the mode, the shell-running commands break under a read-only posture; if it does not,
read-only is not a boundary against commands. **Test:** run `/test` once from a
plan-mode session.

**Q6 — Does `git status --porcelain` stay empty across a full review session?** The
§1.4 formulation depends on it. **Test:** run it before and after one review.

---

## 12. Drift corrected from v1.0

| v1.0 location | Was | Now | Authority |
|---|---|---|---|
| Line 412, `format.sh` | `black "$1"` | ruff — `black` is superseded and is not in the standard | CORRECTION 21 §9 corrected this in **seven scope documents; this file was missed** |
| Lines 429–435 | 6 `.cursor/rules/*.mdc` incl. `learning-mode`, `python-production-standards`, `evaluation` | 8 `.claude/rules/*.md` per §7 | Repo state |
| Line 8, Applies to | DataVault, PolicyPulse, FormSense, ODI, StreamSmart, AFC | **Four flagships** — PolicyPulse, DataVault, Crucible, PostCheck — plus FormSense, AFC | Roadmap v10.0 |
| Line 537 | "Aligned with Roadmap v8.2" | Roadmap v10.0, CORRECTIONS 39–41 | Roadmap v10.0 |
| Template name | `cursor_task_brief.md` | `task_brief.md` — harness-neutral | This document |
| Plan directory | `.cursor/plans/` | `.github/plans/` — harness-neutral, sits beside `.github/templates/` | This document |
| Step 4 heading | "Self-Review" | "Cross-harness review" — the whole point is that it is **not** self-review | §4 |

⚠️ **The last two are renames and are NOT executed by this document.** Both require a
path-hardcoding audit before they are safe — the same audit already outstanding for the
`agent/` → `agents/` rename, covering `build_claude_agents.py`, the `claude-agents-check`
pre-commit hook, all nine command bodies in `.github/docs/prompts/`, and any scope
document referencing `cursor_task_brief.md`. **Capability audit before destructive edits.**

---

## 13. Migration notes: Codex → Cursor → dual harness

| What changes | What stays the same |
|---|---|
| Two editors open, one at a time | Control gates — you always approve |
| Write permission is explicit and exclusive | Manual commits and pushes |
| Review is a foreign agent on a cold read | Issue → Plan → Code → Review → PR cycle |
| Plans are harness-neutral, in `.github/plans/` | Templates are the source of truth for Issues, PRs, briefs, labels |
| Enforcement moved from prompt text to `settings.json` + hook | "No vibe coding" — every line understood before commit |

### What survived from v1.0 intact

- **The four templates** — still the single source of truth, now read by both harnesses.
- **The Task Brief concept** — which turns out to be the *enabling* mechanism for the
  dual harness rather than a cost of it (§4 Step 1).
- **Gates 0–6** — unchanged, with 1.5 inserted.
- **Claude (browser project)** — still the strategic advisor for roadmap-aligned decisions.

### What v1.0 got right and should be kept in mind

v1.0's Step 4 already instructed the reviewer *"do NOT propose scope expansion, only
recommend fixes and missing tests,"* and `.cursor/commands/review.md` already said *"do
NOT fix anything — report only."* Both instincts were correct and both are preserved
verbatim. **What v1.0 could not fix was that the reviewer and the writer were the same
agent in the same context.** That is the single change this document exists to make.

---

**Document status:** v2.0 — proposal of record, pending CORRECTION 42
**Date:** August 30, 2026
**Replaces:** `cursor_workflow.md` v1.0 (April 06, 2026)
**Aligned with:** Roadmap v10.0 (CORRECTIONS 39, 40, 41) · ADR-001 §5a · `AGENTS.md`
**Blocking before ratification:** §11 Q1–Q6 answered by observation · §12 path audit ·
CORRECTION 42 written and signed off
**Not executed here:** scope-document propagation · `.cursor/` removal · the two renames
in §12 · the §8.1 skills→commands move
