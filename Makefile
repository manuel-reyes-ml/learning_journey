# learning_journey — task entry points.
#
# Every task has exactly one spelling here. Hooks, CI and I all call the same
# target, so "works on my machine" and "passes in CI" cannot drift apart.
#
# `make claude-agents` is named in the banner of every generated agent file and
# in the failure message of the claude-agents-check hook — this file is what
# makes that instruction real.

PYTHON ?= python3

SPELLER := courses/cs50_harvard/code/05_data_structures/speller/py_src
CODE_PATHS := scripts llm-api-smoke-test $(SPELLER)

.DEFAULT_GOAL := help

.PHONY: help sync hooks hooks-run hooks-update claude-agents claude-agents-check claude-rules \
		claude-rules-check claude-rules-list lint format test claude-gen

help:  ## Show the available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

# --- environment -------------------------------------------------------------

sync:  ## Install every workspace member and every dependency group
	uv sync --all-packages --all-groups

# --- git hooks ---------------------------------------------------------------

hooks:  ## Install pre-commit into .git/hooks (pre-commit + commit-msg stages)
	pre-commit install --install-hooks

hooks-run:  ## Run every hook against every file
	pre-commit run --all-files

hooks-update:  ## Refresh hook pins and freeze them to SHAs
	pre-commit autoupdate --freeze

# --- Claude Code harness -----------------------------------------------------

claude-agents:  ## Regenerate .claude/agents/ and .claude/output-styles/ from shared prompts
	$(PYTHON) scripts/build_claude_agents.py

claude-agents-check:  ## Fail if any generated agent file is stale
	$(PYTHON) scripts/build_claude_agents.py --check

claude-rules:  ## Rebuild .claude/rules/*.md from the canonical .cursor/rules/*.mdc bodies.
	python3 scripts/build_claude_rules.py

claude-rules-check:  ## Fail if a generated rule file is out of date or orphaned (CI / pre-commit).
	python3 scripts/build_claude_rules.py --check

claude-rules-list:  ## Show which .mdc maps to which rule, and whether it is path-scoped.
	python3 scripts/build_claude_rules.py --list

claude-gen: claude-agents claude-rules  ## Regenerate both harness artifacts in one step.

# --- quality -----------------------------------------------------------------
# Paths match the `files:` scope of the ruff hooks in .pre-commit-config.yaml.
# If one changes, change the other.

lint:  ## Lint the real code paths
	uv run ruff check $(CODE_PATHS)

format:  ## Format the real code paths
	uv run ruff format $(CODE_PATHS)

# --- tests -------------------------------------------------------------------
# One invocation per workspace member, on purpose. pytest reads exactly ONE
# config file per run, so a single root-level run would discard each member's
# [tool.pytest.ini_options] and collide their identically-named `tests` packages.

test:  ## Run every workspace member's test suite
	uv run pytest llm-api-smoke-test/tests
	uv run pytest $(SPELLER)/tests
