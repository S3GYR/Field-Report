from __future__ import annotations

from pathlib import Path

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.models import Report

settings = get_settings()


class ReportPdfService:
    def generate_pdf(self, report_id: int) -> Path:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.platypus import (
            KeepTogether,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )

        with SessionLocal() as session:
            report = session.get(Report, report_id)
            if not report:
                raise ValueError("Report not found")

            output_path = settings.exports_root / f"report-{report.number}.pdf"
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=A4,
                leftMargin=18 * mm,
                rightMargin=18 * mm,
                topMargin=20 * mm,
                bottomMargin=20 * mm,
            )
            styles = getSampleStyleSheet()
            story = []

            story.append(Paragraph(f"Rapport {report.number}", styles["Title"]))
            story.append(Spacer(1, 6 * mm))

            info_data = [
                ["Client", report.client],
                ["Site", report.site],
                ["Date de visite", str(report.visit_date)],
                ["M&eacute;t&eacute;o", report.weather],
                ["Statut", report.status],
            ]
            info_table = Table(info_data, colWidths=[40 * mm, None])
            info_table.setStyle(
                TableStyle(
                    [
                        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ]
                )
            )
            story.append(info_table)
            story.append(Spacer(1, 6 * mm))

            if report.comments:
                story.append(Paragraph("Commentaires", styles["Heading2"]))
                story.append(Paragraph(report.comments, styles["BodyText"]))
                story.append(Spacer(1, 6 * mm))

            if report.tasks:
                story.append(Paragraph("T&acirc;ches", styles["Heading2"]))
                task_data = [["Description", "Statut", "Co&ucirc;t", "Dur&eacute;e"]]
                for t in report.tasks:
                    task_data.append(
                        [
                            t.description,
                            t.status,
                            f"{t.estimated_cost:.2f} &euro;" if t.estimated_cost else "—",
                            f"{t.estimated_duration:.1f} h" if t.estimated_duration else "—",
                        ]
                    )
                task_table = Table(task_data, repeatRows=1)
                task_table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3f4f6")),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 4),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                        ]
                    )
                )
                story.append(KeepTogether(task_table))
                story.append(Spacer(1, 6 * mm))

            if report.photos:
                story.append(Paragraph("Photos", styles["Heading2"]))
                for photo in report.photos:
                    story.append(Paragraph(photo.filename, styles["BodyText"]))
                story.append(Spacer(1, 6 * mm))

            if report.signature:
                story.append(Paragraph("Signature", styles["Heading2"]))
                sig = report.signature
                story.append(Paragraph(f"Nom : {sig.name}", styles["BodyText"]))
                if sig.role:
                    story.append(Paragraph(f"R&ocirc;le : {sig.role}", styles["BodyText"]))
                story.append(Paragraph(f"Date : {sig.signed_on}", styles["BodyText"]))

            doc.build(story)
            return output_path


report_pdf_service = ReportPdfService()
