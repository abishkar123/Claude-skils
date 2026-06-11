"""MCP Connector Agent.

Owns the connector registry, the 7-question pre-flight safety gate, the
permission ledger, and Connector Usage Notes. It never calls a connector that
the host did not register AND the user did not authorize — discovery only,
never assumption.

The host application wires real MCP calls in by registering a Connector with
a `fetch` callable. Without one, every workflow falls back to manual mode.
"""

from dataclasses import dataclass, field
from typing import Callable, Optional

from ..privacy import PermissionLedger
from ..templates import connector_usage_note


@dataclass
class Connector:
    name: str                       # e.g. "calendar", "tasks", "gmail", "github"
    scope: str                      # least-privilege scope, e.g. "calendar.readonly"
    data_accessed: str              # exactly what will be read
    data_excluded: str              # what is never read
    risk: str                       # low / medium / high
    manual_fallback: str            # how to do the same thing by hand
    fetch: Optional[Callable[[str], str]] = None  # host-injected MCP call


# Least-privilege defaults for the connectors named in the system design.
DEFAULT_CONNECTORS = {
    "calendar": Connector(
        name="calendar", scope="calendar.readonly",
        data_accessed="event times/titles in a bounded date range",
        data_excluded="attendees, descriptions, attachments, other calendars",
        risk="low",
        manual_fallback="paste your meetings as 'Day - time - title'",
    ),
    "tasks": Connector(
        name="tasks", scope="tasks.readonly",
        data_accessed="open tasks, due dates, overdue items",
        data_excluded="completed-task history",
        risk="low",
        manual_fallback="paste your open task list",
    ),
    "gmail": Connector(
        name="gmail", scope="gmail.readonly (user-selected threads only)",
        data_accessed="sender/subject/deadline lines of selected messages",
        data_excluded="full inbox scans, unselected bodies, attachments",
        risk="medium",
        manual_fallback="paste the commitments/deadlines from the emails",
    ),
    "drive": Connector(
        name="drive", scope="drive.readonly (user-named files only)",
        data_accessed="the named documents",
        data_excluded="folder browsing, file discovery, sharing metadata",
        risk="medium",
        manual_fallback="paste the relevant notes/sections",
    ),
    "github": Connector(
        name="github", scope="repo.readonly (named repos)",
        data_accessed="PR titles, merge dates, commit counts (own activity)",
        data_excluded="code contents, unnamed private repos, others' activity",
        risk="low",
        manual_fallback="paste a list of merged PRs / shipped work",
    ),
    "notes": Connector(
        name="notes", scope="pages.readonly (user-named pages)",
        data_accessed="the named pages",
        data_excluded="workspace-wide search, others' pages",
        risk="medium",
        manual_fallback="paste the relevant notes",
    ),
    "collab": Connector(
        name="collab", scope="readonly (named channels/boards/tickets)",
        data_accessed="ticket status, assigned items, named-thread summaries",
        data_excluded="DMs, private channels, full-history exports",
        risk="medium",
        manual_fallback="paste ticket IDs/status and blockers",
    ),
}


class MCPConnectorAgent:
    name = "mcp-connector"

    def __init__(self, ledger: Optional[PermissionLedger] = None):
        self.ledger = ledger or PermissionLedger()
        self.registry: dict[str, Connector] = {}

    # -- discovery & authorization -------------------------------------
    def register(self, name: str, fetch: Callable[[str], str]) -> None:
        """Host wires in a real MCP call for a known connector."""
        spec = DEFAULT_CONNECTORS.get(name)
        if spec is None:
            raise KeyError(f"unknown connector {name!r}; add it to DEFAULT_CONNECTORS")
        spec.fetch = fetch
        self.registry[name] = spec

    def authorize(self, name: str) -> None:
        spec = DEFAULT_CONNECTORS[name]
        self.ledger.authorize(name, spec.scope, (spec.data_accessed,))

    # -- the 7-question pre-flight gate --------------------------------
    def gate(self, name: str, necessary: bool, user_already_provided: bool):
        """Returns (allowed: bool, reason: str). Any 'no' means manual mode."""
        if name not in self.registry or self.registry[name].fetch is None:
            return False, "service not available"
        if not necessary or user_already_provided:
            return False, "not necessary — user input suffices"
        if not self.ledger.is_authorized(name):
            return False, "not authorized by the user this session"
        return True, "ok"

    # -- use a connector ------------------------------------------------
    def fetch(self, name: str, request: str) -> tuple[str, str]:
        """Call the connector and return (data, connector_usage_note)."""
        spec = self.registry[name]
        data = spec.fetch(request)
        note = connector_usage_note(
            services=f"{spec.name} ({spec.scope})",
            purpose=request,
            accessed=spec.data_accessed,
            excluded=spec.data_excluded,
            stored="Nothing",
            risk=spec.risk,
            scope=f"{spec.scope}, this session only",
            fallback=spec.manual_fallback,
        )
        return data, note

    def recommendations(self) -> str:
        """Human-readable connector recommendations with privacy notes."""
        lines = ["Connector recommendations (all optional, least privilege):"]
        for spec in DEFAULT_CONNECTORS.values():
            available = "available" if spec.name in self.registry else "not detected"
            lines.append(
                f"- {spec.name}: scope={spec.scope} | reads: {spec.data_accessed} "
                f"| never reads: {spec.data_excluded} | risk: {spec.risk} "
                f"| status: {available} | manual fallback: {spec.manual_fallback}"
            )
        return "\n".join(lines)
