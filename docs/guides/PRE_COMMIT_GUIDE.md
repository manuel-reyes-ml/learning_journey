# pre-commit — Setting Up Hooks on an Existing or New Repo

The local enforcement layer for every repo in the portfolio (roadmap
CORRECTION 21). Written from the `learning_journey` rollout and applied to
`1099_reconciliation_pipeline`.

**Prerequisite:** the repo is already on uv — see [`UV_GUIDE.md`](UV_GUIDE.md).
The `uv-lock` hook below has nothing to guard until `pyproject.toml` and
`uv.lock` exist.

---

## Contents

1. [How it works](#1-how-it-works)
2. [Why it's worth it](#2-why-its-worth-it)
3. [One-time machine setup](#3-one-time-machine-setup)
4. [The standard config](#4-the-standard-config)
5. [Adopting hooks in a repo](#5-adopting-hooks-in-a-repo)
6. [Triaging the errors ruff can't fix](#6-triaging-the-errors-ruff-cant-fix)
7. [Conventional Commits](#7-conventional-commits)
8. [Mirroring the hooks in CI](#8-mirroring-the-hooks-in-ci)
9. [1099 repo — PII guard](#9-1099-repo--pii-guard)
10. [Troubleshooting](#10-troubleshooting)
11. [Maintenance](#11-maintenance)

---

## 1. How it works

`git commit` doesn't write a commit in one step. It pauses at fixed points and
runs any executable it finds in `.git/hooks/`:

- **`pre-commit`** — after staging, before the commit is written. Sees your **code**.
- **`commit-msg`** — after the message exists, before the commit is written.
  Sees your **message**.

Any non-zero exit aborts the commit.

The catch: `.git/hooks/pre-commit` is **one file**, it isn't version-controlled,
and it doesn't travel with a clone. The `pre-commit` tool solves that by
installing *itself* into that slot. Git calls the tool; the tool reads
`.pre-commit-config.yaml` — which *is* tracked — and decides what to run.

```
git commit
  └─ .git/hooks/pre-commit          (written by `pre-commit install`)
       └─ reads .pre-commit-config.yaml
            ├─ stashes unstaged changes
            ├─ filters staged files per hook (files: / exclude: / types:)
            ├─ runs each hook in its own cached env (~/.cache/pre-commit)
            └─ any non-zero exit → commit aborted
  └─ .git/hooks/commit-msg          (checks the message text)
  └─ commit object written
```

### Three commands, three different things

| Command | What it does |
|---|---|
| `pre-commit run --all-files` | A **manual** sweep. Wires nothing into git. |
| `pre-commit install` (`make hooks`) | **Wires** the hooks into `.git/hooks/` so they fire on every commit. |
| CI running `pre-commit run --all-files` | The **gate**. Can't be bypassed. |

Two behaviours that surprise everyone:

- **A hook that fixes a file still fails the commit.** The fix is in your
  working tree; `git add` it and commit again. pre-commit won't sneak an edit
  into a snapshot you never saw.
- **`commit-msg` hooks never run under `pre-commit run --all-files`** — there's
  no message to check. So without `pre-commit install`, Conventional Commits is
  enforced **nowhere**.

---

## 2. Why it's worth it

**One irreversible category.** Git history is append-only. Once a secret or a
real participant record is committed and pushed, deleting the file doesn't
remove it — it's in every clone. The hook is the last point where that's
preventable.

- GitGuardian's *State of Secrets Sprawl 2026* found 28.65 million new
  hardcoded secrets in public GitHub commits during 2025, up 34% year over year.
- The same report found commits co-authored by AI coding assistants leaked
  secrets at roughly **double** the baseline rate. A repo written through an
  agentic harness is in that population by construction.

**One ordinary category.** A formatting issue costs seconds at commit, minutes
in CI, and a whole review cycle if a human has to point at it.

**The honest counter-case.** Hooks are bypassable (`git commit --no-verify`),
so they are not a control on their own. Slow hooks make people commit less
often. The answer to both: **keep hooks fast, and make CI the gate.** Hooks
are the warning; CI is the wall.

---

## 3. One-time machine setup

```bash
uv tool install pre-commit --with pre-commit-uv
brew install go
```

- **Not `pip install`, and not into `.venv`.** pre-commit is an application.
  Installed in a venv, the hook script hardcodes that venv's Python path and
  breaks the moment you rebuild it.
- **`--with pre-commit-uv`** makes pre-commit build Python hook environments
  through uv — faster, and uv's own TLS stack sidesteps macOS certificate
  problems for those hooks.
- **`brew install go`** — the gitleaks hook is built from Go source. Without a
  Go toolchain, pre-commit downloads one over Python's `urllib`, which fails on
  macOS with `CERTIFICATE_VERIFY_FAILED` unless you've fixed Python's
  certificate store. See [Troubleshooting](#10-troubleshooting).

Installing a tool never changes `uv.lock`. No re-lock needed.

---

## 4. The standard config

`.pre-commit-config.yaml` at the repo root. Adjust the ruff `files:` regex to
your repo's real code paths.

```yaml
# Local enforcement layer (roadmap CORRECTION 21).
# Governing rule: this hook set is a strict SUBSET of the CI gate.
# CI runs `pre-commit run --all-files`, so it is a superset by construction.
#
# Setup:        uv tool install pre-commit --with pre-commit-uv
# First run:    pre-commit run --all-files     (inspect before installing)
# Install:      make hooks
# Maintenance:  pre-commit autoupdate --freeze

minimum_pre_commit_version: "3.2.0"

# A plain `pre-commit install` wires BOTH stages, so the commit-msg hook
# below is actually installed rather than silently skipped.
default_install_hook_types: [pre-commit, commit-msg]

repos:
  # --- Tier A: basics + secret boundary -------------------------------------
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-merge-conflict
      - id: check-added-large-files
        args: [--maxkb=1000]
      # Deliberately NOT excluded anywhere — a scanner with holes in it is a
      # scanner you cannot cite.
      - id: detect-private-key

  # --- Tier A: lint + format ------------------------------------------------
  # ruff-check --fix runs BEFORE ruff-format: a lint fix can emit code that
  # then needs reformatting. Scoped with `files:` because the hook receives
  # changed files directly, so `include`/`exclude` in pyproject.toml is ignored.
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.16.4
    hooks:
      - id: ruff-check
        args: [--fix]
        files: ^(src/|tests/|scripts/)
      - id: ruff-format
        files: ^(src/|tests/|scripts/)

  # --- Tier A: lockfile -----------------------------------------------------
  # Fires only when pyproject.toml or uv.lock change; fails if dependencies
  # were edited without regenerating the lock.
  - repo: https://github.com/astral-sh/uv-pre-commit
    rev: 0.9.28
    hooks:
      - id: uv-lock

  # --- Tier A: secret scanning ----------------------------------------------
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.30.1
    hooks:
      - id: gitleaks

  # --- Tier C: Conventional Commits -----------------------------------------
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v4.4.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
```

**Run `pre-commit autoupdate --freeze` immediately after creating this file.**
The `rev:` values above are starting points; `--freeze` resolves them to
current release SHAs.

### Scoping decisions

- **Hooks that rewrite files** (`trailing-whitespace`, `end-of-file-fixer`,
  ruff) can be excluded from archive directories — churn there isn't quality.
  Example from `learning_journey`: `exclude: ^courses/`.
- **Security hooks** (`detect-private-key`, `gitleaks`) are never excluded.
- **Notebook-bearing flagships** (DataVault, ODI, FormSense, AFC, Crucible)
  add `nbstripout` per Correction 21 Tier B. Repos whose notebooks are
  deliberate teaching artifacts with outputs (`learning_journey`) don't.

### Optional: generated-artifact drift

For repos carrying the Claude Code harness:

```yaml
  - repo: local
    hooks:
      - id: claude-agents-check
        name: claude agents in sync with shared prompts
        entry: python3 scripts/build_claude_agents.py --check
        language: system
        pass_filenames: false
        files: ^(\.github/docs/prompts/agents/|scripts/build_claude_agents\.py|\.claude/agents/|\.claude/output-styles/)
```

`language: system` uses the interpreter on `PATH` (the script is stdlib-only);
`pass_filenames: false` because the script walks the tree itself.

---

## 5. Adopting hooks in a repo

Four commits, in order. Don't install the hooks until the tree is clean, or
you'll fight them on every commit in between.

### Step 1 — Add the config and refresh pins

```bash
cp <template> .pre-commit-config.yaml
pre-commit autoupdate --freeze
```

### Step 2 — Look before you install

```bash
pre-commit run --all-files
```

Works **before** `pre-commit install` — nothing is wired into git yet, so this
is a pure dry run. **Expect it to fail the first time.** Fixers rewrite files;
ruff reports what it can't fix. Inspect with `git diff`.

### Step 3 — Commit config and cleanup separately

```bash
git add .pre-commit-config.yaml
git commit -m "build(hooks): add pre-commit config"

# fix remaining errors (see §6), then:
git add -A
git commit -m "style: apply pre-commit fixes"
```

A config change mixed with 80 whitespace fixes is unreviewable.

### Step 4 — Wire it into git

```bash
make hooks        # == pre-commit install --install-hooks
```

- `install` writes `.git/hooks/pre-commit` **and** `.git/hooks/commit-msg`
  (because of `default_install_hook_types`).
- `--install-hooks` pre-builds every hook environment now, instead of on your
  first commit.
- **Once per clone.** `.git/` isn't version-controlled. Anyone cloning the
  repo — including you on another machine — runs `make hooks` themselves. Put
  it in the README setup steps.

---

## 6. Triaging the errors ruff can't fix

### 1. Summary by rule

```bash
uv run ruff check --statistics src tests scripts
```

```
14  D103    [ ] undocumented-public-function
 6  B006    [ ] mutable-argument-default
 2  F401    [*] unused-import
Found 22 errors.
[*] 2 fixable with the `--fix` option (6 hidden fixes can be enabled with the `--unsafe-fixes` option).
```

Read the last line first.

### 2. Check for withheld fixes

ruff holds back "unsafe" fixes (ones that may change behaviour or drop
comments). Preview them — `--diff` writes nothing:

```bash
uv run ruff check --diff --unsafe-fixes src tests scripts
uv run ruff check --fix --unsafe-fixes src tests scripts   # if the diff is sane
```

Commit that batch separately from your manual edits.

### 3. Work one rule at a time

```bash
uv run ruff check --select D103 --output-format=concise src tests scripts
uv run ruff rule D103                                  # what it checks and why
```

Which files carry the weight:

```bash
uv run ruff check --select D103 --output-format=concise src | cut -d: -f1 | sort | uniq -c | sort -rn
```

### 4. Fix by class, not by count

| Tier | Rules | Why |
|---|---|---|
| **1 — real defects, fix now** | `F`, `B`, `RUF`, `E7xx` | `B006` (mutable default) is a latent bug, not style |
| **2 — mechanical, batch** | `I`, `UP`, `SIM`, `E501` | one obvious right answer each |
| **3 — documentation, own session** | `D` | real work, zero urgency |

### Rules you'll meet often

**SIM117 — nested `with`.** Combine them. Semantics are identical: `with A, B:`
enters A then B, exits B then A. ruff won't autofix it if comments sit between
the two lines — move comments above and use the parenthesized form to keep one
per manager:

```python
async with (
    limiter,  # rate cap
    sem,  # concurrency cap
):
    ...
```

Dedent the entire body by four spaces, then confirm with a test run.

**D401 — imperative first line.** Start the summary with a verb: `Return`, not
`Returns`. ruff *stems* the first word and checks it against a verb list, so
noun openers whose stem happens to be a verb also fire:

| Opener | D401 |
|---|---|
| `Decorator factory that…` | fires (stems to *decorate*) |
| `Custom format spec…` | fires (stems to *customize*) |
| `Handler for…` / `Wrapper around…` | fires |
| `Async batch driver for…` | clean |
| `Return a decorator that…` | clean |

The durable fix is a habit: summaries say what the **call does**, not what the
**object is**.

### Don't use `--add-noqa`

It converts a visible backlog into invisible debt. If a whole rule genuinely
doesn't apply somewhere, say so once, with a reason:

```toml
[tool.ruff.lint.per-file-ignores]
"tests/*" = ["D", "E501"]   # tests aren't public API; long parametrize lines are fine
```

---

## 7. Conventional Commits

Format: `type(scope): description`

### Types (the hook's default list)

| Type | Use for |
|---|---|
| `feat` | a new user-facing capability |
| `fix` | a bug fix |
| `test` | adding or correcting tests |
| `refactor` | restructuring with no behaviour change |
| `docs` | documentation only |
| `style` | formatting, whitespace |
| `build` | build system, dependencies, `pyproject.toml`, uv |
| `ci` | workflow files |
| `perf` | performance |
| `chore` | maintenance that fits nowhere else |
| `revert` | reverting a commit |

Anything else — `settings`, `config`, `update` — is rejected.

### Scope

A short, **reusable** token naming a part of the codebase: `providers`,
`pytest`, `hooks`, `engines`. Not a sentence. Verified against the hook:

| Scope | Result |
|---|---|
| `(providers)` | pass |
| `(tests, adapter)` | pass — commas and spaces are allowed |
| `(anthropic's adapter)` | **fail — apostrophes are not** |

### Description

Imperative, what the change **accomplishes**, no trailing period:

```
test(providers): add anthropic adapter tests with respx-faked transport
build(uv): migrate from pip requirements to uv
test(pytest): load _alias_httpx plugin so respx patches httpx2
```

### Fixing a rejected message

A rejected commit wasn't created — just commit again. If one slipped through:
`git commit --amend -m "..."`.

---

## 8. Mirroring the hooks in CI

Add a `lint` job that runs pre-commit itself — full template in
[`UV_GUIDE.md` §7](UV_GUIDE.md#7-ci-with-uv):

```yaml
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: astral-sh/setup-uv@bec219d24cd3e171d82865faccec33120bb574f4  # v10.1.0
        with:
          enable-cache: true
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pre-commit
          key: pre-commit-${{ runner.os }}-${{ hashFiles('.pre-commit-config.yaml') }}
      - run: uvx pre-commit run --all-files --show-diff-on-failure
```

One source of truth for every check and every version. Anything a
`--no-verify` commit slipped past locally is caught here. GitHub's
`ubuntu-latest` ships Go and a working CA store, so gitleaks builds without
the macOS certificate issue.

---

## 9. 1099 repo — PII guard

This section applies to `1099_reconciliation_pipeline` and any repo that
handles participant-shaped data.

### What's wrong today

The `.gitignore` header reads *"CRITICAL: REAL DATA (NEVER COMMIT!)"* — and the
two rules under it are **commented out**:

```gitignore
# All real participant data, SSNs, and financial information
#data/raw/
#data/processed/
```

Nothing has leaked: only `.gitkeep` files are tracked in those folders. But
the protection the comment promises doesn't exist. Anything dropped into
`data/raw/` today is committable.

They were most likely commented out to let the `.gitkeep` files in. The
correct pattern ignores the contents and re-includes only the placeholder:

```gitignore
# CRITICAL: REAL DATA (NEVER COMMIT!)
data/raw/*
!data/raw/.gitkeep
data/processed/*
!data/processed/.gitkeep
```

Verify:

```bash
git check-ignore -v data/raw/anything.xlsx     # prints the matching rule → ignored
git check-ignore -v data/raw/.gitkeep          # prints the ! rule → NOT ignored
```

### Why `.gitignore` alone isn't enough

`git add -f` bypasses `.gitignore` entirely. And **gitleaks can't help here**:
it scans text, and an `.xlsx` file is a zip archive. The SSNs inside a
spreadsheet are invisible to any content scanner. This is the gitleaks PII gap
from Correction 41 §4 — for this repo, the risk lives in exactly the file type
scanners can't read.

So guard by **path**, not content. pre-commit's `language: fail` hook fails for
every file it matches:

```yaml
  - repo: local
    hooks:
      - id: forbid-real-data
        name: real participant data must never be committed
        language: fail
        entry: "data/raw/ and data/processed/ may hold real PII. Only synthetic files in data/sample/ are committable."
        files: ^data/(raw|processed)/
        exclude: \.gitkeep$
```

Tested end to end: skipped on a normal commit, and on
`git add -f data/raw/participants.xlsx` it fails with:

```
- exit code: 1

data/raw/ and data/processed/ may hold real PII. Only synthetic files in data/sample/ are committable.

data/raw/participants.xlsx
```

Two layers: `.gitignore` stops the accident, the hook stops the override, CI
(running the same hook) stops the `--no-verify`.

### Synthetic SSNs

`src/core/generate_sample_data.py` generates SSNs with
`rng.randint(100000000, 999999999)`. That range includes numbers the SSA
actually issues, so a "synthetic" record can coincide with a real person's
SSN. Use ranges that are never issued — area `000`, area `666`, or group `00`
— so synthetic data is provably synthetic. Your reserved list already uses
`666778888`; extend the principle to the generator.

This is a code change, so it belongs in its own `fix(sample-data):` commit.

---

## 10. Troubleshooting

### `CERTIFICATE_VERIFY_FAILED` while installing hook environments

Almost always the gitleaks hook: pre-commit tried to download a Go toolchain
via Python's `urllib`, and Python on macOS has no access to Keychain roots.
Hooks built through uv (ruff, uv-lock) succeed because uv has its own TLS
stack — which is why only one hook fails.

1. `brew install go` — removes the download entirely.
2. Fix the root cause: `head -1 $(which pre-commit)` to see which Python.
   - `/Library/Frameworks/Python.framework/...` →
     `/Applications/Python\ 3.14/Install\ Certificates.command`
   - uv-managed Python → see [`UV_GUIDE.md` → SSL](UV_GUIDE.md#ssl-certificate_verify_failed)

Confirm the failing URL: `tail -40 ~/.cache/pre-commit/pre-commit.log`.

### `pre-commit: command not found`

`~/.local/bin` isn't on `PATH` in that shell. See
[`UV_GUIDE.md` → command not found](UV_GUIDE.md#command-not-found-uv-only-in-cursor).

### `files were modified by this hook`

Not an error. `git add` the fixed files and commit again.

### Conventional Commits rejects a message

Check the type against [§7](#7-conventional-commits), then the scope for
apostrophes.

### Skipping a hook

- One hook: `SKIP=gitleaks git commit -m "..."`
- All hooks: `git commit --no-verify`

Fine for a rare emergency. If you reach for either regularly, the hook isn't
earning its place — fix or remove it. CI will still catch whatever you skipped.

---

## 11. Maintenance

- **`make hooks-update`** (`pre-commit autoupdate --freeze`) every month or
  two. Commit as `build(hooks): refresh pinned hook revisions`.
- **After changing `.pre-commit-config.yaml`**, run
  `pre-commit run --all-files` before committing — new hooks apply to the
  whole tree, not just the next diff.
- **Keep ruff paths in sync.** The `files:` regex in the hook and
  `CODE_PATHS` in the Makefile must name the same directories.
- **SHA-pin GitHub Actions too.** Same reasoning as `--freeze`: tags move,
  SHAs don't. A `.github/dependabot.yml` watching `github-actions` keeps them
  current.
- **Once per clone:** `make hooks`.
