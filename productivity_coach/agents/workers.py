"""The four domain agents. Each is a system prompt over BaseAgent; their
workflow rules live in prompts.py so they stay reviewable in one place."""

from .. import prompts
from .base import BaseAgent


class PlanningAgent(BaseAgent):
    name = "planning"
    system_prompt = prompts.PLANNING


class SkillBuildingAgent(BaseAgent):
    name = "skill-building"
    system_prompt = prompts.SKILL_BUILDING


class ProfessionalGrowthAgent(BaseAgent):
    name = "professional-growth"
    system_prompt = prompts.PROFESSIONAL_GROWTH


class ReviewAgent(BaseAgent):
    name = "review"
    system_prompt = prompts.REVIEW
