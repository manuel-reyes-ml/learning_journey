Set up the standard label taxonomy on GitHub and refresh the agent-facing reference.

All context you need has already been injected above this text by
`.github/scripts/labels_run.sh`.

**Do not attempt to load any of it yourself.** This body contains no `!` blocks and no
`@` references by design: command-template substitution is single-pass, so either would
arrive as literal text and silently never run (ADR-0001).

**Check the context first.** If a block above is missing, empty, or shows a line
beginning `CONTEXT_ERROR`, **STOP and report which one**. Do not infer, reconstruct, or
reason from the rules files in place of the missing output.

> ⚠️ **This is the ONE command in the set with an external side effect.** The script
> above has already created/updated labels on GitHub and regenerated the reference doc.
> It is additive — the script's optional prune section stays OFF unless enabled. Per
> ADR-0003 the agent permission map does not gate this; review is the gate, which is
> why the script is named `labels_run.sh` rather than `_context.sh`.

Report, from the blocks above only:
- How many labels now exist, and which were newly created vs updated
- Confirmation that `.github/docs/project_labels.md` was regenerated
- Any errors or warnings from the run

If the reference block reports `CONTEXT_ERROR`, say so plainly and note that
`/draft-issue` and `/pr-prep` both depend on that file and will refuse to suggest
labels until it exists.

Remind me to commit the regenerated reference so issue/PR agents can read it:

    git add .github/docs/project_labels.md
    git commit -m "docs: refresh label reference"

Do **NOT** run `git commit` — I commit manually after reviewing the diff.