"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = []


# =============================================================================
# CORE FUNCTION
# =============================================================================

def format_log_event(event: str, **kwargs: object) -> tuple[str, dict[str, object]]:
    """Build (rendered_msg, extras_dict) directly — no Template intermediary.

    Output shape matches what template_to_msg_extras() produces on 3.14+,
    so the same downstream logger code handles both versions.
    """
    parts = [f"{event} | "]
    for i, (name, raw) in enumerate(kwargs.items()):
        if i > 0:
            parts.append(" ")
        parts.append(f"{name}=")
        
        # Allow callers to pass (value, format_spec) for things like (0.143, ".2f")
        if isinstance(raw, tuple) and len(raw) == 2 and isinstance(raw[1], str):
            value, fmt = raw
            parts.append(format(value, fmt))
        
    return "".join(parts), dict(kwargs)
    
    
def template_to_msg_extras(template: object) -> tuple[str, dict[str, object]]:
    """Stub. Unreachable on Python <3.14 because no Template can exist."""
    raise RuntimeError(
        "template_to_msg_extras() requires Python 3.14+. "
        "On older Python, use format_log_event() which returns "
        "(msg, extras) directly."
    )