"""Privacy state per session: connector authorizations and taint terms.

Even without live MCP connectors, the taint registry is enforced on the
knowledge-search path: any draft search query containing a registered
private term (or an email address) is rejected before it would ever leave
the system, and the incident is logged.
"""

import re
from dataclasses import dataclass, field

_EMAILISH = re.compile(r"[\w.+-]+@[\w-]+\.\w+")


@dataclass
class PrivacyState:
    authorized_connectors: set[str] = field(default_factory=set)
    taint_terms: set[str] = field(default_factory=set)
    incidents: list[str] = field(default_factory=list)

    def register_taint(self, terms: list[str]) -> None:
        self.taint_terms.update(t.strip().lower() for t in terms if t.strip())

    def check_query(self, query: str) -> str | None:
        """Return a rejection reason if the query is tainted, else None."""
        if _EMAILISH.search(query):
            return "email address in search query"
        lowered = query.lower()
        for term in self.taint_terms:
            if term and term in lowered:
                return f"registered private term in search query: '{term}'"
        return None
