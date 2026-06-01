from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from legacy.generer_pdf import generate_pdf as legacy_generate_pdf

from config import EXPORT_DIR


class PdfBuilder:
    """Wrapper around the legacy ReportLab generator (generer_pdf.py)."""

    def __init__(self, export_dir: Path | None = None) -> None:
        self.export_dir = export_dir or EXPORT_DIR
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def build(self, data: Dict[str, Any], filename: str = "report-preview.pdf") -> Path:
        target = self.export_dir / filename
        legacy_generate_pdf(data, target)
        return target


pdf_builder = PdfBuilder()
