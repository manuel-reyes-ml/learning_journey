"""
WAV Volume Changer - Modify audio file volume using a multiplication factor.

A command-line tool that reads a WAV audio file, multiplies each audio sample
by a user-specified factor, and writes the result to a new file. Handles
16-bit PCM audio with automatic clipping prevention.

How WAV Volume Adjustment Works
-------------------------------
1. Read the 44-byte WAV header (contains format info)
2. Read audio samples as 16-bit signed integers
3. Multiply each sample by the volume factor
4. Clamp values to [-32768, 32767] to prevent clipping
5. Write modified samples to output file

Usage
-----
    python volume.py FACTOR -i INPUT_FILE
    python volume.py FACTOR -i INPUT_FILE -o OUTPUT_FILE
    python volume.py FACTOR -i INPUT_FILE -d /path/to/directory
    python volume.py --verbose FACTOR -i INPUT_FILE

Examples
--------
    $ python volume.py 2 -i audio.wav
    14:30:45 : INFO : Success: Updated volume by factor of 2, from audio.wav to output.wav
    14:30:45 : INFO : Processed 44100 samples
    14:30:45 : INFO : Clipped 0 samples
    14:30:45 : INFO : Output file saved to -> 'output.wav'

    $ python volume.py 5 -i quiet.wav -o loud.wav
    14:31:00 : INFO : Success: Updated volume by factor of 5, from quiet.wav to loud.wav
    14:31:00 : INFO : Processed 88200 samples
    14:31:00 : INFO : Clipped 127 samples
    14:31:00 : INFO : Output file saved to -> 'loud.wav'

    $ python volume.py -v 3 -i audio.wav -d ~/Music
    14:32:15 : DEBUG : Verbose mode enabled
    14:32:15 : DEBUG : Searching input file in '/home/user/Music/audio.wav'....
    14:32:15 : DEBUG : Input file found......
    14:32:15 : DEBUG : Opening input and output file to update volume using factor 3....
    14:32:15 : DEBUG : Audio file header verified......
    14:32:15 : INFO : Success: Updated volume by factor of 3, from audio.wav to output.wav

Notes
-----
- Only 16-bit PCM WAV files are supported
- Factor of 0 and 1 are rejected (no change or silent output)
- Samples exceeding 16-bit range are clamped to prevent distortion
- Output file is saved in the same directory as input file by default
"""

from __future__ import annotations
from typing import Final, TypedDict
from pathlib import Path
import argparse
import struct
import logging
import sys


# =============================================================================
# Module Configuration
# =============================================================================

# Exports
__all__ = [
    "validate_input_file",
    "validate_output_file",
    "change_volume",
    "HEADER_SIZE",
    "SAMPLE_SIZE",
    "BIT_FORMAT",
    "FILE_EXT",
    "DATA_DIR",
]

# Program Constants
INT16_MIN: Final[int] = -32768
INT16_MAX: Final[int] = 32767
HEADER_SIZE: Final[int] = 44
SAMPLE_SIZE: Final[int] = 2
BIT_FORMAT: Final[str] = '<h'
FILE_EXT: Final[str] = ".wav"
OUT_FNAME: Final[str] = "output.wav"

# Use '__file__' for the actual file path
DATA_DIR: Final[Path] = Path(__file__).resolve().parent / "data"

# Exit codes (Unix standard)
EXIT_SUCCESS: Final[int] = 0
EXIT_FAILURE: Final[int] = 1
EXIT_KEYBOARD_INTERRUPT: Final[int] = 130

# Make a fix structure for a Dictionary, for Type checker to warn
# later on the program.
class VolumeChangeResult(TypedDict):
    """
    Statistics returned from volume change operation.

    Provides detailed metrics about the audio processing performed,
    including sample counts and the output file location.

    Attributes
    ----------
    bytes_processed : int
        Total number of bytes processed (excluding header).
    samples_processed : int
        Total number of audio samples processed.
    samples_clipped : int
        Number of samples that exceeded 16-bit range and were clamped.
    output_file : Path
        Path to the generated output file.

    Examples
    --------
    >>> result: VolumeChangeResult = {
    ...     "bytes_processed": 88200,
    ...     "samples_processed": 44100,
    ...     "samples_clipped": 15,
    ...     "output_file": Path("output.wav"),
    ... }
    >>> result["samples_clipped"]
    15
    """
    bytes_processed: int
    samples_processed: int
    samples_clipped: int
    output_file: Path
    
    # =============================================================================
    # TYPEDDICT QUICK REFERENCE
    # =============================================================================
    #
    # Basic syntax:
    #     class MyDict(TypedDict):
    #         key1: type1
    #         key2: type2
    #
    # All optional:
    #     class MyDict(TypedDict, total=False):
    #         key1: type1  # Optional
    #
    # Mixed (Python 3.11+):
    #     class MyDict(TypedDict, total=False):
    #         required_key: Required[str]
    #         optional_key: NotRequired[int]
    #
    # Mixed (Python 3.9-3.10):
    #     class _Required(TypedDict):
    #         must_have: str
    #     class MyDict(_Required, total=False):
    #         optional: int
    #
    # Key points:
    #     - Runtime type is just `dict`
    #     - Type checking is STATIC only (IDE/mypy)
    #     - No runtime validation
    #     - JSON serializable
    #     - Use for structured return values
    #
    # =============================================================================

# Inherits from Python's built-in Formatter
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
        message = super().format(record) # Call PARENT's format!
        
        # Step 3: Wrap with color codes
        return f"{color}{message}{self.RESET}"


# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handler with colored formatter
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter(
    fmt='%(asctime)s : %(levelname)s : %(message)s',
    datefmt='%H:%M:%S',
))
logger.addHandler(handler)


# =============================================================================
# Core Functions
# =============================================================================    

def validate_input_file(
    fname: str | None = None,
    input_dir: str | None = None,
    file_ext: str = FILE_EXT,
    data_dir: Path = DATA_DIR,
) -> Path:
    """
    Validate and locate the input audio file.

    Searches for the specified file in the given directory, current
    directory, or default data directory. Handles various extension
    cases and renames files to lowercase .wav if needed.

    Parameters
    ----------
    fname : str or None
        Name of the input file to validate.
    input_dir : str or None, optional
        Directory path to search for the file. If None, searches
        current directory and default data directory.
    file_ext : str, optional
        Expected file extension. Default is ".wav".
    data_dir : Path, optional
        Default directory to search if file not found elsewhere.

    Returns
    -------
    Path
        Validated path to the input file.

    Raises
    ------
    ValueError
        If fname is empty or None.
    FileNotFoundError
        If the file does not exist in any searched location.
    FileExistsError
        If the file exists but has an invalid extension (not WAV).

    Notes
    -----
    Search order:
    1. Specified input_dir (if provided)
    2. Current working directory (if file exists there)
    3. Default data directory

    If file has uppercase extension (.WAV, .Wav), it will be renamed
    to lowercase (.wav) on disk.

    Examples
    --------
    >>> validate_input_file("audio.wav")
    PosixPath('/home/user/project/data/audio.wav')
    >>> validate_input_file("audio.wav", input_dir="~/Music")
    PosixPath('/home/user/Music/audio.wav')
    >>> validate_input_file("")
    Traceback (most recent call last):
    ...
    ValueError: File name cannot be empty
    >>> validate_input_file("song.mp3")
    Traceback (most recent call last):
    ...
    FileExistsError: song.mp3 is not a valid WAV file
    """
    if not fname:
        raise ValueError("File name cannot be empty")
    
    # Convert the string into a Path object
    if input_dir:
        input_file = Path(input_dir).expanduser().resolve() / fname
    else:
        logger.debug("Not directory entered by user, searching in default directories....")
        input_file = Path(fname).resolve() if Path(fname).exists() else data_dir / fname
    
    logger.debug(f"Searching input file in '{input_file}'....")
    if input_file.is_file():
        
        # Check 1: File with the correct extension?
        # .suffix gets the extension (e.g. .Wav)
        if input_file.suffix == file_ext:
            return input_file
        
        # Check 2: It is already a WAV file (but maybe uppercase like .WaV)?
        elif input_file.suffix.lower() == file_ext:
            # .with_suffix automatically replaces the old extension with the new one
            new_input_file = input_file.with_suffix(file_ext)
            input_file.rename(new_input_file) # Rename file on disk
            
            return new_input_file
        
        # Check 3: Does it have not extension at all?
        elif input_file.suffix == "":
            new_input_file = input_file.with_suffix(file_ext)
            input_file.rename(new_input_file)
            
            return new_input_file
        
        # Check 4: It has an extension, but it´s  the wrong find (like .mp3)
        else:
            raise FileExistsError(f"{fname} is not a valid WAV file")
    else:
        raise FileNotFoundError(f"{fname} doesn't exists in directory '{input_file}'")

    # ==============================================================================
    # PATHLIB METHOD QUICK REFERENCE
    # How pathlib distinguishes between files, directories, and non-existent paths:
    # 
    # Assume for these examples: 
    # - "input.wav" is a real file that currently exists on the hard drive.
    # - "Music" is a real folder that currently exists on the hard drive.
    # - "fake.wav" is just a string in memory; it does not exist on the drive yet.
    #
    # | Method      | What it checks                         | input.wav | Music | fake.wav |
    # |-------------|----------------------------------------|-----------|-------|----------|
    # | .is_file()  | Is it a file AND does it exist?        | True      | False | False    |
    # | .is_dir()   | Is it a folder AND does it exist?      | False     | True  | False    |
    # | .exists()   | Does it exist at all (file OR folder)? | True      | True  | False    |
    # ==============================================================================


def validate_output_file(
    input_file: Path | None = None,
    fname: str = OUT_FNAME,
    file_ext: str = FILE_EXT,
) -> Path:
    """
    Generate and validate the output file path.

    Creates the output file path in the same directory as the input
    file, ensuring the correct file extension.

    Parameters
    ----------
    input_file : Path or None
        Path to the validated input file. Used to determine output directory.
    fname : str, optional
        Name for the output file. Default is "output.wav".
    file_ext : str, optional
        Required file extension. Default is ".wav".

    Returns
    -------
    Path
        Path where the output file will be saved.

    Raises
    ------
    ValueError
        If input_file is None or empty.

    Examples
    --------
    >>> input_path = Path("/home/user/Music/audio.wav")
    >>> validate_output_file(input_path)
    PosixPath('/home/user/Music/output.wav')
    >>> validate_output_file(input_path, fname="loud.wav")
    PosixPath('/home/user/Music/loud.wav')
    >>> validate_output_file(input_path, fname="result")
    PosixPath('/home/user/Music/result.wav')
    >>> validate_output_file(None)
    Traceback (most recent call last):
    ...
    ValueError: Input file path cannot be empty
    """
    if not input_file:
        raise ValueError("Input file path cannot be empty")
    
    logger.debug("Input file found......")
    file_path = input_file.parent
    
    output_file = file_path / fname
    
    if output_file.suffix != file_ext:
        output_file = output_file.with_suffix(file_ext)
    
    logger.debug(f"Saving output file in same directory '{output_file}'")
    return output_file


def _validate_factor(factor: str | None = None) -> int:
    """
    Argparse type validator for volume factor.

    Validates that the factor is a non-zero, non-one integer.
    Factor of 0 would create silent audio, factor of 1 makes no change.

    Parameters
    ----------
    factor : str or None
        Raw factor string from command line.

    Returns
    -------
    int
        Validated factor as integer.

    Raises
    ------
    argparse.ArgumentTypeError
        If factor is empty, non-numeric, zero, or one.

    Notes
    -----
    This is a private function used by argparse's type parameter.
    Negative factors are allowed (inverts the waveform).

    Examples
    --------
    >>> _validate_factor("2")
    2
    >>> _validate_factor("-3")
    -3
    >>> _validate_factor("0")
    Traceback (most recent call last):
    ...
    argparse.ArgumentTypeError: Factor cannot be 0 (would create silent audio)
    >>> _validate_factor("1")
    Traceback (most recent call last):
    ...
    argparse.ArgumentTypeError: Factor of 1 makes no change
    >>> _validate_factor("abc")
    Traceback (most recent call last):
    ...
    argparse.ArgumentTypeError: Factor must be numeric
    """ 
    if not factor:
        raise argparse.ArgumentTypeError("Factor cannot be empty")
    
    try:
        factor_int = int(factor.strip())
    except (ValueError, TypeError) as e:
        raise argparse.ArgumentTypeError("Factor must be numeric")
    
    if factor_int == 0:
        raise argparse.ArgumentTypeError("Factor cannot be 0 (would create silent audio)")
    
    if factor_int == 1:
        raise argparse.ArgumentTypeError("Factor of 1 makes no change")
    
    return factor_int


def _validate_wav_header(header:bytes, header_size: int = HEADER_SIZE) -> None:
    """
    Validate WAV file header contains required markers.

    Checks for "RIFF" marker at bytes 0-3 and "WAVE" marker at bytes 8-11,
    which are required for valid WAV files.

    Parameters
    ----------
    header : bytes
        Raw header bytes read from file (should be 44 bytes).
    header_size : int, optional
        Expected header size. Default is 44 bytes.

    Returns
    -------
    None
        Returns nothing if validation passes.

    Raises
    ------
    ValueError
        If header is too short or missing required markers.

    Notes
    -----
    WAV file structure (first 44 bytes):
    
    | Bytes | Content     | Description              |
    |-------|-------------|--------------------------|
    | 0-3   | "RIFF"      | File type marker         |
    | 4-7   | File size   | Size of file - 8 bytes   |
    | 8-11  | "WAVE"      | Format marker            |
    | 12-43 | Format data | Audio format details     |

    Examples
    --------
    >>> header = b'RIFF' + b'\\x00' * 4 + b'WAVE' + b'\\x00' * 32
    >>> _validate_wav_header(header)  # No error
    >>> _validate_wav_header(b'RIFF')
    Traceback (most recent call last):
    ...
    ValueError: Header too short: 4 bytes (need 44)
    >>> _validate_wav_header(b'\\x00' * 44)
    Traceback (most recent call last):
    ...
    ValueError: Not a valid WAV file: missing RIFF marker
    """
    if len(header) < header_size:
        raise ValueError(f"Header too short: {len(header)} bytes (need {header_size})")
    
    # WAV files start with "RIFF" and contain "WAVE"
    if header[0:4] != b"RIFF":
        raise ValueError("Not a valid WAV file: missing RIFF marker")
    
    if header[8:12] != b"WAVE":
        raise ValueError("Not a valid WAV file: missing WAVE marker")
    
    # =============================================================================
    # STRING PREFIXES QUICK REFERENCE
    # =============================================================================
    #
    # | Prefix | Type    | Escapes? | Variables? | Use Case                    |
    # |--------|---------|----------|------------|-----------------------------|
    # | ""     | str     | Yes      | No         | Normal text                 |
    # | r""    | str     | No       | No         | Regex, Windows paths        |
    # | b""    | bytes   | Yes      | No         | Binary files, network data  |
    # | f""    | str     | Yes      | Yes        | String formatting           |
    # | u""    | str     | Yes      | No         | Explicit Unicode (rare)     |
    # | rf""   | str     | No       | Yes        | Regex with variables        |
    # | rb""   | bytes   | No       | No         | Raw binary data             |
    #
    # Key Rules:
    #   - Binary mode (rb/wb) → use b"" for comparisons
    #   - Regex patterns → use r"" to avoid escape confusion
    #   - String formatting → use f"" for readability
    #   - Windows paths → use r"" or Path() from pathlib
    #
    # =============================================================================


def change_volume(
    input_file: Path | None = None,
    output_file: Path | None = None,
    factor: int | None = None,
    bit_format: str = BIT_FORMAT,
    header_size: int = HEADER_SIZE,
    sample_size: int = SAMPLE_SIZE,
    int16_min: int = INT16_MIN,
    int16_max: int = INT16_MAX,
) -> VolumeChangeResult:
    """
    Modify WAV file volume by multiplying samples by a factor.

    Reads a 16-bit PCM WAV file, multiplies each audio sample by the
    given factor, clamps values to prevent clipping, and writes the
    result to a new file.

    Parameters
    ----------
    input_file : Path or None
        Path to the input WAV file.
    output_file : Path or None
        Path where the modified file will be written.
    factor : int or None
        Multiplication factor for volume adjustment.
    bit_format : str, optional
        Struct format string for unpacking samples. Default is '<h'
        (little-endian signed 16-bit integer).
    header_size : int, optional
        Size of WAV header in bytes. Default is 44.
    sample_size : int, optional
        Size of each audio sample in bytes. Default is 2.
    int16_min : int, optional
        Minimum value for 16-bit signed integer. Default is -32768.
    int16_max : int, optional
        Maximum value for 16-bit signed integer. Default is 32767.

    Returns
    -------
    VolumeChangeResult
        Dictionary containing processing statistics:
        - bytes_processed: Total bytes processed
        - samples_processed: Number of audio samples
        - samples_clipped: Samples that were clamped
        - output_file: Path to output file

    Raises
    ------
    FileNotFoundError
        If input_file or output_file is None.
    ValueError
        If factor is None or file is empty or has invalid header.

    Notes
    -----
    Clipping occurs when a sample multiplied by the factor exceeds the
    16-bit signed integer range. Clipped samples are clamped to the
    nearest valid value to prevent audio distortion.

    The function uses struct.unpack/pack for binary conversion:
    - '<h' = little-endian signed short (2 bytes)
    - Values range from -32768 to 32767

    Examples
    --------
    >>> result = change_volume(
    ...     input_file=Path("audio.wav"),
    ...     output_file=Path("output.wav"),
    ...     factor=2,
    ... )
    >>> result["samples_processed"]
    44100
    >>> result["samples_clipped"]
    0
    """
    if not input_file or not output_file:
        raise FileNotFoundError("File(s) path cannot be empty")
    
    if not factor:
        raise ValueError("Factor cannot be empty")
    
    #Open files in "rb" (read binary) and "wb" (write binary) modes
    # Use context manager ('with...') to make sure connector to file is close after with block
    logger.debug(f"Opening input and output file to update volume using factor {factor}....")
    with open(input_file, "rb") as infile, open(output_file, "wb") as outfile:
        
        file_empty = True
        # 1. Read the exact 44-byte header and immediately write it to the new file
        header = infile.read(header_size)
        
        _validate_wav_header(header) # Validate header before processing
        logger.debug(f"Audio file header verified......")
        
        outfile.write(header)

        samples_clipped = 0
        samples_processed = 0
        count_bytes = 0
        
        # 2. Loop through the rest of the file, 2 bytes at a time
        while True:
            sample_bytes = infile.read(sample_size)
                
            # If we didn't get any bytes, we reached the end of the file
            if not sample_bytes:
                break
            
            file_empty = False
            count_bytes += 2
             
            # When you read a file in binary("rb"), Python doesn't see "numbers", it sees raw
            # hex bytes like '\xff\x10'.
                
            # 3. Unpack the 2 raw bytes into a Python integer
            # '<h' tells Python: "This is a Little-Endian, 16-bit signed integer (short)"
            # struct.unpack grabs those bytes and translates them into a human-readable math number(like -543)
            #   - struct.unpack always returns a tuple, because it is designed to unpack 
            #      multiple values at once (e.g., '<hhh' would return 3 integers). 
            #   - Even though we only ask for one value, it returns it like this: (453,)
            sample = struct.unpack(bit_format, sample_bytes)[0]
            samples_processed += 1
            
            # 4. Change the volume (multiply by factor)
            raw_sample = sample * factor
            
            # 5. Prevent Clipping (Clamp values to 16-bit limits)
            # In function - Pythonic clamping with max/min
            clamped = max(int16_min, min(int16_max, raw_sample))
            
            if clamped != raw_sample:
                samples_clipped += 1
            
            # 6. Pack the new integer back into 2 raw bytes and write it
            # struct.pack translates your math back into the raw machine bytes the WAV file expects
            new_sample_bytes = struct.pack(bit_format, clamped)
            outfile.write(new_sample_bytes)
                
        if file_empty:
            raise ValueError(f"File {input_file} is empty")
        
        logger.info(
            f"Success: Updated volume by factor of {factor}, from {input_file.name} to {output_file.name}"
        )
        
    return {
        "bytes_processed":   count_bytes,
        "samples_processed": samples_processed,
        "samples_clipped": samples_clipped,
        "output_file": output_file,
    }
        
        

# =============================================================================
# CLI Entry Point
# =============================================================================
    
def main(argv: list[str] | None = None) -> int:
    """
    Main entry point for the WAV volume changer CLI.

    Parses command-line arguments, validates input/output files,
    processes the audio, and reports results.

    Parameters
    ----------
    argv : list of str or None, optional
        Command-line arguments. If None, uses sys.argv.

    Returns
    -------
    int
        Exit code: 0 on success, 1 on validation/processing error,
        130 on keyboard interrupt.

    Examples
    --------
    >>> main(["2", "-i", "audio.wav"])
    0
    >>> main(["0", "-i", "audio.wav"])  # Factor 0 not allowed
    1
    """
    parser = argparse.ArgumentParser(
        description="Change volume of audio file using a factor from user"
    )
    # No need to add 'nargs' since it changes argument´s output automatically to a list, not single strings
    #   -> parser.add_argument("input_file", nargs=1)
    #   -> Returns a list -> ['input.wav']
    parser.add_argument(
        "-i", "--input-file",  # Standard: -i for short, --input-file for long
        type= str,
        help="Enter file name of input audio file",
    )
    parser.add_argument(
        "-o", "--output-file",
        type=str,
        default=OUT_FNAME,
        help=f"Enter file name of output audio file. Default if 'None': {OUT_FNAME}",
    )
    parser.add_argument(
        "factor",
        type=_validate_factor,
        help="Enter factor number to be used to update volume of audio file",
    )
    parser.add_argument(
        "-d", "--directory",
        type=str,
        help=f"Enter directory or Path to search for input audio file. Default is current directory or {DATA_DIR}"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (debug) output"
    )
    
    args = parser.parse_args(argv)
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")
     
    try:
        input_file = validate_input_file(args.input_file, args.directory)
        output_file = validate_output_file(input_file, args.output_file)
        
        result = change_volume(
            input_file,
            output_file, 
            args.factor,
        )
        
    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user. Exiting.")
        return EXIT_KEYBOARD_INTERRUPT
    
    except (FileExistsError, FileNotFoundError) as e:
        logger.error(f"Error in file: {e}")
        return EXIT_FAILURE
    
    except ValueError as e:
        logger.error(f"Error in processing: {e}")
        return EXIT_FAILURE
    
    except Exception as e:
        logger.exception(f"Unexpected Error: {e}")
        return EXIT_FAILURE
    
    logger.info(f"Processed {result['samples_processed']} samples")
    logger.info(f"Clipped {result['samples_clipped']} samples")
    logger.info(f"Output file saved to -> '{result['output_file']}'")
        
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())