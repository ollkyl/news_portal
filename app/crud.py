from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models, schemas
from datetime import datetime


active_connections = []


def create_news(news: schemas.NewsCreate):
    db = SessionLocal()
    db_news = models.News(**news.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    db.close()
    return db_news


def get_all_news():
    db = SessionLocal()
    news = db.query(models.News).order_by(models.News.created_at.desc()).all()
    db.close()
    return news


def get_settings():
    db = SessionLocal()
    settings = db.query(models.Settings).first()
    if not settings:
        settings = models.Settings()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    db.close()
    return settings


def update_auto_update(enabled: bool):
    db = SessionLocal()
    settings = db.query(models.Settings).first()
    settings.auto_update_enabled = enabled
    db.commit()
    db.close()


def update_latest_news_time(new_time: datetime):
    db = SessionLocal()
    settings = db.query(models.Settings).first()
    settings.latest_news_time = new_time
    db.commit()
    db.close()
