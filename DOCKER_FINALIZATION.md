# DOCKER_FINALIZATION

## Objectif

Un seul point d'entr&eacute;e Docker pour FieldReport en production :

```bash
docker compose up -d
```

Stack : SQLite + FastAPI + Jinja2 + ReportLab. **Aucune d&eacute;pendance React.**

---

## Architecture Docker cible

```
+------------------+
|  Host :8200      |
|  (nginx optionnel)|
+--------+---------+
         |
    +----v----+
    | Backend |
    | FastAPI |
    | Jinja2  |
    | SQLite  |
    | ReportLab|
    +----+----+
         |
    +----v-------------------+
    |  Volume : storage/       |
    |  - reports.db          |
    |  - photos/             |
    |  - exports/            |
    +------------------------+
```

---

## Fichier `docker-compose.yml` (final)

```yaml
version: "3.9"

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    container_name: fieldreport-backend
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8200"]
    environment:
      - DATABASE_URL=sqlite:///./storage/reports.db
      - PYTHONDONTWRITEBYTECODE=1
      - PYTHONUNBUFFERED=1
    volumes:
      - ./storage:/app/backend/storage
    ports:
      - "8200:8200"
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8200/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    restart: unless-stopped
```

**Changements par rapport au compose legacy :**
- Service `frontend` supprim&eacute;
- `depends_on` supprim&eacute;
- Healthcheck ajout&eacute;
- `restart: unless-stopped` ajout&eacute;

---

## Fichier `backend/Dockerfile` (optimis&eacute;)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Installer les d&eacute;pendances syst&egrave;me minimales pour Pillow + ReportLab
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend

WORKDIR /app/backend

# Cr&eacute;er les r&eacute;pertoires de stockage persistants
RUN mkdir -p storage/photos storage/exports

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8200"]
```

---

## Commandes de d&eacute;ploiement

### Premier lancement

```bash
# 1. Cloner / extraire le projet
cd fieldreport

# 2. S'assurer que le r&eacute;pertoire storage existe (sera mont&eacute; en volume)
mkdir -p storage/photos storage/exports

# 3. Builder et lancer
docker compose up -d --build

# 4. Cr&eacute;er les tables SQLite (premier d&eacute;marrage uniquement)
docker exec fieldreport-backend python -c \
  "from app.db.base import Base; from app.db.session import engine; \
   from app.models import Photo, Report, Signature, Task; \
   Base.metadata.create_all(engine)"

# 5. V&eacute;rifier
curl http://localhost:8200/health
```

### Mise &agrave; jour (sans perte de donn&eacute;es)

```bash
docker compose down
docker compose up -d --build
```

**Les donn&eacute;es SQLite et photos sont conserv&eacute;es** car `storage/` est un volume bind mount.

### Arr&ecirc;t

```bash
docker compose down
```

### Backup avant mise &agrave; jour

```bash
cp -r storage storage-backup-$(date +%Y%m%d)
```

---

## V&eacute;rification post-d&eacute;ploiement

| &Eacute;tape | Commande | R&eacute;sultat attendu |
|------|----------|----------------|
| Healthcheck | `curl http://localhost:8200/health` | `{"status":"ok"}` |
| Dashboard UI | `curl -s http://localhost:8200/ | head` | HTML Jinja2 |
| API | `curl http://localhost:8200/api/reports/` | `[]` ou liste JSON |
| PDF g&eacute;n&eacute;ration | Cr&eacute;er rapport puis `POST /api/reports/{id}/generate-pdf` | `{"pdf":"..."}` |

---

## R&eacute;seau et ports

| Service | Port h&ocirc;te | Port conteneur | Description |
|---------|---------------|----------------|-------------|
| Backend | 8200 | 8200 | FastAPI + Jinja2 UI + API REST |

Aucun autre service. Aucune base de donn&eacute;es externe (SQLite embarqu&eacute;).

---

## Notes

- Le conteneur est **stateful** (SQLite sur volume). Pour un d&eacute;ploiement multi-instance, migrer vers PostgreSQL.
- Les photos upload&eacute;es persistent dans `storage/photos/` gr&acirc;ce au volume.
- Les PDF g&eacute;n&eacute;r&eacute;s sont stock&eacute;s dans `storage/exports/`.
