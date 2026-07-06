Generate a pull request description for the current branch.

1. Read `.github/pull_request_template.md` for the required PR format
2. Read `.github/docs/project_labels.md` for approved labels
3. Run `git diff main...HEAD --stat` to get a summary of all changes
4. Run `git log main..HEAD --oneline` to see all commits on this branch
5. Read any commit footers referencing Issue numbers (Refs #XX, Closes #XX)
6. Write a PR description following the exact structure from the template, including:

   - Summary (what and why)
   - Changes (organized by module/area with file paths)
   - Verification Steps (exact commands + expected outcomes)
   - Risk / Impact
   - Closes #XX

7. Suggest a PR title following conventional commits: `type(scope): description showing business impact`
8. Suggest labels from `.github/docs/project_labels.md` only — explain each choice in one sentence
9. Generate 1 paragraph for PR merge extended description in GitHub
10. Output everything as a Markdown block I can copy into GitHub
11. Do NOT create the PR — I will create it manually