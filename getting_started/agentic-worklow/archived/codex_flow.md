# Codex in VS Code vs Codex in the Browser: Recommended Workflow

Use **Browser Codex** where it provides leverage beyond “editing code in the IDE”: **Issue drafting, planning, review, and PR polish**. Use **VS Code Codex** for **implementation** and fast iteration.

This workflow is designed to prevent “surprise commits,” keep your work reviewer-grade, and ensure every artifact (Issues, labels, PRs) stays consistent with your repo’s templates.

---

## Guiding principles

### Source-of-truth hierarchy
1. **GitHub Issue** = contract (scope + acceptance criteria + validation)
2. **VS Code Codex Task Brief** = executable instructions derived from the Issue
3. **Code changes** = must satisfy acceptance criteria and validation plan

### Templates are mandatory inputs
When generating or rewriting artifacts, instruct Browser Codex to read and follow:
- `templates/issue_template.md` (Issue format and required sections)
- `templates/project_labels.md` (approved labels + definitions/usage)
- `templates/pull_request_template.md` (PR body format + required sections)
- `templates/vscode_codex_task_brief.md` (VS Code Codex execution constraints)

### Control gates (non-negotiable)
- **Gate #1 (Implementation):** VS Code Codex may edit files, but **must not commit or push**. You review the diff first and commit manually.
- **Gate #2 (Review):** Browser Codex reviews the diff in “reviewer mode” (correctness, edge cases, naming, docs, tests). No scope creep.

---

## Step-by-step workflow (with where each Codex fits)

### 0) Draft or refine the Issue (Browser Codex)

**Goal:** produce a GitHub Issue that is explicit and testable, formatted exactly like your repo.

**Required inputs (tell Browser Codex to use these)**
- `templates/issue_template.md`
- `templates/project_labels.md`

**What to generate**
- Context / problem statement
- Scope and non-scope
- Acceptance criteria (checkboxes)
- Implementation notes (likely files/functions)
- Edge cases
- Validation / smoke test plan (commands + expected outcomes)
- Suggested labels (from `project_labels.md` only)
- Risks / impact

**Example prompt (Browser Codex)**
> Using `.github/templates/issue_template.md`, draft (or rewrite) a GitHub Issue for: **[one-sentence goal]**, if after your review in repo's module you find is a valid issue to be solved.  
> To determine the correct implementation plan review all modules in main branch to make sure changes are made globally (considering all affected modules) and to avoid unwanted changes are applied.
> Use `.github/templates/project_labels.md` to recommend the correct labels (only from that file).  
> Include explicit acceptance criteria (checkboxes) and a validation/smoke test plan with commands and expected outcomes.  
> Output the final Issue body in Markdown file ready to copy and paste into GitHub and include issue title to be production grade and recruiter friendly.

**Outcome**
- You paste the final markdown into GitHub Issue and apply suggested labels.

---

### 1) Generate the VS Code Codex Task Brief (Browser Codex → VS Code Codex)

**Goal:** convert the Issue + plan into a single, precise “agent brief” that VS Code Codex can execute.

**Required input**
- `templates/vscode_codex_task_brief.md`

**How to use it**
1. In Browser Codex, ask it to fill out `templates/vscode_codex_task_brief.md` for Issue #X.
2. Copy/paste the completed Task Brief into VS Code Codex.

**Example prompt (Browser Codex)**
> Using `.github/templates/vscode_codex_task_brief.md`, generate a complete Task Brief for Issue #X.  
> Enforce: no commits, no pushes, minimal incremental changes, and include validation commands with expected outputs.  
> Ensure the acceptance criteria aligns with the Issue.
> Output the final task_brief body in a Markdown file ready to copy and paste into Codex VS code.

**Outcome**
- A copy/paste-ready Task Brief for VS Code Codex.

---

### 2) Implementation (VS Code Codex)

**Goal:** do ~90% of the code changes here.

**Rules**
- Create/edit modules, refactor, add docstrings, update tests.
- **Do not commit. Do not push.**
- Prefer small, reviewable increments and run smoke tests at defined stop points.

**Your local flow (recommended)**
- After each Codex action:
  - `git status -sb`
  - `git diff`
- Run smoke tests per the Task Brief.

**Outcome**
- You have working changes with a clean diff you’ve reviewed.

---

### 3) Review the diff (Browser Codex)

**Goal:** use Browser Codex as a reviewer to catch edge cases and improve quality without expanding scope.

**What to do**
- Push your branch (after your local review).
- Open the GitHub diff (PR optional).
- Ask Browser Codex for a focused review on:
  - Correctness and edge cases
  - Consistency with conventions (schema, naming, tolerances)
  - Test coverage and failure modes
  - Documentation clarity

**Example prompt (Browser Codex)**
> I implemented Issue #X on branch `<branch>`. Review the diff for correctness, edge cases, and consistency with repo conventions.  
> Do not propose scope expansion; only recommend fixes, naming/structure improvements, and missing validations/tests.
> Do not make edit codes, I want your review and recommendation only if any bug is found.

**Outcome**
- You apply improvements in VS Code, then push again.

---

### 4) PR creation and PR writing (Browser Codex)

**Goal:** produce a professional PR description in your repo’s exact format.

**Required input**
- `templates/pull_request_template.md`

**What to include**
- Summary
- What changed
- Why
- Verification steps (commands)
- Risk/impactNQ
- Next steps
- “Closes #X”
- Any checklist items from the Issue that are now completed

**Example prompt (Browser Codex)**
> Using `.github/templates/pull_request_template.md`, generate a PR description for Issue #X.  
> Base it on the branch diff and this summary: [paste summary].  
> Include verification steps (commands) and add “Closes #X”.  
> Keep language concise and consistent with the template headings.
> Output the final PR body in Markdown file ready to copy and paste into GitHub and include PR title to be production grade and recruiter friendly. Also include suggested labels to be used in the new PR, based on `.github/templates/project_labels.md`.
> Generate 1 paragraph for PR merge extended description in GitHub.

**Outcome**
- Copy/paste into GitHub PR.

---

### 5) Labeling and project hygiene (Browser Codex)

**Goal:** keep labeling consistent and scalable across Issues/PRs.

**Required input**
- `templates/project_labels.md`

**Use cases**
- Suggesting labels during Issue creation
- Auditing if labels match scope (bug vs refactor vs feature)
- Ensuring PR labels align with Issue labels

**Example prompt (Browser Codex)**
> Using `templates/project_labels.md`, recommend the correct labels for Issue #X and the corresponding PR.  
> Explain each label choice in one sentence.

---

## Practical rule of thumb: When should I open Browser Codex?

For each Issue, open Browser Codex **at least twice**:
1. **Before:** Draft/refine Issue using `issue_template.md` + suggest labels from `project_labels.md` + lock plan/checklist + generate VS Code Task Brief
2. **After:** Review diff + write PR description using `pull_request_template.md`

Everything else: **VS Code Codex**.

---

## Concrete example (Issue 3: Roth engine)

- **Browser Codex:**  
  - Draft/refine Issue using `templates/issue_template.md`  
  - Suggest labels using `templates/project_labels.md`  
  - Confirm output schema + validation checklist  
  - Generate VS Code Task Brief using `templates/vscode_codex_task_brief.md`
- **VS Code Codex:** implement `roth_taxable_analysis.py` + run local smoke tests  
- **Browser Codex:** review diff + generate PR description using `templates/pull_request_template.md`
