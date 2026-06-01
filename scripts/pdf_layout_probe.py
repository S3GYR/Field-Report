"""Probe ReportLab layout components to identify LayoutError root cause."""

from __future__ import annotations

import io
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Table

ROOT_DIR = Path(__file__).resolve().parents[1]
FIELD_REPORT_DIR = ROOT_DIR / "field-report"
if str(FIELD_REPORT_DIR) not in sys.path:
    sys.path.insert(0, str(FIELD_REPORT_DIR))

from legacy.generer_pdf import placeholder_image

ASSETS_DIR = ROOT_DIR / "tests" / "assets"
SAMPLE_IMAGE = ASSETS_DIR / "sample.jpg"

styles = getSampleStyleSheet()


def run_case(name: str, flowables):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )
    try:
        doc.build(flowables)
    except Exception as exc:  # noqa: BLE001
        print(f"[case {name}] FAIL -> {exc.__class__.__name__}: {exc}")
    else:
        print(f"[case {name}] OK")


def build_comment_column():
    return KeepTogether(
        [
            Paragraph("<b>Commentaire :</b> Exemple", styles["BodyText"]),
            Paragraph("Altitude : 10 m", styles["BodyText"]),
        ]
    )


def main() -> None:
    img = Image(str(SAMPLE_IMAGE), width=80 * mm, height=60 * mm)
    placeholder = placeholder_image(80 * mm, 60 * mm)
    comments = build_comment_column()

    run_case("image_only", [img])
    run_case("placeholder_only", [placeholder])
    run_case("comments_only", [comments])

    table_no_keep = Table(
        [[img, build_comment_column()]],
        colWidths=[80 * mm, None],
        style=[
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ],
    )
    run_case("table_without_keep", [table_no_keep])

    table_with_simple_paragraph = Table(
        [[img, Paragraph("Commentaire isolé", styles["BodyText"])]]
    )
    run_case("table_simple_paragraph", [table_with_simple_paragraph])

    table_with_keep = Table(
        [[placeholder_image(80 * mm, 60 * mm), build_comment_column()]],
        colWidths=[80 * mm, None],
        style=[
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ],
    )
    section = KeepTogether([table_with_keep])
    run_case("table_with_keep", [section])


if __name__ == "__main__":
    main()
