"""LLM provider layer: paid OpenAI model + free Groq model.

Groq exposes an OpenAI-compatible API, so both providers share the
AsyncOpenAI client — only base_url, key, and model differ. If the Groq key
is missing, Groq-assigned roles transparently fall back to OpenAI (and
vice versa) so the system degrades instead of crashing.
"""

import logging
from functools import lru_cache

from openai import AsyncOpenAI

from .config import GROQ_BASE_URL, Provider, settings

log = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def _client(provider: Provider) -> AsyncOpenAI:
    if provider == "groq":
        return AsyncOpenAI(api_key=settings.groq_api_key, base_url=GROQ_BASE_URL)
    return AsyncOpenAI(api_key=settings.openai_api_key)


def _resolve(provider: Provider) -> tuple[Provider, str]:
    """Pick (provider, model), falling back if the requested key is absent."""
    if provider == "groq" and not settings.groq_api_key:
        log.warning("GROQ_API_KEY missing — falling back to OpenAI")
        provider = "openai"
    if provider == "openai" and not settings.openai_api_key:
        if settings.groq_api_key:
            log.warning("OPENAI_API_KEY missing — falling back to Groq")
            provider = "groq"
        else:
            raise RuntimeError("No LLM API key configured (OPENAI_API_KEY / GROQ_API_KEY)")
    model = settings.groq_model if provider == "groq" else settings.openai_model
    return provider, model


async def complete(
    provider: Provider,
    system: str,
    messages: list[dict],
    *,
    temperature: float = 0.4,
    max_tokens: int = 4096,
    json_mode: bool = False,
) -> str:
    """One chat completion. `messages` are prior {role, content} turns."""
    provider, model = _resolve(provider)
    kwargs: dict = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = await _client(provider).chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[{"role": "system", "content": system}, *messages],
        **kwargs,
    )
    return response.choices[0].message.content or ""
