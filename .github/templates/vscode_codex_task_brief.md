# templates/vscode_codex_task_brief.md
# VS Code Codex Task Brief

> Purpose: This template is copied into VS Code Codex to execute work safely and predictably.
> Key control: **No commits and no pushes**. You (human) will review diffs and commit manually.

---

## Task metadata

- **Issue:** #<ISSUE_NUMBER> — <ISSUE_TITLE>
- **Branch:** <branch-name>
- **Owner:** <your name>
- **Date:** <YYYY-MM-DD>

---

## Objective (one paragraph)

Implement Issue #<ISSUE_NUMBER> by delivering: <describe the user-visible or pipeline-visible outcome>.
The implementation must align with existing repo conventions and satisfy the acceptance criteria below.

---

## Hard constraints (must follow)

1. **Do not commit. Do not push. Do not tag. Do not open PRs.**  
   - If you believe a commit is necessary, stop and explain why; wait for manual action.
2. Make **minimal, incremental changes**. Prefer small diffs over broad refactors.
3. **Do not change behavior outside scope.** If scope is unclear, stop and list assumptions/questions.
4. Preserve repo conventions: naming, schema fields, tolerance rules, logging style, and directory structure.
5. Keep changes testable: add/adjust tests or validations where appropriate.

---

## Repo conventions to follow

- Output schema fields required: <list required fields>
- Tolerances / thresholds: <reference config objects or constants>
- Naming patterns: <e.g., snake_case functions, suffix conventions>
- DataFrame standards: <e.g., required columns, canonical NA behavior>
- Error handling/logging: <e.g., raise vs warn, logger usage>

---

## Files expected to change (planned)

| File | Change type | Why |
|------|------------|-----|
| `<path/to/file.py>` | add/modify | <reason> |
| `<path/to/other.py>` | refactor | <reason> |
| `<tests/...>` | add/modify | <reason> |

If additional files need to change, stop and justify before proceeding.

---

## Execution plan (do in order)

### Step 1 — <short step name>
- **Edit:** `<file>`
- **Change:** <what you will do>
- **Stop point:** After this step, stop and summarize the diff.

### Step 2 — <short step name>
- **Edit:** `<file>`
- **Change:** <what you will do>
- **Stop point:** After this step, stop and summarize the diff.

### Step 3 — <short step name>
- **Edit:** `<file>`
- **Change:** <what you will do>
- **Stop point:** After this step, stop and summarize the diff.

(Continue as needed.)

---

## Acceptance criteria (must satisfy)

- [ ] <criterion 1, written as an observable outcome>
- [ ] <criterion 2>
- [ ] <criterion 3>
- [ ] No breaking changes to existing behavior outside scope.
- [ ] Output remains compatible with: `<downstream function/module>`.

---

## Edge cases to handle explicitly

- <edge case 1>
- <edge case 2>
- <edge case 3>

If an edge case cannot be addressed without scope expansion, stop and explain tradeoffs.

---

## Validation / smoke tests (run locally)

Provide commands I can run, and what “success” looks like.

### Quick checks (after each major step)
- `python -m compileall <relevant_dir>`  
  **Expected:** no syntax errors.
- `<lint/test command>`  
  **Expected:** no failures.

### Functional validation (end-to-end)
- `<command to run unit tests or a focused test file>`  
  **Expected:** tests pass.
- `<command to run a notebook/script if applicable>`  
  **Expected:** output matches expected schema and key scenarios.

---

## Deliverable summary (what to output to me at the end)

When you finish editing files (without committing), provide:

1. **What changed and why** (bullet list)
2. **Files changed** (list)
3. **Key logic decisions** (brief)
4. **Exactly what I should review in `git diff`** (callouts)
5. **Exact validation commands** (copy/paste-ready)

---

## Stop conditions (important)

Stop and ask for direction if:
- The Issue requirements conflict with repo conventions.
- You need to change additional files not listed above.
- You cannot meet acceptance criteria without scope expansion.
- You are unsure about business logic or thresholds.
