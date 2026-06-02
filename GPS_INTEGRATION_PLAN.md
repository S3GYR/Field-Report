# GPS_INTEGRATION_PLAN

FieldReport v1.1 — Géolocalisation automatique des photos
Date : 2026-06-02

---

## Objectif

Acquérir automatiquement les coordonnées GPS au moment de l'upload d'une photo, les stocker en base de données, les afficher dans l'interface et les exporter dans le PDF.

---

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌─────────────┐
│  Navigateur │────▶│  API POST /api/ │────▶│   SQLite    │
│ geolocation │     │  photos/{id}    │     │   photos    │
└─────────────┘     └─────────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  PDF Export  │
                    │  ReportLab   │
                    └──────────────┘
```

---

## Modèle de données

### Table `photos`

| Colonne | Type | Nullable | Description |
|---------|------|----------|-------------|
| `gps_lat` | `FLOAT` | Oui | Latitude en degrés décimaux |
| `gps_lng` | `FLOAT` | Oui | Longitude en degrés décimaux |
| `gps_accuracy` | `FLOAT` | Oui | Précision en mètres (rayon) |

### Schémas Pydantic

```python
class PhotoBase(BaseModel):
    gps_lat: Optional[float] = Field(default=None, ge=-90, le=90)
    gps_lng: Optional[float] = Field(default=None, ge=-180, le=180)
    gps_accuracy: Optional[float] = Field(default=None, ge=0)
```

---

## Acquisition côté client

### Déclenchement

La modal d'upload photo déclenche l'acquisition GPS dès son ouverture (`transitionend`).

```javascript
function acquireGps() {
    const status = document.getElementById("gps-status");
    document.getElementById("gps-lat").value = "";
    document.getElementById("gps-lng").value = "";
    document.getElementById("gps-accuracy").value = "";
    status.textContent = "GPS : acquisition en cours…";

    if (!navigator.geolocation) {
        status.textContent = "GPS : non disponible";
        return;
    }

    navigator.geolocation.getCurrentPosition(
        pos => {
            document.getElementById("gps-lat").value = pos.coords.latitude;
            document.getElementById("gps-lng").value = pos.coords.longitude;
            document.getElementById("gps-accuracy").value = pos.coords.accuracy;
            status.textContent = `GPS : ${pos.coords.latitude.toFixed(5)}, ${pos.coords.longitude.toFixed(5)} (±${Math.round(pos.coords.accuracy)}m)`;
        },
        () => { status.textContent = "GPS : échec de l'acquisition"; },
        { enableHighAccuracy: true, timeout: 10000 }
    );
}

document.getElementById("modal-photo").addEventListener("transitionend", acquireGps);
```

### Gestion des erreurs

| Scénario | Comportement |
|----------|--------------|
| GPS non disponible (`navigator.geolocation === undefined`) | Message "GPS : non disponible", upload possible sans coordonnées |
| Refus utilisateur | Message "GPS : échec de l'acquisition", upload possible sans coordonnées |
| Timeout (> 10s) | Message "GPS : échec de l'acquisition", upload possible sans coordonnées |
| Précision faible (> 50m) | Coordonnées conservées, l'utilisateur voit la précision affichée |

---

## Transmission API

### Endpoint

```python
@router.post("/{report_id}", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
def upload_photo(
    report_id: int,
    file: UploadFile = File(...),
    gps_lat: float | None = Form(default=None),
    gps_lng: float | None = Form(default=None),
    gps_accuracy: float | None = Form(default=None),
    db: Session = Depends(get_db),
):
```

Les coordonnées transitent en `multipart/form-data` (obligatoire car upload de fichier) via `Form(...)`.

---

## Affichage UI

### Dans `report_detail.html`

```javascript
const gpsLink = (p.gps_lat != null && p.gps_lng != null)
    ? el("a", {
        href: `https://maps.google.com/?q=${p.gps_lat},${p.gps_lng}`,
        target: "_blank",
        text: `GPS : ${p.gps_lat.toFixed(5)}, ${p.gps_lng.toFixed(5)}`
      })
    : el("span", { text: "", style: "display:none;" });
```

Lien ouvrant Google Maps à la position exacte de la photo.

---

## Export PDF

### Intégration dans `pdf_service.py`

```python
for photo in report.photos:
    photo_path = settings.storage_root / photo.filepath
    if photo_path.exists():
        img = Image(str(photo_path), width=120 * mm, height=80 * mm)
        img.keepRatio = True
        story.append(img)
    if photo.gps_lat is not None and photo.gps_lng is not None:
        story.append(Paragraph(
            f"GPS : {photo.gps_lat:.5f}, {photo.gps_lng:.5f} (±{photo.gps_accuracy or '?' }m)",
            styles["BodyText"]
        ))
    if photo.comment:
        story.append(Paragraph(f"Commentaire : {photo.comment}", styles["BodyText"]))
    story.append(Spacer(1, 3 * mm))
```

---

## Tests recommandés

| Test | Résultat attendu |
|------|------------------|
| Ouvrir modal photo sur Android avec GPS activé | Coordonnées affichées dans `<div id="gps-status">` |
| Ouvrir modal photo avec GPS désactivé | Message "échec de l'acquisition", upload sans coordonnées |
| Upload photo avec GPS | `gps_lat`, `gps_lng`, `gps_accuracy` stockés en base |
| Visualiser photo avec GPS | Lien "GPS : lat, lng" visible, cliquable vers Google Maps |
| Générer PDF avec photo GPS | Coordonnées et image visibles dans le PDF |
