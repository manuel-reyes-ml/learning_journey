""" """

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import anthropic
import structlog
from anthropic.types import Message, TextBlock
from dotenv import dotenv_values, find_dotenv
from rich.align import Align
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from structlog.typing import FilteringBoundLogger

from learning_journey.claude.client import get_client
from learning_journey.claude.settings import ConfigError

if TYPE_CHECKING:
    from typing import Literal

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


def add_user_message(messages: list[dict[str, str]], text: str) -> None:
    """ """
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages: list[dict[str, str]], text: str) -> None:
    """ """
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def chat(
    messages: list[dict[str, str]],
    system_prompt: str,
    *,
    client: anthropic.Anthropic,
    settings: Settings,
) -> TextBlock:
    """ """
    params = {
        "model": settings.claude_model,
        "max_tokens": settings.default_max_tokens,
        "messages": messages,
        "system": system_prompt,
    }

    message: Message = client.messages.create(**params)
    log.info(
        "messaged_received",
        tokens_in=message.usage.input_tokens,
        tokens_out=message.usage.output_tokens,
        blocks=[*message.content],
    )

    for block in message.content:
        if isinstance(block, TextBlock):
            return block
    raise ValueError("No text block was found in message object")


def show_message(text: str, role: Literal["user", "assistant"]) -> None:
    """ """
    is_user = role == "user"
    bubble = Panel(
        Text(text) if is_user else Markdown(text),  # render LLM replies as markdown
        title="You" if is_user else "Assitant",
        title_align="right" if is_user else "left",
        border_style="cyan" if is_user else "green",
        expand=False,  # shrink-wrap short messages
    )
    console.print(
        Align(
            bubble,
            align="right" if is_user else "left",
            width=int(console.width * MAX_BUBBLE),
        )
    )


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

    messages: list[dict[str, str]] = []
    system_prompt = sleep_trainer_prompt + settings.system_prompt

    while True:
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
            answer = chat(messages, system_prompt, client=client, settings=settings)
        except anthropic.AuthenticationError as e:  # 401: bad key
            log.error("bad_key", error=e)
            return 1
        except anthropic.RateLimitError as e:  # 429
            log.error("rate_limit", error=e)
            return 1
        except anthropic.APIStatusError as e:  # any other non-2xx
            log.error("other_api_error", error=e.response, code=e.status_code)
            return 1
        except anthropic.APIConnectionError as e:  # network
            log.error("bad_network", error=e)
            return 1
        except ValueError as exc:
            log.error("chat_error", error=exc)
            return 1
        except Exception as exc:
            log.error("other_error", error=exc)
            return 1

        show_message(answer.text, "assistant")
        add_assistant_message(messages, answer.text)

    print("=" * 30)
    print("Program finished. Thanks :)")
    print("=" * 30)

    return 0


if __name__ == "__main__":
    sys.exit(main())
