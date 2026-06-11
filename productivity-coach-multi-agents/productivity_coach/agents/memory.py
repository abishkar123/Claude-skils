"""Database Memory Agent.

Stores only structured, user-approved records: plans, reviews, habit logs,
skill progress, evidence logs. Storage is opt-in; when no approved database
exists the system stays fully functional via paste-back STATE blocks that the
agents emit in every durable output.

MongoDB collections (created lazily):
    plans, reviews, habit_logs, skill_progress, evidence_log
Retention is the user's to manage; delete-on-request is honored via delete().
"""

from datetime import datetime, timezone
from typing import Optional

from ..config import settings

COLLECTIONS = ("plans", "reviews", "habit_logs", "skill_progress", "evidence_log")


class MemoryAgent:
    name = "memory"

    def __init__(self):
        self._db = None
        if settings.storage_enabled and settings.mongodb_uri:
            try:
                from pymongo import MongoClient
                self._db = MongoClient(
                    settings.mongodb_uri, serverSelectionTimeoutMS=3000
                )[settings.mongodb_db]
            except Exception:
                self._db = None  # degrade silently to paste-back mode

    @property
    def enabled(self) -> bool:
        return self._db is not None

    def save(self, collection: str, record: dict) -> Optional[str]:
        """Persist a user-approved record. Returns the id, or None if storage
        is unavailable (caller should rely on the STATE block instead)."""
        if collection not in COLLECTIONS:
            raise KeyError(f"unknown collection {collection!r}")
        if not self.enabled:
            return None
        record = {**record, "created_at": datetime.now(timezone.utc)}
        return str(self._db[collection].insert_one(record).inserted_id)

    def recall(self, collection: str, query: dict, limit: int = 5) -> list[dict]:
        if not self.enabled:
            return []
        cursor = self._db[collection].find(query).sort("created_at", -1).limit(limit)
        return [{**doc, "_id": str(doc["_id"])} for doc in cursor]

    def delete(self, collection: str, query: dict) -> int:
        """Honor delete-on-request."""
        if not self.enabled:
            return 0
        return self._db[collection].delete_many(query).deleted_count

    def context_for(self, collection: str, query: dict) -> str:
        """Render recent records as context for an agent, or empty string."""
        records = self.recall(collection, query)
        if not records:
            return ""
        lines = [f"Recent stored {collection} (user-approved storage):"]
        lines += [str(r) for r in records]
        return "\n".join(lines)
