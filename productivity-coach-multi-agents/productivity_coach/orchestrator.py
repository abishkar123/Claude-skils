"""Orchestrator Agent.

Routes requests, selects workflows, decides whether MCP is needed (and
allowed), coordinates the domain agents, runs the QA gate, and produces the
final answer. Multi-intent requests ("review my week and plan next week")
run as a Review -> Planning pipeline.
"""

import re

from . import prompts
from .agents.base import BaseAgent
from .agents.knowledge import KnowledgeAgent
from .agents.mcp_connector import MCPConnectorAgent
from .agents.memory import MemoryAgent
from .agents.qa import QAAgent
from .agents.workers import (
    PlanningAgent,
    ProfessionalGrowthAgent,
    ReviewAgent,
    SkillBuildingAgent,
)

# Cheap keyword routing first; the model classifier is the fallback.
_KEYWORD_ROUTES = [
    (r"\bweekend\b", "weekend-plan"),
    (r"\b(week|weekly)\b.*\bplan|\bplan\b.*\bweek\b", "weekly-plan"),
    (r"\b(today|tomorrow|daily|morning)\b.*\b(plan|execut)|\bplan\b.*\b(today|tomorrow|day)\b", "daily-execution"),
    (r"\bskill|learn|roadmap|30/60/90|practice\b", "skill-building"),
    (r"\bpromotion|career|resume|linkedin|evidence|growth\b", "professional-growth"),
    (r"\bquarterly review\b", "review-quarterly"),
    (r"\bmonthly review\b", "review-monthly"),
    (r"\b(weekly review|review my week)\b", "review-weekly"),
    (r"\b(daily review|review my day|end of day)\b", "review-daily"),
    (r"\bhabit\b", "habit"),
    (r"\bconnector|mcp\b", "meta"),
    (r"\b(resource|documentation|docs|what's new|latest)\b", "knowledge"),
]

# Which connectors are potentially relevant per intent.
_CONNECTOR_CANDIDATES = {
    "weekly-plan": ("calendar", "tasks"),
    "weekend-plan": ("calendar",),
    "daily-execution": ("calendar", "tasks"),
    "professional-growth": ("github", "collab"),
    "review-weekly": ("calendar", "tasks", "github"),
    "review-monthly": ("github",),
}

_MEMORY_COLLECTION = {
    "weekly-plan": "plans", "weekend-plan": "plans", "daily-execution": "plans",
    "skill-building": "skill_progress", "professional-growth": "evidence_log",
    "review-daily": "reviews", "review-weekly": "reviews",
    "review-monthly": "reviews", "review-quarterly": "reviews",
    "habit": "habit_logs",
}


class _Classifier(BaseAgent):
    name = "orchestrator-classifier"
    system_prompt = prompts.ORCHESTRATOR_CLASSIFY
    # Fast, cheap routing — full reasoning is not needed to pick a label.

    def __init__(self):
        super().__init__(model="claude-haiku-4-5")


class Orchestrator:
    def __init__(self, connector_agent: MCPConnectorAgent | None = None,
                 memory: MemoryAgent | None = None):
        self.connectors = connector_agent or MCPConnectorAgent()
        self.memory = memory or MemoryAgent()
        self.qa = QAAgent()
        self.agents = {
            "weekly-plan": PlanningAgent(),
            "weekend-plan": PlanningAgent(),
            "daily-execution": PlanningAgent(),
            "habit": PlanningAgent(),
            "skill-building": SkillBuildingAgent(),
            "professional-growth": ProfessionalGrowthAgent(),
            "review-daily": ReviewAgent(),
            "review-weekly": ReviewAgent(),
            "review-monthly": ReviewAgent(),
            "review-quarterly": ReviewAgent(),
            "knowledge": KnowledgeAgent(),
        }

    # -- routing ---------------------------------------------------------
    def classify(self, request: str) -> str:
        lowered = request.lower()
        for pattern, intent in _KEYWORD_ROUTES:
            if re.search(pattern, lowered):
                return intent
        label = _Classifier().run(request).strip().lower()
        return label if label in self.agents or label == "meta" else "weekly-plan"

    # -- MCP decision ------------------------------------------------------
    def _gather_mcp_context(self, intent: str, request: str) -> tuple[str, str]:
        """Returns (context, usage_notes). Empty strings mean manual mode."""
        context_parts, notes = [], []
        for name in _CONNECTOR_CANDIDATES.get(intent, ()):
            allowed, _reason = self.connectors.gate(
                name, necessary=True,
                user_already_provided=False,
            )
            if allowed:
                data, note = self.connectors.fetch(name, f"data for {intent}")
                context_parts.append(f"[{name} via MCP]\n{data}")
                notes.append(note)
        return "\n\n".join(context_parts), "".join(notes)

    # -- main entry --------------------------------------------------------
    def handle(self, request: str, deep_qa: bool = True) -> str:
        intent = self.classify(request)

        if intent == "meta":
            return self.connectors.recommendations()

        # Multi-intent: a review request that also asks for a plan.
        if intent.startswith("review-") and re.search(r"\bplan\b", request.lower()):
            review = self._run_agent(intent, request, deep_qa)
            plan_req = (
                "Using the carry-forward items from this review, build the plan "
                f"the user asked for.\n\nReview:\n{review}\n\nOriginal request: {request}"
            )
            plan = self._run_agent("weekly-plan", plan_req, deep_qa)
            return f"{review}\n\n{'=' * 60}\n\n{plan}"

        return self._run_agent(intent, request, deep_qa)

    def _run_agent(self, intent: str, request: str, deep_qa: bool) -> str:
        agent = self.agents[intent]

        mcp_context, mcp_notes = self._gather_mcp_context(intent, request)
        memory_context = ""
        collection = _MEMORY_COLLECTION.get(intent)
        if collection:
            memory_context = self.memory.context_for(collection, {})

        context = "\n\n".join(p for p in (mcp_context, memory_context) if p)
        output = agent.run(request, context)
        if mcp_notes:
            output += "\n" + mcp_notes

        # QA gate with one repair round.
        result = self.qa.gate(output, mcp_used=bool(mcp_notes), deep=deep_qa)
        if not result.passed:
            output = agent.run(
                request,
                context + "\n\nYour previous draft failed QA for these reasons; "
                "fix them and follow the required output frame exactly:\n"
                + result.report() + "\n\nPrevious draft:\n" + output,
            )
            if mcp_notes:
                output += "\n" + mcp_notes

        # Offer storage only when a database is approved and available.
        if collection and self.memory.enabled:
            self.memory.save(collection, {"intent": intent, "request": request,
                                          "output": output})
            output += "\n[Stored in approved database: collection "
            output += f"'{collection}'. Say 'delete it' to remove.]"
        return output
