from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SessionCreate(BaseModel):
    god_id: int
    session_type: str  # "focus" or "break"
    duration_seconds: int
    started_at: datetime


class SessionComplete(BaseModel):
    completed_at: datetime | None = None


class Session(BaseModel):
    id: int
    god_id: int
    session_type: str
    duration_seconds: int
    started_at: datetime
    completed_at: datetime | None
    was_completed: bool

    model_config = ConfigDict(from_attributes=True)


class TodaySessions(BaseModel):
    count: int
    sessions: list[Session]
