# README_PRODUCTION

FieldReport — Rapport de visite technique.

---

## Architecture finale

```
+-------------+     +------------------+     +-------------+
|   Client    +---->+  FastAPI + UV    +---->+   SQLite    |
|  Navigateur |     |  Jinja2 UI       |     |  (fichier)  |
|             |     |  ReportLab PDF   |     |  + photos   |
+-------------+     +------------------+     +-------------+
```

| Couche | Technologie | R&ocirc;le |
|--------|-------------|--------|
| Backend | FastAPI 0.111 | API REST + SSR Jinja2 |
| ORM | SQLAlchemy 2.0 | Mod&egrave;les + Migrations |
| Validation | Pydantic v2 | Sch&eacute;mas API |
| UI | Jinja2 + HTML5 + CSS3 | Pages serveur-rendered |
| Frontend JS | Vanilla JS | Interactions, appels API fetch |
| PDF | ReportLab 4.4 | G&eacute;n&eacute;ration PDF c&ocirc;t&eacute; serveur |
| DB | SQLite | Stockage relationnel embarqu&eacute; |
| Storage | Fichiers locaux | Photos, thumbnails, exports PDF |
| Container | Docker + Compose | D&eacute;ploiement portable |

---

## Installation

### Option A — Docker (recommand&eacute;)

**Pr&eacute;requis** : Docker Engine + Docker Compose

```bash
# 1. Extraire le projet
cd fieldreport

# 2. Cr&eacute;er le volume de stockage
mkdir -p storage/photos storage/exports

# 3. Lancer
docker compose up -d --build

# 4. Initialiser la base (une seule fois)
docker exec fieldreport-backend python -c \
  "from app.db.base import Base; from app.db.session import engine; \
   from app.models import Photo, Report, Signature, Task; \
   Base.metadata.create_all(engine)"

# 5. Ouvrir http://localhost:8200
```

**Mise &agrave; jour** :
```bash
docker compose down
docker compose up -d --build
```

**Arr&ecirc;t** :
```bash
docker compose down
```

---

### Option B — Windows (natif)

**Pr&eacute;requis** : Python 3.11+, pip

```powershell
# 1. Entrer dans le backend
cd backend

# 2. Cr&eacute;er l'environnement virtuel (optionnel mais recommand&eacute;)
python -m venv .venv
.venv\Scripts\activate

# 3. Installer les d&eacute;pendances
pip install -r requirements.txt

# 4. Initialiser la base (une seule fois)
python -c "from app.db.base import Base; from app.db.session import engine; `
  from app.models import Photo, Report, Signature, Task; `
  Base.metadata.create_all(engine)"

# 5. Lancer
python -m uvicorn app.main:app --host 0.0.0.0 --port 8200

# 6. Ouvrir http://localhost:8200
```

---

### Option C — Linux (natif)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -c "from app.db.base import Base; from app.db.session import engine; \
  from app.models import Photo, Report, Signature, Task; \
  Base.metadata.create_all(engine)"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8200
```

---

## Acc&egrave;s

| URL | Description |
|-----|-------------|
| http://localhost:8200/ | Tableau de bord Jinja2 |
| http://localhost:8200/reports | Liste des rapports |
| http://localhost:8200/reports/{id} | D&eacute;tail d'un rapport |
| http://localhost:8200/photos | Galerie photos |
| http://localhost:8200/tasks | Liste des t&acirc;ches |
| http://localhost:8200/signatures | Liste des signatures |
| http://localhost:8200/docs | Swagger UI (API auto-doc) |
| http://localhost:8200/health | Healthcheck JSON |

---

## Sauvegarde SQLite

La base de donn&eacute;es est un fichier unique :

```bash
# Backup
cp storage/reports.db storage/reports-backup-$(date +%Y%m%d).db

# Restore
cp storage/reports-backup-YYYYMMDD.db storage/reports.db
```

**Docker** :
```bash
docker cp fieldreport-backend:/app/backend/storage/reports.db ./reports-backup.db
```

---

## Sauvegarde photos

Les photos sont stock&eacute;es dans `storage/photos/` :

```bash
# Backup
tar czf photos-backup-$(date +%Y%m%d).tar.gz storage/photos/

# Restore
tar xzf photos-backup-YYYYMMDD.tar.gz
```

---

## G&eacute;n&eacute;ration PDF

Deux m&eacute;thodes :

1. **Via l'interface** : Ouvrir un rapport &rarr; bouton "G&eacute;n&eacute;rer le PDF"
2. **Via l'API** :
   ```bash
   curl -X POST http://localhost:8200/api/reports/{id}/generate-pdf
   ```

Les PDF sont &eacute;crits dans `storage/exports/` et accessibles via :
```bash
curl -O http://localhost:8200/exports/report-{number}.pdf
```

---

## Maintenance

### V&eacute;rifier la sant&eacute; de l'application

```bash
curl http://localhost:8200/health
# Attendu : {"status":"ok"}
```

### Validation compl&egrave;te

```powershell
# Windows
.\validate.ps1 -Target all

# Ou manuellement
python scripts/validate_database.py
python scripts/validate_storage.py
python scripts/validate_pdf.py
python scripts/validate_api.py
```

### Nettoyer les exports PDF obsol&egrave;tes

```bash
find storage/exports -name "report-*.pdf" -mtime +30 -delete
```

### Rotation des logs (si configur&eacute;)

FastAPI + Uvicorn loguent sur stdout/stderr. Avec Docker, les logs sont g&eacute;r&eacute;s par le driver de logging Docker.

```bash
docker logs fieldreport-backend --tail 100 -f
```

---

## Structure des r&eacute;pertoires

```
fieldreport/
  backend/
    app/
      api/          # Routes FastAPI (reports, photos, tasks, signatures)
      db/           # SQLAlchemy engine, session, base
      models/       # Mod&egrave;les ORM
      schemas/      # Sch&eacute;mas Pydantic
      services/     # PDF, photo storage
      static/css/   # Styles UI
      static/js/    # Client API vanilla
      templates/    # Pages Jinja2
      main.py       # Point d'entr&eacute;e FastAPI
    tests/          # Tests pytest
    Dockerfile      # Image Docker backend
    requirements.txt
  storage/
    reports.db      # Base SQLite
    photos/         # Photos upload&eacute;es
    exports/        # PDF g&eacute;n&eacute;r&eacute;s
  scripts/          # Scripts de validation
  docker-compose.yml
```

---

## D&eacute;pannage

| Probl&egrave;me | Cause probable | Solution |
|-------------|--------------|----------|
| `no such table: reports` | Base non initialis&eacute;e | Ex&eacute;cuter `Base.metadata.create_all(engine)` |
| `ModuleNotFoundError: weasyprint` | WeasyPrint encore dans requirements | `pip install -r requirements.txt` (sans weasyprint) |
| Photos non affich&eacute;es | Chemin `/storage` non mont&eacute; | V&eacute;rifier `app.mount("/storage", ...)` |
| PDF non g&eacute;n&eacute;r&eacute; | ReportLab manquant | `pip install reportlab` |
| Port 8200 occup&eacute; | Autre processus | `uvicorn ... --port 8201` |

---

## Licence

Projet interne FieldReport.
