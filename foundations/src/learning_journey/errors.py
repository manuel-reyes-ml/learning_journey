""" """

from __future__ import annotations

from collections.abc import Mapping
from enum import IntEnum, unique
from typing import ClassVar


@unique
class ExitCode(IntEnum):
    """Process exit codes returned by every CLI in the repo.

    ``IntEnum`` members are plain integers, so ``sys.exit(ExitCode.NO_INPUT)``
    works directly. ``@unique`` rejects duplicate values when the class is defined.

    Attributes
    ----------
    SUCCESS : int
        0. The command finished normally.
    FAILURE : int
        1. Unexpected error, i.e. a bug.
    USAGE : int
        2. Invalid flags or arguments. Reserved for argparse, which already
        exits with 2; nothing else may use it.
    DATA_ERROR : int
        65 (``EX_DATAERR``). The input exists but its content is wrong.
    NO_INPUT : int
        66 (``EX_NOINPUT``). An input file is missing or unreadable.
    TEMP_FAIL : int
        75 (``EX_TEMPFAIL``). Temporary failure; retrying later may succeed,
        for example when another process holds a lock.
    INTERRUPTED : int
        130 (128 + SIGINT). The user pressed Ctrl-C.

    Notes
    -----
    0, 1 and 2 follow the common CLI convention. 64-78 come from BSD
    ``sysexits.h``, the closest thing to a standard for "why did it fail".
    """

    SUCCESS = 0
    FAILURE = 1
    USAGE = 2
    DATA_ERROR = 65
    NO_INPUT = 66
    TEMP_FAIL = 75
    INTERRUPTED = 130


class AppError(Exception):
    """Base class for failures the user can act on.

    Parameters
    ----------
    message : str
        One sentence saying what went wrong.
    hint : str or None, optional
        One sentence saying what to do next. Default is None (no hint).
    details : Mapping[str, object] or None, optional
        Key/value context. It is shown under the message and logged as
        separate fields, never merged into the message string. Default is None.

    Attributes
    ----------
    code : str
        Class-level, stable kebab-case id such as ``"input-not-found"``. It
        appears in the message and the log, so you can search and alert on it.
        Never reuse or rename a code.
    exit_code : ExitCode
        Class-level process exit code, so CI and shell scripts can branch on it.
    message : str
        The ``message`` argument.
    hint : str or None
        The ``hint`` argument.
    details : dict[str, object]
        A copy of the ``details`` argument (an empty dict if None).

    See Also
    --------
    InputNotFoundError : A required input file or directory is missing.
    DataContractError : The input breaks its header, type or row contract.
    ResourceBusyError : Another process holds the resource; retry later.

    Notes
    -----
    When a hint is given it is also attached with ``add_note`` (PEP 678,
    Python 3.11+). If the error ever escapes uncaught, the default traceback
    still prints the hint under the error line.

    Examples
    --------
    >>> err = DataContractError("bars.csv has no rows", hint="Regenerate it.")
    >>> err.exit_code
    <ExitCode.DATA_ERROR: 65>
    >>> err.log_fields()["error_code"]
    'data-contract-violation'
    """

    code: ClassVar[str] = "app-error"
    exit_code: ClassVar[ExitCode] = ExitCode.FAILURE  # TODO what it ClassVar

    def __init__(
        self,
        message: str,
        *,
        hint: str | None = None,
        details: Mapping[str, object] | None = None,  # TODO why Mapping here
    ) -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint
        self.details: dict[str, object] = dict(details or {})
        if hint:
            self.add_note(f"hint: {hint}")

    def log_fields(self) -> dict[str, object]:
        """Return the error as structured log fields.

        Returns
        -------
        dict[str, object]
            ``error_code``, ``error_type``, ``error`` and ``hint``, followed by
            every key in `details`. Each key becomes its own log field.
        """
        return {
            "error_code": self.code,
            "error_type": type(self).__name__,
            "error": self.message,
            "hint": self.hint,
            **self.details,
        }


class InputNotFoundError(AppError):
    """Raise when an input file or directory the command needs does not exist.

    Exits with `ExitCode.NO_INPUT`. Takes the same parameters as `AppError`.

    Attributes
    ----------
    code : str
        ``"input-not-found"``.
    exit_code : ExitCode
        `ExitCode.NO_INPUT` (66).
    """

    code: ClassVar[str] = "input-not-found"
    exit_code: ClassVar[ExitCode] = ExitCode.NO_INPUT


class DataContractError(AppError):
    """Raise when the input exists but breaks its contract.

    The contract covers the header, the column types and the row count. Exits
    with `ExitCode.DATA_ERROR`. Takes the same parameters as `AppError`.

    Attributes
    ----------
    code : str
        ``"data-contract-violation"``.
    exit_code : ExitCode
        `ExitCode.DATA_ERROR` (65).
    """

    code: ClassVar[str] = "data-contract-violation"
    exit_code: ClassVar[ExitCode] = ExitCode.DATA_ERROR


class ResourceBusyError(AppError):
    """Raise when another process holds a resource, such as a DuckDB file lock.

    Exits with `ExitCode.TEMP_FAIL`, which tells the caller a retry may succeed.
    Takes the same parameters as `AppError`.

    Attributes
    ----------
    code : str
        ``"resource-busy"``.
    exit_code : ExitCode
        `ExitCode.TEMP_FAIL` (75).
    """

    code: ClassVar[str] = "resource-busy"
    exit_code: ClassVar[ExitCode] = ExitCode.TEMP_FAIL
