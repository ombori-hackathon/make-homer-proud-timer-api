from sqlalchemy import JSON, Column, Date, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.sql import func

from app.db import Base


class UserStats(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), default="default", unique=True)
    total_sessions = Column(Integer, nullable=False, default=0)
    total_focus_minutes = Column(Integer, nullable=False, default=0)
    current_streak = Column(Integer, nullable=False, default=0)
    last_session_date = Column(Date, nullable=True)
    sessions_by_god = Column(
        JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
