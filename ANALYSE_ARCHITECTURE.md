# ANALYSE_ARCHITECTURE

FieldReport — Analyse technique détaillée
Date : 2026-06-02

---

## 1. Structure du projet

```
backend/
├── alembic/
│   ├── env.py
│   └── versions/0001_init.py
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py          # Regroupe les 4 routers
│   │   ├── photos.py
│   │   ├── reports.py
│   │   ├── signatures.py
│   │   └── tasks.py
│   ├── core/
│   │   └── config.py            # Pydantic Settings
│   ├── db/
│   │   ├── base.py              # SQLAlchemy DeclarativeBase
│   │   └── session.py           # Engine + SessionLocal + get_db
│   ├── models/
│   │   ├── __init__.py
│   │   └── report.py            # 4 modèles : Report, Photo, Task, Signature
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── report.py            # Schémas Pydantic CRUD
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pdf_service.py       # ReportLab
│   │   └── photo_storage.py     # Pillow thumbnails
│   ├── static/
│   │   ├── css/main.css
│   │   └── js/app.js
│   └── templates/
│       ├── layout.html
│       ├── dashboard.html
│       ├── reports.html
│       ├── report_detail.html
│       ├── photos.html
│       ├── tasks.html
│       └── signatures.html
├── requirements.txt
└── tests/
    ├── conftest.py
    ├── test_api.py
    └── test_reports_api.py

field-report/                     # Package legacy (encore référencé ?)
```

---

## 2. Dépendances

| Package | Version | Usage | Statut |
|---------|---------|-------|--------|
| fastapi | 0.111.0 | Framework API + routing | Actif |
| uvicorn[standard] | 0.30.0 | Serveur ASGI | Actif |
| SQLAlchemy | 2.0.30 | ORM SQLite | Actif |
| alembic | 1.13.1 | Migrations | Actif |
| pydantic | 2.7.1 | Validation | Actif |
| pydantic-settings | 2.2.1 | Config env | Actif |
| python-multipart | 0.0.9 | Upload files | Actif |
| passlib[bcrypt] | 1.7.4 | Auth (non utilisé) | **Mort** |
| jinja2 | 3.1.4 | Templates HTML | Actif |
| reportlab | 4.4.0 | PDF | Actif |
| pillow | 10.3.0 | Thumbnails | Actif |
| httpx | 0.27.0 | Tests HTTP | Actif |
| pytest | 8.2.0 | Tests | Actif |

**Code mort** : `passlib` est installé mais aucune authentification n'est implémentée.

---

## 3. Organisation FastAPI

### Application (`app.main.create_app`)

- CORS middleware configuré avec `allow_origins=["*"]` (trop permissif pour production)
- Routers montés sous `/api`
- Static files : `/static`, `/exports`, `/storage`
- Routes UI : `/`, `/reports`, `/reports/{id}`, `/photos`, `/tasks`, `/signatures`
- Healthcheck : `/health`

### Router aggregation (`app.api.__init__`)

```python
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(photos.router, prefix="/photos", tags=["photos"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(signatures.router, prefix="/signatures", tags=["signatures"])
```

**Incohérence** : `photos.router` a des endpoints mixtes :
- `POST /{report_id}` → upload photo pour un rapport
- `GET /` → liste toutes les photos
- `GET /{photo_id}` → détail photo
- `PUT /{photo_id}` → update photo
- `DELETE /{photo_id}` → delete photo

Le prefix `/photos` est cohérent mais l'upload est `POST /photos/{report_id}` ce qui peut prêter à confusion (on pourrait s'attendre à `POST /reports/{id}/photos`).

---

## 4. Modèles SQLAlchemy (`app.models.report`)

### Report

| Champ | Type | Contraintes | Remarque |
|-------|------|-------------|----------|
| id | Integer | PK, auto | |
| number | String(50) | unique, not null, index | Numéro de rapport |
| visit_date | Date | not null | Date de visite |
| client | String(120) | not null | Client |
| site | String(240) | not null | Site/chantier |
| weather | Enum(WeatherType) | default=unknown | Météo |
| comments | Text | nullable | Observations |
| status | Enum(ReportStatus) | default=draft, index | Statut |
| created_at | DateTime | default=utcnow | |
| updated_at | DateTime | default=utcnow, onupdate | |

### Photo

| Champ | Type | Remarque |
|-------|------|----------|
| id | Integer PK | |
| report_id | Integer FK | CASCADE delete |
| filename | String(255) | |
| filepath | String(500) | Relatif à storage_root |
| thumbnail_path | String(500) | Nullable |
| gps_lat | Float | Nullable — **prêt pour géoloc** |
| gps_lng | Float | Nullable — **prêt pour géoloc** |
| comment | Text | Nullable |
| priority | Enum(PhotoPriority) | default=none |

**Constat** : `gps_lat` et `gps_lng` existent déjà dans le modèle. Ils ne sont juste pas alimentés par l'API d'upload.

### Task

| Champ | Type | Remarque |
|-------|------|----------|
| id | Integer PK | |
| report_id | Integer FK | CASCADE |
| photo_id | Integer FK | SET NULL (lien optionnel à une photo) |
| description | Text | not null |
| status | Enum(TaskStatus) | default=todo, index |
| estimated_cost | Numeric(12,2) | Nullable |
| estimated_duration | Float | Nullable (heures) |

### Signature

| Champ | Type | Remarque |
|-------|------|----------|
| id | Integer PK | |
| report_id | Integer FK | unique=True (1 signature par rapport) |
| name | String(120) | |
| role | String(120) | Nullable |
| signed_on | Date | Nullable |
| signature_image | String(500) | Nullable (chemin fichier image) |

---

## 5. Schémas Pydantic (`app.schemas.report`)

**Incohérence mineure** : `CreatePhoto` inclut `gps_lat`/`gps_lng` mais l'endpoint d'upload (`api.photos.upload_photo`) n'accepte pas ces champs dans le FormData. Le schéma est prêt, l'endpoint ne l'utilise pas.

**Anomalie** : `PhotoResponse` n'inclut pas `report_id`. Lorsqu'on liste toutes les photos, on ne sait pas à quel rapport elles appartiennent sans faire une jointure côté client. Pourtant le template `photos.html` fait exactement ça (`_reports.find(r => r.id === p.report_id)`).

---

## 6. Routes API

### Rapports (`/api/reports`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Liste tous les rapports |
| POST | `/` | Crée un rapport |
| GET | `/{id}` | Détail rapport |
| PUT | `/{id}` | Modifie rapport |
| DELETE | `/{id}` | Supprime rapport |
| POST | `/{id}/generate-pdf` | Génère le PDF |

### Photos (`/api/photos`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/{report_id}` | Upload photo pour un rapport |
| GET | `/` | Liste toutes les photos |
| GET | `/{photo_id}` | Détail photo |
| PUT | `/{photo_id}` | Modifie commentaire/priorité |
| DELETE | `/{photo_id}` | Supprime photo |

**Risque** : L'upload photo ne permet pas de transmettre `gps_lat`/`gps_lng` car il est `multipart/form-data` avec seulement `file: UploadFile`.

### Tâches (`/api/tasks`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/{report_id}` | Crée une tâche pour un rapport |
| GET | `/` | Liste toutes les tâches |
| GET | `/{task_id}` | Détail tâche |
| PUT | `/{task_id}` | Modifie tâche |
| DELETE | `/{task_id}` | Supprime tâche |

### Signatures (`/api/signatures`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Liste toutes les signatures |
| GET | `/{report_id}` | Détail signature par rapport |
| POST | `/{report_id}` | Crée une signature pour un rapport |
| PUT | `/{report_id}` | Modifie signature par rapport |
| DELETE | `/{report_id}` | Supprime signature par rapport |

**Anomalie** : Les signatures sont indexées par `report_id`, pas par `signature_id`. C'est un choix métier (1 signature par rapport) mais c'est inhabituel pour un CRUD REST.

---

## 7. Services

### PhotoStorageService (`app.services.photo_storage`)

- Stocke les photos dans `storage/photos/YYYY/MM/`
- Génère des thumbnails avec Pillow (640px max)
- Utilise `datetime.utcnow()` (déprécié en Python 3.12+)
- Nommage : `{slug}-{timestamp}.{ext}`
- Suppression fichier + thumbnail

**Dette technique** : `datetime.utcnow()` déprécié → `datetime.now(timezone.utc)`

### ReportPdfService (`app.services.pdf_service`)

- Génère PDF avec ReportLab
- Layout tabulaire basique
- Affiche les photos (uniquement le nom de fichier, pas l'image elle-même)
- Affiche les informations de signature

**Manque fonctionnel** : Les photos ne sont pas intégrées dans le PDF. Seul le nom de fichier apparaît.
**Manque fonctionnel** : Les coordonnées GPS ne sont pas exportées dans le PDF.

---

## 8. Base de données SQLite

- Fichier : `storage/reports.db`
- Engine : `create_engine(settings.database_url, connect_args={"check_same_thread": False})`
- Migrations : Alembic (`alembic/versions/0001_init.py`)
- Session : `SessionLocal` avec `autocommit=False, autoflush=False`

---

## 9. Code mort identifié

| Fichier/Référence | Description |
|-------------------|-------------|
| `passlib[bcrypt]` dans requirements.txt | Aucune authentification implémentée |
| `field-report/` package | Code legacy dupliqué (anciennes API non FastAPI) |
| `frontend/` | Code React obsolète (Docker service retiré, code encore présent) |
| `backend/debug_pdf2.py` | Fichier de debug temporaire |
| `report_detail.html:227` | `editReportInfo()` redirige vers `/reports/{id}/edit` qui n'existe pas |
| `reports.html` modal weather values | `rainy`, `windy` dans le select mais `rain`, `storm` dans le modèle. **Incohérence** |

---

## 10. Doublons

| Doublon | Localisation | Impact |
|---------|-------------|--------|
| `tests/` (racine) vs `backend/tests/` | Deux suites de tests partiellement redondantes | Maintenance doublée |
| `storage/` (racine) vs `backend/storage/` | Deux répertoires de stockage | Risque de confusion |

---

## 11. Incohérences et dette technique

| # | Problème | Fichier(s) | Sévérité |
|---|----------|------------|----------|
| 1 | `prompt()` pour l'édition de tâches/signatures | `tasks.html`, `signatures.html`, `report_detail.html` | **Haute** — Inutilisable sur mobile |
| 2 | `datetime.utcnow()` déprécié | `photo_storage.py`, `report.py` | Moyenne — Warnings pytest |
| 3 | Valeurs météo incohérentes (UI vs modèle) | `reports.html` (`rainy`, `windy`) vs `report.py` (`rain`, `storm`) | **Haute** — Création de rapport avec valeur invalide possible |
| 4 | Pas de capture photo native | `report_detail.html`, `photos.html` | **Haute** — UX terrain |
| 5 | GPS non exploité malgré champs DB | `photos.py`, `report_detail.html` | Moyenne — Fonctionnalité manquante |
| 6 | Photos non intégrées au PDF | `pdf_service.py` | Moyenne — PDF incomplet |
| 7 | `editReportInfo()` redirige vers une route inexistante | `report_detail.html` | Moyenne — 404 |
| 8 | Pas de pagination API | Tous les endpoints list | Moyenne — Non scalable |
| 9 | Pas de recherche API | Tous | Moyenne — Recherche client uniquement |
| 10 | CORS `allow_origins=["*"]` | `main.py` | Faible — Sécurité |
| 11 | `confirmDelete` utilise `confirm()` natif | `app.js` | Moyenne — Pas de modal propre |
| 12 | Pas de gestion d'erreurs réseau | Templates JS | Moyenne — UX fragile |
| 13 | `__pycache__` dans le repo | Plusieurs répertoires | Faible — Git |

---

## 12. Risques de régression

| Risque | Mitigation |
|--------|------------|
| Modification du modèle Photo (GPS) | Ajout de colonnes nullable → migration Alembic nécessaire |
| Modification de l'upload photo (capture natif) | Changement HTML uniquement, pas d'impact API |
| Remplacement des `prompt()` | Changement JS/HTML uniquement, pas d'impact API |
| Ajout recherche client | Changement JS uniquement |
| Modification modal confirmation | Changement JS uniquement |
| Intégration photo dans PDF | Modification `pdf_service.py` — risque si chemin d'image incorrect |

---

## 13. Préparation V1.1 — Points d'attention

1. **Migration Alembic** : Ajouter `gps_accuracy` (Float, nullable) au modèle Photo
2. **Endpoint photo** : Modifier `upload_photo` pour accepter `gps_lat`, `gps_lng`, `gps_accuracy` en plus de `file`
3. **Template report_detail** : Le formulaire photo doit transmettre les coordonnées GPS
4. **Incohérence météo** : Corriger les `<option value>` dans `reports.html` pour correspondre à l'enum `WeatherType`
5. **PDF** : Ajouter une section "Géolocalisation" et intégrer les images si possible
6. **Tests** : Mettre à jour les tests pour couvrir les nouveaux champs GPS
