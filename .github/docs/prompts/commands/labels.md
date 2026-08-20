Set up the standard label taxonomy on GitHub and refresh the agent-facing reference.

> ⚠️ This skill **writes to GitHub** — it creates/updates labels via the idempotent
> script. It is additive (the script's optional prune section stays OFF unless you
> enabled it). Pass `owner/repo` as an argument to target a specific repo, or leave
> blank for the current one.
>
> 🔒 Note this is the **one skill in the set with an external side effect**, which is
> why it is `disable-model-invocation: true` and deliberately **not** `context: fork` —
> a side-effecting action belongs in the main conversation where I can see it, not in
> a background subagent.

Target repo: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null`

Run the setup script (creates/updates labels, then regenerates the reference doc):
!`bash .github/scripts/setup-labels.sh $ARGUMENTS`

Confirm the regenerated reference (first 25 lines):
!`head -25 .github/docs/project_labels.md`

Then report:
- How many labels now exist and whether any were newly created vs updated
- Confirmation that `.github/docs/project_labels.md` was regenerated
- Any errors or warnings from the run

Remind me to commit the regenerated reference so issue/PR agents can read it:

    git add .github/docs/project_labels.md
    git commit -m "docs: refresh label reference"

Do **NOT** run `git commit` — I commit manually after reviewing the diff.
