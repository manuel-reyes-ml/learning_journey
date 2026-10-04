# uv — Migrating an Existing Repo & Starting a New One

A working guide for every Python repo in the portfolio. Written from the
`learning_journey` migration (every error in the troubleshooting section
actually happened) and applied to `1099_reconciliation_pipeline`.

Companion: [`PRE_COMMIT_GUIDE.md`](PRE_COMMIT_GUIDE.md) — do this guide first;
the hooks guide assumes a `pyproject.toml` and `uv.lock` already exist.

---

## Contents

1. [The mental model](#1-the-mental-model)
2. [One-time machine setup](#2-one-time-machine-setup)
3. [Path A — Starting a new repo](#3-path-a--starting-a-new-repo)
4. [Path B — Migrating an existing pip repo](#4-path-b--migrating-an-existing-pip-repo)
5. [Worked example — `1099_reconciliation_pipeline`](#5-worked-example--1099_reconciliation_pipeline)
6. [Monorepos — uv workspaces](#6-monorepos--uv-workspaces)
7. [CI with uv](#7-ci-with-uv)
8. [Makefile template](#8-makefile-template)
9. [Daily command cheat sheet](#9-daily-command-cheat-sheet)
10. [Troubleshooting — every error we actually hit](#10-troubleshooting--every-error-we-actually-hit)
11. [Production rules](#11-production-rules)

---

## 1. The mental model

Four files, three roles:

| File | Role | Who writes it | Committed? |
|---|---|---|---|
| `pyproject.toml` | **what you asked for** — direct deps, Python range, tool config | you | yes |
| `uv.lock` | **what you got** — every resolved version, transitive included | uv | yes |
| `.venv/` | **what's installed** — the environment on disk | uv | **never** |
| `.python-version` | which Python this project uses locally | `uv python pin` | yes |

`requirements.txt` from `pip freeze` collapses all three roles into one file,
which is why you can't tell which of its 130 lines you actually chose.

### Libraries vs applications

This distinction decides where every tool goes.

- **Libraries** — your code `import`s them → project dependencies (`uv add`).
  pandas, pydantic, pytest.
- **Applications** — you *run* them, your code never imports them → installed
  globally with `uv tool install`. pre-commit, gitleaks, uv itself.

`uv tool install` never touches `pyproject.toml` or `uv.lock`, so it never
requires a re-lock.

### Version specifiers

`uv add pandas` writes `pandas>=3.0.5` — a **floor** at whatever it just
resolved. The floor lives in `pyproject.toml`; the exact version lives in
`uv.lock`. Add a **ceiling** for anything pre-1.0 or anything whose major
version you don't control:

```toml
dependencies = ["anthropic>=1.0,<2.0"]   # an open upper bound let 0.x → 1.x through silently
```

---

## 2. One-time machine setup

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

uv lands in `~/.local/bin`. The installer adds that directory to `PATH` in your
shell profile, but **only shells started afterward see it**.

- Terminal says `command not found: uv` → `source $HOME/.local/bin/env`
- Cursor/VS Code terminal still can't find it → **quit the app fully (`Cmd+Q`)
  and reopen**. The integrated terminal inherits `PATH` from the app process,
  not from a fresh login shell.

### Install the global tools

```bash
uv tool install pre-commit --with pre-commit-uv
brew install go            # lets pre-commit build gitleaks without a download
```

### Fix Python's certificate store (macOS)

Python on macOS does not read the Keychain. If anything fails with
`CERTIFICATE_VERIFY_FAILED`, see
[Troubleshooting → SSL](#ssl-certificate_verify_failed).

---

## 3. Path A — Starting a new repo

### Decide the shape first

| Repo type | Command | Result |
|---|---|---|
| **Installable package** (pipeline, CLI, anything with tests) | `uv init --package` | `src/<name>/` layout + build backend; imports are `from <name>...` |
| Notebooks / scripts collection, nothing to install | `uv init --bare` | just `pyproject.toml` |
| Multiple packages in one repo | see [§6](#6-monorepos--uv-workspaces) | workspace |

**Default to `--package` for anything that will be a portfolio flagship.** It
gives you a real importable name. The 1099 repo's `from src.config import ...`
is what happens without it — the package is literally named `src`.

### Steps

```bash
mkdir my_project && cd my_project
git init
uv init --package
uv python pin 3.14
```

Open `pyproject.toml` and set the support floor explicitly:

```toml
requires-python = ">=3.12"   # your CI matrix must be a subset of this range
```

`requires-python` is your **support floor**. `.python-version` is your **local
dev version**. They are different facts — keep both.

Add dependencies:

```bash
uv add pandas pydantic                 # runtime → [project.dependencies]
uv add --dev pytest ruff               # dev tooling → [dependency-groups] dev
uv add --group notebooks ipykernel     # optional group for VS Code notebooks
```

`ipykernel` is all VS Code/Cursor needs to run notebooks — you don't need the
whole `jupyterlab` stack unless you use the browser UI.

### Add tool config to `pyproject.toml`

```toml
[tool.uv]
default-groups = ["dev", "notebooks"]   # `uv sync` installs these automatically

[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
addopts = ["-ra", "--strict-markers", "--strict-config", "--import-mode=importlib"]

[tool.ruff]
line-length = 100
target-version = "py312"               # match your requires-python floor

[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "UP", "SIM", "RUF", "D"]

[tool.ruff.lint.pydocstyle]
convention = "numpy"

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["D", "E501"]
```

`--import-mode=importlib` is pytest's recommendation for new projects: it
doesn't mutate `sys.path` and doesn't require unique test file basenames.

### Verify and commit

```bash
uv sync
uv run pytest
git add pyproject.toml uv.lock .python-version src/ tests/
git commit -m "build: initialise project with uv"
```

Then go straight to [`PRE_COMMIT_GUIDE.md`](PRE_COMMIT_GUIDE.md), then add
[CI](#7-ci-with-uv).

---

## 4. Path B — Migrating an existing pip repo

One variable at a time. Don't rename packages, restructure folders, or upgrade
libraries during the migration — each of those is its own commit later.

### Step 0 — Branch and baseline

```bash
git checkout -b build/uv-migration
python -m pytest -q          # record what passes BEFORE you change anything
```

### Step 1 — Find your real direct dependencies

**Never run `uv add -r requirements.txt` on a `pip freeze` file.** It writes
every transitive package into `pyproject.toml` as if you'd asked for it —
you'd be pinned to `appnope==0.1.4` forever and unable to tell which lines
matter. Import `.in` files if you have them; never `.txt` freezes.

Instead, discover what your code actually imports. Save as
`scripts/find_imports.py` (or run from `/tmp`):

```python
"""List top-level third-party imports across .py files and notebooks."""

import ast
import json
import sys
from pathlib import Path

SKIP = {".venv", "venv", ".git", "node_modules", "build", "dist"}
local = {p.name for p in Path(".").iterdir() if p.is_dir()} | {
    p.stem for p in Path(".").glob("*.py")
}
found: dict[str, set[str]] = {}


def scan(source: str, origin: str) -> None:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names = [node.module]
        else:
            continue
        for name in names:
            top = name.split(".")[0]
            if top not in sys.stdlib_module_names and top not in local:
                found.setdefault(top, set()).add(origin)


for path in Path(".").rglob("*"):
    if SKIP & set(path.parts):
        continue
    if path.suffix == ".py":
        scan(path.read_text(errors="ignore"), str(path))
    elif path.suffix == ".ipynb":
        try:
            cells = json.loads(path.read_text(errors="ignore")).get("cells", [])
        except json.JSONDecodeError:
            continue
        code = "\n".join(
            "".join(c.get("source", [])) for c in cells if c.get("cell_type") == "code"
        )
        code = "\n".join(
            ln for ln in code.splitlines() if not ln.lstrip().startswith(("%", "!"))
        )
        scan(code, str(path))

for mod in sorted(found):
    print(f"{mod:<20} {len(found[mod]):>3} file(s)")
```

```bash
python3 scripts/find_imports.py
```

**Then add what the script can't see:**

- **Dynamically loaded engines.** pandas imports `openpyxl` only when you read
  or write `.xlsx`. If you touch Excel, you need `openpyxl` even though no file
  imports it.
- **Import name ≠ PyPI name.** Translate before `uv add`:

| `import` | `uv add` |
|---|---|
| `yaml` | `pyyaml` |
| `bs4` | `beautifulsoup4` |
| `PIL` | `pillow` |
| `sklearn` | `scikit-learn` |
| `dotenv` | `python-dotenv` |
| `cv2` | `opencv-python` |

### Step 2 — Leave the old venv

```bash
deactivate      # "command not found" means you're already out
rm -rf .venv    # uv rebuilds it; you never activate it again
```

### Step 3 — Create `pyproject.toml`

```bash
uv init --bare
uv python pin 3.14
```

Use `--bare` for a migration even if the repo *should* eventually be a package
— converting to `--package` means renaming imports, which is a separate change.

Set `requires-python` to the floor you'll test in CI.

### Step 4 — Add dependencies

```bash
uv add pandas openpyxl matplotlib           # runtime, from step 1
uv add --dev pytest ruff
uv add --group notebooks ipykernel          # only if the repo has notebooks
```

### Step 5 — Port pytest config

If tests used `PYTHONPATH=. pytest` or `sys.path` hacks, move that into config
so it's declared rather than remembered:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]      # only for non-packaged repos whose tests import from the repo root
addopts = ["-ra", "--strict-markers"]
```

`pythonpath` entries resolve relative to pytest's **rootdir** (the directory
holding this `pyproject.toml`), not your shell's working directory.

### Step 6 — Verify, delete, commit

```bash
uv sync
uv run pytest
```

Compare against your step-0 baseline. **A migration that surfaces a failing
test is working correctly** — in `learning_journey` it exposed a `REPORT` →
`Report` rename the old broken CI had been hiding for months.

```bash
git rm requirements.txt requirements-dev.txt
git add pyproject.toml uv.lock .python-version
git commit -m "build(uv): migrate from pip requirements to uv"
```

### Step 7 — Point your editor at the new venv

`Cmd+Shift+P` → **Python: Select Interpreter** → `./.venv/bin/python` at the
**repo root**. Then **Python: Restart Language Server**.

If `pandas` or `pytest` show as unresolved, the editor is still pointed at the
deleted venv. That's the whole diagnosis.

---

## 5. Worked example — `1099_reconciliation_pipeline`

Findings from reading the repo as of Sept 2026.

### What's there now

- `requirements.txt` — ~130-line `pip freeze`, including the full Jupyter stack
- `requirements-dev.txt` — `-r requirements.txt` + `pytest>=8.0`
- `ci.yml` — the same pip workflow `learning_journey` had: 3.11–3.14 matrix,
  `PYTHONPATH: .`, `actions/setup-python`
- Code imports the package **as `src`** (`from src.config import ...`,
  `from src.engines.match_planid import ...`)

### Real direct dependencies

Running `find_imports.py` against the repo:

```
faker                  1 file(s)
matplotlib             4 file(s)
pandas                36 file(s)
pytest                 7 file(s)
```

Plus `openpyxl` (the repo reads and writes `.xlsx`; pandas loads it
dynamically). **130 lines → 4 runtime dependencies.** That contrast is worth
a line in the README.

### Decision: keep `from src...` for now

Converting to a proper `src/reconciliation/` package means rewriting imports
across 44 Python files and 11 notebooks. That's the right end state for the
Track B public repo, but it's a refactor, not a migration. Migrate first,
rename later, as separate commits.

### Commands

```bash
git checkout -b build/uv-migration
python -m pytest -q                              # baseline

deactivate; rm -rf .venv
uv init --bare
uv python pin 3.14

uv add pandas openpyxl matplotlib faker
uv add --dev pytest ruff
uv add --group notebooks ipykernel
```

Then add to `pyproject.toml`:

```toml
[tool.uv]
default-groups = ["dev", "notebooks"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]          # makes `import src.config` resolve from the repo root
addopts = ["-ra", "--strict-markers"]
```

A single-package repo **should** have `[tool.pytest.ini_options]` at the root —
unlike a workspace root (see [§6](#6-monorepos--uv-workspaces)).

```bash
uv sync
uv run pytest
git rm requirements.txt requirements-dev.txt
git add pyproject.toml uv.lock .python-version
git commit -m "build(uv): migrate from pip requirements to uv"
```

### Before you do anything else in this repo

Read [`PRE_COMMIT_GUIDE.md` §9](PRE_COMMIT_GUIDE.md#9-1099-repo--pii-guard).
The `.gitignore` rules protecting `data/raw/` and `data/processed/` are
**commented out**. Nothing has leaked — only `.gitkeep` files are tracked
there — but the protection you think exists doesn't.

---

## 6. Monorepos — uv workspaces

Use when one repo holds several installable packages with their own
`pyproject.toml` (e.g. `learning_journey` with `llm-api-smoke-test` and
`speller`). One lockfile, one shared `.venv`, members installed editable.

### Root `pyproject.toml`

```toml
[project]
name = "learning-journey"
requires-python = ">=3.12"      # must be compatible with EVERY member's floor
dependencies = [...]

[dependency-groups]
dev = ["ruff>=0.16"]            # NO pytest here — members own their pytest pins

[tool.uv.workspace]
members = ["llm-api-smoke-test", "path/to/other_package"]
```

**Do not put `[tool.pytest.ini_options]` at a workspace root.** pytest reads
exactly one config file per run; a root block silently overrides each member's
own (`asyncio_mode`, `--strict-markers`, coverage scope).

### Sync and test

```bash
uv sync --all-packages --all-groups     # plain `uv sync` installs only the root
uv run pytest llm-api-smoke-test/tests  # one invocation PER member
uv run pytest path/to/other_package/tests
```

Each invocation finds its own member's config automatically. Never run bare
`uv run pytest` from a workspace root — it collects everything, including
coursework named `test_*.py`, and collides identically-named `tests` packages.

### Adding a dependency to a specific member

```bash
uv add --package llm-api-smoke-test --group test "httpx2>=2.0,<3.0"
```

Without `--package`, uv writes to the **root** `pyproject.toml`.

### Member test dependencies

Use `[dependency-groups]`, not `[project.optional-dependencies]`. Extras
(`pkg[test]`) are for your *users*; groups are for *developing* the package.
Compose groups with `{include-group = "..."}`:

```toml
[dependency-groups]
test = ["pytest>=8.0,<10.0", "pytest-asyncio>=0.23,<2.0"]
dev = [{include-group = "test"}, "ruff>=0.5,<1.0"]
```

There is no bracket syntax for groups. `"my-pkg[test]"` refers to an **extra**
and silently resolves to nothing once `test` is a group.

---

## 7. CI with uv

`.github/workflows/ci.yml` for a single-package repo:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: lint + hooks
    runs-on: ubuntu-latest
    timeout-minutes: 10
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

  tests:
    name: tests (py${{ matrix.python-version }})
    runs-on: ubuntu-latest
    timeout-minutes: 15
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.12", "3.13", "3.14"]   # subset of requires-python
    steps:
      - uses: actions/checkout@v6
      - uses: astral-sh/setup-uv@bec219d24cd3e171d82865faccec33120bb574f4  # v10.1.0
        with:
          python-version: ${{ matrix.python-version }}
          enable-cache: true
      - run: uv sync --locked
      - run: uv run pytest
```

For a workspace: `uv sync --all-packages --all-groups --locked`, and one
`uv run pytest <member>/tests` step per member.

**Key choices:**

- **`--locked`** fails if `uv.lock` is stale. Plain `uv sync` silently
  regenerates it — CI would then test a different dependency set than your
  machine.
- **No `actions/setup-python`.** `setup-uv` with `python-version` handles it.
- **No `PYTHONPATH`.** Declared in `pyproject.toml` instead.
- **SHA-pinned `setup-uv`.** Tags are movable pointers; SHAs aren't. Astral's
  own docs pin this way. Floating majors like `@v10` only exist if the
  maintainer publishes them — `setup-uv` doesn't.
- **The `lint` job runs pre-commit itself**, so CI is a superset of your local
  hooks by construction.

---

## 8. Makefile template

Every task gets one spelling. Hooks, CI, and you call the same target.
Recipe lines **must** start with a real tab.

```makefile
PYTHON ?= python3
CODE_PATHS := src tests

.DEFAULT_GOAL := help
.PHONY: help sync hooks hooks-run hooks-update lint format test

help:  ## Show the available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

sync:  ## Install dependencies and default groups
	uv sync

hooks:  ## Install pre-commit into .git/hooks (pre-commit + commit-msg)
	pre-commit install --install-hooks

hooks-run:  ## Run every hook against every file
	pre-commit run --all-files

hooks-update:  ## Refresh hook pins and freeze them to SHAs
	pre-commit autoupdate --freeze

lint:  ## Lint
	uv run ruff check $(CODE_PATHS)

format:  ## Format
	uv run ruff format $(CODE_PATHS)

test:  ## Run the test suite
	uv run pytest
```

---

## 9. Daily command cheat sheet

| Goal | Command |
|---|---|
| Add a runtime dependency | `uv add pandas` |
| Add a dev tool | `uv add --dev ruff` |
| Add to a named group | `uv add --group notebooks ipykernel` |
| Add to a workspace member | `uv add --package <member> <dep>` |
| Remove a dependency | `uv remove pandas` / `uv remove --dev pytest` |
| Install everything from the lock | `uv sync` |
| Install a workspace fully | `uv sync --all-packages --all-groups` |
| Re-resolve after editing `pyproject.toml` | `uv lock` |
| Upgrade one package | `uv lock --upgrade-package pandas` |
| Run anything in the env | `uv run pytest`, `uv run python script.py` |
| Run a tool without installing it | `uvx ruff check .` |
| Install a global tool | `uv tool install pre-commit --with pre-commit-uv` |
| See the dependency tree | `uv tree` |
| Which Python? | `uv run python --version` |

**When to re-lock:** only after editing `pyproject.toml`. Installing a tool,
activating anything, or running tests never requires it. The `uv-lock`
pre-commit hook catches you if you forget.

---

## 10. Troubleshooting — every error we actually hit

### `command not found: uv` (only in Cursor)

Cursor started before the installer edited your profile. `Cmd+Q` and reopen.
Immediate fix for one session: `source $HOME/.local/bin/env`.

### `No solution found ... your workspace's requirements are unsatisfiable`

Read the two `depends on` lines — they name the conflict. Our case:

```
learning-journey:dev depends on pytest>=9.1.1
llm-api-smoke-test[dev] depends on pytest>=8.0,<9.0
```

`uv add --dev pytest` at the root wrote a floor above a member's ceiling. Fix:
`uv remove --dev pytest` at the root. Ignore any `sys_platform == 'win32'` in
the message — uv resolves for every platform, and that's just the first split
it tried.

### Root and member `requires-python` disagree

The workspace root's floor must be compatible with every member's. Set the root
to the highest member floor (e.g. `>=3.12`), and drop any CI matrix version
below it.

### `warning: The package ... does not have an extra named 'test'`

Something still says `"pkg[test]"` after `test` became a dependency group.
Replace it with `{include-group = "test"}`.

### `Unknown config option: asyncio_mode` / `'asyncio' not found in markers`

`pytest-asyncio` isn't installed. Almost always the previous error in disguise:
the `test` group never synced. **Don't** register the marker manually — that
silences the first message and your async tests still won't run.

### `ModuleNotFoundError` for your own package after migrating

Its editable install lived in the deleted venv. Workspace: add it to
`[tool.uv.workspace] members` and `uv sync --all-packages`. Single repo:
`pythonpath = ["."]` in pytest config.

### `ImportPathMismatchError: ('tests.conftest', ...)`

Two directories named `tests/` both contain `__init__.py`, collected in one
pytest process. Run one pytest invocation per package.

### Bare `uv run pytest` collects coursework / wrong files

No `testpaths` configured (correct at a workspace root). Pass explicit paths.

### Pylance underlines `pandas`, `pytest`, your own package

1. Wrong interpreter → Select Interpreter → `./.venv/bin/python` at repo root.
2. If only **your own package** stays red: setuptools' editable install uses
   an import hook Pylance can't follow. Add to `.vscode/settings.json`:

```json
{ "python.analysis.extraPaths": ["path/to/package/src"] }
```

### `Error importing plugin "tests.xxx": No module named 'tests'`

A `-p tests.xxx` plugin needs the package root on the path:
`pythonpath = ["src", "."]`.

### `Unable to resolve action astral-sh/setup-uv@v10`

No floating `v10` tag exists. Use the SHA pin from [§7](#7-ci-with-uv).

### SSL: `CERTIFICATE_VERIFY_FAILED`

Python on macOS has no access to Keychain roots. Check which Python you're on:

```bash
head -1 $(which pre-commit)
```

- **`/Library/Frameworks/Python.framework/...`** →
  `/Applications/Python\ 3.14/Install\ Certificates.command`
- **uv-managed Python** → copy a bundle somewhere stable and export it:

```bash
mkdir -p ~/.certs
uvx --from certifi python -c "import certifi, shutil; shutil.copy(certifi.where(), '$HOME/.certs/cacert.pem')"
echo 'export SSL_CERT_FILE="$HOME/.certs/cacert.pem"' >> ~/.zshrc
source ~/.zshrc
```

Single quotes in the `echo` so `$HOME` resolves at shell startup. Restart
Cursor fully afterward.

### A dependency jumped a major version and broke things

An open upper bound let it through. Our case: `anthropic>=0.40` pulled 1.x,
which swapped `httpx` for `httpx2`. Pin `>=X,<X+1` on anything you don't
control.

---

## 11. Production rules

1. **Commit `uv.lock`. Never commit `.venv`.**
2. **Never `pip install` in a uv project.** It bypasses `pyproject.toml` and
   `uv.lock`, and the next `uv sync` removes it.
3. **Never import a `pip freeze` file.** Reconstruct direct deps from imports.
4. **`--locked` in CI, plain `uv sync` locally.** Fail remotely, self-heal
   locally.
5. **Ceilings on anything pre-1.0 or fast-moving.**
6. **`requires-python` and the CI matrix must agree.** Two statements of the
   same fact.
7. **Applications via `uv tool install`, libraries via `uv add`.**
8. **Migrate first, refactor later.** One variable per commit.
9. **Declare what you import.** If a file under `src/` imports it, it's in
   `dependencies` — even when something else happens to pull it in.
10. **A migration that surfaces a failing test is a success.** It found
    something the old setup was hiding.
