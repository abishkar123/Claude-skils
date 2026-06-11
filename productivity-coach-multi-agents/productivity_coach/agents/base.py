"""Base agent: a thin wrapper around the Anthropic Messages API.

Each specialized agent is a system prompt plus optional pre/post hooks. Calls
stream and return the final message text so long plans don't hit HTTP
timeouts.
"""

import anthropic

from ..config import settings

_client = None


def client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


class BaseAgent:
    name = "base"
    system_prompt = ""

    def __init__(self, model: str | None = None):
        self.model = model or settings.model

    def run(self, user_input: str, context: str = "") -> str:
        """Send one request to Claude and return the text of the reply."""
        content = user_input if not context else f"{context}\n\n---\n\n{user_input}"
        with client().messages.stream(
            model=self.model,
            max_tokens=settings.max_tokens,
            thinking={"type": "adaptive"},
            output_config={"effort": settings.effort},
            system=[{
                "type": "text",
                "text": self.system_prompt,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": content}],
        ) as stream:
            message = stream.get_final_message()
        if message.stop_reason == "refusal":
            return "The model declined this request. Try rephrasing it."
        return "".join(b.text for b in message.content if b.type == "text")
