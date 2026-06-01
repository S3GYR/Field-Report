"""Storage validation tests for FieldReport."""

from __future__ import annotations

import io
import sys
from pathlib import Path

import pytest
from fastapi import UploadFile

ROOT_DIR = Path(__file__).resolve().parents[1]
FIELD_REPORT_DIR = ROOT_DIR / "field-report"
ASSETS_DIR = ROOT_DIR / "tests" / "assets"

if not FIELD_REPORT_DIR.exists():  # pragma: no cover
    pytest.skip("field-report directory missing", allow_module_level=True)

if not ASSETS_DIR.exists():  # pragma: no cover
    pytest.skip("tests/assets directory missing", allow_module_level=True)

if str(FIELD_REPORT_DIR) not in sys.path:
    sys.path.insert(0, str(FIELD_REPORT_DIR))

from storage import delete_file, save_upload  # type: ignore  # noqa: E402
from config import STORAGE_DIR  # type: ignore  # noqa: E402

SAMPLE_FILES = ("sample.jpg", "sample.png", "sample.webp")


@pytest.mark.parametrize("filename", SAMPLE_FILES)
def test_upload_and_delete_roundtrip(tmp_path, filename: str):
    file_path = ASSETS_DIR / filename
    data = file_path.read_bytes()
    upload = UploadFile(filename=filename, file=io.BytesIO(data))
    meta = save_upload(upload)

    stored_path = STORAGE_DIR / meta["filepath"]
    thumb_path = Path(STORAGE_DIR / meta["thumbnail_path"])

    assert stored_path.exists()
    assert thumb_path.exists()

    delete_file(meta["filepath"])
    assert not stored_path.exists()
    assert not thumb_path.exists()
