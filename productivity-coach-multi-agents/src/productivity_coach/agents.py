"""Agent registry: maps each specialist to its prompt files, workflows,
and the provider role that runs it (specialist=OpenAI paid by default)."""

from dataclasses import dataclass, field

from .prompts import specialist_system


@dataclass(frozen=True)
class Agent:
    key: str
    agent_file: str
    workflows: tuple[str, ...] = field(default=())

    @property
    def system(self) -> str:
        return specialist_system(self.agent_file, list(self.workflows))


AGENTS: dict[str, Agent] = {
    a.key: a
    for a in [
        Agent("planning", "planning-agent",
              ("weekly-planning", "weekend-planning", "daily-execution")),
        Agent("skill_building", "skill-building-agent", ("skill-building",)),
        Agent("professional_growth", "professional-growth-agent",
              ("professional-growth",)),
        Agent("review", "review-agent", ("personal-review",)),
        Agent("knowledge_search", "knowledge-search-agent"),
        Agent("general", "orchestrator"),  # fallback for meta/system questions
    ]
}

ROUTABLE = [k for k in AGENTS if k != "general"]
