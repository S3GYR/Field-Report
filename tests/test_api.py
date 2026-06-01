"""API validation scaffolding for FieldReport."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
FIELD_REPORT_DIR = ROOT_DIR / "field-report"

if not FIELD_REPORT_DIR.exists():  # pragma: no cover
    pytest.skip("field-report directory missing", allow_module_level=True)

if str(FIELD_REPORT_DIR) not in sys.path:
    sys.path.insert(0, str(FIELD_REPORT_DIR))

from main import app  # type: ignore  # noqa: E402

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("status") == "ok"


@pytest.mark.skip("REST endpoints not implemented yet – update once CRUD routes exist")
def test_reports_crud_flow():
    ...


@pytest.mark.skip("REST endpoints not implemented yet – update once CRUD routes exist")
def test_photos_crud_flow():
    ...


@pytest.mark.skip("REST endpoints not implemented yet – update once CRUD routes exist")
def test_tasks_crud_flow():
    ...
