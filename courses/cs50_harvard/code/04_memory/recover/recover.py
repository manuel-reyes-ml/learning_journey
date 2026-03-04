"""
Recover JPEG images from a raw forensic memory card image.

A Python reimplementation of the CS50 pset4 "Recover" problem,
refactored to production-grade standards with full type safety,
structured logging, and CLI support.

The module reads a binary memory card dump block-by-block (512 bytes),
detects JPEG SOI (Start of Image) signatures, and writes each
recovered image to a separate file.

Usage
-----
Command-line::

    python recover.py -i card.raw
    python recover.py -i card.raw -d /path/to/dir --auto-rename -v

As a library::

    from recover import validate_infile, recover_jpeg
    infile = validate_infile("card.raw")
    result = recover_jpeg(infile)

Notes
-----
- JPEG signatures are detected by matching the first 4 bytes of each
  512-byte block against the SOI marker: ``0xFF 0xD8 0xFF 0xE0-0xEF``.
- Images are written to a ``recovered/`` subdirectory with
  zero-padded filenames (e.g., ``image_001.jpeg``).
- Original CS50 problem: https://cs50.harvard.edu/x/2024/psets/4/recover/

Author
------
Manuel (GitHub: @manuelreyes-ml)

Version
-------
1.0.0
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations  # Must be at the beginning of the file
from logging.handlers import RotatingFileHandler
from typing import Final, NamedTuple, TypedDict
from dataclasses import dataclass
from enum import IntEnum, unique
from pathlib import Path
import argparse
import logging
import struct
import sys


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================

# =====================================================
# Exports
# =====================================================

# Controls: 'from module import *'
__all__ = [
    # Core functions
    "validate_infile",
    "generate_outfile",
    "recover_jpeg",
    # Types (needed by consumers of recover_jpeg's return value)
    "JPEGRecoverResult",
    "ImageVariables",
    "ExitCode",
    # Configuration (useful for custom workflows)
    "FileDirectories",
    "FileName",
    "ImageData",
    # Module-level constants
    "MIN_BLOCK_SIZE",
    "KB_PER_BYTE",
    "BLOCK_SIZE",
]


# =====================================================
# Module Level Constants
# ===================================================== 

# For I/O configuration
MIN_BLOCK_SIZE: Final[int] = 4
KB_PER_BYTE: Final[int] = 1024
BLOCK_SIZE: Final[int] = 512

# For file_handler configuration
MAX_LOG_BYTES: Final[int] = 5 * 1024 * 1024
BACKUP_COUNT: Final[int] = 3
LOG_FNAME: Final[str] = "recover.log"
LEVEL_DEFAULT: Final[int] = logging.INFO


# =====================================================
# Type Aliases
# =====================================================

type ImagesReport = dict[str, ImageVariables]


# =====================================================
# Dataclass Frozen Constants
# ===================================================== 

# Directories
@dataclass(frozen=True, slots=True)
class FileDirectories:
    """
    Immutable container for directory paths used during recovery.

    All paths are resolved relative to the module file location,
    ensuring consistent behavior regardless of the working directory.

    Attributes
    ----------
    CUR_DIR : Path
        Absolute path to the directory containing this module.
    INPUT_DIR : Path
        Default directory to search for raw memory card files.
    OUT_DIR : Path
        Default directory where recovered JPEG files are written.

    Examples
    --------
    >>> dirs = FileDirectories()
    >>> dirs.INPUT_DIR.name
    'memory_card'
    >>> dirs.OUT_DIR.name
    'recovered'
    """
    CUR_DIR: Final[Path] = Path(__file__).resolve().parent
    INPUT_DIR: Final[Path] = CUR_DIR / "memory_card"
    OUT_DIR: Final[Path] = CUR_DIR / "recovered"
    LOG_DIR: Final[Path] = CUR_DIR / "py_log"

# File information
@dataclass(frozen=True, slots=True)
class FileName:
    """
    Immutable container for file naming conventions.

    Attributes
    ----------
    INFILE_EXT : str
        Expected extension for raw memory card input files.
    OUTFILE_EXT : str
        Extension applied to recovered JPEG output files.
    OUT_FNAME : str
        Prefix for recovered image filenames (e.g., ``image_001.jpeg``).

    Examples
    --------
    >>> fn = FileName()
    >>> fn.OUTFILE_EXT
    '.jpeg'
    """
    INFILE_EXT: str = ".raw"
    OUTFILE_EXT: str = ".jpeg"
    OUT_FNAME: str = "image_"  # complete during file writing


# =====================================================
# Dataclass Instantiation
# =====================================================

# Following PEP 8 standars, name of an instance should be lowercase,
# unless it is a global constant itself.
file_directories = FileDirectories()
filename = FileName()


# =====================================================
# Other Class Configuration
# =====================================================

# JPEG Image information
class ImageData(IntEnum):
    """
    JPEG SOI (Start of Image) marker bytes and bitmask.

    The first three bytes of a JPEG file are always ``0xFF 0xD8 0xFF``.
    The fourth byte ranges from ``0xE0`` to ``0xEF``; the bitmask
    ``0xF0`` isolates the upper nibble for comparison.

    Attributes
    ----------
    BYTE_0 : int
        First SOI byte (``0xFF``).
    BYTE_1 : int
        Second SOI byte (``0xD8``).
    BYTE_2 : int
        Third SOI byte (``0xFF``).
    BYTE_3 : int
        Fourth SOI byte lower bound (``0xE0``).
    BITS_MASK : int
        Bitmask for the fourth byte (``0xF0``), matching range
        ``0xE0``-``0xEF``.

    Examples
    --------
    >>> hex(ImageData.BYTE_0)
    '0xff'
    >>> hex(ImageData.BITS_MASK)
    '0xf0'
    """
    BYTE_0 = 0xff
    BYTE_1 = 0xd8
    BYTE_2 = 0xff
    BYTE_3 = 0xe0
    BITS_MASK = 0xf0  # Mask for 4th byte range (0xe0-0xef)
    
# Exit codes (Unix standard)
@unique  # Ensure no duplicate values
class ExitCode(IntEnum):
    """
    Process exit codes following Unix conventions.

    Attributes
    ----------
    SUCCESS : int
        Normal termination (0).
    FAILURE : int
        General error (1).
    KEYBOARD_INTERRUPT : int
        Terminated by Ctrl+C (130).
    """
    SUCCESS = 0
    FAILURE = 1
    KEYBOARD_INTERRUPT = 130
    
class ByteSignature(NamedTuple):
    """
    First four bytes of a block, used for JPEG signature detection.

    Parameters
    ----------
    byte_0 : int
        First byte of the block.
    byte_1 : int
        Second byte of the block.
    byte_2 : int
        Third byte of the block.
    byte_3 : int
        Fourth byte of the block.

    Examples
    --------
    >>> sig = ByteSignature(0xff, 0xd8, 0xff, 0xe0)
    >>> sig.byte_0 == 0xff
    True
    """
    byte_0: int
    byte_1: int
    byte_2: int
    byte_3: int

# TypedDict makes a fix structure for a Dictionary,
# for Type checker to warn later on the program.
class ImageVariables(TypedDict):
    """
    Per-image metadata stored in the recovery report.

    Attributes
    ----------
    kb_size : float
        Size of the recovered image in kilobytes.
    """
    kb_size: float

class JPEGRecoverResult(TypedDict):
    """
    Structured result returned by :func:`recover_jpeg`.

    Attributes
    ----------
    images_recovered : int
        Total number of JPEG images found and written.
    images_details : ImagesReport
        Mapping of filename to :class:`ImageVariables` with size info.
    output_file : Path or None
        Directory where recovered images were saved, or ``None``
        if no images were recovered.
    """
    images_recovered: int
    images_details: ImagesReport  # Nested dictionary
    output_file: Path | None
    

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
    
    # Override the parent´s format method
    def format(self, record) -> str:
        # Step 1: Get the color for this log level 
        color = self.COLORS.get(record.levelno, self.RESET)
        
        # Step 2: Format the message normally first
        # This produces: "14:30:45 : INFO : Your message here"
        message = super().format(record)  # Call PARENT's format!
        
        # Step 3: Wrap with color codes
        return f"{color}{message}{self.RESET}"
    

# Set up logging
# Move configuration into a setup function called by main()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Let handlers decide their own level


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

def _build_outfile_path(
    out_fname: str | None = None,
    out_dir: Path = file_directories.OUT_DIR,
) -> Path:
    """
    Construct a full output file path, creating the directory if needed.

    Parameters
    ----------
    out_fname : str or None
        The output filename (e.g., ``"image_001.jpeg"``).
    out_dir : Path, optional
        Target directory for the output file
        (default: ``FileDirectories.OUT_DIR``).

    Returns
    -------
    Path
        Full resolved path to the output file.

    Raises
    ------
    ValueError
        If ``out_fname`` is an empty string.
    TypeError
        If ``out_fname`` is not a string.

    Examples
    --------
    >>> path = _build_outfile_path("image_001.jpeg")
    >>> path.name
    'image_001.jpeg'
    """
    if out_fname == "":
        raise ValueError("out_fname cannot be empty")
    
    if not isinstance(out_fname, str):
        raise TypeError(f"out_fname must a string. Got '{type(out_fname)}'")
    
    if not out_dir.exists():
        out_dir.mkdir(parents=True, exist_ok=True)
    
    return out_dir / out_fname


def _is_jpeg_start(
    buffer: ByteSignature | None = None,
    byte_0: int = ImageData.BYTE_0,
    byte_1: int = ImageData.BYTE_1,
    byte_2: int = ImageData.BYTE_2,
    byte_3: int = ImageData.BYTE_3,
    bits_mask: int = ImageData.BITS_MASK,
) -> bool:
    """
    Check if a 4-byte signature matches the JPEG SOI marker.

    Compares the first three bytes exactly and applies a bitmask
    to the fourth byte to match the range ``0xE0``-``0xEF``.

    Parameters
    ----------
    buffer : ByteSignature or None
        Named tuple containing the first 4 bytes of a block.
    byte_0 : int, optional
        Expected first byte (default: ``0xFF``).
    byte_1 : int, optional
        Expected second byte (default: ``0xD8``).
    byte_2 : int, optional
        Expected third byte (default: ``0xFF``).
    byte_3 : int, optional
        Expected fourth byte after masking (default: ``0xE0``).
    bits_mask : int, optional
        Bitmask applied to the fourth byte (default: ``0xF0``).

    Returns
    -------
    bool
        ``True`` if bytes match the JPEG SOI signature.

    Raises
    ------
    ValueError
        If ``buffer`` is ``None`` or empty.

    Examples
    --------
    >>> sig = ByteSignature(0xff, 0xd8, 0xff, 0xe1)
    >>> _is_jpeg_start(sig)
    True
    >>> sig = ByteSignature(0x00, 0x00, 0x00, 0x00)
    >>> _is_jpeg_start(sig)
    False
    """
    if not buffer: 
        raise ValueError("Buffer cannot be empty")
    
    return (
        buffer.byte_0 == byte_0 and
        buffer.byte_1 == byte_1 and
        buffer.byte_2 == byte_2 and
        (
            buffer.byte_3 & 
            bits_mask
        ) == byte_3
    )
    
    
def _configure_logging(
    log_to_file: bool = True,
    console_verbose: bool = False,
    level: int = LEVEL_DEFAULT,
    log_fname: str = LOG_FNAME,
    max_bytes: int = MAX_LOG_BYTES,
    backup_count: int = BACKUP_COUNT,
    logs_dir: Path = file_directories.LOG_DIR,
    formatter_class: type[logging.Formatter] = ColoredFormatter,
) -> None:
    """
    Configure console logging with colored output.

    Sets up a :class:`StreamHandler` with :class:`ColoredFormatter`.
    Checks for existing handlers to prevent duplicates when
    ``main()`` is called multiple times (e.g., in tests).

    Parameters
    ----------
    verbose : bool, optional
        If ``True``, set log level to ``DEBUG``; otherwise ``INFO``
        (default: ``False``).

    Examples
    --------
    >>> _configure_logging(verbose=True)
    >>> logger.level == logging.DEBUG
    True
    """
    level = logging.DEBUG if console_verbose else level
    
    # Prevent duplicate handlers if this function is called multiple times (e.g. pytest)
    if logger.hasHandlers():
        logger.handlers.clear()
    
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter_class(
        fmt='%(asctime)s : %(levelname)s : %(message)s',
        datefmt='%H:%M:%S',
    ))
    logger.addHandler(console_handler)
    
    if log_to_file:
        # parents=True: create any missing parent directories
        # exist_ok=True: no error if directory already exists
        logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = logs_dir / log_fname
        
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        # %(name)s shows module name (recover)
        file_handler.setFormatter(logging.Formatter(
            fmt='%(asctime)s : %(levelname)s : %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        ))
        logger.addHandler(file_handler)
    

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def validate_infile(
    fname: str | None = None,
    input_dir: Path | str | None = None,
    auto_rename: bool = False,
    infile_ext: str = filename.INFILE_EXT,
    default_dir: Path = file_directories.INPUT_DIR,
) -> Path:
    """
    Validate and resolve the input memory card file path.

    Locates the file in the given or default directory, verifies it
    exists, and checks the file extension. Optionally renames files
    with non-standard extensions (e.g., ``.RaW`` or missing extension).

    Parameters
    ----------
    fname : str or None
        Name of the input file (e.g., ``"card.raw"``).
    input_dir : Path, str, or None, optional
        Directory to search for the file. If ``None``, searches the
        current working directory first, then ``default_dir``.
    auto_rename : bool, optional
        If ``True``, automatically rename files with incorrect or
        missing extensions to ``infile_ext`` (default: ``False``).
    infile_ext : str, optional
        Required file extension (default: ``".raw"``).
    default_dir : Path, optional
        Fallback directory when ``input_dir`` is not provided
        (default: ``FileDirectories.INPUT_DIR``).

    Returns
    -------
    Path
        Validated absolute path to the input file.

    Raises
    ------
    ValueError
        If ``fname`` is ``None``, empty, or has an invalid extension.
    FileNotFoundError
        If the file does not exist in the resolved directory.

    Examples
    --------
    >>> path = validate_infile("card.raw")
    >>> path.suffix
    '.raw'
    >>> path = validate_infile("card.RAW", auto_rename=True)
    >>> path.suffix
    '.raw'
    """
    if not fname:
        raise ValueError("File name cannot be empty")
    
    if input_dir:
        if not isinstance(input_dir, Path):
            input_dir = Path(input_dir)
        input_dir = input_dir.expanduser().resolve()
        in_file = input_dir / fname
    else: 
        logger.debug("Not directory entered by user, searching in default directory....")
        in_file = Path(fname).resolve() if Path(fname).exists() else default_dir / fname
    
    if in_file.is_file():
        
        # Check 1: File with correct extension?
        # .suffix gets the extension (.raw)
        if in_file.suffix == infile_ext:
            return in_file
        
        # Check 2: It is already a RAW file (but maybe uppercase like .RaW or not extension)?
        elif in_file.suffix.lower() == infile_ext or in_file.suffix == "":
            if auto_rename:
                logger.debug(
                    f"Auto-renaming file {in_file.name} to {in_file.with_suffix(infile_ext).name}"
                )
                new_in_file = in_file.with_suffix(infile_ext)
                in_file.rename(new_in_file)
                # .name returns just file name ('card.raw')
                logger.info(f"File name updated successfully to {new_in_file.name}")
                return new_in_file
            else:
                # Multiple lines using f-strings for readability
                logger.warning(f"File '{in_file.name}' has non-standard extension. "
                                   f"Use auto-rename=True to fix.") 
                return in_file
        else:
            raise FileExistsError(f"{fname} is not a valid '{infile_ext}' file")
    else:
        raise FileNotFoundError(f"{fname} doesn't exist in directory '{in_file}'")
# BEFORE — validate_infile does TWO jobs:
# Job 1: Validate a file path (logic)
# Job 2: Ask a human what to do (user interaction)

# PRODUCTION PATTERN — each layer handles its own job:

#  main()           → Handles ALL user interaction (argparse, prompts)
#  validate_infile  → Handles ONLY validation logic
#  recover_jpeg     → Handles ONLY recovery logic

# The "decision" flows DOWN as a parameter, not UP as an input() call


def generate_outfile(
    image_counter: int | str | None = None,
    file_ext: str = filename.OUTFILE_EXT,
    fname: str = filename.OUT_FNAME,
) -> Path:
    """
    Generate a zero-padded output file path for a recovered image.

    Constructs a filename like ``image_001.jpeg`` from the counter
    value, then delegates to :func:`_build_outfile_path` for
    directory creation and path resolution.

    Parameters
    ----------
    image_counter : int, str, or None
        Sequence number for the image. Strings must contain only
        digits (leading/trailing whitespace is stripped).
    file_ext : str, optional
        File extension for the output (default: ``".jpeg"``).
    fname : str, optional
        Filename prefix (default: ``"image_"``).

    Returns
    -------
    Path
        Full path to the output file (e.g.,
        ``recovered/image_001.jpeg``).

    Raises
    ------
    TypeError
        If ``image_counter`` is not an ``int`` or ``str``.
    ValueError
        If ``image_counter`` is empty or contains non-digit characters.

    Examples
    --------
    >>> generate_outfile(1).name
    'image_001.jpeg'
    >>> generate_outfile("42").name
    'image_042.jpeg'
    """
    # If its any other Type than 'int' or 'str' (eg. None, float)
    if not isinstance(image_counter, (int, str)):
        raise TypeError(f"image_count must be an integer or string. Got '{type(image_counter)}'")
    
    # If its empty
    if image_counter == "":
        raise ValueError("image_counter cannot be empty")
    
    if isinstance(image_counter, str):
        if not image_counter.strip().isdigit(): 
            raise ValueError("image_counter string must only contain digits")   

        image_counter = int(image_counter.strip())

    out_fname = f"{fname}{image_counter:03}{file_ext}"
        
    return _build_outfile_path(out_fname)
    
        
def recover_jpeg(
    infile: Path | None = None,
    block_size: int = BLOCK_SIZE,
    kb_per_byte: int = KB_PER_BYTE,
    min_block_size: int = MIN_BLOCK_SIZE,
) -> JPEGRecoverResult:
    """
    Recover JPEG images from a raw forensic memory card image.

    Reads a binary file block-by-block, detecting JPEG SOI signatures
    (``0xFF 0xD8 0xFF 0xE0-0xEF``) at block boundaries and writing
    each image to a separate output file. Uses ``try/finally`` to
    guarantee file handle cleanup even on unexpected errors.

    Parameters
    ----------
    infile : Path or None
        Path to the raw memory card image file.
    block_size : int, optional
        Number of bytes per read block (default: 512).
    kb_per_byte : int, optional
        Divisor for converting bytes to kilobytes (default: 1024).
    min_block_size : int, optional
        Minimum buffer length required for signature detection
        (default: 4). Blocks shorter than this are written to the
        current image (if open) and terminate the read loop.

    Returns
    -------
    JPEGRecoverResult
        Dictionary containing:

        - **images_recovered** (*int*) -- Total number of JPEGs found.
        - **images_details** (*ImagesReport*) -- Per-image file sizes
          in KB, keyed by filename.
        - **output_file** (*Path or None*) -- Directory where images
          were saved.

    Raises
    ------
    ValueError
        If ``infile`` is ``None`` or the file contains no JPEG data.

    Examples
    --------
    >>> from pathlib import Path
    >>> result = recover_jpeg(Path("memory_card/card.raw"))
    >>> result["images_recovered"]
    50
    >>> result["images_details"]["image_001.jpeg"]["kb_size"]
    42.5
    """
    if not infile:
        raise ValueError("Input file cannot be empty")
    
    with open(infile, "rb") as inputf:
        
        kbytes: float = 0.0
        image_counter: int = 0
        out_filename = None
        output_dir = None
        out_handler = None
        images_result: ImagesReport = {}
        
        try:
            while True:
                buffer: bytes = inputf.read(block_size)
                
                if not buffer:
                    break
                
                if len(buffer) < min_block_size:  # Guard if buffer is less than signature (4 bytes)
                    if out_handler:
                        # Ensure remaining bytes are being written to image file
                        out_handler.write(buffer) 
                    break
                
                b0, b1, b2, b3 = struct.unpack("<BBBB", buffer[0:4])
                signature = ByteSignature(b0, b1, b2, b3)
                
                # Check if the block is the start of a new JPEG
                if _is_jpeg_start(signature): 
                    #If we were already writing a file, close it
                    if out_handler:
                        # .tell() returns the current position of the file pointer in bytes
                        kbytes = out_handler.tell() / kb_per_byte
                        out_handler.close()
                        
                        if out_filename:
                            images_result[out_filename.name] = ImageVariables(kb_size=kbytes)
                    
                    # Open a new file to start writing
                    image_counter += 1
                    out_filename = generate_outfile(image_counter)
                    out_handler = open(out_filename, "wb")
                    
                    # Write the start of the image
                    out_handler.write(buffer)
                
                # If it´s not a new JPEG start, but we have a file open, keep writing
                elif out_handler:
                    out_handler.write(buffer)
        
        finally:
            # Ensure the file is closed even if an error occurs
            # finally always executes - error or no error
            # Close the last file if one was open        
            if out_handler:
                kbytes = out_handler.tell() / kb_per_byte
                out_handler.close()
                
                if out_filename:
                    images_result[out_filename.name] = ImageVariables(kb_size=kbytes)
                    output_dir = out_filename.parent
            
    if not images_result:
        raise ValueError(f"{infile.name} is empty")
    
    return {
        "images_recovered": image_counter,
        "images_details": images_result,
        "output_file": output_dir,
    }

    
# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main(argv: list[str] | None = None)-> ExitCode:
    """
    CLI entry point for JPEG recovery from memory card images.

    Parses command-line arguments, validates the input file,
    runs the recovery process, and prints a summary report.

    Parameters
    ----------
    argv : list of str or None, optional
        Command-line arguments. If ``None``, reads from
        ``sys.argv`` (default: ``None``).

    Returns
    -------
    ExitCode
        ``SUCCESS`` (0) on normal completion, ``FAILURE`` (1) on
        error, or ``KEYBOARD_INTERRUPT`` (130) if terminated by user.

    Examples
    --------
    From the command line::

        $ python recover.py -i card.raw
        $ python recover.py -i card.raw -d ./data --auto-rename -v

    Programmatic usage (e.g., in tests)::

        >>> exit_code = main(["-i", "card.raw", "-v"])
        >>> exit_code == ExitCode.SUCCESS
        True
    """
    parser = argparse.ArgumentParser(
        description="Recover all images from memory card file, with"
                    f" {filename.OUTFILE_EXT} extension signature"
    )
    parser.add_argument(
        "-i", "--input-file",  # Short and long flag arguments (optional)
        required=True,
        type=str,
        help=f"Enter memory card file, format '{filename.INFILE_EXT}'",
    )
    parser.add_argument(
        "-o", "--output-file",
        type=str,
        help=f"Enter desired prefix for output. Default: '{filename.OUT_FNAME}'",
    )
    parser.add_argument(
        "-d", "--directory",
        type=str,
        help="Enter directory path to search for input file." 
             f"Default: '{file_directories.INPUT_DIR}'"
    )
    parser.add_argument(
        "--auto-rename",
        action="store_true",
        help="Automatically rename input file to standard extension"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (debug) output",
    )
    parser.add_argument(
        "--no-log-file",
        action="store_true",
        help="Disable file logging (console only)"
    )
    
    args = parser.parse_args(argv)
    
    # Logging configured HERE, not on import 
    _configure_logging(
        console_verbose=args.verbose,
        log_to_file=not args.no_log_file,
    )
    
    if args.verbose:
        logger.debug("Verbose mode enabled (console debug output)")
        
    try:
        input_file = validate_infile(
            args.input_file,
            args.directory,
            auto_rename=args.auto_rename)
        
        report: JPEGRecoverResult = recover_jpeg(input_file)
        
    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user. Exiting.")
        return ExitCode.KEYBOARD_INTERRUPT
    
    except (FileExistsError, FileNotFoundError) as e:
        logger.error(f"File Error: {e}")
        return ExitCode.FAILURE
    
    except (ValueError, TypeError, struct.error) as e:  # struct.error is for unpacking errors
        logger.error(f"Processing Error: {e}")
        return ExitCode.FAILURE
    
    except Exception as e: 
        logger.exception(f"Unexpected Error: {e}")  # Behaves like .error but includes TraceBack info
        return ExitCode.FAILURE
    
    
    # Print out report using logging
    logger.info(f"Recovered {report['images_recovered']} images from file")
    
    for image, size in report["images_details"].items():
        logger.info(f"Name: {image}, Size: {size['kb_size']} KB")
        
    logger.info(f"All images are saved in: '{report['output_file']}'\n")
    
    return ExitCode.SUCCESS
    
    
if __name__ == "__main__":
    sys.exit(main())