"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
from logging.handlers import RotatingFileHandler
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final
import argparse
import logging
import random
import sys


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================

# =====================================================
# Exports
# =====================================================

# Controls: from 'module' import *
__all__ = []


# =====================================================
# Module Level Constants
# =====================================================

# For random selection and generations build up
ALLELES: Final[list[str]] = ['A', 'B', 'O']
DEFAULT_GEN_COUNT: Final[int] = 3

# For final output format
INDENT_LENGTH: Final[int] = 4


# =====================================================
# Random Generator
# =====================================================

# Production pattern: seed at the top
random.seed()  # Uses system entropy - different each run


# =====================================================
# Dataclasses
# ===================================================== 

@dataclass(frozen=True, slots=True)
class FileHandlerConfig:
    """
    """
    LEVEL_DEFAULT: Final[int] = logging.INFO
    ENCODING: Final[str] = "utf-8"
    BACKUP_COUNT: Final[int] = 3
    FILE_MB: Final[int] = 5      # megabytes
    MEGABYTE: Final[int] = 1024  # kilobytes
    KILOBYTE: Final[int] = 1024  # bytes
    
    @property
    def max_log_bytes(self) -> int:
        """
        """
        return self.FILE_MB * self.MEGABYTE * self.KILOBYTE


@dataclass(frozen=True, slots=True)
class FileDirectories:
    """
    """
    CUR_DIR: Final[Path] = Path(__file__).resolve().parent
    LOG_DIR: Final[Path] = CUR_DIR / "py_log"
    
    def create_log_fname(self) -> str:
        """
        """
        return f"{self.CUR_DIR.name}.log"
    
    @property
    def log_file(self) -> Path:
        """
        """
        return self.LOG_DIR / self.create_log_fname()
    

@dataclass
class Person:
    """
    """
    # Here, lambda is a zero-argument function that, when called,
    # creates and returns a fresh [None, None] list.
    # Each person always has two elements: Person (parents) or None slots
    parents: list[Person | None] = field(default_factory=lambda: [None, None])
    alleles: list[str] = field(default_factory=list)  # on each call creates emtpy list[]
    
    # ❌ DANGEROUS — every Person shares the SAME list object
    # parents: list[Person | None] = [None, None]

    # If you mutated one person's parents, every person's parents would change
    # because they all point to the same list in memory. This is the mutable default
    # argument trap — same pattern used in BMP filter work.

    # default_factory solves this by requiring a callable (a function). 
    # Every time a new Person is created, dataclasses calls that function
    # to produce a brand-new, independent list:
    #   Person A gets created → calls lambda → fresh [None, None]
    #   Person B gets created → calls lambda → different fresh [None, None]
    #   Person C gets created → calls lambda → another fresh [None, None]
    

# =====================================================
# Dataclass Instantiation
# =====================================================

fhandler_config = FileHandlerConfig()
file_dirs = FileDirectories()


# =====================================================
# Logging Configuration
# =====================================================

# Inherits from Python´s built-in Formatter
class ColoredFormatter(logging.Formatter):
    """
    Custom logging formatter that adds ANSI color codes based on log level.

    Inherits from Python's built-in logging.Formatter and overrides the
    format method to wrap log messages in terminal color codes.

    Attributes
    ----------
    COLORS : dict of {int: str}
        Mapping of logging level constants to ANSI color codes.
    RESET : str
        ANSI code to reset terminal color to default.

    Examples
    --------
    >>> handler = logging.StreamHandler()
    >>> handler.setFormatter(ColoredFormatter(
    ...     fmt='%(levelname)s : %(message)s'
    ... ))
    >>> logger.addHandler(handler)
    >>> logger.info("This appears in green")
    >>> logger.error("This appears in red")
    """
    # Color codes for each level
    COLORS: Final[dict[int, str]] = {
        logging.DEBUG:     "\033[90m",   # Gray
        logging.INFO:      "\033[92m",   # Green
        logging.WARNING:   "\033[93m",   # Yellow
        logging.ERROR:     "\033[91m",   # Red
        logging.CRITICAL:  "\033[1;91m", # Bold Red
    }
    RESET: Final[str] = "\033[0m"
    
    # Override the parent's format method
    def format(self, record) -> str:
        # Step 1: Get the color for this log level
        color = self.COLORS.get(record.levelno, self.RESET)
        
        # Step 2: Format the message normally first
        # This produces: "14:30:45 : INFO : Your message here"
        # super() calls PARENT's format() method
        message = super().format(record) 
        
        # Step 3: Wrap with color codes
        return f"{color}{message}{self.RESET}"
    

# Set up logging
# Move configuration into a setup function called by main()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Let handlers decide their own level!


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

def _config_logging(
    log_to_file: bool = True,
    console_verbose: bool = False,
    file_dirs: FileDirectories = file_dirs,
    fhandler_config: FileHandlerConfig = fhandler_config,
    formatter_class: type[logging.Formatter] = ColoredFormatter,
) -> None:
    """
    """
    # Prevent duplicate handlers if this function is
    # called multiple times (e.g. pytest).
    if logger.hasHandlers():
        logger.handlers.clear()
        
    level = logging.DEBUG if console_verbose else fhandler_config.LEVEL_DEFAULT
        
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter_class(
        fmt='%(asctime)s : %(levelname)s : %(message)s',
        datefmt='%H:%M:%S',
    ))
    
    if log_to_file:
        # parents=True: create any missing parent directories
        # exist_ok=True: no error if directory already exists
        file_dirs.LOG_DIR.mkdir(parents=True, exist_ok=True)
    
        file_handler = RotatingFileHandler(
            filename=file_dirs.log_file.name,  # .name returns only file name
            maxBytes=fhandler_config.max_log_bytes,
            backupCount=fhandler_config.BACKUP_COUNT,
            encoding=fhandler_config.ENCODING,
        )
        file_handler.setLevel(logging.DEBUG)
        # %(name)s shows module name (inheritance)
        file_handler.setFormatter(logging.Formatter(
            fmt='%(asctime)s : %(levelname)s : %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        ))
        logger.addHandler(file_handler)
    

def _random_allele(alleles: list[str] = ALLELES) -> str:
    """
    """
    # Picks one random element from the sequence
    return random.choice(alleles)


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def create_family(generations: int = DEFAULT_GEN_COUNT) -> Person:
    """
    """
    if generations <= 0:
        raise ValueError("Generations must be positive")
    
    person = Person()
    
    if generations == 1:
        # Oldest generation - no parents, random alleles
        person.alleles = [_random_allele(), _random_allele()]
        # parents already default to [None, None] - nothing to do
        
    else:
        parent_0 = create_family(generations - 1)
        
        parent_1 = create_family(generations -1)
    
        person.parents = [parent_0, parent_1]
        
        person.alleles = [
            _random_allele(parent_0.alleles),
            _random_allele(parent_1.alleles),
        ]
        
    return person