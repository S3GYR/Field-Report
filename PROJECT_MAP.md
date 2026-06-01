# PROJECT_MAP

Inventaire établi à partir des fichiers réellement présents dans le dépôt (`git branch refactor-fieldreport`). Les chemins ci-dessous utilisent la structure actuelle (backend/ + frontend/ + artefacts legacy). Aucune modification n’a été effectuée sur le code.

## Racine

| Chemin | Taille approx. | Rôle | Statut recommandé |
| --- | --- | --- | --- |
| `docker-compose.yml` | 590 o | Compose v3 gérant services `backend` et `frontend`, volumes `./storage` | À refondre (un seul service FastAPI) |
| `README_NEW_UTF8.md` | 21 Ko | Documentation complète de l’état actuel | À mettre à jour après refactor |
| `MIGRATION_PLAN.md` | 4 Ko | Plan de migration (fichiers à supprimer/fusionner/renommer) | À maintenir |
| `ARCHITECTURE_AUDIT.md` | 5 Ko | Audit de l’architecture existante | À maintenir |
| `PROJECT_MAP.md` | — | Ce document | À maintenir |
| `template_sans_images.html` | 75 Ko | Application legacy offline (HTML/CSS/JS monolithique) | À migrer vers templates Jinja2 puis supprimer |
| `generer_pdf.py` | 24 Ko | Générateur PDF ReportLab autonome | Base pour `pdf.py` future |
| `storage/` | dossiers | Contient `photos/`, `exports/` (uploads + PDF) | À conserver (montage Docker) |

## backend/

### Racine backend

| Chemin | Taille | Rôle |
| --- | --- | --- |
| `backend/requirements.txt` | 225 o | Dépendances backend (FastAPI, SQLAlchemy, WeasyPrint, etc.) |
| `backend/Dockerfile` | 311 o | Image backend (uvicorn + dependencies) |
| `backend/alembic.ini` | 532 o | Config migrations Alembic |
| `backend/alembic/` | env.py (1,2 Ko) + versions (3,6 Ko) | Script migration initial (création tables) |
| `backend/tests/` | 2 fichiers (~2,5 Ko) | Tests Pytest CRUD rapports + fixture client |

### backend/app/

| Sous-répertoire | Fichiers | Rôle |
| --- | --- | --- |
| `app/__init__.py` | vide | Néant |
| `app/main.py` | 1 Ko | Création FastAPI, CORS, routes, montages static |
| `app/core/config.py` | 943 o | Settings Pydantic (DB, storage) |
| `app/db/` | `base.py`, `session.py` | Base SQLAlchemy + engine `sqlite:///./storage/reports.db` |
| `app/models/` | `report.py`, `__init__.py` | ORM Report/Photo/Task/Signature |
| `app/schemas/` | `report.py`, `__init__.py` | Pydantic Create/Update/Response |
| `app/api/` | `reports.py`, `photos.py`, `tasks.py`, `signatures.py`, `__init__.py` | Routes FastAPI |
| `app/services/` | `photo_storage.py`, `pdf_service.py`, `__init__.py` | Services stockage files & PDF |
| `app/pdf/report.html` | 2,1 Ko | Template Jinja2 pour PDF WeasyPrint |

## frontend/

| Chemin | Taille | Rôle | Notes |
| --- | --- | --- | --- |
| `frontend/package.json` | 753 o | Dépendances React/Vite/TypeScript/Leaflet | Lecture seule des données |
| `frontend/package-lock.json` | 275 Ko | Verrouillage npm | Volumineux |
| `frontend/tsconfig*.json` | ~1,2 Ko | Config TypeScript | Utilisé par Vite/TSX |
| `frontend/vite.config.ts` | ~0,5 Ko | Config Vite | Définit plugins React/PWA |
| `frontend/Dockerfile` | 193 o | Build frontend (npm install + build) | Sert d’image Node dédiée |
| `frontend/public/manifest.json` | 399 o | PWA | Décrit la web app offline |
| `frontend/public/icons/` | ~0,4 Ko | Icônes PWA | Utilisées par manifest |
| `frontend/src/` | ~8,5 Ko | App.tsx, pages (Dashboard, Report, Photos, Tasks, Export), composants (Header, MapView, PhotoCard, ShellLayout, Toolbar), hooks (`useReports`), services (`api.ts`), styles | SPA lecture seule; ne couvre pas CRUD |

## Dossiers stockage

| Chemin | Rôle |
| --- | --- |
| `storage/photos/` | Uploads utilisateurs + miniatures |
| `storage/exports/` | PDF générés par WeasyPrint |

## Synthèse des dépendances clés (tirées des fichiers présents)

- **Python** : FastAPI, SQLAlchemy, Pydantic, Alembic, WeasyPrint, Pillow (optionnel), ReportLab (dans script legacy), pytest.
- **Node** : React, React Router, React Query, Vite, Leaflet, PostCSS/Tailwind (dans CSS), PWA plugin.

## Éléments à fusionner / migrer (selon MIGRATION_PLAN)

- API + services → futurs `main.py`, `database.py`, `models.py`, `schemas.py`, `storage.py`, `pdf.py`.
- HTML legacy → templates Jinja2 (`templates/index.html`, `reports.html`, `report.html`, `photos.html`, `pdf_template.html`).
- SPA React → supprimée après migration UI côté serveur.
- WeasyPrint → remplacé par ReportLab (réutilisation `generer_pdf.py`).

Ce document sert de carte de référence avant refactorisation. Toutes les informations proviennent d’un inventaire réel (`Path.rglob`) du dépôt sans modification des sources.
