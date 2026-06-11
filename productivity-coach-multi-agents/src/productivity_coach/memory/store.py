"""Database Memory layer: MongoDB when configured, ledger fallback otherwise.

Writes happen only through the API with an explicit `user_approved` flag —
the storage gate from agents/database-memory-agent.md, in code.
"""

import json
from datetime import datetime, timezone
from typing import Protocol

from ..config import settings

COLLECTIONS = {"plans", "reviews", "habits", "skills", "evidence", "goals"}


class MemoryStore(Protocol):
    persistent: bool

    async def save(self, collection: str, record: dict, sensitivity: str) -> dict: ...
    async def list(self, collection: str, limit: int = 50) -> list[dict]: ...
    async def delete_all(self, collection: str) -> int: ...


def _stamp(record: dict, sensitivity: str) -> dict:
    return {**record, "user_approved": True, "sensitivity": sensitivity,
            "source": "manual", "created_at": datetime.now(timezone.utc).isoformat()}


class LedgerStore:
    """No database: nothing persisted server-side. save() returns a
    copy-pasteable ledger block the user keeps in their own notes."""

    persistent = False

    async def save(self, collection: str, record: dict, sensitivity: str) -> dict:
        block = _stamp(record, sensitivity)
        return {
            "stored": False,
            "ledger_block": "# productivity-ledger · paste back in any future session\n"
                            + json.dumps({"collection": collection, **block}, indent=2),
        }

    async def list(self, collection: str, limit: int = 50) -> list[dict]:
        return []

    async def delete_all(self, collection: str) -> int:
        return 0


class MongoStore:
    persistent = True

    def __init__(self, uri: str, db_name: str):
        from motor.motor_asyncio import AsyncIOMotorClient
        self._db = AsyncIOMotorClient(uri)[db_name]

    async def save(self, collection: str, record: dict, sensitivity: str) -> dict:
        doc = _stamp(record, sensitivity)
        result = await self._db[collection].insert_one(dict(doc))
        return {"stored": True, "id": str(result.inserted_id)}

    async def list(self, collection: str, limit: int = 50) -> list[dict]:
        docs = await self._db[collection].find().sort("created_at", -1) \
                                         .to_list(length=limit)
        for d in docs:
            d["_id"] = str(d["_id"])
        return docs

    async def delete_all(self, collection: str) -> int:
        result = await self._db[collection].delete_many({})
        return result.deleted_count


def build_store() -> MemoryStore:
    if settings.mongodb_uri:
        return MongoStore(settings.mongodb_uri, settings.mongodb_db)
    return LedgerStore()
