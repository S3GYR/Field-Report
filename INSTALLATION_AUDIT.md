# INSTALLATION_AUDIT

FieldReport v1.1 — Audit préalable à la documentation d'exploitation
Date : 2026-06-02
Auditeur : Architecte DevOps

---

## 1. Arborescence du projet

```
fieldreport/
├── .git/                       # Repository Git
├── .gitignore                  # Exclusions Git
├── docker-compose.yml          # Orchestration Docker
├── Makefile                   # Cibles de validation
├── pyproject.toml             # Métadonnées Python
├── README.txt                 # Guide usage v1.0 legacy
├── README_PRODUCTION.md       # README existant
├── backend/
│   ├── Dockerfile             # Image conteneur
│   ├── requirements.txt       # Dépendances Python
│   ├── alembic/               # Migrations SQLAlchemy
│   ├── alembic.ini            # Config Alembic
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # Point d'entrée FastAPI
│   │   ├── api/               # Routes REST
│   │   │   ├── __init__.py
│   │   │   ├── photos.py
│   │   │   ├── reports.py
│   │   │   ├── signatures.py
│   │   │   └── tasks.py
│   │   ├── core/              # Configuration
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   ├── db/                # Base de données
│   │   │   ├── __init__.py
│   │   │   ├── base.py        # DeclarativeBase
│   │   │   └── session.py     # Engine + SessionLocal
│   │   ├── models/            # Modèles ORM
│   │   │   ├── __init__.py
│   │   │   └── report.py      # Report, Photo, Task, Signature
│   │   ├── schemas/           # Schémas Pydantic
│   │   │   ├── __init__.py
│   │   │   └── report.py
│   │   ├── services/          # Services métier
│   │   │   ├── __init__.py
│   │   │   ├── pdf_service.py
│   │   │   └── photo_storage.py
│   │   ├── static/            # Assets frontend
│   │   │   ├── css/
│   │   │   │   └── main.css
│   │   │   └── js/
│   │   │       └── app.js
│   │   └── templates/         # Templates Jinja2
│   │       ├── layout.html
│   │       ├── dashboard.html
│   │       ├── reports.html
│   │       ├── report_detail.html
│   │       ├── photos.html
│   │       ├── tasks.html
│   │       ├── signatures.html
│   │       └── history.html
│   ├── tests/                 # Tests pytest
│   │   ├── conftest.py
│   │   └── test_api.py
│   └── storage/               # Données persistantes (Docker volume)
│       ├── photos/            # Photos uploadées (YYYY/MM/)
│       ├── exports/           # PDF générés
│       └── reports.db         # Base SQLite
├── scripts/                   # Scripts de validation
│   ├── validate_database.py
│   ├── validate_storage.py
│   ├── validate_pdf.py
│   ├── validate_api.py
│   └── validate_end_to_end.py
├── storage/                   # Données persistantes (hors Docker)
│   ├── photos/
│   └── exports/
├── field-report/              # Projet legacy v1.0
├── frontend/                  # Frontend legacy (non utilisé v1.1)
└── legacy/                    # Archives legacy
```

---

## 2. Dépendances identifiées

### Python (backend/requirements.txt)

| Package | Version | Rôle |
|---------|---------|------|
| fastapi | 0.111.0 | Framework web API |
| uvicorn[standard] | 0.30.0 | Serveur ASGI |
| sqlalchemy | 2.0.30 | ORM base de données |
| alembic | 1.13.1 | Migrations DB |
| pydantic | 2.7.1 | Validation données |
| pydantic-settings | 2.2.1 | Config via env |
| python-multipart | 0.0.9 | Upload fichiers |
| passlib[bcrypt] | 1.7.4 | Hash mots de passe (préparé v2) |
| jinja2 | 3.1.4 | Templates HTML |
| reportlab | 4.4.0 | Génération PDF |
| pillow | 10.3.0 | Manipulation images |
| httpx | 0.27.0 | Client HTTP (tests) |
| pytest | 8.2.0 | Tests unitaires |

### Système (Dockerfile)

| Package système | Rôle |
|-----------------|------|
| libjpeg62-turbo-dev | Décompression JPEG (Pillow) |
| zlib1g-dev | Compression zlib (Pillow) |

### Runtime externe

| Dépendance | Version | Rôle |
|------------|---------|------|
| Docker Engine | >= 24.0 | Conteneurisation |
| Docker Compose | >= 2.20 | Orchestration |
| Python (hors Docker) | 3.11+ | Exécution native optionnelle |

---

## 3. Variables d'environnement

| Variable | Défaut | Description | Source |
|----------|--------|-------------|--------|
| `DATABASE_URL` | `sqlite:///./storage/reports.db` | URL connexion SQLite | `docker-compose.yml` |
| `PYTHONDONTWRITEBYTECODE` | `1` | Pas de `.pyc` | `docker-compose.yml`, `Dockerfile` |
| `PYTHONUNBUFFERED` | `1` | Logs non bufferisés | `docker-compose.yml`, `Dockerfile` |
| `app_name` | `Field Report Manager` | Nom application | `config.py` |
| `api_prefix` | `/api` | Préfixe routes API | `config.py` |
| `storage_root` | `storage` | Dossier stockage racine | `config.py` |
| `photos_root` | `storage/photos` | Dossier photos | `config.py` |
| `exports_root` | `storage/exports` | Dossier PDF | `config.py` |
| `photo_max_size_mb` | `15` | Taille max upload photo | `config.py` |
| `thumbnail_max_px` | `640` | Taille max thumbnail | `config.py` |

**Note** : Aucun fichier `.env` n'est présent dans le repository. Les variables sont injectées via `docker-compose.yml` ou codées en dur dans `config.py` avec des valeurs par défaut.

---

## 4. Ports utilisés

| Port | Protocole | Direction | Service | Description |
|------|-----------|-----------|---------|-------------|
| 8200 | TCP | Ingress | backend | Port applicatif FastAPI / Uvicorn |
| 8200 | TCP | Externe | docker-compose | Mapping hôte:conteneur `8200:8200` |

**Aucun autre port** n'est utilisé par l'application. Pas de base de données externe, pas de cache, pas de queue.

---

## 5. Volumes persistants

### Docker Compose

| Volume hôte | Volume conteneur | Description |
|-------------|-------------------|-------------|
| `./storage` | `/app/backend/storage` | Base SQLite + photos + exports |

### Contenu du volume

| Chemin (hôte) | Chemin (conteneur) | Type | Description |
|---------------|-------------------|------|-------------|
| `./storage/reports.db` | `/app/backend/storage/reports.db` | Fichier | Base SQLite |
| `./storage/photos/` | `/app/backend/storage/photos/` | Dossier | Photos uploadées (arborescence YYYY/MM/) |
| `./storage/exports/` | `/app/backend/storage/exports/` | Dossier | PDF générés |

### Stratégie de persistance

- Le volume `./storage` est bind-mounté (pas de named volume Docker)
- Les données survivent à `docker-compose down`
- Les données sont **perdues** si le répertoire `./storage` est supprimé

---

## 6. Chemins de stockage

| Rôle | Chemin relatif | Chemin absolu (conteneur) | Note |
|------|---------------|--------------------------|------|
| Base de données | `storage/reports.db` | `/app/backend/storage/reports.db` | Créée automatiquement au premier lancement |
| Photos | `storage/photos/YYYY/MM/` | `/app/backend/storage/photos/YYYY/MM/` | Organisées par date d'upload |
| Thumbnails | `storage/photos/YYYY/MM/*.thumb.jpg` | `/app/backend/storage/photos/YYYY/MM/*.thumb.jpg` | Générés automatiquement |
| Exports PDF | `storage/exports/` | `/app/backend/storage/exports/` | Nommé `report-{number}.pdf` |

---

## 7. Fichiers de configuration

| Fichier | Rôle | Format |
|---------|------|--------|
| `docker-compose.yml` | Orchestration services | YAML |
| `backend/Dockerfile` | Construction image | Dockerfile |
| `backend/requirements.txt` | Dépendances Python | Texte |
| `backend/alembic.ini` | Configuration migrations | INI |
| `backend/app/core/config.py` | Configuration application | Python |
| `Makefile` | Raccourcis validation | Makefile |

**Pas de fichier `.env`** — les configurations sont soit dans `docker-compose.yml`, soit codées en dur.

---

## 8. Besoins système

### Minimal (démonstration, 1 utilisateur)

| Ressource | Valeur |
|-----------|--------|
| CPU | 1 cœur |
| RAM | 512 Mo |
| Disque | 2 Go (OS + app + données initiales) |
| OS | Ubuntu 22.04 LTS, Debian 12, ou tout OS compatible Docker |

### Recommandé (production, photos terrain)

| Ressource | Valeur |
|-----------|--------|
| CPU | 2 cœurs |
| RAM | 1 Go |
| Disque | 20 Go SSD (10 Go OS + app, 10 Go données) |
| OS | Ubuntu 24.04 LTS ou Debian 12 |
| Réseau | Connexion Internet (pour GPS / cartes) |

### Besoins réseau

| Protocole | Port | Direction | Description |
|-----------|------|-----------|-------------|
| HTTP | 80/tcp | Entrant | Accès utilisateurs (via reverse proxy) |
| HTTPS | 443/tcp | Entrant | Accès utilisateurs sécurisé |
| SSH | 22/tcp | Entrant | Administration serveur |
| DNS | 53/udp | Sortant | Résolution noms (Let's Encrypt, updates) |
| HTTP | 80/tcp | Sortant | Let's Encrypt validation |

---

## 9. Architecture d'exécution

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Utilisateur   │─────▶│  Reverse Proxy   │─────▶│   Docker Host   │
│  (navigateur)   │      │  (Nginx/Traefik) │      │  (Ubuntu/Debian)│
└─────────────────┘      └──────────────────┘      └─────────────────┘
                              HTTPS 443                  │
                              HTTP 80                    │
                                                           ▼
                                              ┌──────────────────────┐
                                              │  fieldreport-backend  │
                                              │  (conteneur Docker)   │
                                              │  FastAPI + Uvicorn    │
                                              │  Port 8200            │
                                              └──────────────────────┘
                                                        │
                                                        ▼
                                              ┌──────────────────────┐
                                              │  Volume bind-mount   │
                                              │  ./storage           │
                                              │  ├── reports.db      │
                                              │  ├── photos/         │
                                              │  └── exports/        │
                                              └──────────────────────┘
```

---

## 10. Points d'attention identifiés

### Sécurité

- CORS configuré en `allow_origins=["*"]` — ouvert à tous les domaines
- Pas d'authentification implémentée
- Pas de HTTPS natif dans le conteneur
- Pas de rate limiting

### Fiabilité

- SQLite mono-utilisateur (pas de concurrence d'écriture)
- Pas de réplication de base de données
- Pas de sauvegarde automatique configurée
- Le conteneur redémarre `unless-stopped` (pas `always`)

### Scalabilité

- Architecture mono-instance par design
- Pas de load balancing
- Pas de cache distribué

### Maintenance

- `datetime.utcnow()` déprécié (warnings pytest) — non bloquant
- Pas de système de logging centralisé
- Pas de monitoring (métriques, alerting)
