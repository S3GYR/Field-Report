from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.models import Report

settings = get_settings()
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "pdf"


class ReportPdfService:
    def __init__(self) -> None:
        self.env = Environment(
            loader=FileSystemLoader(TEMPLATES_DIR),
            autoescape=select_autoescape(["html", "jinja"]),
        )

    def render(self, report: Report) -> str:
        template = self.env.get_template("report.html")
        return template.render(report=report, settings=settings)

    def generate_pdf(self, report_id: int) -> Path:
        from weasyprint import HTML

        with SessionLocal() as session:
            report = session.get(Report, report_id)
            if not report:
                raise ValueError("Report not found")
            html_content = self.render(report)
            output_path = settings.exports_root / f"report-{report.number}.pdf"
            HTML(string=html_content, base_url=str(TEMPLATES_DIR)).write_pdf(output_path)
            return output_path


report_pdf_service = ReportPdfService()
