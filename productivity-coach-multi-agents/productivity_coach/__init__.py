"""productivity-coach Multi Agents — a privacy-first multi-agent productivity
operating system (weekly/weekend/daily planning, skill-building, professional
growth, reviews) with optional MCP connectors and optional MongoDB memory."""

from .config import Mode, settings
from .orchestrator import Orchestrator

__all__ = ["Orchestrator", "Mode", "settings"]
