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
    
    for i, (name, raw) in enumerate(kwargs.items()):
        if i > 0:
            parts.append(" ")
        parts.append(f"{name}=")
        
        # Allow callers to pass (value, format_spec) for things like (0.143, ".2f")
        if isinstance(raw, tuple) and len(raw) == 2 and isinstance(raw[1], str):
            value, fmt = raw
            # 1. The kwarg name becomes the expression argument. Interpolation(value, name) is
            # the line that makes everything work. name is the keyword's identifier as a string
            # ("count"), and that's exactly what your extract_values() reads via interp.expression
            # to populate the JSON values dict. Skip the second arg and every key in your structured
            # logs becomes "".
            parts.append(Interpolation(value, name, None, fmt))
        else:
            parts.append(Interpolation(raw, name))
            
    # The len(strings) == len(interpolations) + 1 invariant. The Template format requires N+1
    # string slots for N interpolations. That's why the trailing parts.append("") is there —
    # without it, your last item is an Interpolation, the constructor inserts an empty string
    # after it for you, and you'll see a slightly weird repr but still correct behavior.
    # Adding it explicitly is just defensive and self-documenting.
    parts.append("")
    
    # Consecutive strings get concatenated by the constructor. 
    # parts = ["dictionary_loaded | ", "count="] followed by an Interpolation is fine — the
    # constructor merges the two strings into "dictionary_loaded | count=" automatically. 
    # So you don't have to obsessively interleave; you just need some string between
    # consecutive interpolations.
    return Template(*parts)


# Usage
# tmpl = format_log_event(
#     "spell_check_done",
#    file="austen.txt",
#    elapsed=(0.1423, ".2f"),  # → "elapsed=0.14"
#    misspelled=42,
#   )