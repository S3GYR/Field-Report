from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

try:  # pragma: no cover - optional dependency in some environments
    from PIL import Image
except ImportError:  # pragma: no cover - fallback when pillow unavailable
    Image = None

import re
import unicodedata

from fastapi import UploadFile

from app.core.config import get_settings

settings = get_settings()


class PhotoStorageService:
    def __init__(self) -> None:
        self.root = settings.photos_root
        self.root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _slugify(name: str) -> str:
        normalized = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
        normalized = re.sub(r"[^a-zA-Z0-9-]+", "-", normalized.lower()).strip("-")
        return normalized or "photo"

    def _target_dir(self) -> Path:
        now = datetime.utcnow()
        target = self.root / f"{now:%Y}" / f"{now:%m}"
        target.mkdir(parents=True, exist_ok=True)
        return target

    def save(self, file: UploadFile) -> dict:
        target_dir = self._target_dir()
        safe_name = self._slugify(Path(file.filename or "photo").stem)
        extension = Path(file.filename or "jpg").suffix or ".jpg"
        final_name = f"{safe_name}-{int(datetime.utcnow().timestamp())}{extension}"
        final_path = target_dir / final_name

        with final_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        thumb_path = final_path.with_suffix(".thumb.jpg")
        self._make_thumbnail(final_path, thumb_path)

        return {
            "filename": final_name,
            "filepath": str(final_path.relative_to(settings.storage_root)),
            "thumbnail_path": str(thumb_path.relative_to(settings.storage_root)),
        }

    def delete(self, relative_path: str) -> None:
        if not relative_path:
            return
        full_path = settings.storage_root / relative_path
        if full_path.exists():
            full_path.unlink(missing_ok=True)
        thumb = full_path.with_suffix(".thumb.jpg")
        if thumb.exists():
            thumb.unlink(missing_ok=True)

    @staticmethod
    def _make_thumbnail(src: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)

        if Image is None:  # pragma: no cover - fallback copy when pillow missing
            shutil.copyfile(src, dest)
            return

        with Image.open(src) as img:
            img.thumbnail((settings.thumbnail_max_px, settings.thumbnail_max_px))
            img.save(dest, "JPEG", quality=85)


photo_storage = PhotoStorageService()
