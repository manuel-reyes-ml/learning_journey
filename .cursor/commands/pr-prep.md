Generate a pull request description for the current branch.

1. Read `.github/pull_request_template.md` for the required PR format
2. Read `.github/docs/project_labels.md` for approved labels
3. Run `git diff main...HEAD --stat` to get a summary of all changes
4. Run `git log main..HEAD --oneline` to see all commits on this branch
5. Run `git diff main...HEAD --name-only -- docs/adr architecture.dsl docs/diagrams README.md`
   to see whether architecture artifacts changed on this branch
6. Read any commit footers referencing Issue numbers (Refs #XX, Closes #XX)
7. Write a PR description following the template's **actual section order**:

   - **Packs active** — tick only the packs this change touches; expand and fill only
     those, delete the rest. They must match the linked Issue and the task brief
   - **Objective** — the problem this PR solves + the concrete deliverable
   - **Scope** — in scope / out of scope
   - **What changed** — files changed/added by area, then the high-level approach
   - **Architecture & decisions** — ADR added where a real alternative was rejected (or
     state why none was needed) · `architecture.dsl` updated if boundaries changed ·
     diagrams regenerated via `make diagrams`, not hand-edited · README ① Production
     ② Cost ③ Architecture still accurate after this change
   - **Acceptance Criteria** — observable outcomes mirrored from the Issue
   - **Validation** — the uv-native commands from the template, with pasted results
   - **Reproducibility & environment** — `uv.lock` in sync, seeds, config pinned
   - **Security & data hygiene** — the template's checklist
   - **Risks / Edge Cases** — risk, edge cases covered, mitigation/rollback
   - **Reviewer Notes** — the 2-3 things most likely to be wrong
   - **Linking** — `Closes #XX`

8. Suggest a PR title in conventional-commits form: `type(scope): description`, imperative,
   lowercase, max 72 characters, stating the outcome
9. Suggest labels from `.github/docs/project_labels.md` only — explain each choice in one sentence
10. Generate 1 paragraph for the PR merge extended description in GitHub
11. Do not invent validation results — leave `<TODO: paste output>` where a command has not run
12. Keep production figures out of the description: the deposition test applies to PR text too
13. If the ticked packs do not match the Issue or the task brief, flag the mismatch rather
    than guessing which is right
14. Output everything as a Markdown block I can copy into GitHub
15. Do NOT create the PR — I will create it manually