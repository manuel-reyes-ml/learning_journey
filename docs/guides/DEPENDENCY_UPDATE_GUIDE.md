# Dependency Updates — Keeping a uv Workspace Current

The routine for checking, choosing, applying and verifying dependency updates in
every uv repo in the portfolio. Written against the `learning_journey` workspace
(four projects, one `uv.lock`); every command here was run against it.

Companions:
- [`UV_GUIDE.md`](UV_GUIDE.md) — setup, workspaces, CI. Read §1 (mental model)
  and §6 (workspaces) first; this guide assumes both.
- [`PRE_COMMIT_GUIDE.md`](PRE_COMMIT_GUIDE.md) — the `uv-lock` hook and the
  Conventional Commits rules used in [§8](#8-commit).

---

## Contents

1. [The mental model](#1-the-mental-model)
2. [Cadence — when to run this](#2-cadence--when-to-run-this)
3. [Pre-flight](#3-pre-flight)
4. [Step 1 — Audit: what is out of date?](#4-step-1--audit-what-is-out-of-date)
5. [Step 2 — Preview: what would change?](#5-step-2--preview-what-would-change)
6. [Step 3 — Triage: pick the version and the range](#6-step-3--triage-pick-the-version-and-the-range)
7. [Step 4 — Apply](#7-step-4--apply)
8. [Step 5 — Verify and commit](#8-commit)
9. [Adding a new dependency to a member](#9-adding-a-new-dependency-to-a-member)
10. [Worked examples](#10-worked-examples)
11. [Troubleshooting](#11-troubleshooting)
12. [Quick reference](#12-quick-reference)
13. [Update log](#13-update-log)

---

## 1. The mental model

Two files, two facts:

| File | Holds | Changed by |
|---|---|---|
| `pyproject.toml` | the **range** you allow — `anthropic>=1.17,<2` | you, or `uv add` with an explicit specifier |
| `uv.lock` | the **exact version** installed — `anthropic 1.17.0` | `uv lock`, `uv lock --upgrade[-package]`, `uv add` |

So there are two kinds of update, and they are different jobs:

- **Within range** (1.5.0 → 1.17.0 under `<2`): only `uv.lock` changes.
  Low risk, routine.
- **Out of range** (openai 2.x → 3.x under `<3.0`): `pyproject.toml` must change.
  The ceiling stopped it on purpose. Needs a changelog read and a decision.

Workspace facts that shape every command below:

- **One lockfile, one `.venv`** for all members. A package has exactly one
  version across the whole workspace, so the tightest range in any member wins.
- **`--package` takes the `[project] name`, not the folder name.**

| Folder | `--package` name |
|---|---|
| `/` (root) | `learning-journey` |
| `foundations/` | `lj-foundations` |
| `llm-api-smoke-test/` | `llm-api-smoke-test` |
| `courses/cs50_harvard/code/05_data_structures/speller/py_src/` | `cs50-speller` |

---

## 2. Cadence — when to run this

| Trigger | What to run |
|---|---|
| **Every fortnight** (start of each activation-plan block) | The full routine, §3–§8 (packages) |
| **Monthly**, i.e. every second fortnight | Add §7f (hook pins) to that fortnight's branch |
| After `uv self update`, or whenever `ruff` moves in `uv.lock` | §7f |
| `uv audit` or a security advisory names a package you use | §5–§8 for that one package, same day |
| You need a feature from a newer release | §5–§8 for that one package |
| Before tagging a release or a portfolio demo | §4 audit only, to know what you're shipping |

**Cool-down rule:** don't take a release on the day it ships. Resolve against
what existed a week ago (`--exclude-newer "7 days"`, §5). Brand-new releases are
where yanked versions and supply-chain incidents happen; a week of other people
installing it is free QA.

---

## 3. Pre-flight

```bash
git status                          # must be clean — one variable per commit
git switch -c chore/<issue#>-update-dependencies   # git-workflow branch naming
uv self update                      # uv itself (installer-managed uv only)
uv --version
uv lock --check                     # lockfile already matches pyproject.toml?
make sync                           # == uv sync --all-packages --all-groups
make test                           # baseline: tests pass BEFORE you change anything
```

If `make test` fails before you've updated anything, stop and fix that first.
Otherwise you can't tell whether an update broke something.

**Keep three uv versions compatible:** your local `uv`, the `uv-pre-commit`
`rev:` in `.pre-commit-config.yaml` (its tag is a uv version), and CI's
`astral-sh/setup-uv` (which installs the latest uv unless told otherwise). If
the `uv-lock` hook rewrites `uv.lock` every time you commit, these have drifted
apart. Fix it with `make hooks-update` plus `uv self update`.

To make a too-old uv fail loudly instead of silently writing a different lock,
set a floor in the root `pyproject.toml`:

```toml
[tool.uv]
required-version = ">=0.11"
```

---

## 4. Step 1 — Audit: what is out of date?

Per project, direct dependencies only (the ones you chose):

```bash
uv tree --package learning-journey   --outdated --depth 1
uv tree --package lj-foundations     --outdated --depth 1
uv tree --package llm-api-smoke-test --outdated --depth 1
uv tree --package cs50-speller       --outdated --depth 1
```

Output reads `anthropic v1.5.0 (latest: v1.17.0)`, meaning locked version vs.
newest on PyPI. `(group: dev)` / `(extra: test)` tells you which section it
lives in.

Everything installed, including transitive packages, as a flat table:

```bash
uv pip list --outdated
```

Who pulls a transitive package in (when one you never chose shows up):

```bash
uv tree --invert --package filelock
```

For a single package's release history and Python support, use PyPI:

```bash
curl -s https://pypi.org/pypi/anthropic/json | python3 -c "
import json, sys; d = json.load(sys.stdin); i = d['info']
print('latest:', i['version'], '| requires-python:', i['requires_python'])
for r in i['requires_dist'] or []:
    if 'extra' not in r: print('  needs', r)"
```

Look at `requires-python` (must include 3.14) and `needs` (new transitive
dependencies arrive here).

### Security audit

```bash
uv audit                 # every locked package vs. the OSV vulnerability database
uv audit --no-dev        # runtime dependencies only
```

`uv audit` is **experimental** in uv 0.11 (it prints a warning; silence it with
`--preview-features audit-command`). It needs network access to `api.osv.dev`.
A finding here jumps the queue: update that package today with §5–§8 rather
than waiting for the fortnight.

---

## 5. Step 2 — Preview: what would change?

`--dry-run` resolves without writing anything. Run it before every apply.

```bash
# Everything, within current ranges
uv lock --upgrade --dry-run

# Everything, with the 7-day cool-down
uv lock --upgrade --exclude-newer "7 days" --dry-run

# One package
uv lock --upgrade-package anthropic --dry-run

# One package, to a specific version (must be inside the range)
uv lock --upgrade-package "anthropic==1.12.0" --dry-run
```

Read the output line by line:

- `Update X vA -> vB`: a version bump. Check whether the **major** number changed.
- `Add X`: a **new transitive dependency**. Example: anthropic 1.17 adds
  `opentelemetry-api`. Fine, but you should know about it.
- `Remove X`: something no longer needed.

**A transitive major bump is easy to miss.** The 2026-10-21 dry run showed
`filelock v3.32.6 -> v4.2.4`. You never chose filelock, so no ceiling of yours
protects you. If a transitive major bump breaks tests, see
[§11](#a-transitive-package-jumped-a-major-version).

---

## 6. Step 3 — Triage: pick the version and the range

For each package in the dry-run output, decide which case it is:

| Case | Example | Action |
|---|---|---|
| Patch/minor, inside range | numpy 2.5.3 → 2.5.4 | Take it with the bulk `uv lock --upgrade` |
| Minor inside range, but a lot changed | anthropic 1.5 → 1.17 (12 minors in 2 months) | Skim the changelog, then take it |
| Major, blocked by your ceiling | openai `<3.0`, 3.35 out | Read the migration guide → decide → §7c |
| Major, transitive | filelock 3 → 4 | Take it; constrain only if tests break |

### Changelog checklist (anything beyond a patch)

1. **Breaking changes / removals:** search the changelog for "breaking",
   "removed", "deprecated", "requires".
2. **Python support:** `requires-python` includes 3.14 and wheels exist for
   `cp314` (or the package is pure Python, `py3-none-any`).
3. **New dependencies:** the `needs` list from §4, or `Add` lines from §5.
4. **Release age:** older than 7 days (the cool-down rule).
5. **Your code:** grep for the APIs the changelog mentions:
   `grep -rn "temperature\|top_p" llm-api-smoke-test/src`.

### Choosing the range

- **Floor (`>=`)**: the lowest version you have actually **tested**. For your
  apps that's usually the version you're upgrading to. Don't leave the floor at
  a version you've never run.
- **Ceiling (`<`)**: the next major version, `<X+1`. Required for anything
  pre-1.0 or fast-moving (UV_GUIDE §1, Production rule 5).
- **Never `==` in `pyproject.toml`.** The exact pin belongs in `uv.lock`.

`uv add --bounds` writes these for you when you don't give a specifier:

| `--bounds` | `uv add httpx` writes | Use for |
|---|---|---|
| `lower` (default) | `httpx>=0.28.1` | — (no ceiling; avoid) |
| `major` | `httpx>=0.28.1,<0.29.0` for 0.x · `>=1.17.0,<2.0.0` for 1.x+ | **Default choice** |
| `minor` | `>=1.17.0,<1.18.0` | Libraries known to break on minors |
| `exact` | `==1.17.0` | Don't — let the lock pin |

For 0.x packages, `major` shifts one place (Cargo-style): `0.28.1` → `<0.29.0`.

Optional: make `major` the default for every `uv add` in this repo:

```toml
# root pyproject.toml
[tool.uv]
add-bounds = "major"
```

---

## 7. Step 4 — Apply

### 7a. Bulk, within ranges (the fortnightly default)

```bash
uv lock --upgrade --exclude-newer "7 days"
make sync
```

Only `uv.lock` changes. If one package from the batch breaks tests, roll it back
on its own instead of abandoning the batch:

```bash
git checkout uv.lock                                # back to the old lock
uv lock --upgrade --exclude-newer "7 days" --dry-run
uv lock --upgrade-package pkg-a --upgrade-package pkg-b   # everything except the breaker
```

### 7b. One package, within range

```bash
uv lock --upgrade-package anthropic
make sync
```

### 7c. Raise the range (floor and/or ceiling)

Give the specifier explicitly:

```bash
uv add --package llm-api-smoke-test "anthropic>=1.17,<2"
```

**Gotcha, verified:** `uv add <pkg>` on a package that is **already declared**
keeps your existing range and only re-locks. Even
`uv add --package llm-api-smoke-test anthropic --bounds major --upgrade-package anthropic`
left `>=1.0,<2.0` unchanged. To change `pyproject.toml`, always write the
version range yourself.

The trailing comment on the line survives `uv add`, so update stale comments
by hand. Example: `# 0.x SDK; no upper bound yet` next to a 1.x pin.

### 7d. Same package in several members

`structlog` is declared in `llm-api-smoke-test` (`>=24.1`), `cs50-speller`
(`>=25.0`) and `lj-foundations` (`>=26.1,<27`). The lock picks **one** version
that satisfies all three. To keep the workspace consistent, give every member
the same range:

```bash
uv add --package llm-api-smoke-test "structlog>=26.1,<27"
uv add --package cs50-speller       "structlog>=26.1,<27"
```

### 7e. Remove a dependency

```bash
uv remove --package lj-foundations structlog
uv remove --package lj-foundations --group dev ruff
```

### 7f. Hooks — refresh pre-commit pins (same branch)

Package updates and hook updates belong in the **same branch**, because two
hooks run tools that also live in `uv.lock`:

| Hook in `.pre-commit-config.yaml` | Must match | Why |
|---|---|---|
| `ruff-pre-commit` | `ruff` in `uv.lock` (what `make lint` and VS Code run) | Two ruff versions can format the same file differently |
| `uv-pre-commit` | your local `uv --version` | Different uv versions can write different `uv.lock` files |

**Where the versions are:** each `rev:` is a commit SHA, and the comment shows
the release it points to:

```yaml
rev: 44b5042edab9382aba712eed4f9c7bab7a3d6a3e  # frozen: v0.17.0
```

`repo: local` hooks (the `claude-agents-check` / `claude-rules-check`
generators) have no `rev:`; they run your own scripts and are never updated.

**Run it after §7a–§7e and `uv self update`, so it can be compared against the
new lock:**

```bash
make hooks-update                          # == pre-commit autoupdate --freeze
git diff .pre-commit-config.yaml           # read every rev: change
uv tree --package learning-journey --depth 1 | grep ruff   # venv ruff version
grep -A1 "ruff-pre-commit" .pre-commit-config.yaml         # hook ruff version
uv --version                               # vs. the uv-pre-commit "# frozen:" tag
make hooks-run                             # every hook, every file, new versions
```

What it changes: **only `.pre-commit-config.yaml`**. Hooks install in their own
environments under `~/.cache/pre-commit`, not in `.venv`, so nothing in
`pyproject.toml` or `uv.lock` moves.

Example run on 2026-10-21:

```
pre-commit-hooks         already up to date!
ruff-pre-commit          v0.17.0 -> v0.17.1
uv-pre-commit            0.13.0  -> 0.13.4
gitleaks                 already up to date!
nbstripout               already up to date!
conventional-pre-commit  already up to date!
```

**If versions don't line up after the refresh:**

- Hook ruff is newer than the venv ruff → `uv lock --upgrade-package ruff`, so
  the venv catches up.
- Venv ruff is newer than the hook → the hook's new release isn't out yet; edit
  nothing and re-check at the next refresh.
- `uv-pre-commit` is newer than your local uv → `uv self update`.

**If `make hooks-run` rewrites files**, a newer ruff changed its formatting.
Keep that out of the pin commit (see §8): commit the pin bump first, then the
reformatted files on their own.

---

<a id="8-commit"></a>

## 8. Step 5 — Verify and commit

```bash
uv lock --check     # lock matches every pyproject.toml (what CI's --locked enforces)
make sync
make lint
make test           # one pytest run per member
make hooks-run      # every pre-commit hook, every file
git diff --stat     # expect: uv.lock · pyproject.toml (§7c–§7e) · .pre-commit-config.yaml (§7f)
```

Commit `pyproject.toml` and `uv.lock` **together, in the same commit**. One
without the other is exactly what the `uv-lock` hook and CI's
`uv sync --locked` reject.

Commit messages (Conventional Commits; `build` is the type for dependencies):

```bash
git commit -m "build(deps): refresh uv.lock within existing ranges"
git commit -m "build(deps): bump anthropic floor to 1.17 in llm-api-smoke-test"
git commit -m "build(deps): add structlog to lj-foundations"
```

One branch, **separate commits** in this order, so each commit has one reason to
exist and can be reverted alone:

```bash
git add uv.lock '*pyproject.toml'                 # 1. packages (§7a–§7e); quoted glob = every member
git commit -m "build(deps): refresh uv.lock within existing ranges"

git add .pre-commit-config.yaml                   # 2. hook pins (§7f)
git commit -m "build(hooks): refresh pinned hook revisions"

git add -u                                        # 3. only if hooks-run reformatted files
git commit -m "style(format): apply ruff 0.17.1"
```

Then add one row to the [update log](#13-update-log), push the branch, and let
CI confirm on a clean runner.

---

## 9. Adding a new dependency to a member

```bash
# runtime dependency → [project.dependencies]
uv add --package lj-foundations "structlog>=26.1,<27"

# test/dev tooling → [dependency-groups]
uv add --package lj-foundations --group test "pytest-mock>=3.14,<4"
uv add --package lj-foundations --group dev  "pyright>=1.1,<2"

# root project (notebooks, scripts/) → omit --package
uv add "polars>=1.30,<2"
```

Equivalent: `cd foundations && uv add ...`, since uv picks the member from the
current directory. Prefer `--package` in scripts, the Makefile and agent
instructions, because it doesn't depend on where the shell happens to be.

Never `uv pip install` a dependency. It bypasses `pyproject.toml` and
`uv.lock`, so it works on your machine and fails in CI.

If a package is already in the shared `.venv` because another member uses it,
**still declare it** in every member that imports it (UV_GUIDE Production
rule 9). `uv sync --package lj-foundations` installs only that member's
declared dependencies.

---

## 10. Worked examples

### anthropic in `llm-api-smoke-test` (within range, raise floor)

```bash
uv tree --package llm-api-smoke-test --outdated --depth 1
#   anthropic v1.5.0 (latest: v1.17.0)
uv lock --upgrade-package anthropic --dry-run
#   Update anthropic v1.5.0 -> v1.17.0
#   Add opentelemetry-api v1.45.1          ← new transitive dep
# Changelog 1.7–1.12: Pydantic>=1.10 required (have 2.13), parse/tool-runner
# stop sending the beta header, world-writable config files refused.
uv add --package llm-api-smoke-test "anthropic>=1.17,<2"
make test
git commit -am "build(deps): bump anthropic floor to 1.17 in llm-api-smoke-test"
```

### structlog in `foundations` (new declaration, nothing to download)

```bash
uv add --package lj-foundations "structlog>=26.1,<27"
#   foundations/pyproject.toml: dependencies = ["structlog>=26.1,<27"]
#   uv.lock: +4 lines (lj-foundations now requires structlog; 26.1.0 already locked)
uv tree --package lj-foundations
git commit -am "build(deps): add structlog to lj-foundations"
```

### Snapshot — ceilings currently holding something back (2026-10-21)

| Package | Declared | Locked | Latest | Where | Next step |
|---|---|---|---|---|---|
| openai | `>=1.40,<3.0` | 2.54.0 | 3.35.1 | llm-api-smoke-test | Read the 3.0 migration notes, then §7c |
| pytest-cov | `>=5.0,<7.0` | 6.3.0 | 7.1.0 | foundations, llm-api-smoke-test | Check the 7.0 changelog; raise both members together |
| ruff | `>=0.5,<1.0` (members) | 0.16.7 | 0.17.1 | all | In range; the bulk refresh takes it (see note) |

Note on ruff: `.pre-commit-config.yaml` runs ruff **v0.17.0**, while the venv
(`make lint`, VS Code) runs **0.16.7**. Two ruff versions can disagree on
formatting. A bulk refresh (§7a) takes the venv to 0.17.1 and `make hooks-update`
(§7f) takes the hook to v0.17.1, so running both in the same branch closes the gap.

This table goes stale. Regenerate it with §4 rather than trusting it.

---

## 11. Troubleshooting

### `uv add` didn't change my version range

The package was already declared, so uv kept your specifier. Pass it explicitly:
`uv add --package <member> "pkg>=X,<Y"` (§7c).

### `No solution found ... requirements are unsatisfiable`

Two members (or the root and a member) declare ranges with no overlap, e.g. one
`pytest<9` and one `pytest>=9`. Remember: one lockfile, one version per
package. Find every declaration and align them:

```bash
grep -rn '"pytest' --include=pyproject.toml .
```

### CI fails on `uv sync --locked`

`pyproject.toml` changed but `uv.lock` wasn't regenerated or committed. Run
`uv lock`, commit `uv.lock`, push. `uv lock --check` locally catches this first.

### The `uv-lock` hook keeps modifying `uv.lock`

The hook's uv version and your local uv disagree on the lock format. See §3
("Keep three uv versions compatible").

<a id="a-transitive-package-jumped-a-major-version"></a>

### A transitive package jumped a major version

You don't import it, so don't add it to `dependencies`. Constrain it at the
workspace root instead. A constraint limits the version without making the
package a requirement:

```toml
# root pyproject.toml
[tool.uv]
constraint-dependencies = ["filelock<4"]
```

Leave a comment saying why and when to remove it, and revisit it at the next
fortnightly update.

### A direct dependency jumped a major version and broke things

Its range had no ceiling. Add `<X+1` (UV_GUIDE §10, the anthropic 0.x → 1.x
incident).

### The new version needs a Python you don't run

Check `requires-python` on PyPI (§4). Every member declares `>=3.14`, and uv
won't pick a release that excludes 3.14. If uv keeps resolving to an old
version, this is often why.

---

## 12. Quick reference

| Goal | Command |
|---|---|
| Outdated direct deps, one member | `uv tree --package <name> --outdated --depth 1` |
| Outdated everything (flat) | `uv pip list --outdated` |
| Who depends on X | `uv tree --invert --package X` |
| Known vulnerabilities (experimental) | `uv audit` |
| Preview a full refresh | `uv lock --upgrade --dry-run` |
| Preview with 7-day cool-down | `uv lock --upgrade --exclude-newer "7 days" --dry-run` |
| Preview one package | `uv lock --upgrade-package X --dry-run` |
| Preview one package to a version | `uv lock --upgrade-package "X==1.2.3" --dry-run` |
| Refresh everything in range | `uv lock --upgrade --exclude-newer "7 days"` |
| Refresh one package in range | `uv lock --upgrade-package X` |
| Change the range | `uv add --package <name> "X>=A,<B"` |
| Add with an auto ceiling | `uv add --package <name> X --bounds major` |
| Add to a group | `uv add --package <name> --group test X` |
| Remove | `uv remove --package <name> X` |
| Lock matches pyproject? | `uv lock --check` |
| Install what the lock says | `make sync` |
| Full verification | `make lint && make test && make hooks-run` |
| Update uv itself | `uv self update` |
| Update hook pins (only edits `.pre-commit-config.yaml`) | `make hooks-update` |
| Review hook pin changes | `git diff .pre-commit-config.yaml` |
| Hook ruff vs. venv ruff | `grep -A1 ruff-pre-commit .pre-commit-config.yaml` · `uv tree --package learning-journey --depth 1 \| grep ruff` |
| Run every hook with new pins | `make hooks-run` |
| Commit hook pins | `git commit -m "build(hooks): refresh pinned hook revisions"` |

---

## 13. Update log

One row per update commit, newest first. This is the record of what changed,
when, and why.

| Date | Scope | Change | Why / notes | Commit |
|---|---|---|---|---|
| 2026-10-21 | lj-foundations | `+ structlog>=26.1,<27` | Declare an import that only worked through the shared venv | — |
| 2026-10-21 | llm-api-smoke-test | anthropic 1.5.0 → 1.17.0, floor `>=1.17,<2` | Adds `opentelemetry-api` as a transitive dependency | — |
