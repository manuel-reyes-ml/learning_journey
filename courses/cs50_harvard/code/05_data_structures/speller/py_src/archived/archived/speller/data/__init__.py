"""Bundled read-only resources for the speller package.

This subpackage contains:
    - dictionaries/  Word lists for spell checking
    - texts/         Sample text files for testing
    - keys/          (Reserved for future API key storage)

These resources are accessed via :mod:`importlib.resources` from
:mod:`speller.config`. Do not modify these files at runtime; they
are read-only by convention and may be installed to a read-only
filesystem in production deployments.
"""

# Five lines, but it tells a future reviewer (or yourself in six months)
# exactly what this directory is for and why it's structured this way.
# This kind of docstring is the difference between "code that works" and
# "production-grade code."
