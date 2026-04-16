"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import json
import logging
from typing import Any, Final, override
from string.templatelib import Template, Interpolation

from speller.config import file_dirs, fhandler_config


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = []


# =============================================================================
# CORE FUNCTIONS — Template Processing
# =============================================================================

def render_message(template: Template) -> str:
    """Render a Template as a human-readable string (f-string equivalent).

    Iterates over the Template's parts and reconstructs the final
    string, applying any format specs to interpolated values.

    This replicates what an f-string does automatically — but here
    YOU control the rendering.  The same Template can be rendered
    differently by different functions (this one for humans,
    :func:`extract_values` for machines).

    Parameters
    ----------
    template : Template
        A t-string ``Template`` object from ``string.templatelib``.

    Returns
    -------
    str
        The fully rendered string, identical to what an f-string
        would have produced.

    Examples
    --------
    >>> count = 143091
    >>> render_message(t"Loaded {count} words")
    'Loaded 143091 words'
    >>> render_message(t"Time: {0.1423:.2f}s")
    'Time: 0.14s'
    """
    parts: list[str] = []
    
    for item in template:
        # ─── Structural pattern matching (Python 3.10+) ───
        # match/case is the idiomatic way to process Template parts.
        # Each element is either a str (static text) or an
        # Interpolation (a variable with metadata).
        match item:
            case str() as text:
                # Static text - pass through unchanged
                parts.append(text)
            case Interpolation() as interp:
                # Dynamic value - apply format spec if present
                # interp.value = the actual Python object (int, str, etc.)
                # interp.format_spec = the format string after ':' (e.g. ".2f")
                # interp.expression = the source code text (e.g. "count")
                if interp.format_spec:
                    parts.append(format(interp.value, interp.format_spec))
                else:
                    parts.append(str(interp.value))
    
    return "".join(parts)


def extract_values(template: Template) -> dict[str, Any]:
    """Extract interpolated values from a Template as a dictionary.

    Pulls out every ``Interpolation`` and maps its source expression
    to its runtime value.  This is the machine-readable counterpart
    to :func:`render_message`.

    Parameters
    ----------
    template : Template
        A t-string ``Template`` object.

    Returns
    -------
    dict of {str : Any}
        Mapping of expression text to runtime value.
        Example: ``{"count": 143091, "path": "dictionaries/large"}``

    Examples
    --------
    >>> count = 143091
    >>> extract_values(t"Loaded {count} words")
    {'count': 143091}
    """
    values: dict[str, Any] = {}
    
    for item in template:
        match item:
            case Interpolation() as interp:
                #interp.expression is the source text: "count", "path.name", etc.
                values[interp.expression] = interp.value
                
    return values


# =============================================================================
# CUSTOM FORMATTER CLASSES
# =============================================================================

class TemplateMessageFormatter(logging.Formatter):
    """Formatter that renders Template objects as colored human text.

    Extends the same pattern as :class:`~speller.logger.ColoredFormatter`
    but adds Template awareness.  When ``record.msg`` is a ``Template``,
    it renders it via :func:`render_message` before the parent formats
    the timestamp and level.

    When ``record.msg`` is a plain ``str`` (normal log call), it falls
    through to standard ``Formatter`` behavior — fully backward compatible.

    Attributes
    ----------
    COLORS : dict of {int : str}
        ANSI color codes per log level (same as ColoredFormatter).
    RESET : str
        ANSI reset code.
    """
    
    COLORS: Final[dict[int, str]] = {
        logging.DEBUG:    "\033[90m",    # Gray
        logging.INFO:     "\033[92m",    # Green
        logging.WARNING:  "\033[93m",    # Yellow
        logging.ERROR:    "\033[91m",    # Red
        logging.CRITICAL: "\033[1;91m",  # Bold Red
    }
    RESET: Final[str] = "\033[0m"
    
    @override
    def format(self, record: logging.LogRecord) -> str:
        """Format a log record, rendering any Template to human text.

        The key insight: ``record.msg`` holds whatever was passed to
        ``logger.info()``.  If it's a Template, we render it BEFORE
        the parent class calls ``getMessage()`` (which would just
        call ``str()`` on it and lose the structured data).

        Parameters
        ----------
        record : logging.LogRecord
            The log record to format.

        Returns
        -------
        str
            Colored, human-readable log line.
        """
        # ─── Template-aware rendering ───
        # Check if the message is a Template BEFORE the parent processes it.
        # This is the interception point that t-strings enable.
        if isinstance(record.msg, Template):
            record.msg = render_message(record.msg)
            record.args = None # Clear args - already rendered
            
        color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"
    
    
