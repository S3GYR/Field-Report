from __future__ import annotations

from app.core.config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

settings = get_settings()
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
