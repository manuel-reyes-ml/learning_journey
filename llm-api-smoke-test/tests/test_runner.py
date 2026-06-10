"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import pytest

from llm_api_smoke_test.providers import SmokeTestResult
from llm_api_smoke_test.runner import DEFAULT_PROMPT, run_smoke_tests

# Note: FakeSyncProvider is in conftest.py — auto-discovered by pytest.
# We import it from conftest only for type hints.
from tests.conftest import FakeSyncProvider

# =============================================================================
# Happy path
# =============================================================================

