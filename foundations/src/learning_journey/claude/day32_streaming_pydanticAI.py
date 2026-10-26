""" """

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
    from typing import Final, Literal

    from structlog.typing import FilteringBoundLogger

    from learning_journey.claude.settings import Settings

# structlog through Python's standard logging module, use structlog.stdlib.get_logger() instead.
# That function is already properly typed, so it needs no annotation.
log: FilteringBoundLogger = structlog.get_logger()

env_path = find_dotenv(usecwd=True, raise_error_if_not_found=True)
log.info(".env_found", file_path=env_path, values=list(dotenv_values(env_path)))

logfire.configure(send_to_logfire="if-token-present")
logfire.instrument_pydantic_ai()

MAX_BUBBLE: Final[float] = 0.6  # bubbles use at most 60% of terminal width

# Guardrail: cap tokens per run so a runaway reply can't burn budget.
# Raises UsageLimitExceeded when a limit is hit.
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


# Agent[None, str]: the two type parameters are the dependency type (none here)
# and the output type (str).
def build_agent(settings: Settings, system_prompt: str) -> Agent[None, str]:
    """ """
    model = AnthropicModel(
        settings.claude_model,
        provider=AnthropicProvider(
            api_key=settings.anthropic_api_key.get_secret_value(),
        ),
    )
    return Agent(
        model,
        output_type=str,  # plain-text chat; swap for a BaseModel later
        instructions=system_prompt,
        model_settings=ModelSettings(max_tokens=settings.default_max_tokens),
        name="direct_chat",
    )


def build_bubble(text: str, role: Literal["user", "assistant"]) -> Align:
    """ """
    is_user = role == "user"
    bubble = Panel(
        Text(text) if is_user else Markdown(text or "..."),  # render LLM replies as markdown
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
    """ """
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
    # Live has exited -> this printsBELOW the bubble
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
    """ """
    console.print(build_bubble(text, role))


async def main() -> int:
    """ """
    try:
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
        # console.input blocks; run it in a thread so the event loop stays free
        user_message = (await asyncio.to_thread(console.input, "[bold cyan]> [/]")).strip()
        if user_message.lower() in {"exit", "quit"}:
            break

        show_message(user_message, "user")

        # Order matters here. AuthenticationError and RateLimitError are subclasses
        # of APIStatusError, so they must come before it, or the general handler will
        # catch them first. Don't catch TypeError broadly to handle the missing key.
        # That would also hide real bugs in your code. The up-front check gives a
        # clearer message for portfolio-grade code.
        try:
            async with agent.run_stream(
                user_message,
                message_history=history,
                usage_limits=RUN_LIMITS,
            ) as run:
                await show_streaming_reply(run)
                history = run.all_messages()  # user turn + assistant turn now included
        except ModelHTTPError as e:  # 401, 429, 5xx... (subclass: catch first)
            log.error(
                "model_http_error",
                status_code=e.status_code,
                model=e.model_name,
                body=e.body,
            )
            return 1
        except ModelAPIError as e:  # other provider/API failures
            log.error("model_api_error", model=e.model_name, error=str(e))
            return 1
        except UsageLimitExceeded as e:  # your guardrail tripped
            log.warning("usage_limit_exceeded", error=str(e))
            return 1
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
    sys.exit(asyncio.run(main()))  # the one sync edge
