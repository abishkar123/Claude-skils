#!/usr/bin/env python3
"""CLI for productivity-coach Multi Agents.

Examples:
  python cli.py "Plan my week: ~30 focused hours, ship auth, prep Thursday's
                 design review, 3 gym sessions. Last week I overcommitted."
  python cli.py "Run my monthly review" --no-deep-qa
  python cli.py "Which connectors would help me?"
  python cli.py "Plan tomorrow" --authorize calendar      # only if a calendar
                                                          # MCP is wired in
  python cli.py "Plan my week" --enable-storage           # requires MONGODB_URI

Requires ANTHROPIC_API_KEY in the environment.
"""

import argparse
import sys

from productivity_coach import Orchestrator, settings
from productivity_coach.agents.mcp_connector import DEFAULT_CONNECTORS


def main() -> int:
    parser = argparse.ArgumentParser(description="productivity-coach Multi Agents")
    parser.add_argument("request", help="what you want planned/reviewed/built")
    parser.add_argument(
        "--authorize", default="",
        help=f"comma-separated connectors to authorize this session "
             f"(known: {', '.join(DEFAULT_CONNECTORS)})",
    )
    parser.add_argument(
        "--enable-storage", action="store_true",
        help="approve storing this session's durable artifacts in MongoDB "
             "(requires MONGODB_URI; nothing is stored otherwise)",
    )
    parser.add_argument(
        "--no-deep-qa", action="store_true",
        help="skip the model-based QA review (deterministic checks still run)",
    )
    args = parser.parse_args()

    settings.storage_enabled = args.enable_storage

    orchestrator = Orchestrator()
    for name in filter(None, (c.strip() for c in args.authorize.split(","))):
        if name not in DEFAULT_CONNECTORS:
            print(f"warning: unknown connector {name!r} ignored", file=sys.stderr)
            continue
        # Authorization is recorded; the connector still does nothing until a
        # host wires a real MCP call in via MCPConnectorAgent.register().
        orchestrator.connectors.authorize(name)

    print(orchestrator.handle(args.request, deep_qa=not args.no_deep_qa))
    return 0


if __name__ == "__main__":
    sys.exit(main())
