from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STORAGE_DIR = BASE_DIR / "storage"
PHOTO_DIR = STORAGE_DIR / "photos"
EXPORT_DIR = STORAGE_DIR / "exports"
LEGACY_DB_PATH = STORAGE_DIR / "reports.db"
DEFAULT_DB_PATH = DATA_DIR / "reports.db"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

for directory in (DATA_DIR, STORAGE_DIR, PHOTO_DIR, EXPORT_DIR, TEMPLATES_DIR, STATIC_DIR):
    directory.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    """Settings dedicated to the new FieldReport architecture."""

    app_name: str = "Field Report"
    api_prefix: str = "/api"
    debug: bool = False
    database_url: str = f"sqlite:///{DEFAULT_DB_PATH.as_posix()}"
    photo_max_size_mb: int = 15
    thumbnail_max_px: int = 640

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    # Auto-detect legacy SQLite path (storage/reports.db) for backwards compatibility.
    if LEGACY_DB_PATH.exists() and not DEFAULT_DB_PATH.exists():
        settings.database_url = f"sqlite:///{LEGACY_DB_PATH.as_posix()}"
    return settings


settings = get_settings()
