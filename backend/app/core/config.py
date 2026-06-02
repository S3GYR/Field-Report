from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "Field Report Manager"
    api_prefix: str = "/api"
    database_url: str = "sqlite:///./storage/reports.db"
    storage_root: Path = Path("storage")
    photos_root: Path = storage_root / "photos"
    exports_root: Path = storage_root / "exports"
    photo_max_size_mb: int = 15
    thumbnail_max_px: int = 640

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.storage_root.mkdir(parents=True, exist_ok=True)
    settings.photos_root.mkdir(parents=True, exist_ok=True)
    settings.exports_root.mkdir(parents=True, exist_ok=True)
    return settings
