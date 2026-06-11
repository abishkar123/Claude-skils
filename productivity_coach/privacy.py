"""Privacy guards: search-query sanitization and the session permission ledger.

Hard rule: private personal, employer, email, document, calendar, or database
content must never be sent into internet search queries. The sanitizer is a
gate, not a scrubber — if a query looks private, it is rejected rather than
"cleaned up" and sent anyway.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"\+?\d[\d\s().-]{7,}\d")
URL_WITH_PATH_RE = re.compile(r"https?://\S+/\S+")

# Words that suggest the query embeds private/workplace content.
PRIVATE_MARKERS = (
    "my manager", "my boss", "my employer", "my company", "my team",
    "my salary", "my email", "my calendar", "my doctor", "confidential",
    "internal", "performance review", "my coworker",
)


class PrivateQueryError(ValueError):
    """Raised when a search query would leak private content."""


def sanitize_search_query(query: str) -> str:
    """Return the query if it is safe for an internet search, else raise.

    Generic learning/documentation topics pass through unchanged. Anything
    containing emails, phone numbers, deep URLs, or private-context markers
    is rejected so the caller falls back to manual mode.
    """
    if EMAIL_RE.search(query):
        raise PrivateQueryError("query contains an email address")
    if PHONE_RE.search(query):
        raise PrivateQueryError("query contains a phone number")
    if URL_WITH_PATH_RE.search(query):
        raise PrivateQueryError("query contains a specific URL path")
    lowered = query.lower()
    for marker in PRIVATE_MARKERS:
        if marker in lowered:
            raise PrivateQueryError(f"query references private context ({marker!r})")
    return query.strip()


@dataclass
class Grant:
    connector: str
    scope: str
    data_classes: tuple
    granted_at: str


@dataclass
class PermissionLedger:
    """Session-scoped record of which connectors the user authorized."""

    grants: dict = field(default_factory=dict)

    def authorize(self, connector: str, scope: str, data_classes: tuple) -> Grant:
        grant = Grant(
            connector=connector,
            scope=scope,
            data_classes=data_classes,
            granted_at=datetime.now(timezone.utc).isoformat(),
        )
        self.grants[connector] = grant
        return grant

    def is_authorized(self, connector: str) -> bool:
        return connector in self.grants

    def get(self, connector: str):
        return self.grants.get(connector)
