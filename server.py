#!/usr/bin/env python3
"""FastAPI backend for the productivity-coach Multi Agents UI.

Run:
    pip install fastapi uvicorn
    export ANTHROPIC_API_KEY=sk-ant-...
    uvicorn server:app --reload --port 8000

The React app (ui/) talks to /api/*; a production build in ui/dist is served
statically at /.
"""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from productivity_coach import Orchestrator, settings
from productivity_coach.agents.mcp_connector import DEFAULT_CONNECTORS

app = FastAPI(title="productivity-coach Multi Agents")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# One orchestrator per server process = one "session" (permission ledger
# lives for the lifetime of the process, mirroring the session-only grants).
orchestrator = Orchestrator()


class AskRequest(BaseModel):
    request: str
    deep_qa: bool = True


class AuthorizeRequest(BaseModel):
    connector: str
    authorized: bool


@app.get("/api/connectors")
def connectors():
    return [
        {
            "name": spec.name,
            "scope": spec.scope,
            "accesses": spec.data_accessed,
            "excludes": spec.data_excluded,
            "risk": spec.risk,
            "fallback": spec.manual_fallback,
            "available": spec.name in orchestrator.connectors.registry,
            "authorized": orchestrator.connectors.ledger.is_authorized(spec.name),
        }
        for spec in DEFAULT_CONNECTORS.values()
    ]


@app.post("/api/connectors/authorize")
def authorize(body: AuthorizeRequest):
    if body.connector not in DEFAULT_CONNECTORS:
        raise HTTPException(404, f"unknown connector {body.connector!r}")
    if body.authorized:
        orchestrator.connectors.authorize(body.connector)
    else:
        orchestrator.connectors.ledger.grants.pop(body.connector, None)
    return {"ok": True}


@app.get("/api/status")
def status():
    return {
        "model": settings.model,
        "storage_enabled": settings.storage_enabled,
        "storage_connected": orchestrator.memory.enabled,
        "api_key_present": bool(os.environ.get("ANTHROPIC_API_KEY")),
    }


@app.post("/api/ask")
def ask(body: AskRequest):
    text = body.request.strip()
    if not text:
        raise HTTPException(400, "empty request")
    intent = orchestrator.classify(text)
    try:
        output = orchestrator.handle(text, deep_qa=body.deep_qa)
    except Exception as e:  # surface model/connector errors to the UI
        raise HTTPException(502, str(e))
    return {"intent": intent, "output": output}


# Serve the built React app when present (ui/dist after `npm run build`).
_dist = Path(__file__).parent / "ui" / "dist"
if _dist.is_dir():
    app.mount("/", StaticFiles(directory=_dist, html=True), name="ui")
