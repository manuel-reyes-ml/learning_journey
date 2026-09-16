""" """

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

# The SDK appends "/v1/messages" to its default base_url. Matching the
# absolute URL (rather than a respx base_url) keeps the assertion
# self-documenting: if this route fires, the client really did aim at
# Anthropic and not somewhere else.
_MESSAGES_URL: str = "https://api.anthropic.com/v1/messages"

# The SDK lifts `message._request_id` off this response header. It is NOT in
# the JSON body — a common source of "why is request_id None?".
_REQUEST_ID: str = "req_011CQtest"

# No fixture is defined here on purpose. conftest's `provider_settings` is
# already Anthropic-shaped (name="Anthropic", model="claude-sonnet-4-6"), so
# this module consumes it rather than duplicating it.


# =============================================================================
# TEST HELPERS
# =============================================================================
