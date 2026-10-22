"""Day 29: first Claude API call — the moment the SDK era opens.

Install first:  uv add anthropic
(Runtime dependency — no --dev. Commit pyproject.toml + uv.lock together.)
"""

import anthropic

# The client reads ANTHROPIC_API_KEY from your environment automatically —
# which is WHY Step 8 put it in ~/.zshrc and never in code. If this line
# errors with "api_key not set", your env var isn't loaded (new terminal?).
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",  # model id — check docs for current names
    max_tokens=500,  # HARD CAP on response length. Always set it:
    # it is your cost + runaway guard.
    system=(  # the SYSTEM prompt sets persistent behavior —
        "You are a retirement-plan communications assistant. "
        "Explain concepts for plan participants: plain English, no jargon, "
        "4 sentences maximum."
    ),
    messages=[  # the conversation: a list of role+content turns
        {
            "role": "user",
            "content": "What does Box 7 code G on my 1099-R mean?",
        }
    ],
)

# response.content is a LIST of blocks (text, tool calls...). Text lives in .text:
print(response.content[0].text)

# The response also carries USAGE — tokens in/out. Log it from day one;
# cost-awareness is literally a heading in your README standard (Correction 18).
print(f"\ntokens: in={response.usage.input_tokens} out={response.usage.output_tokens}")
