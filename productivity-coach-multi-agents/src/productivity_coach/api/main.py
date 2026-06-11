"""FastAPI backend for the productivity coach.

Run: uvicorn productivity_coach.api.main:app --reload
"""

import logging

from fastapi import FastAPI, HTTPException

from ..config import settings
from ..memory.store import COLLECTIONS, build_store
from ..orchestrator import Session, run_turn
from .schemas import (
    ChatRequest,
    ChatResponse,
    CreateSessionResponse,
    SaveRecordRequest,
    SessionInfo,
    TaintRequest,
)

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Productivity Coach — Multi-Agent OS",
    version="0.1.0",
    description="Weekly/weekend/daily planning, skill-building, professional "
                "growth, and reviews. Specialists on OpenAI (paid); routing "
                "and QA on Groq (free).",
)

_sessions: dict[str, Session] = {}
_store = build_store()


def _get(session_id: str) -> Session:
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(404, "unknown session_id")
    return session


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "specialist_model": f"{settings.specialist_provider}:{settings.openai_model}",
        "router_qa_model": f"{settings.router_provider}:{settings.groq_model}",
        "storage": "mongodb" if _store.persistent else "ledger-fallback",
        "openai_key": bool(settings.openai_api_key),
        "groq_key": bool(settings.groq_api_key),
    }


@app.post("/sessions", response_model=CreateSessionResponse)
async def create_session():
    session = Session()
    _sessions[session.id] = session
    return CreateSessionResponse(
        session_id=session.id,
        mode="manual",
        providers={
            "specialists": f"{settings.specialist_provider}:{settings.openai_model}",
            "router": f"{settings.router_provider}:{settings.groq_model}",
            "qa": f"{settings.qa_provider}:{settings.groq_model}",
        },
    )


@app.get("/sessions/{session_id}", response_model=SessionInfo)
async def session_info(session_id: str):
    s = _get(session_id)
    return SessionInfo(
        session_id=s.id,
        turns=len([m for m in s.history if m["role"] == "user"]),
        authorized_connectors=sorted(s.privacy.authorized_connectors),
        taint_terms_registered=len(s.privacy.taint_terms),
        privacy_incidents=s.privacy.incidents,
        storage_approved=s.storage_approved,
    )


@app.post("/sessions/{session_id}/messages", response_model=ChatResponse)
async def chat(session_id: str, body: ChatRequest):
    if not (settings.openai_api_key or settings.groq_api_key):
        raise HTTPException(503, "no LLM API key configured — set "
                                 "OPENAI_API_KEY and/or GROQ_API_KEY (see .env.example)")
    session = _get(session_id)
    result = await run_turn(session, body.message)
    return ChatResponse(
        session_id=session.id,
        reply=result.reply,
        agents_used=result.agents_used,
        qa_verdict=result.qa_verdict,
        warnings=result.warnings,
    )


@app.post("/sessions/{session_id}/privacy/taint")
async def register_taint(session_id: str, body: TaintRequest):
    session = _get(session_id)
    session.privacy.register_taint(body.terms)
    return {"registered": len(session.privacy.taint_terms)}


@app.post("/sessions/{session_id}/storage/approve")
async def approve_storage(session_id: str):
    session = _get(session_id)
    session.storage_approved = True
    return {"storage_approved": True,
            "backend": "mongodb" if _store.persistent else "ledger-fallback"}


@app.post("/sessions/{session_id}/records")
async def save_record(session_id: str, body: SaveRecordRequest):
    session = _get(session_id)
    # Storage gate: explicit per-request approval AND session-level approval.
    if not (body.user_approved and session.storage_approved):
        raise HTTPException(403, "storage gate: requires session storage "
                                 "approval and user_approved=true on the record")
    if body.collection not in COLLECTIONS:
        raise HTTPException(422, f"collection must be one of {sorted(COLLECTIONS)}")
    return await _store.save(body.collection, body.record, body.sensitivity)


@app.get("/records/{collection}")
async def list_records(collection: str, limit: int = 50):
    if collection not in COLLECTIONS:
        raise HTTPException(422, f"collection must be one of {sorted(COLLECTIONS)}")
    return await _store.list(collection, limit=limit)


@app.delete("/records/{collection}")
async def delete_records(collection: str):
    if collection not in COLLECTIONS:
        raise HTTPException(422, f"collection must be one of {sorted(COLLECTIONS)}")
    deleted = await _store.delete_all(collection)
    return {"deleted": deleted}
