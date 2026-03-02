"""
py_src — BMP image filter processing package.

Provides CLI and programmatic access to four image filters
(grayscale, reflect, blur, edges) for 24-bit BMP files.

Examples
--------
CLI usage::

    $ python -m py_src blur -i image.bmp

Programmatic usage::

    >>> from py_src import main
    >>> main(["blur", "-i", "image.bmp"])
"""
# Adding public API exports makes the pakacge more professional

from .bmp_main import main

__all__ = ["main"]
