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
    """Build a Template from an event name and kwargs.

    Renders as: ``"{event} | k1={v1} k2={v2} ..."``

    Each kwarg name becomes the ``expression`` field on its Interpolation,
    so JsonTemplateFormatter.extract_values() produces a structured
    ``values`` dict keyed by the kwarg names.

    Examples
    --------
    >>> tmpl = format_log_event("spell_check", file="cat.txt", count=42)
    >>> # On the file handler:
    >>> # {"message": "spell_check | file=cat.txt count=42",
    >>> #  "values": {"file": "cat.txt", "count": 42}}
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


def template_to_msg_extras(template: Template) -> tuple[str, dict[str, object]]:
    """Render a Template and extract its raw interpolation values.

    Returns the fully-rendered message (format specs applied) AND a dict of
    raw, unformatted values keyed by source expression. This dual-output is
    what powers the dual-handler logging architecture: the rendered string
    goes to the human console; the raw dict goes to JSON for observability.
    """
    parts: list[str] = []
    extras: dict[str, object] = {}
    
    for piece in template:
        match piece:
            case str() as text:
                parts.append(text)
            case Interpolation() as interp:
                extras[interp.expression] = interp.value  # raw value preserved
                if interp.format_spec:
                    parts.append(format(interp.value, interp.format_spec))
                else:
                    parts.append(str(interp.value))
            
            # Defensive - Template iteration only yields these two types
            case _:  # Default case (wildcard)
                raise TypeError(f"Unexpected Template piece: {type(piece)!r}")
            
    return "".join(parts), extras