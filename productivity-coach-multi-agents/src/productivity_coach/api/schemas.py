from pydantic import BaseModel, Field


class CreateSessionResponse(BaseModel):
    session_id: str
    mode: str
    providers: dict


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=20000)


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    agents_used: list[str]
    qa_verdict: str
    warnings: list[str]


class TaintRequest(BaseModel):
    terms: list[str] = Field(description="Private terms to block from search queries")


class SaveRecordRequest(BaseModel):
    collection: str
    record: dict
    sensitivity: str = "routine"
    user_approved: bool = False


class SessionInfo(BaseModel):
    session_id: str
    turns: int
    authorized_connectors: list[str]
    taint_terms_registered: int
    privacy_incidents: list[str]
    storage_approved: bool
