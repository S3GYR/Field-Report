import argparse
import base64
import io
import json
import os
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Sequence

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.platypus import (
    Image,
    KeepInFrame,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from xml.sax.saxutils import escape

ROOT_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_FILE = ROOT_DIR / "rapport_data.json"
DEFAULT_OUTPUT_FILE = ROOT_DIR / "rapport.pdf"
DOC_LEFT_MARGIN = 18 * mm
DOC_RIGHT_MARGIN = 18 * mm
DOC_TOP_MARGIN = 20 * mm
DOC_BOTTOM_MARGIN = 20 * mm
DOC_FRAME_WIDTH = A4[0] - DOC_LEFT_MARGIN - DOC_RIGHT_MARGIN
DOC_FRAME_HEIGHT = A4[1] - DOC_TOP_MARGIN - DOC_BOTTOM_MARGIN

DEBUG_LAYOUT = os.environ.get("PDF_DEBUG_LAYOUT", "0") not in {"0", "false", "False", ""}
DEBUG_CURRENT_PAGE = 1
DEBUG_REMAINING_HEIGHT = DOC_FRAME_HEIGHT


STATUS_LABELS = {
    "todo": "À faire",
    "inprogress": "En cours",
    "done": "Terminée",
}
PRIORITY_LABELS = {
    "high": "Haute",
    "med": "Moyenne",
    "low": "Basse",
}

def main() -> None:
    args = parse_args()
    data = load_data(args.input)
    output_path = resolve_output_path(args.output, data)
    generate_pdf(data, output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Générer un rapport de terrain au format PDF")
    parser.add_argument(
        "-i",
        "--input",
        default=str(DEFAULT_DATA_FILE),
        help="Chemin vers le fichier JSON contenant les données du rapport",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Chemin de sortie du PDF généré (optionnel)",
    )
    return parser.parse_args()


def resolve_output_path(cli_value: str | None, data: Dict[str, Any]) -> Path:
    candidate = cli_value or data.get("output_pdf")
    path = Path(candidate) if candidate else DEFAULT_OUTPUT_FILE
    if not path.is_absolute():
        path = ROOT_DIR / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def load_data(input_path: str | None) -> Dict[str, Any]:
    path = Path(input_path or DEFAULT_DATA_FILE)
    if not path.is_absolute():
        path = ROOT_DIR / path
    if not path.exists():
        sample = default_data()
        if path == DEFAULT_DATA_FILE:
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(sample, handle, ensure_ascii=False, indent=2)
            print(f"[info] Fichier d'exemple créé : {path.name}")
            return sample
        raise FileNotFoundError(f"Impossible de trouver le fichier de données : {path}")
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    data.setdefault("info", {})
    data.setdefault("photos", [])
    return data


def default_data() -> Dict[str, Any]:
    today_iso = datetime.now().strftime("%Y-%m-%d")
    return {
        "info": {
            "projet": "Modernisation de la médiathèque",
            "lieu": "Montreuil",
            "intervenant": "Équipe BTP Nord",
            "date": today_iso,
            "meteo": "☀️",
            "gps": "48.855, 2.424",
        },
        "photos": [
            {
                "name": "Photo_001.jpg",
                "title": "Façade principale",
                "description": "Contrôle visuel de la façade bois fraîchement posée.",
                "priority": "high",
                "location": "48.85510, 2.42411",
                "comment": "Reprendre l'alignement des lames sur la travée nord.",
                "tasks": [
                    {
                        "numero": "T-101",
                        "description": "Vérifier joints d'étanchéité",
                        "date": today_iso,
                        "statut": "inprogress",
                        "cout": "800",
                        "duree": "1 j",
                    },
                    {
                        "numero": "T-102",
                        "description": "Corriger fixation lisse",
                        "statut": "todo",
                    },
                ],
            },
            {
                "name": "Photo_002.jpg",
                "title": "Salle de lecture",
                "description": "Pose des luminaires suspendus",
                "priority": "med",
                "location": "48.85540, 2.42450",
                "comment": "Prévoir une protection des suspensions avant peinture.",
                "tasks": [
                    {
                        "numero": "T-201",
                        "description": "Tester l'intensité lumineuse",
                        "date": today_iso,
                        "statut": "done",
                        "cout": "450",
                        "duree": "0.5 j",
                    }
                ],
            },
        ],
        "global_comment": "Chantier globalement conforme. Attention aux reprises de bardage.",
        "signature": {
            "name": "Laura Dupont",
            "title": "Conductrice de travaux",
            "date": today_iso,
            "validated": True,
        },
    }


def generate_pdf(data: Dict[str, Any], output_path: Path) -> None:
    stats = compute_stats(data)
    styles = build_styles()
    story = build_story(data, stats, styles)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=DOC_LEFT_MARGIN,
        rightMargin=DOC_RIGHT_MARGIN,
        topMargin=DOC_TOP_MARGIN,
        bottomMargin=DOC_BOTTOM_MARGIN,
    )
    doc.build(
        story,
        onFirstPage=lambda canvas, document: draw_cover(canvas, document, data, stats),
        onLaterPages=lambda canvas, document: draw_footer(canvas, document, data),
    )
    print(f"✅ PDF généré : {output_path}")


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=16,
            textColor=colors.HexColor("#2d5016"),
            spaceBefore=6,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubHeading",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=12,
            spaceBefore=4,
            spaceAfter=2,
            textColor=colors.HexColor("#34495e"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Meta",
            fontName="Helvetica",
            fontSize=9,
            textColor=colors.HexColor("#6b6b6b"),
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodySmall",
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Comment",
            fontName="Helvetica-Oblique",
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#5c4a1e"),
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableHeader",
            fontName="Helvetica-Bold",
            fontSize=9,
            textColor=colors.white,
            alignment=1,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableCell",
            fontName="Helvetica",
            fontSize=9,
            leading=11,
        )
    )
    return styles


def build_story(data: Dict[str, Any], stats: Dict[str, Any], styles) -> List[Any]:
    reset_debug_layout_tracking()
    story: List[Any] = [Spacer(1, 1), PageBreak()]
    story.extend(build_info_section(data.get("info", {}), stats, styles))
    story.extend(build_photos_section(data.get("photos", []), styles))
    story.extend(build_summary_section(stats, styles))
    story.extend(build_comment_section(data, styles))
    story.extend(build_signature_section(data.get("signature"), styles))
    return story


def build_info_section(info: Dict[str, Any], stats: Dict[str, Any], styles) -> List[Any]:
    rows = []
    mapping = [
        ("Projet / Chantier", info.get("projet")),
        ("Commune", info.get("lieu")),
        ("Intervenant", info.get("intervenant")),
        ("Date du rapport", format_date(info.get("date"))),
        ("GPS", info.get("gps")),
        ("Météo", info.get("meteo")),
    ]
    for label, value in mapping:
        rows.append(
            [
                Paragraph(f"<b>{escape_html(label)}</b>", styles["TableCell"]),
                Paragraph(escape_html(text_or_dash(value)), styles["BodySmall"]),
            ]
        )
    table = Table(rows, colWidths=[40 * mm, None])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f9f7f1")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#d9d4cc")),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#d9d4cc")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    stats_summary = Paragraph(
        f"Photos : <b>{stats['photos_count']}</b> &nbsp;&nbsp;|&nbsp;&nbsp; Tâches renseignées : <b>{stats['tasks_count']}</b>",
        styles["Meta"],
    )
    return [Paragraph("Informations générales", styles["SectionTitle"]), table, Spacer(1, 4 * mm), stats_summary, Spacer(1, 8 * mm)]


def build_photos_section(photos: Sequence[Dict[str, Any]], styles) -> List[Any]:
    if not photos:
        return [Paragraph("Aucune photo renseignée pour ce rapport.", styles["BodySmall"]), Spacer(1, 6 * mm)]
    blocks: List[Any] = [Paragraph("Photos commentées", styles["SectionTitle"])]
    for idx, photo in enumerate(photos, start=1):
        blocks.extend(build_photo_section(photo, idx, styles))
    return blocks


def build_photo_section(photo: Dict[str, Any], idx: int, styles) -> List[Any]:
    title = photo.get("title") or photo.get("name") or f"Photo {idx:02d}"
    header = Paragraph(f"Photo {idx:02d} — {escape_html(title)}", styles["SubHeading"])
    debug_log_flowable("header", header, idx)
    meta_parts = []
    if photo.get("priority"):
        meta_parts.append(f"Priorité : <b>{escape_html(priority_label(photo['priority']))}</b>")
    if photo.get("location"):
        meta_parts.append(f"Localisation : {escape_html(photo['location'])}")
    meta = Paragraph(" · ".join(meta_parts), styles["Meta"]) if meta_parts else Spacer(1, 0)
    debug_log_flowable("meta", meta, idx)
    description = (
        Paragraph(escape_html(photo.get("description")), styles["BodySmall"])
        if photo.get("description")
        else Spacer(1, 0)
    )
    debug_log_flowable("description", description, idx)

    img = image_flowable(photo)
    debug_log_flowable("image_or_placeholder", img, idx)
    right_column: List[Any] = []
    if photo.get("comment"):
        right_column.append(Paragraph(f"<b>Commentaire :</b> {escape_html(photo['comment'])}", styles["Comment"]))
    if photo.get("gps_altitude"):
        right_column.append(Paragraph(f"Altitude : {escape_html(str(photo['gps_altitude']))} m", styles["Meta"]))
    if not right_column:
        right_column.append(Paragraph("", styles["BodySmall"]))
    layout = Table(
        [[img, right_column]],
        colWidths=[80 * mm, None],
        style=[
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ],
    )
    debug_log_flowable("table_layout", layout, idx)
    tasks_table = build_tasks_table(photo.get("tasks", []), styles)
    content: List[Any] = [header, meta, description, layout]
    if tasks_table:
        debug_log_flowable("tasks_table", tasks_table, idx)
        content.append(tasks_table)
    content.append(Spacer(1, 6 * mm))
    block = KeepTogether(content)
    debug_log_flowable("keep_together_block", block, idx)
    return [block]


def build_tasks_table(tasks: Sequence[Dict[str, Any]], styles) -> Table | None:
    meaningful = [t for t in tasks if any(t.get(field) for field in ("numero", "description", "statut", "date", "cout", "duree"))]
    if not meaningful:
        return None
    data = [
        [
            Paragraph("N°", styles["TableHeader"]),
            Paragraph("Description", styles["TableHeader"]),
            Paragraph("Statut", styles["TableHeader"]),
            Paragraph("Date", styles["TableHeader"]),
            Paragraph("Coût", styles["TableHeader"]),
            Paragraph("Durée", styles["TableHeader"]),
        ]
    ]
    for task in meaningful:
        data.append(
            [
                Paragraph(escape_html(text_or_dash(task.get("numero"))), styles["TableCell"]),
                Paragraph(escape_html(text_or_dash(task.get("description"))), styles["TableCell"]),
                Paragraph(escape_html(status_label(task.get("statut"))), styles["TableCell"]),
                Paragraph(escape_html(format_date(task.get("date"))), styles["TableCell"]),
                Paragraph(escape_html(format_cell_cost(task.get("cout"))), styles["TableCell"]),
                Paragraph(escape_html(text_or_dash(task.get("duree"))), styles["TableCell"]),
            ]
        )
    table = Table(data, colWidths=[20 * mm, None, 25 * mm, 22 * mm, 20 * mm, 20 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d5016")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("LINEABOVE", (0, 0), (-1, -1), 0.5, colors.HexColor("#d9d4cc")),
                ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#d9d4cc")),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#d9d4cc")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def build_summary_section(stats: Dict[str, Any], styles) -> List[Any]:
    tasks = stats.get("tasks", [])
    if not tasks:
        return []
    data = [
        [
            Paragraph("Photo", styles["TableHeader"]),
            Paragraph("Tâche", styles["TableHeader"]),
            Paragraph("Statut", styles["TableHeader"]),
            Paragraph("Coût", styles["TableHeader"]),
            Paragraph("Durée", styles["TableHeader"]),
        ]
    ]
    for task in tasks:
        photo_label = f"{task['photo_index']:02d} — {task['photo_name']}"
        data.append(
            [
                Paragraph(escape_html(photo_label), styles["TableCell"]),
                Paragraph(escape_html(text_or_dash(task.get("description"))), styles["TableCell"]),
                Paragraph(escape_html(status_label(task.get("statut"))), styles["TableCell"]),
                Paragraph(escape_html(format_cell_cost(task.get("cout"))), styles["TableCell"]),
                Paragraph(escape_html(text_or_dash(task.get("duree"))), styles["TableCell"]),
            ]
        )
    table = Table(data, colWidths=[45 * mm, None, 25 * mm, 20 * mm, 20 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5c4a1e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#d9d4cc")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#d9d4cc")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    budget = stats.get("total_cost", 0.0)
    resume = Paragraph(
        f"Budget estimé : <b>{format_currency(budget)}</b> — Statuts : "
        + ", ".join(
            f"{status_label(key)} {count}" for key, count in stats.get("status_counter", {}).items()
        ),
        styles["Meta"],
    )
    return [Paragraph("Récapitulatif des tâches", styles["SectionTitle"]), table, Spacer(1, 4 * mm), resume, Spacer(1, 8 * mm)]


def build_comment_section(data: Dict[str, Any], styles) -> List[Any]:
    comment = data.get("global_comment")
    if not comment:
        return []
    text = escape_html(comment).replace("\n", "<br/>")
    return [Paragraph("Commentaire global", styles["SectionTitle"]), Paragraph(text, styles["BodySmall"]), Spacer(1, 8 * mm)]


def build_signature_section(signature: Dict[str, Any] | None, styles) -> List[Any]:
    if not signature:
        return []
    rows = []
    if signature.get("name"):
        rows.append(["Nom", signature["name"]])
    if signature.get("title"):
        rows.append(["Fonction", signature["title"]])
    if signature.get("place"):
        rows.append(["Lieu", signature["place"]])
    if signature.get("date"):
        rows.append(["Date", format_date(signature.get("date"))])
    if signature.get("validated"):
        rows.append(["Validation", "Rapport approuvé"])
    if not rows:
        return []
    table = Table(
        [[Paragraph(f"<b>{escape_html(lbl)}</b>", styles["TableCell"]), Paragraph(escape_html(text_or_dash(val)), styles["BodySmall"])] for lbl, val in rows],
        colWidths=[35 * mm, None],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f0f7e8")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#c9e2c0")),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c9e2c0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ],
    )
    return [Paragraph("Signature & validation", styles["SectionTitle"]), table]


def image_flowable(photo: Dict[str, Any]) -> Any:
    placeholder = placeholder_image(80 * mm, 60 * mm)
    source = decode_image_source(photo)
    if source is None:
        return placeholder
    try:
        img = Image(source, width=80 * mm, height=60 * mm)
        img.hAlign = "LEFT"
        return img
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] Impossible de charger l'image pour {photo.get('name', 'inconnu')} : {exc}")
        return placeholder


def decode_image_source(photo: Dict[str, Any]):
    image_path = photo.get("image_path") or photo.get("path") or photo.get("name")
    if image_path:
        path = Path(image_path)
        if not path.is_absolute():
            path = ROOT_DIR / path
        if path.exists():
            return str(path)
    b64_value = photo.get("image_b64")
    if b64_value:
        try:
            payload = b64_value.split(",")[-1]
            return io.BytesIO(base64.b64decode(payload))
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] Décodage base64 impossible ({exc})")
    return None


def placeholder_image(width: float, height: float):
    drawing = Drawing(width, height)
    drawing.add(
        Rect(0, 0, width, height, fillColor=colors.HexColor("#f6f6f6"), strokeColor=colors.HexColor("#cccccc"), strokeWidth=0.5)
    )
    drawing.add(
        String(
            width / 2,
            height / 2 - 5,
            "Image indisponible",
            fontName="Helvetica",
            fontSize=9,
            fillColor=colors.HexColor("#888888"),
            textAnchor="middle",
        )
    )
    return KeepInFrame(width, height, [drawing], hAlign="LEFT", vAlign="MIDDLE", mode="shrink")


def debug_log_flowable(label: str, flowable: Any, photo_idx: int) -> None:
    if not DEBUG_LAYOUT:
        return
    global DEBUG_CURRENT_PAGE, DEBUG_REMAINING_HEIGHT
    try:
        width, height = flowable.wrap(DOC_FRAME_WIDTH, DEBUG_REMAINING_HEIGHT)
    except Exception as exc:  # noqa: BLE001
        width = height = None
        est_page = DEBUG_CURRENT_PAGE
        info = f"wrap_error={exc}"
    else:
        est_page = DEBUG_CURRENT_PAGE
        info = ""
        if height is not None:
            if height > DEBUG_REMAINING_HEIGHT and DEBUG_REMAINING_HEIGHT != DOC_FRAME_HEIGHT:
                DEBUG_CURRENT_PAGE += 1
                est_page = DEBUG_CURRENT_PAGE
                DEBUG_REMAINING_HEIGHT = DOC_FRAME_HEIGHT - height
            else:
                DEBUG_REMAINING_HEIGHT -= height
    print(
        f"[layout-debug] photo={photo_idx} component={label} type={type(flowable).__name__} "
        f"width={width} height={height} est_page~{est_page} {info}"
    )


def reset_debug_layout_tracking() -> None:
    global DEBUG_CURRENT_PAGE, DEBUG_REMAINING_HEIGHT
    DEBUG_CURRENT_PAGE = 1
    DEBUG_REMAINING_HEIGHT = DOC_FRAME_HEIGHT


def compute_stats(data: Dict[str, Any]) -> Dict[str, Any]:
    photos = data.get("photos", [])
    tasks_entries = []
    status_counter: Counter[str] = Counter()
    total_cost = 0.0
    for index, photo in enumerate(photos, start=1):
        for task in photo.get("tasks", []):
            if not any(task.get(field) for field in ("numero", "description", "statut", "cout")):
                continue
            entry = dict(task)
            entry["photo_index"] = index
            entry["photo_name"] = photo.get("title") or photo.get("name") or f"Photo {index:02d}"
            tasks_entries.append(entry)
            status_counter[task.get("statut") or "non_renseigne"] += 1
            total_cost += normalize_cost(task.get("cout"))
    return {
        "photos_count": len(photos),
        "tasks_count": len(tasks_entries),
        "tasks": tasks_entries,
        "status_counter": status_counter,
        "total_cost": total_cost,
        "generated_on": datetime.now(),
    }


def draw_cover(canvas, doc, data: Dict[str, Any], stats: Dict[str, Any]) -> None:
    canvas.saveState()
    width, height = A4
    primary = colors.HexColor("#2d5016")
    accent = colors.HexColor("#7a9e4e")
    canvas.setFillColor(primary)
    canvas.rect(0, height * 0.55, width, height * 0.45, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 12)
    canvas.drawString(28 * mm, height - 35 * mm, "Document officiel — Visite de terrain")
    canvas.setFont("Helvetica-Bold", 36)
    canvas.drawString(28 * mm, height - 55 * mm, "Rapport de terrain")
    info = data.get("info", {})
    canvas.setFont("Helvetica", 18)
    canvas.drawString(28 * mm, height - 75 * mm, text_or_dash(info.get("lieu")))
    canvas.setFillColor(accent)
    canvas.rect(28 * mm, height - 82 * mm, 50 * mm, 2, fill=1, stroke=0)

    canvas.setFillColor(colors.black)
    canvas.setFont("Helvetica-Bold", 14)
    y = height * 0.55 - 20 * mm
    details = [
        ("Projet", info.get("projet")),
        ("Intervenant", info.get("intervenant")),
        ("Date", format_date(info.get("date"))),
        ("Coordonnées", info.get("gps")),
    ]
    for label, value in details:
        canvas.drawString(28 * mm, y, f"{label} : {text_or_dash(value)}")
        y -= 8 * mm

    stats_boxes = [
        ("Photos", str(stats.get("photos_count", "—"))),
        ("Tâches", str(stats.get("tasks_count", "—"))),
    ]
    if info.get("meteo"):
        stats_boxes.append(("Météo", text_or_dash(info.get("meteo"))))
    box_y = height - 115 * mm
    box_x = 28 * mm
    for label, value in stats_boxes:
        canvas.setFillColor(primary)
        canvas.roundRect(box_x, box_y, 45 * mm, 20 * mm, 4 * mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(box_x + 4 * mm, box_y + 14 * mm, label.upper())
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(box_x + 4 * mm, box_y + 6 * mm, value)
        box_x += 50 * mm

    canvas.setFillColor(primary)
    canvas.rect(0, 20 * mm, width, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 9)
    generated = stats.get("generated_on")
    generated_str = generated.strftime("%d/%m/%Y %H:%M") if isinstance(generated, datetime) else ""
    canvas.drawString(20 * mm, 24 * mm, f"Rapport généré le {generated_str}")
    canvas.restoreState()


def draw_footer(canvas, doc, data: Dict[str, Any]) -> None:
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(colors.HexColor("#d9d4cc"))
    canvas.line(doc.leftMargin, 25 * mm, width - doc.rightMargin, 25 * mm)
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#555555"))
    project = data.get("info", {}).get("projet") or "Rapport de terrain"
    canvas.drawString(doc.leftMargin, 21 * mm, project)
    canvas.drawRightString(width - doc.rightMargin, 21 * mm, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def escape_html(value: Any) -> str:
    if value is None:
        return ""
    return escape(str(value))


def text_or_dash(value: Any) -> str:
    text = str(value).strip() if value is not None else ""
    return text or "—"


def format_date(value: Any) -> str:
    if not value:
        return "—"
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y")
    try:
        parsed = datetime.fromisoformat(str(value))
        return parsed.strftime("%d/%m/%Y")
    except ValueError:
        return str(value)


def status_label(value: Any) -> str:
    if not value:
        return "Non renseigné"
    return STATUS_LABELS.get(str(value).lower(), str(value))


def priority_label(value: Any) -> str:
    return PRIORITY_LABELS.get(str(value).lower(), str(value))


def normalize_cost(value: Any) -> float:
    if value in (None, ""):
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    cleaned = (
        text.replace("€", "")
        .replace("EUR", "")
        .replace(" ", "")
        .replace("\xa0", "")
        .replace(",", ".")
    )
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def format_currency(value: float) -> str:
    formatted = f"{value:,.2f}".replace(",", " ").replace(".", ",")
    return f"{formatted} €"


def format_cell_cost(value: Any) -> str:
    if isinstance(value, (int, float)):
        return format_currency(float(value))
    text = str(value).strip() if value is not None else ""
    return text or "—"


if __name__ == "__main__":
    main()
