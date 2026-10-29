""" """

from __future__ import annotations

import sys
from collections.abc import Generator
from typing import TYPE_CHECKING

import anthropic
import structlog
from dotenv import dotenv_values, find_dotenv
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from learning_journey.claude.client import get_client
from learning_journey.claude.settings import ConfigError

if TYPE_CHECKING:
    from typing import Literal

    from anthropic.types import Message, MessageParam
    from structlog.typing import FilteringBoundLogger

    from learning_journey.claude.settings import Settings

# structlog through Python's standard logging module, use structlog.stdlib.get_logger() instead.
# That function is already properly typed, so it needs no annotation.
log: FilteringBoundLogger = structlog.get_logger()

env_path = find_dotenv(usecwd=True, raise_error_if_not_found=True)
log.info(".env_found", file_path=env_path, values=list(dotenv_values(env_path)))


console = Console()
MAX_BUBBLE: float = 0.6  # bubbles use at most 60% of terminal width


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


def add_user_message(messages: list[MessageParam], text: str) -> None:
    """ """
    user_message: MessageParam = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages: list[MessageParam], text: str) -> None:
    """ """
    assistant_message: MessageParam = {"role": "assistant", "content": text}
    messages.append(assistant_message)


# Becomes a generator that yields text deltas. It knows nothing about Rich,
# so the API logic stays separate from the UI.
# Before: stream_chat only yielded text, so -> Iterator[str] was the right, minimal type.
#   Iterator is the protocol: any object with __iter__ and __next__. Generator is a function
#   with yield that Python turns into an iterator automatically.
# After: it also returns the final Message, so -> Generator[YieldType, SendType, ReturnType]
#   is required. Here str is what it yields, None means you never .send() into it,
#   and Message is what it returns.
def stream_chat(
    messages: list[MessageParam],
    system_prompt: str,
    *,
    client: anthropic.Anthropic,
    settings: Settings,
) -> Generator[str, None, Message]:
    """ """
    params = {
        "model": settings.claude_model,
        "max_tokens": settings.default_max_tokens,
        "messages": messages,
        "system": system_prompt,
    }

    with client.messages.stream(**params) as stream:
        yield from stream.text_stream
        return stream.get_final_message()  # becomes StopIteration.value


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


def show_streaming_reply(chunks: Generator[str, None, Message]) -> str:
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
        while True:
            try:
                chunk = next(chunks)
            except StopIteration as stop:
                final: Message = stop.value  # the returned Message
                break
            reply += chunk
            live.update(build_bubble(reply, "assistant"))

    # Live has exited -> this printsBELOW the bubble
    log.info(
        "message_received",
        tokens_in=final.usage.input_tokens,
        tokens_out=final.usage.output_tokens,
        stop_reason=final.stop_reason,
    )
    if not reply:
        raise ValueError("Stream produced no text")
    return reply


def show_message(text: str, role: Literal["user", "assistant"]) -> None:
    """ """
    console.print(build_bubble(text, role))


def main() -> int:
    """ """
    try:
        client, settings = get_client()
        log.info("key_accepted", api_key=settings.anthropic_api_key.get_secret_value()[-4:])
    except ConfigError as e:
        # log.exception(event="") produces the full traceback for deeper analysis
        log.error("config_error", error=e)  # clean one-line exit, no traceback
        return 1

    print("=" * 70)
    print("Chat with LLM Program -- type 'exit' or 'quit' to end the program.")
    print("=" * 70)

    messages: list[MessageParam] = []
    system_prompt = sleep_trainer_prompt + settings.system_prompt

    while True:
        print("\n")
        user_message = console.input("[bold cyan]> [/]").strip()
        if user_message.lower() in {"exit", "quit"}:
            break

        show_message(user_message, "user")
        add_user_message(messages, user_message)

        # Order matters here. AuthenticationError and RateLimitError are subclasses
        # of APIStatusError, so they must come before it, or the general handler will
        # catch them first. Don't catch TypeError broadly to handle the missing key.
        # That would also hide real bugs in your code. The up-front check gives a
        # clearer message for portfolio-grade code.
        try:
            answer = show_streaming_reply(
                stream_chat(messages, system_prompt, client=client, settings=settings)
            )
        except anthropic.APIStatusError as e:  # any other non-2xx
            log.error(
                "anthropic_api_error",  # 401, 429, 5xx, ...
                error_type=type(e).__name__,  # "RateLimitError", "AuthenticationError", etc..
                status_code=e.status_code,
                request_id=e.request_id,  # include this in support tickets
                message=e.message,
            )
            return 1
        except anthropic.APIConnectionError as e:  # network / timeout
            log.error("anthropic_connection_error", error_type=type(e).__name__, message=e.message)
            return 1
        except ValueError as e:
            log.error("stream_error", error=e)
            return 1
        except Exception as e:
            log.error("other_error", error=e)
            return 1

        add_assistant_message(messages, answer)

    print("=" * 30)
    print("Program finished. Thanks :)")
    print("=" * 30)

    return 0


if __name__ == "__main__":
    sys.exit(main())
