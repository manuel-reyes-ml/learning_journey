"""
Package entry point for ``python -m py_src``.

Delegates immediately to ``main()`` in ``bmp_main`` to keep
the entry point minimal and all logic in one place.

Usage
-----
::

    $ python -m py_src blur -i image.bmp
    $ python -m py_src all -i image.bmp -v
    $ python -m py_src grayscale edges -i photo.bmp -d ~/pictures/
"""

import sys

from .bmp_main import main

sys.exit(main())