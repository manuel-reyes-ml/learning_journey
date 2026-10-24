""" """

from __future__ import annotations

import sys
from typing import Literal

import anthropic
import structlog
from anthropic import Anthropic
from anthropic.types import Message, TextBlock
from dotenv import dotenv_values, find_dotenv
from rich.align import Align
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from structlog.typing import FilteringBoundLogger

from learning_journey.claude.settings import settings

# structlog through Python's standard logging module, use structlog.stdlib.get_logger() instead.
# That function is already properly typed, so it needs no annotation.
log: FilteringBoundLogger = structlog.get_logger()

env_path = find_dotenv(usecwd=True, raise_error_if_not_found=True)
log.info(".env_found", file_path=env_path, values=list(dotenv_values(env_path)))

# Reads that file and copies each pair into os.environ, the environment of
# the running Python process only. It does not change your OS, your shell,
# or other programs.
#
# Walks up parent folders and stops at the first .env it finds.
# load_dotenv()

# if not os.getenv("ANTHROPIC_API_KEY"):
#    raise RuntimeError("ANTHROPIC_API-KEY not set - check your .env location")

# key = os.environ.get("ANTHROPIC_API_KEY", "")
# if not key.startswith("sk-ant-"):
#     log.error("bad_key", key_starts_with=key[:7])
#     raise ValueError(
#         f"ANTHROPIC_API_KEY looks malformed (starts with {key[:7]!r}, length {len(key)}). "
#         "Re-copy it from the Console with the copy button."
#     )

console = Console()
MAX_BUBBLE: float = 0.6  # bubbles use at most 60% of terminal width

client = Anthropic(api_key=settings.anthropic_api_key.get_secret_value())
log.info("key_accepted", api_key=settings.anthropic_api_key.get_secret_value()[-4:])

system: str = (
    "You are a retirement-plan communications assistant. "
    "Explain concepts for plan participants: plain English, no jargon, "
    "2 sentences maximum."
    "You are chatting in a terminal. Reply conversationally in short plain-text "
    "paragraphs, like a text message. No headings, bullet lists, bold, or tables "
    "unless the user asks for them."
)


def add_user_message(messages: list[dict[str, str]], text: str) -> None:
    """ """
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages: list[dict[str, str]], text: str) -> None:
    """ """
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def chat(messages: list[dict[str, str]], system: str | None = None) -> TextBlock:
    """ """
    params = {
        "model": settings.claude_model,
        "max_tokens": settings.default_max_tokens,
        "messages": messages,
    }
    if system:
        params["system"] = system

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
    print("=" * 70)
    print("Chat with LLM Program -- type 'exit' or 'quit' to end the program.")
    print("=" * 70)
    messages: list[dict[str, str]] = []

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
            answer = chat(messages, system=system)
        except anthropic.AuthenticationError as e:  # 401: bad key
            log.error("bad_key", exception=e)
            return 1
        except anthropic.RateLimitError as e:  # 429
            log.error("rate_limit", exception=e)
            return 1
        except anthropic.APIStatusError as e:  # any other non-2xx
            log.error("other_api_error", exception=e.response, code=e.status_code)
            return 1
        except anthropic.APIConnectionError as e:  # network
            log.error("bad_network", exception=e)
            return 1
        except ValueError as exc:
            log.error("chat_error", exception=exc)
            return 1
        except Exception as exc:
            log.error("other_error", exception=exc)
            return 1

        show_message(answer.text, "assistant")
        add_assistant_message(messages, answer.text)

    print("=" * 30)
    print("Program finished. Thanks :)")
    print("=" * 30)
    return 0


if __name__ == "__main__":
    sys.exit(main())
