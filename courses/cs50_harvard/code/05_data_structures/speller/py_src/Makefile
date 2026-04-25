# =============================================================================
# Speller — Makefile
# =============================================================================
# Single source of truth for common developer tasks. Run `make help` to see
# everything available. All targets assume you're running in the project root
# (where pyproject.toml lives) with a virtual environment activated.
# =============================================================================

SHELL := /bin/bash
PY ?= python
SRC := src/speller

.PHONY: help install install-dev clean lint format typecheck test test-cov \
		build wheel-install wheel-test all

.DEFAULT_GOAL := help


# ─── HELP ───────────────────────────────────────────────────────
help:  ## Show this help menu
	@echo "Speller - available commandas:"
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


# ─── TESTS ──────────────────────────────────────────────────────
test:  ## Run the test suite
	pytest

test-cov:  ## Run tests with coverage report
	pytest --cov=speller --cov-report=term-missing

test-v:  ## Run tests with verbose
	pytest -v tests/


# ─── BUILD & PACKAGING ──────────────────────────────────────────
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