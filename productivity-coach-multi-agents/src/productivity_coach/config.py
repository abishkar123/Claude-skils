from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent.parent
PROMPTS_DIR = PROJECT_ROOT / "agents"
WORKFLOWS_DIR = PROJECT_ROOT / "workflows"
TEMPLATES_FILE = PROJECT_ROOT / "templates" / "output-templates.md"

Provider = Literal["openai", "groq"]

GROQ_BASE_URL = "https://api.groq.com/openai/v1"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str = ""
    openai_model: str = "gpt-4o"

    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    router_provider: Provider = "groq"
    specialist_provider: Provider = "openai"
    qa_provider: Provider = "groq"

    mongodb_uri: str | None = None
    mongodb_db: str = "productivity_coach"

    coach_host: str = "0.0.0.0"
    coach_port: int = 8000


settings = Settings()
