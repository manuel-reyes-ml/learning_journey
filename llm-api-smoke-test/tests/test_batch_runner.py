"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import asyncio
import pytest

from llm_api_smoke_test.batch_runner import batch_smoke_test

# Note: FakeAsyncProvider is in conftest.py
from tests.conftest import FakeAsyncProvider


# pytestmark applies @pytest.mark.asyncio to EVERY test in this file —
# the per-test decorator boilerplate disappears.
pytestmark = pytest.mark.asyncio

# =============================================================================
# Happy path
# =============================================================================

