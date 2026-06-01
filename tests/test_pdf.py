"""ReportLab PDF validation for FieldReport."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
FIELD_REPORT_DIR = ROOT_DIR / "field-report"
LEGACY_DIR = FIELD_REPORT_DIR / "legacy"

if not FIELD_REPORT_DIR.exists():  # pragma: no cover
    pytest.skip("field-report directory missing", allow_module_level=True)

if not LEGACY_DIR.exists():  # pragma: no cover
    pytest.skip("legacy generer_pdf module missing", allow_module_level=True)

if str(FIELD_REPORT_DIR) not in sys.path:
    sys.path.insert(0, str(FIELD_REPORT_DIR))

from pdf import pdf_builder  # type: ignore  # noqa: E402

SAMPLE_DATA = {
    "info": {
        "projet": "Validation chantier",
        "lieu": "Paris",
        "intervenant": "Equipe QA",
        "date": "2026-05-31",
        "gps": "48.8566, 2.3522",
        "meteo": "☀️",
    },
    "photos": [
        {
            "name": "Photo_001.jpg",
            "title": "Zone A",
            "description": "Contrôle visuel.",
            "priority": "high",
            "location": "48.85, 2.35",
            "comment": "RAS",
            "tasks": [
                {
                    "numero": "T-001",
                    "description": "Vérifier",
                    "statut": "todo",
                    "date": "2026-05-31",
                    "cout": "500",
                    "duree": "1j",
                }
            ],
        }
    ],
    "global_comment": "Test fonctionnel.",
    "signature": {
        "name": "QA",
        "title": "Responsable",
        "date": "2026-05-31",
        "validated": True,
    },
}


def test_pdf_generation_creates_file(tmp_path):
    pdf_path = pdf_builder.build(SAMPLE_DATA, filename="test-report.pdf")
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 0
