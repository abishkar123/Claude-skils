"""Loads agent system prompts and workflow specs from the markdown definitions.

The markdown files under agents/ and workflows/ are the single source of
truth for agent behavior — the code wires them into the LLM calls.
"""

from functools import lru_cache

from .config import PROMPTS_DIR, TEMPLATES_FILE, WORKFLOWS_DIR


@lru_cache(maxsize=None)
def agent_prompt(name: str) -> str:
    """Return the '## System Prompt' body (plus everything after it) of an agent file."""
    text = (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")
    marker = "## System Prompt"
    return text.split(marker, 1)[1].strip() if marker in text else text


@lru_cache(maxsize=None)
def workflow_spec(name: str) -> str:
    return (WORKFLOWS_DIR / f"{name}.md").read_text(encoding="utf-8")


@lru_cache(maxsize=None)
def output_templates() -> str:
    return TEMPLATES_FILE.read_text(encoding="utf-8")


def specialist_system(agent_file: str, workflows: list[str]) -> str:
    parts = [agent_prompt(agent_file)]
    if workflows:
        parts.append("## Workflow specifications\n\n" +
                     "\n\n---\n\n".join(workflow_spec(w) for w in workflows))
    parts.append("## Output contract (mandatory)\n\n" + output_templates())
    parts.append(
        "## Hard constraints\n"
        "- You have NO external tools, connectors, or storage. Work only "
        "from the conversation. If data is missing, state assumptions and "
        "proceed, or name the minimal manual paste that would help.\n"
        "- Never fabricate calendar, email, task, or historical data.\n"
        "- If the user approved storage, end with a ledger block matching "
        "the schemas in the output contract."
    )
    return "\n\n".join(parts)
