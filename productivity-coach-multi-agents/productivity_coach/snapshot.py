"""Immutable execution snapshots.

Every orchestrator run appends a read-only snapshot so the system has an
auditable, in-process trace of what happened — which intent was routed, what
the agent produced, whether QA passed, and whether a repair was attempted.
This is the immutable-state pattern from the orchestration article: state
transitions are recorded as append-only events, never mutated in place.

Snapshots live in RAM only (no disk, no DB). They are deliberately ephemeral:
cleared when the process restarts. Long-term storage of outputs is handled by
MemoryAgent (user-approved MongoDB) or the paste-back STATE block.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from typing import Optional


def _sha8(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:8]


@dataclass(frozen=True)   # frozen = immutable once created
class Snapshot:
    run_id: str            # sha8 of (timestamp + request)
    timestamp: float       # time.time()
    intent: str
    request_hash: str      # sha8 of raw request (not the text itself)
    mcp_connectors: tuple[str, ...]
    qa_passed_first: bool
    repair_attempted: bool
    qa_passed_final: bool
    compensated: bool      # True when both attempts failed → graceful degradation
    output_hash: str       # sha8 of final output text


@dataclass
class SnapshotLog:
    _entries: list[Snapshot] = field(default_factory=list, init=False)

    def record(self, **kwargs) -> Snapshot:
        snap = Snapshot(**kwargs)
        self._entries.append(snap)
        return snap

    def latest(self, n: int = 5) -> list[Snapshot]:
        return list(self._entries[-n:])

    def summary(self) -> str:
        if not self._entries:
            return "No runs recorded this session."
        lines = ["Session run log (immutable):"]
        for s in self._entries[-10:]:
            status = "compensated" if s.compensated else ("repaired" if s.repair_attempted else "clean")
            lines.append(
                f"  [{s.run_id}] {s.intent} | qa_final={'pass' if s.qa_passed_final else 'fail'} "
                f"| {status} | mcp={','.join(s.mcp_connectors) or 'none'}"
            )
        return "\n".join(lines)


# Module-level singleton: shared across the process for this session.
session_log = SnapshotLog()
