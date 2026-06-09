"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import Protocol

import pytest

from llm_api_smoke_test.register import (
    DictInfo,
    ProviderList,
    RunResults,
    dicts,
    register_class,
)

# =============================================================================
# Test-only fake provider classes
# =============================================================================
 
# We define minimal classes here — NOT in conftest — because these are
# specific to registry tests.  They don't even need to implement smoke_test;
# the registry just stores classes.