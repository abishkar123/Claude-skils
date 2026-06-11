"""Central configuration for the productivity-coach multi-agent system."""

import os
from dataclasses import dataclass, field
from enum import Enum


class Mode(str, Enum):
    MANUAL = "manual"
    MCP_ASSISTED = "mcp"
    HYBRID = "hybrid"


@dataclass
class Settings:
    # Model used by every agent. Override per-agent via Agent.model.
    model: str = os.environ.get("PC_MODEL", "claude-opus-4-8")
    max_tokens: int = int(os.environ.get("PC_MAX_TOKENS", "16000"))
    effort: str = os.environ.get("PC_EFFORT", "high")

    # Storage is opt-in only (privacy rule: never store without approval).
    storage_enabled: bool = False
    mongodb_uri: str = os.environ.get("MONGODB_URI", "")
    mongodb_db: str = os.environ.get("PC_DB", "productivity_coach")

    # Capacity model used by the Planning Agent and QA Agent.
    max_capacity_utilization: float = 0.80   # plans above this get a warning
    hard_capacity_limit: float = 1.00        # plans above this are rejected
    max_must_dos_per_day: int = 3
    max_deep_work_hours_per_day: float = 4.0
    min_weekend_rest_fraction: float = 0.40

    # Connectors the user has authorized this session, e.g. {"calendar", "tasks"}.
    authorized_connectors: set = field(default_factory=set)


settings = Settings()
