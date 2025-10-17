from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from datetime import datetime, timezone
from .db import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    auto_update_enabled = Column(Boolean, default=False)
    latest_news_time = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
