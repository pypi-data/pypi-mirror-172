"""
This module is part of the 'web-compressor' package,
which is released under GPL-3.0-only license.
"""

from .core import WebCompressor
from .handlers.hasher import Hasher
from .handlers.minifier import Minifier
from .handlers.optimizer import Optimizer

__all__ = [
    # Main class
    "WebCompressor",
    # Subclasses
    "Hasher",
    "Minifier",
    "Optimizer",
]
