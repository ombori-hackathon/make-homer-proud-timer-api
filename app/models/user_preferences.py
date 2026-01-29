from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.sql import func

from app.db import Base


class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), default="default", unique=True, nullable=False)
    selected_god_id = Column(Integer, ForeignKey("gods.id"), nullable=True, index=True)
    favorite_god_ids = Column(
        JSON().with_variant(JSONB, "postgresql"), nullable=False, default=list
    )
    auto_select_favorites = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
