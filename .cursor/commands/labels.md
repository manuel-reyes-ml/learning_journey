Set up the standard GitHub labels for a repository and regenerate the label reference.

Usage: `/labels` (current repo) or `/labels owner/repo` (specific repo)

⚠️ This command WRITES to GitHub — it creates/updates labels via the idempotent script.
It is additive (the script's optional prune section stays OFF unless you enabled it).

1. Confirm the target repo: run `gh repo view --json nameWithOwner -q .nameWithOwner`
   (or use the `owner/repo` I provided after the command)
2. Run the setup script (creates/updates labels AND regenerates the reference doc):
   `bash .github/scripts/setup-labels.sh <owner/repo>`
3. Show the regenerated reference: run `head -25 .github/docs/project_labels.md`
4. Report:
   - How many labels now exist, and whether any were newly created vs updated
   - Confirmation that `.github/docs/project_labels.md` was regenerated
   - Any errors or warnings from the run
5. Remind me to commit the regenerated reference so issue/PR commands can read it:
   `git add .github/docs/project_labels.md && git commit -m "docs: refresh label reference"`
6. Do NOT run `git commit` — I commit manually after reviewing the diff
