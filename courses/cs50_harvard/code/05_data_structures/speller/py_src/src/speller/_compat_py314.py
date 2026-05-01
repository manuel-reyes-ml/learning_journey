"""PEP 750 t-string log formatter. Requires Python 3.14+."""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from string.templatelib import Interpolation, Template


# =============================================================================
# CORE FUNCTION
# =============================================================================

def format_log_event(event: str, **kwargs: object) -> Template:
    """Build a Template from an event name and arbitrary kwargs.

    Renders as: "{event} | key1=value1 key2=value2 ..."
    Each kwarg becomes an Interpolation whose expression is the kwarg name,
    so extract_values() produces {"key1": value1, "key2": value2, ...}
    in the JSON output.
    """
    parts: list[str | Interpolation] = [f"{event} | "]
    
    for i, (name, value) in enumerate(kwargs.items()):
        if i > 0:
            parts.append(" ")
        parts.append(f"{name}=")
        parts.append(Interpolation(value, name))
    
    parts.append("")  # trailing statis segment to satisfy len(strings) == len(interpolation) + 1
    
    return Template(*parts)