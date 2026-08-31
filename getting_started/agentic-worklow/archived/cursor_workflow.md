# Cursor IDE: Production-Grade Development Workflow

## Building with Cursor Agent — From Issue to Merged PR

**Author:** Manuel Reyes
**Version:** 1.0
**Date:** April 06, 2026
**Applies to:** All portfolio projects (DataVault, PolicyPulse, FormSense, ODI, StreamSmart, AFC)

This workflow replaces the Codex dual-tool flow with a single-IDE approach using Cursor's
Plan Mode, Agent Mode, Commands, and Hooks. It preserves the same control gates and
production standards.

---

## Guiding Principles

### Source-of-truth hierarchy (unchanged)
1. **GitHub Issue** = contract (scope + acceptance criteria + validation)
2. **Task Brief** = execution plan derived from the Issue (filed-out `cursor_task_brief.md`)
3. **Code changes** = must satisfy task brief acceptance criteria and validation plan

### Templates are mandatory inputs
When generating or reviewing Issues, PRs, task briefs, or labels, Cursor must read and follow:
- `.github/templates/issue_template.md` — Issue format and required sections
- `.github/templates/project_labels.md` — approved labels + definitions/usage
- `.github/templates/pull_request_template.md` — PR body format + required sections
- `.github/templates/cursor_task_brief.md` — Agent execution contract (files, steps, validation, stop conditions)

These files live in `.github/templates/` of every repo and are version-controlled. Copy them
from the 1099 Reconciliation Pipeline repo when scaffolding new projects. Every
Issue, PR, task brief, and label must conform to these templates — no exceptions.

### The "no vibe coding" rule
- **YOU commit. YOU push. YOU create the PR.**
- Cursor generates commit messages, PR descriptions, and review summaries — you approve them.
- Every diff is reviewed by you before it leaves your machine.
- Cursor Agent can run terminal commands (tests, linting) but **never** `git commit` or `git push`
  unless you explicitly invoke a `/pr` command after reviewing the diff.

### Why manual commits beat agent commits
| Agent commits | Manual commits |
|---------------|----------------|
| "Surprise" changes in history | Every commit tells YOUR story |
| Hard to revert cleanly | Clean atomic commits you understand |
| Breaks "no vibe coding" principle | Forces you to review every diff |
| Recruiters see AI-generated history | Recruiters see professional commit hygiene |

---

## Cursor Modes — When to Use Each

| Mode | Trigger | Use For | Control Level |
|------|---------|---------|---------------|
| **Plan Mode** | `Shift+Tab` in agent input | Architecture, scope, implementation plan | You approve plan before any code |
| **Agent Mode** | Default agent input | Implementation, refactoring, tests, docstrings | Agent edits files; you review diffs |
| **Chat Mode** | Ask without executing | Explain code, compare approaches, debug thinking | No file changes |
| **Commands** | `/command-name` | Repeatable workflows (lint, test, pr-prep) | You define; agent executes |

### Mapping from Codex Workflow

| Codex Workflow Step | Cursor Equivalent |
|--------------------|-------------------|
| Browser Codex → Draft Issue using `issue_template.md` | `/draft-issue` command (reads same template) or Claude |
| Browser Codex → Suggest labels from `project_labels.md` | `/draft-issue` and `/pr-prep` both read `project_labels.md` |
| Browser Codex → Generate Task Brief using `vscode_codex_task_brief.md` | `/task-brief` command (reads `cursor_task_brief.md`) → Plan Mode fills it |
| VS Code Codex → Implementation | **Agent Mode** executes the task brief (no commits, no pushes) |
| Browser Codex → Review diff | **Chat Mode** with `@Branch` or `/review` command |
| Browser Codex → Write PR using `pull_request_template.md` | `/pr-prep` command (reads same template) |
| Browser Codex → Label hygiene | `/draft-issue` and `/pr-prep` suggest labels from `project_labels.md` |

---

## Step-by-Step Workflow

### Step 0: Plan the Issue (Plan Mode + Claude)

**Goal:** Produce a GitHub Issue that is explicit and testable, formatted
exactly like your repo's standard.

**Required inputs:**
- `.github/templates/issue_template.md` (Issue format)
- `.github/templates/project_labels.md` (approved labels only)

**Option A — Use Claude (this project) for issue drafting:**
Best for complex issues where you want strategic alignment with your roadmap.
Claude has full context of all 7 project scopes and your standards.

**Example prompt (Claude):**
> Using `.github/templates/issue_template.md`, draft a GitHub Issue for:
> **[one-sentence goal]**.
> Review all modules in main branch to identify affected files globally.
> Use `.github/templates/project_labels.md` to recommend the correct labels (only from that file).
> Include explicit acceptance criteria (checkboxes) and a validation/smoke test plan
> with commands and expected outcomes.
> Output the final Issue body in Markdown ready to paste into GitHub.

**Option B — Use Cursor Plan Mode:**
Best for implementation-focused issues where you already know the scope.

```
# In Cursor, toggle Plan Mode (Shift+Tab), then:

"Read .github/templates/issue_template.md and .github/templates/project_labels.md.
Plan the implementation for: [one-sentence goal].
Review all modules in src/ to identify affected files.
Output a complete GitHub Issue following the template with:
scope, acceptance criteria (checkboxes), files to change,
edge cases, validation commands with expected outputs,
and suggested labels from project_labels.md only."
```

**Save the plan:**
Click "Save to workspace" → stored in `.cursor/plans/issue-XX-description.md`

**Outcome:** Paste into GitHub Issue. Apply suggested labels.

---

### Step 1: Generate Task Brief (Plan Mode)

**Goal:** Convert the approved Issue into a precise execution contract that Agent Mode follows.

**Required input:**
- `.github/templates/cursor_task_brief.md` (task brief template)
- The GitHub Issue you just created (Issue #XX)

**Use Plan Mode (`Shift+Tab`) to fill out the template:**

```
"Read .github/templates/cursor_task_brief.md.
Generate a complete Task Brief for Issue #XX.
Review all modules in src/ and tests/ to identify the exact files to change.
Fill in every section: objective, files to change, execution steps with
stop points, acceptance criteria, edge cases, and validation commands.
Enforce: no commits, no pushes, minimal incremental changes.
Save the completed brief to .cursor/plans/"
```

**Or use the `/task-brief` command:**
Type `/task-brief 12` in the agent input (where `12` is the Issue number).

**Save the plan:**
Click "Save to workspace" → stored in `.cursor/plans/issue-XX-task-brief.md`

**Review the brief before proceeding:**
- Are the right files listed?
- Are the execution steps in the right order?
- Are the acceptance criteria testable?
- Do the validation commands match what you'd actually run?

Edit the brief directly if anything needs adjustment. This is your last chance to
correct scope before the agent starts writing code.

**Outcome:** A filled-out task brief saved in `.cursor/plans/` — the execution contract for Step 3.

---

### Step 2: Pre-Implementation Checkpoint

Before Cursor touches any code:

```bash
# Create feature branch from latest main
git checkout main
git pull origin main
git checkout -b feature/XX-short-description

# Defensive checkpoint (clean state to revert to)
git status -sb   # Should be clean
```

**Why:** If the agent produces something you don't like, `git checkout .` returns
you to this clean state instantly.

---

### Step 3: Implementation (Agent Mode — Executes Task Brief)

**Goal:** Do ~90% of the code changes here, following the task brief step by step.

**Rules for Agent Mode:**
- Create/edit modules, refactor, add docstrings, update tests ✅
- Run `pytest`, `ruff check`, `make lint` via terminal ✅
- **Do NOT commit. Do NOT push.** ❌
- Follow the task brief execution steps in order
- **STOP at each stop point** and report the diff

**How to start — paste the task brief into Agent Mode:**

```
"Execute the task brief in .cursor/plans/issue-XX-task-brief.md.
Follow the execution steps in order. Stop after each step and
report what changed. Do NOT commit or push."
```

**After each Agent stop point, review:**

```bash
git status -sb          # What files changed?
git diff                # Exactly what changed?
git diff --stat         # Summary of changes
```

**Run validation per the task brief:**

```bash
make test               # All tests pass?
make lint               # No linting errors?
```

**If something goes wrong:**

```bash
# Undo everything the agent did (back to last checkpoint)
git checkout .
git clean -fd

# Or undo specific files
git checkout -- src/ai/guardrails.py
```

---

### Step 4: Self-Review (Chat Mode)

**Goal:** Use Cursor as a reviewer to catch edge cases without expanding scope.

```
# In Chat Mode (no file edits):

"Review the diff on this branch (@Branch) against the acceptance criteria
in .cursor/plans/issue-XX-task-brief.md. Check for:
- Correctness and edge cases listed in the task brief
- Consistency with repo conventions (type hints, docstrings, logging)
- Test coverage gaps
- from __future__ import annotations in every new module
Do NOT propose scope expansion. Only recommend fixes and missing tests."
```

**Apply fixes in Agent Mode, then review the diff again.**

---

### Step 5: Commit (YOU — Manually)

**Goal:** Create clean, atomic commits with professional messages.

**Option A — Write commit message yourself:**

```bash
git add -p                    # Interactive staging (review each hunk)
git commit -m "feat(guardrails): add PII leak scanner for AI responses

Regex-based scanner for SSN, phone, email patterns.
Runs on every AI response before display.
Tests cover detection, edge cases, and false positives.

Refs #12"
```

**Option B — Let Cursor generate the message, you approve:**

```
# In Chat Mode:
"Look at @Commit (Diff of Working State). Write a commit message
following conventional commits format: type(scope): description.
Include a body explaining what and why. Add 'Refs #XX' footer."
```

Then copy the message Cursor generates, review it, and run `git commit -m "..."`.

**Rules:**
- Stage with `git add -p` (interactive) — never blind `git add .`
- Read the generated message before using it — edit if needed
- One logical change per commit

---

### Step 6: Push and PR Preparation

```bash
git push -u origin feature/XX-short-description
```

**Required inputs:**
- `.github/templates/pull_request_template.md` (PR format)
- `.github/templates/project_labels.md` (approved labels only)

**Generate PR description with a Cursor command:**

Create `.cursor/commands/pr-prep.md`:

```markdown
Generate a pull request description for the current branch.

1. Read `.github/templates/pull_request_template.md` for the required PR format
2. Read `.github/templates/project_labels.md` for approved labels
3. Look at the diff between this branch and main with `git diff main...HEAD`
4. Read the GitHub Issue linked in the commit footers (Refs #XX)
5. Write a PR description following the exact structure from the template
6. Add "Closes #XX" linking to the Issue
7. Suggest a PR title following: type(scope): description with business impact
8. Suggest labels from project_labels.md only — explain each choice in one sentence
9. Output as a Markdown block I can copy into GitHub
```

**Invoke:** Type `/pr-prep` in the agent input. Copy the output into GitHub PR.

---

### Step 7: Post-Merge Cleanup

```bash
git checkout main
git pull origin main
git branch -d feature/XX-short-description   # Delete local branch
```

---

## Cursor Commands (`.cursor/commands/`)

Store these as Markdown files, version-controlled in every repo:

| Command | File | What It Does |
|---------|------|-------------|
| `/draft-issue <goal>` | `draft-issue.md` | Drafts GitHub Issue from template + suggests labels |
| `/task-brief <issue#>` | `task-brief.md` | Generates filled Task Brief from Issue + template |
| `/pr-prep` | `pr-prep.md` | Generates PR description from template + branch diff |
| `/review` | `review.md` | Runs linters + summarizes issues |
| `/test` | `test.md` | Runs `make test` and reports failures with suggested fixes |
| `/eval` | `eval.md` | Runs `deepeval test run tests/test_eval.py` and reports scores |
| `/commit-msg` | `commit-msg.md` | Generates conventional commit message from staged diff |

### How commands with arguments work

Some commands need input from you — type it after the command name:

```
/draft-issue Add PII scanning for AI response guardrails
/task-brief 12
```

The agent receives the full command instructions from the `.md` file **plus** whatever
you typed after the command name. The command file says "use the Issue number provided
after this command" and the agent picks up `12` from your input.

Commands that don't need arguments (like `/review`, `/test`, `/commit-msg`, `/pr-prep`)
work from the current branch context automatically — just type the command name.

### Example: `/review` command

Create `.cursor/commands/review.md`:

```markdown
Review the current working state for production readiness.

1. Run `ruff check src/ tests/` and report any issues
2. Run `mypy src/` and report type errors
3. Check that every .py file starts with `from __future__ import annotations`
4. Check that logger calls use %s/%d formatting (not f-strings)
5. Run `pytest tests/ -v` and report failures
6. Summarize: what passes, what needs fixing, and suggested next steps
```

### Example: `/commit-msg` command

Create `.cursor/commands/commit-msg.md`:

```markdown
Generate a commit message for the currently staged changes.

1. Run `git diff --staged` to see exactly what's staged
2. Write a commit message following conventional commits:
   - type(scope): subject (imperative mood, max 72 chars)
   - Blank line
   - Body explaining what changed and why (wrap at 72 chars)
   - Footer: Refs #XX or Closes #XX if applicable
3. Output the complete message in a code block I can copy
4. Do NOT run git commit — I will commit manually
```

---

## Cursor Hooks (`.cursor/hooks/`)

Hooks auto-run scripts at key points in the agent loop. Use sparingly:

### Auto-format after agent edits

Create `.cursor/hooks.json`:

```json
{
  "version": 1,
  "hooks": {
    "file_edited": [
      {
        "command": "bash .cursor/hooks/format.sh"
      }
    ]
  }
}
```

Create `.cursor/hooks/format.sh`:

```bash
#!/bin/bash
# Auto-format after every agent file edit
black "$1" 2>/dev/null
ruff check --fix "$1" 2>/dev/null
```

```bash
chmod +x .cursor/hooks/format.sh
```

**Why:** Prevents the agent from generating code that fails `make lint`.
Your diff is always pre-formatted when you review it.

---

## Complete `.cursor/` Directory Structure

```
.cursor/
├── rules/                              # Production standards (version-controlled)
│   ├── git-workflow.mdc                # alwaysApply: true
│   ├── learning-mode.mdc              # alwaysApply: true
│   ├── python-production-standards.mdc # alwaysApply: true
│   ├── streamlit-patterns.mdc         # Auto-attached: app/**/*.py
│   ├── ai-sdk-patterns.mdc            # Auto-attached: src/ai/**/*.py
│   └── evaluation.mdc                 # Auto-attached: tests/test_eval.py
├── commands/                           # Repeatable agent workflows
│   ├── draft-issue.md                 # /draft-issue → draft Issue from template
│   ├── task-brief.md                  # /task-brief → generate Task Brief from Issue
│   ├── pr-prep.md                     # /pr-prep → generate PR from template
│   ├── review.md                      # /review → lint + type check + test
│   ├── test.md                        # /test → run tests, report failures
│   ├── eval.md                        # /eval → run DeepEval, report scores
│   └── commit-msg.md                  # /commit-msg → generate commit message
├── hooks/                              # Auto-run scripts
│   └── format.sh                      # Auto-format after agent edits
├── hooks.json                          # Hook configuration
└── plans/                              # Saved task briefs and implementation plans
    └── issue-XX-task-brief.md         # Filled-out task brief per Issue
```

---

## Control Gates Summary

| Gate | What | Who | When |
|------|------|-----|------|
| **Gate 0** | Issue approval | YOU | Before any planning starts |
| **Gate 1** | Task Brief approval | YOU | Review filled-out brief before implementation |
| **Gate 2** | Diff review | YOU | After every Agent stop point (`git diff`) |
| **Gate 3** | Staging review | YOU | `git add -p` (interactive, hunk by hunk) |
| **Gate 4** | Commit message | YOU | Review generated message before committing |
| **Gate 5** | PR review | YOU | Review generated PR description before creating |
| **Gate 6** | Push | YOU | Manual `git push` after all gates pass |

**The agent NEVER crosses a gate without your explicit approval.**

---

## Quick Reference: Daily Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  CURSOR PRODUCTION WORKFLOW — DAILY CYCLE                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  0. ISSUE    /draft-issue <goal> → uses issue_template.md    │
│              + project_labels.md → paste into GitHub Issue    │
│                                                              │
│  1. BRIEF    /task-brief <issue#> → uses cursor_task_brief   │
│              Fill from Issue → save to .cursor/plans/        │
│              Review brief → approve before coding             │
│                                                              │
│  2. BRANCH   git checkout -b feature/XX-description          │
│                                                              │
│  3. BUILD    Agent Mode → execute task brief → NO commits    │
│              Stop at each step → git diff → review            │
│              Run: make test && make lint                       │
│                                                              │
│  4. REVIEW   Chat Mode + @Branch → check vs task brief       │
│              /review → automated checks                       │
│                                                              │
│  5. COMMIT   git add -p → /commit-msg → review → commit      │
│              YOU commit. YOU own the history.                  │
│                                                              │
│  6. PR       git push → /pr-prep → uses pull_request_template│
│              + project_labels.md → paste into GitHub PR       │
│                                                              │
│  7. CLEAN    Merge → git branch -d → next issue               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Migration Notes: Codex → Cursor

| What Changes | What Stays the Same |
|-------------|-------------------|
| No more switching between Browser and VS Code Codex | Control gates (you always approve) |
| Plans saved as `.md` files in repo (versioned) | Manual commits and pushes |
| Commands replace repeated prompts | Issue → Plan → Code → Review → PR cycle |
| Hooks auto-format code | Templates still used for Issues/PRs |
| Single IDE for everything | "No vibe coding" — every line understood |

### What to keep from your Codex workflow
- **Templates** (`issue_template.md`, `pull_request_template.md`, `project_labels.md`, `cursor_task_brief.md`)
  — still the single source of truth for all Issues, PRs, task briefs, and labels. Now referenced
  directly by Cursor commands (`/draft-issue`, `/task-brief`, `/pr-prep`).
- **Task Brief concept** — preserved as `cursor_task_brief.md` template, filled out via `/task-brief`
  command or Plan Mode, saved to `.cursor/plans/`. Same gated workflow: brief → approve → execute.
- **Gate #1 and #2** — preserved as Gates 0-6 (more granular)
- **Claude (this project)** — still your strategic advisor for roadmap-aligned decisions

### What's new in Cursor
- **Plan Mode** fills out `cursor_task_brief.md` (replaces Browser Codex task brief generation)
- **`/task-brief` command** automates task brief generation from Issue + template
- **Commands** (`/draft-issue`, `/pr-prep`, `/review`, `/commit-msg`) automate repetitive prompts
- **Hooks** auto-format code after every agent edit
- **`@Branch`** context lets the agent review your current work naturally
- **`.cursor/plans/`** stores filled-out task briefs as documented history of implementation decisions

---

**Document Status:** v1.0
**Date:** April 06, 2026
**Replaces:** `codex_flow.md` (Codex dual-tool workflow)
**Aligned with:** Roadmap v8.2, git-workflow.mdc, python-production-standards.mdc
