from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None

import re
import unicodedata

from fastapi import UploadFile

from config import PHOTO_DIR, STORAGE_DIR, settings


def _slugify(name: str) -> str:
    normalized = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-zA-Z0-9-]+", "-", normalized.lower()).strip("-")
    return normalized or "photo"


def _target_dir() -> Path:
    now = datetime.utcnow()
    target = PHOTO_DIR / f"{now:%Y}" / f"{now:%m}"
    target.mkdir(parents=True, exist_ok=True)
    return target


def save_upload(file: UploadFile) -> dict[str, str]:
    target_dir = _target_dir()
    safe_name = _slugify(Path(file.filename or "photo").stem)
    extension = Path(file.filename or "jpg").suffix or ".jpg"
    final_name = f"{safe_name}-{int(datetime.utcnow().timestamp())}{extension}"
    final_path = target_dir / final_name

    with final_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    thumb_path = final_path.with_suffix(".thumb.jpg")
    _make_thumbnail(final_path, thumb_path)

    return {
        "filename": final_name,
        "filepath": str(final_path.relative_to(STORAGE_DIR)),
        "thumbnail_path": str(thumb_path.relative_to(STORAGE_DIR)),
    }


def delete_file(relative_path: Optional[str]) -> None:
    if not relative_path:
        return
    full_path = STORAGE_DIR / relative_path
    if full_path.exists():
        full_path.unlink(missing_ok=True)
    thumb = full_path.with_suffix(".thumb.jpg")
    if thumb.exists():
        thumb.unlink(missing_ok=True)


def _make_thumbnail(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if Image is None:
        shutil.copyfile(src, dest)
        return
    with Image.open(src) as img:
        img.thumbnail((settings.thumbnail_max_px, settings.thumbnail_max_px))
        img.save(dest, "JPEG", quality=85)
