"""API key smoke test package.
 
Verifies that Anthropic and Gemini API keys are correctly configured by
sending a single short prompt to each provider and reporting the result.
 
This is a learning artifact for Manuel Reyes' GenAI-First career
transformation (Roadmap v8.3) — production-grade Python patterns at the
smallest possible scale: Pydantic config, Protocol-based provider abstraction,
layer-boundary discipline, lazy-formatted logging, NumPy-style docstrings.
"""

from __future__ import annotations

import logging

# Library logging pattern: stay silent unless the application configures
# logging. The CLI entry point (__main__.py) calls configure_logging() to
# acivate console/file handlers.
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Package metadata
__version__ = "0.1.0"