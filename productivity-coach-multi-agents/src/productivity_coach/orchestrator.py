"""Orchestrator pipeline: route (Groq, free) → specialist (OpenAI, paid) →
QA gate (Groq, free) → assemble. Mirrors ARCHITECTURE.md."""

import json
import logging
import uuid
from dataclasses import dataclass, field

from .agents import AGENTS, ROUTABLE
from .config import settings
from .llm import complete
from .privacy import PrivacyState
from .prompts import agent_prompt

log = logging.getLogger(__name__)

ROUTER_SYSTEM = f"""You are the routing layer of a multi-agent productivity OS.
Classify the user's latest message into one or more specialists:
{", ".join(ROUTABLE)}.
Routing hints: planning = week/weekend/day plans, capacity, priorities.
skill_building = learning a skill, roadmaps, practice. professional_growth =
career, promotion, resume, evidence of impact. review = retrospectives,
"how did I do", habits review. knowledge_search = needs current external
resources/docs. Use "general" only for questions about the system itself.
Multiple agents are allowed when the request genuinely spans domains.
Respond with JSON only: {{"agents": ["..."], "reason": "..."}}"""

QA_SYSTEM = agent_prompt("quality-assurance-agent") + """

Evaluate the draft below. Respond with JSON only:
{"verdict": "approve" | "annotate" | "bounce",
 "warnings": ["user-facing warning lines, only if annotate"],
 "defects": ["specific fixes for the producer, only if bounce"]}"""


@dataclass
class Session:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    history: list[dict] = field(default_factory=list)
    privacy: PrivacyState = field(default_factory=PrivacyState)
    storage_approved: bool = False


@dataclass
class TurnResult:
    reply: str
    agents_used: list[str]
    qa_verdict: str
    warnings: list[str]


async def _route(history: list[dict]) -> list[str]:
    try:
        raw = await complete(settings.router_provider, ROUTER_SYSTEM,
                             history[-6:], temperature=0.0,
                             max_tokens=200, json_mode=True)
        agents = [a for a in json.loads(raw).get("agents", []) if a in AGENTS]
        return agents or ["general"]
    except Exception:
        log.exception("router failed; defaulting to planning")
        return ["planning"]


async def _qa(draft: str) -> dict:
    try:
        raw = await complete(settings.qa_provider, QA_SYSTEM,
                             [{"role": "user", "content": draft}],
                             temperature=0.0, max_tokens=600, json_mode=True)
        data = json.loads(raw)
        if data.get("verdict") in {"approve", "annotate", "bounce"}:
            return data
    except Exception:
        log.exception("QA gate failed; shipping unannotated")
    return {"verdict": "approve", "warnings": [], "defects": []}


async def _run_specialist(key: str, session: Session) -> str:
    agent = AGENTS[key]
    system = agent.system
    if session.privacy.taint_terms:
        system += ("\n\n## Session privacy register\nThe following terms are "
                   "PRIVATE and must never appear in any suggested search "
                   "query: " + ", ".join(sorted(session.privacy.taint_terms)))
    if not session.storage_approved:
        system += ("\n\nStorage is NOT approved this session — emit ledger "
                   "blocks only, never claim anything was saved.")
    return await complete(settings.specialist_provider, system,
                          session.history, temperature=0.5, max_tokens=4096)


async def run_turn(session: Session, user_message: str) -> TurnResult:
    session.history.append({"role": "user", "content": user_message})
    agents = await _route(session.history)

    drafts: list[tuple[str, str]] = []
    for key in agents:
        # knowledge_search query hygiene: refuse tainted requests up front
        if key == "knowledge_search":
            reason = session.privacy.check_query(user_message)
            if reason:
                session.privacy.incidents.append(f"search request blocked: {reason}")
                drafts.append((key, f"⚠ Search declined — {reason}. Rephrase "
                                    "the request without private content and "
                                    "I'll find generic resources."))
                continue
        drafts.append((key, await _run_specialist(key, session)))

    draft = "\n\n---\n\n".join(d for _, d in drafts)

    qa = await _qa(draft)
    warnings = qa.get("warnings", []) or []
    if qa["verdict"] == "bounce" and qa.get("defects"):
        # One revision maximum, then annotate-and-ship.
        fixes = "\n".join(f"- {d}" for d in qa["defects"])
        session.history.append({"role": "assistant", "content": draft})
        session.history.append({"role": "user", "content":
                                "QA gate bounced this draft. Revise it, fixing "
                                f"exactly these defects, keep everything else:\n{fixes}"})
        draft = await _run_specialist(agents[0], session)
        session.history = session.history[:-2]
        qa2 = await _qa(draft)
        warnings = qa2.get("warnings", []) or []

    reply = draft
    if warnings:
        reply += "\n\n### QA warnings\n" + "\n".join(f"- ⚠ {w}" for w in warnings)

    session.history.append({"role": "assistant", "content": reply})
    return TurnResult(reply=reply, agents_used=agents,
                      qa_verdict=qa["verdict"], warnings=warnings)
