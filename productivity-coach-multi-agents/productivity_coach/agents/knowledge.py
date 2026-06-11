"""Knowledge and Search Agent.

Only generic, sanitized queries ever reach this agent. There is no live
search dependency here: if a search MCP/tool is wired in by the host, it can
be injected via `search_fn`; otherwise the agent answers from general
knowledge and labels resources "not verified as current".
"""

from typing import Callable, Optional

from .. import prompts
from ..privacy import PrivateQueryError, sanitize_search_query
from .base import BaseAgent


class KnowledgeAgent(BaseAgent):
    name = "knowledge"
    system_prompt = prompts.KNOWLEDGE

    def __init__(self, search_fn: Optional[Callable[[str], str]] = None, **kw):
        super().__init__(**kw)
        self.search_fn = search_fn

    def run(self, user_input: str, context: str = "") -> str:
        try:
            query = sanitize_search_query(user_input)
        except PrivateQueryError as e:
            return (
                f"Search blocked ({e}). Private content never goes into search "
                "queries. Manual fallback: rephrase as a generic topic, e.g. "
                "'<technology> best practices 2026', and ask again."
            )
        if self.search_fn is not None:
            results = self.search_fn(query)
            context = f"Search query used: {query}\nSearch results:\n{results}"
            return super().run(user_input, context)
        return super().run(
            user_input,
            context=(
                "No live search tool is available. Answer from general "
                f"knowledge. The sanitized query would have been: {query!r}. "
                "Label each recommended resource 'not verified as current'."
            ),
        )
