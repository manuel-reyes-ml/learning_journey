# =============================================================================
# Speller — Makefile
# =============================================================================
# Single source of truth for common developer tasks. Run `make help` to see
# everything available. All targets assume you're running in the project root
# (where pyproject.toml lives) with a virtual environment activated.
# =============================================================================

## Variables: 
# 	:= means "set this value once, right now"
# 	?= means "set this only if it's not already set in the environment"
# The ?= python lets someone override it: make PY=python3.13 test
SHELL := /bin/bash
PY ?= python
SRC := src/speller
PYTEST := tests

# This declares "these targets are tasks, not files." Without .PHONY, if a file named
# test existed in your project root, make test would see the file, decide it's already
# up-to-date, and refuse to run. .PHONY says "never check for a file — always run
# the commands."
.PHONY: help install install-dev clean lint format typecheck test test-cov test-v \
		build wheel-install wheel-test all

# When someone types just make with no argument, this is what runs. Pointing it at help is
# the friendliest possible default — newcomers see the menu instead of getting an error or
# having a random target execute.
.DEFAULT_GOAL := help


# ─── HELP ───────────────────────────────────────────────────────
# By default, make prints every command before running it (you saw this in my test output).
# Prefixing with @ silences that echo. Use it for echo statements and metadata output so the
# terminal stays clean.
#
# 1. grep finds every line matching the pattern name: ## Description
# 2. sort alphabetizes them
# 3. awk splits on ##  and prints with cyan ANSI color codes (\033[36m) on the target name
# The $$ is a make-escape for the shell's $. Make uses $ for its own variables, so to pass a
# literal $ through to the shell you double it.
# 
# You don't need to memorize this line. Just copy it into every Makefile and keep writing
# target: ## Description comments. The help menu takes care of itself forever.
help:  ## Show this help menu
	@echo "Speller - available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
	@echo ""


# ─── SETUP ────────────────────────────────────────────────────── 
install:  ## Install the package editable mode
	$(PY) -m pip install -e .

install-dev:  ## Install with dev + test dependencies
	$(PY) -m pip install -e ".[dev,test]"


# ─── CODE QUALITY ───────────────────────────────────────────────
lint:  ## Run ruff linter (catches style and bugs)
	ruff check $(SRC)

format:  ## Auto-format code with ruff
	ruff format $(SRC)
	ruff check --fix $(SRC)

typecheck:  ## Run mypy static type checker (strict mode via pyproject.toml)
	mypy $(SRC) $(PYTEST)

# ─── TESTS ──────────────────────────────────────────────────────
test:  ## Run the test suite
	pytest

test-cov:  ## Run tests with coverage report
	pytest --cov=speller --cov-report=term-missing

test-v:  ## Run tests with verbose
	pytest -v tests/


# ─── BUILD & PACKAGING ──────────────────────────────────────────
# The clean before the colon is a dependency — make runs clean first, then build.
# This means make build always starts fresh, no stale artifacts. Similarly,
# wheel-test depends on wheel-install, which depends on build.
# One command chains the whole thing.
clean:  ## Remove build artifacts and caches
	rm -rf build/ dist/ *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true

build: clean  ## Build a wheel in dist/
	$(PY) -m build --wheel

wheel-install: build  ## Build the wheel AND install it via pipx (isolated)
	pipx install --force dist/*.whl

wheel-test: wheel-install  ## Build, install, and smoke-test the wheel
	@echo ""
	@echo "━━━ Testing installed wheel ━━━"
	speller --help
	@echo ""
	@echo "✓ Wheel test passed"



# ─── CONVENIENCE ────────────────────────────────────────────────
all: format lint typecheck test  ## Run format, lint, typecheck, and tests