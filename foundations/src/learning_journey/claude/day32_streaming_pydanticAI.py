"""Stream Claude replies into Rich chat bubbles with Pydantic AI.

Day 32 learning script: a terminal chat that streams each reply live inside
a Rich panel ("bubble"), keeps typed conversation history between turns, and
traces every run with Logfire when a token is configured.

Notes
-----
**Event loop.** One loop per thread schedules coroutines. It runs one piece
of Python at a time and switches to another task whenever the current one
waits on I/O. This gives concurrency, not parallelism, which suits LLM calls
because they are mostly waiting on the network.

**async def.** Defines a coroutine function. Calling it does not run its
body; it returns a coroutine object that must be awaited or handed to an
event loop.

**await.** Runs an awaitable and pauses only the current coroutine until it
finishes. The event loop stays free to run other tasks meanwhile.

**async with / async for.** A context manager whose enter and exit are
awaited, and a loop whose "get next item" step is awaited.

**asyncio.run(coro).** The single bridge from synchronous to asynchronous
code. It creates an event loop, runs ``coro`` to completion, shuts down
async generators and the default thread pool, closes the loop, and returns
the coroutine's result. It cannot be called while another loop is already
running in the same thread (Jupyter, FastAPI); there you ``await`` instead.

**asyncio.to_thread(func, *args).** Runs a blocking synchronous function
in a worker thread and returns an awaitable for its result, so the event
loop is not frozen while that function waits.

**Sync vs async rule.** A function is ``async`` only if it awaits
something. Builders and printers here do no I/O, so they are plain ``def``.
Anything that waits on the network or the keyboard is ``async def``.

**Pydantic AI layers.**

- ``AnthropicProvider``: who/where. Holds the API key and creates the
  ``AsyncAnthropic`` client (httpx2 transport) that sends HTTP requests.
- ``AnthropicModel``: how. Translates provider-neutral Pydantic AI messages
  into Claude Messages API requests and parses streamed events back.
- ``Agent``: what. Bundles model, instructions, model settings, output type
  and (later) tools. Built once, reused for every run.
- Run: one call to ``agent.run_stream``. Produces a ``StreamedRunResult``
  that exposes streamed text, usage and the updated message history.
- History: a list of typed ``ModelMessage`` objects (``ModelRequest`` /
  ``ModelResponse``) passed back in as ``message_history`` each turn.

References
----------
.. [1] Python docs, "Coroutines and Tasks",
   https://docs.python.org/3/library/asyncio-task.html
.. [2] Pydantic AI docs, "Agents",
   https://pydantic.dev/docs/ai/core-concepts/agent/
.. [3] Pydantic AI API, "pydantic_ai.result",
   https://pydantic.dev/docs/ai/api/pydantic-ai/result/
"""

# Makes ALL annotations lazy strings (PEP 563). That is why `Final` and `Literal`
# can be imported only under TYPE_CHECKING below and still be used in annotations:
# Python never evaluates them at runtime, only type checkers (mypy/pyright) read them.
from __future__ import annotations

import asyncio
import sys
from typing import TYPE_CHECKING

import logfire
import structlog
from dotenv import dotenv_values, find_dotenv
from pydantic_ai import Agent
from pydantic_ai.exceptions import (
    ModelAPIError,
    ModelHTTPError,
    UnexpectedModelBehavior,
    UsageLimitExceeded,
)
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.result import StreamedRunResult
from pydantic_ai.settings import ModelSettings
from pydantic_ai.usage import UsageLimits
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from learning_journey.claude.client import get_client
from learning_journey.claude.settings import ConfigError

if TYPE_CHECKING:
    # Only imported while type-checking; zero runtime cost (see __future__ note above).
    from typing import Final, Literal

    from structlog.typing import FilteringBoundLogger

    from learning_journey.claude.settings import Settings

# structlog through Python's standard logging module, use structlog.stdlib.get_logger() instead.
# That function is already properly typed, so it needs no annotation.
log: FilteringBoundLogger = structlog.get_logger()

# dotenv_values() only READS .env into a dict; it does NOT put values into os.environ.
env_path = find_dotenv(usecwd=True, raise_error_if_not_found=True)
log.info(".env_found", file_path=env_path, values=list(dotenv_values(env_path)))

# Plain sync calls: they register config and hooks, no network I/O.
# "if-token-present": export spans only when LOGFIRE_TOKEN is set; otherwise a no-op.
logfire.configure(send_to_logfire="if-token-present")
# Every Agent run becomes an "agent run" span with nested model-call spans.
logfire.instrument_pydantic_ai()

MAX_BUBBLE: Final[float] = 0.6  # bubbles use at most 60% of terminal width

# Per-run guardrails; breaching one raises UsageLimitExceeded.
# output_tokens_limit is checked after each response; request_limit before each
# model call (stops tool-call loops once tools exist).
RUN_LIMITS: Final[UsageLimits] = UsageLimits(output_tokens_limit=2_000, request_limit=3)

console = Console()

rpc_prompt: str = (
    "You are a retirement-plan communications assistant. "
    "Explain concepts for plan participants: plain English, no jargon, "
    "2 sentences maximum."
)

sleep_trainer_prompt: str = (
    "You are an expert baby sleep trainer. "
    "Explain concepts for parents: plain English, no jargon, "
    "2 sentences maximum."
)


def build_agent(settings: Settings, system_prompt: str) -> Agent[None, str]:
    """Build the reusable chat agent for Claude.

    Parameters
    ----------
    settings : Settings
        Validated app settings. Supplies the model name, the API key
        (``SecretStr``) and the default ``max_tokens``.
    system_prompt : str
        Instructions sent to the model on every request of every run.

    Returns
    -------
    Agent[None, str]
        Agent with no dependency type (``None``) and plain-text output
        (``str``). The generic parameters let type checkers verify
        ``run.output`` and tool signatures.

    See Also
    --------
    pydantic_ai.Agent.run_stream : Starts one streamed run of this agent.

    Notes
    -----
    Synchronous on purpose: constructing the provider, model and agent
    performs no I/O; the first network call happens inside ``run_stream``.
    Build it once and reuse it, like a FastAPI app. ``instructions`` are
    taken from the agent on every request rather than read back from the
    saved history, so changing them affects the next run immediately.
    """
    model = AnthropicModel(
        settings.claude_model,
        provider=AnthropicProvider(
            api_key=settings.anthropic_api_key.get_secret_value(),
        ),
    )
    return Agent(
        model,
        output_type=str,  # swap for a Pydantic BaseModel to get validated structured output
        instructions=system_prompt,
        # Provider-neutral; Pydantic AI maps it to Anthropic's max_tokens.
        model_settings=ModelSettings(max_tokens=settings.default_max_tokens),
        name="direct_chat",  # label in the startup banner and in Logfire traces
    )


def build_bubble(text: str, role: Literal["user", "assistant"]) -> Align:
    """Build one chat bubble as a Rich renderable.

    Parameters
    ----------
    text : str
        Message body. User text is shown verbatim; assistant text is
        rendered as Markdown.
    role : {"user", "assistant"}
        Controls title, border colour and alignment.

    Returns
    -------
    rich.align.Align
        Panel aligned right for the user and left for the assistant,
        capped at ``MAX_BUBBLE`` of the terminal width.
    """
    is_user = role == "user"
    bubble = Panel(
        Text(text) if is_user else Markdown(text or "..."),  # placeholder before 1st token
        title="You" if is_user else "Assistant",
        title_align="right" if is_user else "left",
        border_style="cyan" if is_user else "green",
        expand=False,  # shrink-wrap short messages
    )

    return Align(
        bubble,
        align="right" if is_user else "left",
        width=int(console.width * MAX_BUBBLE),
    )


async def show_streaming_reply(run: StreamedRunResult[None, str]) -> str:
    """Render a streamed reply live inside a bubble, then log usage.

    Parameters
    ----------
    run : StreamedRunResult[None, str]
        The open run yielded by ``agent.run_stream``. Must be consumed
        while its ``async with`` block is still open.

    Returns
    -------
    str
        The complete reply text.

    Raises
    ------
    ValueError
        If the stream finished without producing any text.

    Notes
    -----
    Asynchronous because each ``async for`` step awaits the next batch of
    tokens from the network.

    ``stream_text()`` with its default ``delta=False`` yields the full text
    received so far (not just the new chunk), grouped roughly every 0.1 s
    by ``debounce_by``. A bubble that re-renders its whole content needs
    exactly that.

    Rich ``Live`` is a synchronous context manager used inside a coroutine.
    That is safe: entering, updating and exiting it are instant, and Rich
    repaints from its own background thread. Sync code inside async code is
    only a problem when it blocks.

    ``run.usage`` is a property, complete only once the stream has finished,
    so it is read after the ``Live`` block.
    """
    reply = ""

    # The pattern: you construct a Live object with a renderable,
    # use it as a context manager, and can swap the renderable
    # on the fly by calling update()
    with Live(
        build_bubble("", "assistant"),
        console=console,
        refresh_per_second=12,
    ) as live:
        async for reply in run.stream_text():  # async iteration
            live.update(build_bubble(reply, "assistant"))

    usage = run.usage
    # Printed after Live exits, so it lands below the finished bubble.
    log.info(
        "message_received",
        tokens_in=usage.input_tokens,
        tokens_out=usage.output_tokens,
        requests=usage.requests,
        cost_usd=str(usage.cost),  # best-effort estimate; None if model not priced
    )
    if not reply:
        raise ValueError("Stream produced no text")
    return reply


def show_message(text: str, role: Literal["user", "assistant"]) -> None:
    """Print a static (non-streaming) bubble.

    Parameters
    ----------
    text : str
        Message body.
    role : {"user", "assistant"}
        Bubble style; see ``build_bubble``.
    """
    console.print(build_bubble(text, role))


async def main() -> int:
    """Run the interactive chat loop.

    Returns
    -------
    int
        Process exit code: ``0`` on a normal exit (``exit``/``quit``),
        ``1`` on configuration or model errors.

    See Also
    --------
    build_agent : Builds the agent reused by every turn.
    show_streaming_reply : Renders each streamed reply.

    Notes
    -----
    One turn of the loop:

    1. ``await asyncio.to_thread(console.input, ...)`` reads the prompt in a
       worker thread; ``main`` pauses until Enter is pressed.
    2. Entering ``async with agent.run_stream(...)`` builds the request
       (instructions + ``history`` + new prompt), checks ``request_limit``,
       sends it through ``AsyncAnthropic`` and waits until Claude starts
       streaming the answer. That wait is the time to first token.
    3. ``await show_streaming_reply(run)`` streams the text into the bubble.
    4. ``run.all_messages()`` returns the previous history plus this turn and
       becomes ``history`` for the next turn.
    5. Exiting the ``async with`` block finalizes the run (closes the stream,
       records usage and messages, ends the Logfire span), even on error.

    Exception handlers are matched top to bottom, so subclasses come first:
    ``ModelHTTPError`` (has ``status_code``) is a subclass of
    ``ModelAPIError``. Pydantic AI wraps the Anthropic SDK's own errors
    (authentication, rate limit, server) into these provider-neutral types.
    """
    try:
        # TODO: also builds a sync anthropic client that is never used here.
        # A small get_settings() helper would avoid creating it.
        _client, settings = get_client()
        log.info("key_accepted", api_key=settings.anthropic_api_key.get_secret_value()[-4:])
    except ConfigError as e:
        # log.exception(event="") produces the full traceback for deeper analysis
        log.error("config_error", error=e)  # clean one-line exit, no traceback
        return 1

    print("=" * 70)
    print("Chat with LLM Program -- type 'exit' or 'quit' to end the program.")
    print("=" * 70)

    system_prompt = sleep_trainer_prompt + settings.system_prompt
    agent = build_agent(settings, system_prompt)
    history: list[ModelMessage] = []

    while True:
        print("\n")
        # REVIEW: Ctrl+C here cancels main(), but the worker thread stays blocked in
        # input(), so shutdown may wait until Enter is pressed. Harmless for a CLI.
        user_message = (await asyncio.to_thread(console.input, "[bold cyan]> [/]")).strip()
        if user_message.lower() in {"exit", "quit"}:
            break

        show_message(user_message, "user")

        # Don't catch TypeError broadly to handle a missing key: it would also hide
        # real bugs. The up-front ConfigError check gives a clearer message.
        try:
            async with agent.run_stream(
                user_message,
                message_history=history,
                usage_limits=RUN_LIMITS,
            ) as run:
                await show_streaming_reply(run)
                # Reassign, don't append: keeps history exactly what Pydantic AI saw.
                history = run.all_messages()  # user turn + assistant turn now included
        except ModelHTTPError as e:  # 401, 429, 5xx... (subclass: catch first)
            log.error(
                "model_http_error",
                status_code=e.status_code,
                model=e.model_name,
                body=e.body,  # provider error body; look here for the request id
            )
            return 1
        except ModelAPIError as e:  # network and other non-HTTP provider failures
            log.error("model_api_error", model=e.model_name, error=str(e))
            return 1
        except UsageLimitExceeded as e:  # your guardrail tripped
            # `continue` keeps the chat alive; history is unchanged,
            # so the user can simply rephrase.
            log.warning("usage_limit_exceeded", error=str(e), correction="rephrase_prompt")
            continue
        except UnexpectedModelBehavior as e:  # malformed/empty model output
            log.error("unexpected_model_behavior", error=str(e))
            return 1
        except ValueError as e:
            log.error("stream_error", error=e)
            return 1

    print("=" * 30)
    print("Program finished. Thanks :)")
    print("=" * 30)

    return 0


if __name__ == "__main__":
    # asyncio.run returns main()'s int; sys.exit turns it into the exit code.
    sys.exit(asyncio.run(main()))
