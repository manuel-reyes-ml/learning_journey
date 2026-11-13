""" """

from __future__ import annotations

import argparse
import uuid
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Final

import structlog
from rich.console import Console
from rich.text import Text

from learning_journey.errors import AppError, ExitCode
from learning_journey.logging_setup import get_logger

__all__ = [
    "add_observability_args",
    "print_error",
    "run",
]


out: Final[Console] = Console()
err: Final[Console] = Console(stderr=True)

log = get_logger("learning_journey.cli")


def _log_note(log_file: Path | None, run_id: str) -> str:
    """Build the ``note:`` line that points the user to the log record.

    Parameters
    ----------
    log_file : Path or None
        The ``--log-file`` path, or None if the run keeps no log file.
    run_id : str
        The id bound to every log event of this run.

    Returns
    -------
    str
        Where to find the details, or how to keep them next time.
    """
    if log_file is not None:
        return f"Details in {log_file} (run_id={run_id})"
    return f"Rerun with --log-file PATH to keep a structured record (run_id={run_id})."


def add_observability_args(parser: argparse.ArgumentParser) -> None:
    """Add the flags every script shares: ``-v``, ``--log-file`` and ``--traceback``.

    Parameters
    ----------
    parser : argparse.ArgumentParser
        The script's parser. The flags are added in place, under an
        "output and logging" group in ``--help``.

    See Also
    --------
    learning_journey.logging_setup.configure_logging : Consumes these flags.
    """
    group = parser.add_argument_group("output and logging")
    group.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Show log events on stderr: -v for INFO, -vv for DEBUG.",
    )
    group.add_argument(
        "--log-file",
        type=Path,
        metavar="PATH",
        help="Also write structured JSON logs (DEBUG and up) to PATH, appending.",
    )
    group.add_argument(
        "--traceback",
        action="store_true",
        help="On an unexpected error, also print the full traceback.",
    )


def print_error(
    message: str,
    *,
    code: str | None = None,
    details: Mapping[str, object] | None = None,
    hint: str | None = None,
    note: str | None = None,
) -> None:
    """Print an error to stderr in the style uv and pip use.

    Parameters
    ----------
    message : str
        One sentence saying what went wrong.
    code : str or None, optional
        Stable error id shown as ``error[code]``. Default is None (plain ``error``).
    details : Mapping[str, object] or None, optional
        Context printed as indented, aligned ``key: value`` lines. Default is None.
    hint : str or None, optional
        What to do next, printed after a ``hint:`` label. Default is None.
    note : str or None, optional
        Extra information, printed after a ``note:`` label. Default is None.

    Notes
    -----
    The lines are built from `rich.text.Text` pieces rather than Rich markup
    strings. Messages often contain square brackets (lists, paths) that Rich
    would otherwise read as style tags and swallow.

    ``soft_wrap=True`` stops Rich from inserting hard line breaks, so each line
    stays a single line in CI logs and when copied.

    Examples
    --------
    >>> print_error(
    ...     "bars_daily.csv does not match its column contract",
    ...     code="data-contract-violation",
    ...     details={"expected": "ticker, session_date", "found": "ticker, date"},
    ...     hint="Regenerate the seed files, then rerun this loader.",
    ... )  # doctest: +SKIP
    error[data-contract-violation]: bars_daily.csv does not match its column contract
      expected: ticker, session_date
      found:    ticker, date
    hint: Regenerate the seed files, then rerun this loader.
    """
    label = f"error[{code}]" if code else "error"
    err.print(Text.assemble((label, "bold red"), ": ", message), soft_wrap=True)
    if details:
        width = max(len(key) for key in details) + 1
        for key, value in details.items():
            err.print(
                Text.assemble(" ", (f"{key}:".ljust(width), "dim"), " ", str(value)),
                soft_wrap=True,
            )
    if hint:
        err.print(Text.assemble(("hint", "bold cyan"), ": ", hint), soft_wrap=True)
    if note:
        err.print(Text.assemble(("note", "bold"), ": ", note), soft_wrap=True)


def run(
    command: Callable[[], None],
    *,
    name: str,
    log_file: Path | None,
    show_traceback: bool,
) -> ExitCode:
    """Run a command inside the error boundary and return its exit code.

    This is the one place that turns exceptions into exit codes and messages.
    The command itself only raises; it never prints errors or calls
    ``sys.exit()``.

    Parameters
    ----------
    command : Callable[[], None]
        The work to do, with its arguments already bound (for example with
        `functools.partial`).
    name : str
        Command name, bound to every log event as ``command``.
    log_file : Path or None
        The ``--log-file`` path, used to tell the user where details are.
    show_traceback : bool
        On an unexpected error, also print a Rich traceback to stderr.

    Returns
    -------
    ExitCode
        `ExitCode.SUCCESS`; the error's own ``exit_code`` for an `AppError`;
        `ExitCode.INTERRUPTED` on Ctrl-C; `ExitCode.FAILURE` for anything else.

    See Also
    --------
    learning_journey.errors.AppError : Base class of the expected errors.

    Notes
    -----
    A random ``run_id`` is bound to the logging context for the whole run, so
    every event (ours and third-party) carries it. The user sees the same id
    in the ``note:`` line, which leads from the terminal to the matching lines
    in the log file.

    * Expected errors are logged at ERROR level without a traceback: their
      fields already describe the problem.
    * Unexpected errors are logged with ``log.exception``, which records the
      full traceback in the log file.
    """
    run_id = uuid.uuid4().hex[:12]
    with structlog.contextvars.bound_contextvars(run_id=run_id, command=name):
        log.debug("command_started")
        try:
            command()
        except AppError as exc:
            log.error("command_failed", exit_code=int(exc.exit_code), **exc.log_fields())
            print_error(
                exc.message,
                code=exc.code,
                details=exc.details,
                hint=exc.hint,
                note=_log_note(log_file, run_id),
            )
            return exc.exit_code
        except KeyboardInterrupt:
            log.warning("command_interrupted")
            err.print(Text.assemble(("aborted", "bold yellow"), ": interrupted by user."))
            return ExitCode.INTERRUPTED
        except Exception as exc:  # the boundary: a bug must never escape as a raw crash
            log.exception("command_crashed", error_type=type(exc).__name__, error=str(exc))
            print_error(
                f"Unexpected {type(exc).__name__}: {exc}",
                hint=None
                if show_traceback
                else "This looks like a bug, not a data problem. "
                "Rerun with --traceback to see where it failed.",
                note=_log_note(log_file, run_id),
            )
            if show_traceback:
                err.print_exception(show_locals=False)  # never print locals: PII
            return ExitCode.FAILURE

        log.info("command_succeeded")
        return ExitCode.SUCCESS
