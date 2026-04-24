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