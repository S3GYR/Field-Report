"""Database validation tests for the new FieldReport stack."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from sqlalchemy import inspect

ROOT_DIR = Path(__file__).resolve().parents[1]
FIELD_REPORT_DIR = ROOT_DIR / "field-report"

if not FIELD_REPORT_DIR.exists():  # pragma: no cover - safety guard
    pytest.skip("field-report directory missing", allow_module_level=True)

if str(FIELD_REPORT_DIR) not in sys.path:
    sys.path.insert(0, str(FIELD_REPORT_DIR))

from database import Base, engine, init_db  # type: ignore  # noqa: E402


def test_tables_exist():
    """init_db should create all expected tables in the target SQLite file."""

    init_db()
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    expected = {"reports", "photos", "tasks", "signatures"}
    assert expected.issubset(tables), tables


def test_reports_columns_match_spec():
    inspector = inspect(engine)
    columns = {column["name"] for column in inspector.get_columns("reports")}
    expected = {
        "id",
        "number",
        "visit_date",
        "client",
        "site",
        "status",
        "created_at",
        "updated_at",
    }
    assert expected.issubset(columns)


def test_sqlalchemy_metadata_includes_all_models():
    tables = Base.metadata.tables.keys()
    for table_name in ("reports", "photos", "tasks", "signatures"):
        assert table_name in tables
