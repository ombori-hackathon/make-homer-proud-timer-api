from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.sql import func

from app.db import Base


class God(Base):
    __tablename__ = "gods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    domain = Column(String(100), nullable=False)
    icon = Column(String(50), nullable=False)
    coaching_style = Column(String(200), nullable=False)
    focus_messages = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False)
    break_messages = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False)
    session_start_messages = Column(
        JSON().with_variant(JSONB, "postgresql"), nullable=False
    )
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
