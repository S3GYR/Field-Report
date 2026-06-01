# REFACTOR_SPEC

Référence officielle pour la refonte FieldReport. Aucune modification de code n’a été effectuée ; toutes les informations proviennent des fichiers réellement présents dans le dépôt (`git branch refactor-fieldreport`).

---

## 1. Inventaire complet (statut par fichier)

### Racine du dépôt

#### README.txt (si présent)

- **Taille** : NON VÉRIFIÉ (fichier repéré par `find_by_name`, contenu non consulté).
- **Rôle** : Ancienne documentation brève.
- **Dépendances** : Aucune.
- **Statut** : RENOMMER → `README.md` (version finale post-refonte).
- **Motif** : Harmoniser avec la documentation officielle.
- **Risques / Impact** : Faibles (documentaire).

#### README_NEW_UTF8.md (≈21 Ko)

- **Rôle** : Documentation technique actuelle (état existant).
- **Dépendances** : Référence tous les sous-systèmes (backend, frontend, legacy).
- **Statut** : FUSIONNER → deviendra `README.md` final (mise à jour de contenu).
- **Impact** : Nécessite relecture complète après refonte.

#### ARCHITECTURE_AUDIT.md / PROJECT_MAP.md / MIGRATION_PLAN.md

- **Taille** : 5 Ko / 4 Ko / 4 Ko.
- **Rôle** : Documents d’analyse et de planification.
- **Dépendances** : S’appuient sur l’arborescence actuelle.
- **Statut** : CONSERVER (serviront d’historique).

#### REFACTOR_SPEC.md / DATABASE_MIGRATION.md

- **Rôle** : (ce document + futur document BD).
- **Statut** : CONSERVER.

#### docker-compose.yml (590 o)

- **Rôle** : Compose à deux services (frontend+backend) + volume `./storage`.
- **Dépendances** : Backend Dockerfile, Frontend Dockerfile.
- **Statut** : FUSIONNER → nouveau `docker-compose.yml` mono-service FastAPI (volumes `./data` et `./storage`).

#### template_sans_images.html (75 Ko)

- **Rôle** : Application legacy offline (HTML/CSS/JS complet).
- **Dépendances** : localStorage/sessionStorage, Leaflet CDN, ReportLab script (export CSV/print).
- **Statut** : SUPPRIMER une fois toutes les vues migrées vers Jinja2.
- **Remplacé par** : `templates/*.html` (dashboard, photos, tâches, rapports).
- **Risques** : Perte temporaire du mode offline → prévoir phase de validation.

#### generer_pdf.py (24 Ko)

- **Rôle** : Générateur PDF ReportLab autonome.
- **Dépendances** : `reportlab`, JSON `rapport_data.json`.
- **Statut** : FUSIONNER → `pdf.py` (service ReportLab unique).
- **Fonctions réutilisées** : `compute_stats`, `build_story`, `draw_cover`, `draw_footer`.

#### storage/photos/, storage/exports/

- **Rôle** : Stockage fichiers utilisateurs.
- **Statut** : CONSERVER (volumes persistants). Aucun fichier suivi → NON VÉRIFIÉ.

---

### backend/

#### backend/requirements.txt (225 o)

- **Rôle** : Dépendances backend (FastAPI, SQLAlchemy, Pydantic, WeasyPrint…).
- **Dépendances** : pip/uvicorn.
- **Statut** : RENOMMER → racine `requirements.txt` (inclure ReportLab, retirer WeasyPrint quand supprimé).

#### backend/Dockerfile (311 o)

- **Rôle** : Image uvicorn dédiée.
- **Statut** : FUSIONNER → nouveau Dockerfile racine (unique service).

#### backend/alembic.ini + backend/alembic/env.py + versions/0001_init.py

- **Rôle** : Configuration Alembic (création tables initiales).
- **Statut** : SUPPRIMER (refonte basée sur création automatique SQLAlchemy / migrations futures à définir après stabilisation).
- **Risques** : Faibles si nouvelle base (SQLite) générée automatiquement.

#### backend/tests/conftest.py & backend/tests/test_reports_api.py

- **Rôle** : Fixtures FastAPI + test CRUD rapports.
- **Statut** : FUSIONNER → nouvelle suite de tests (répertoire `tests/`).
- **Dépendances** : FastAPI TestClient, sqlite temporaire.

#### `backend/app/__init__.py`, `backend/app/models/__init__.py`, `backend/app/schemas/__init__.py`, `backend/app/services/__init__.py`

- **Rôle** : Initialisation packages.
- **Statut** : SUPPRIMER (structure plate future).

#### backend/app/main.py (1 033 o)

- **Rôle** : Fabrique FastAPI + CORS + montage static + route health.
- **Dépendances** : `app.api`, `settings`.
- **Statut** : FUSIONNER → `main.py` (racine).
- **Fonctionnalités conservées** : configuration FastAPI, StaticFiles, health.

#### backend/app/core/config.py (943 o)

- **Rôle** : Settings Pydantic (app, API prefix, `sqlite:///./storage/reports.db`, storage dirs, tailles photos).
- **Dépendances** : `pydantic-settings`, `pathlib`.
- **Statut** : FUSIONNER → `config.py` (racine) avec chemins `BASE_DIR`, `DATA_DIR`, `PHOTO_DIR`, `EXPORT_DIR` (cible fournie).

#### backend/app/db/base.py & backend/app/db/session.py

- **Rôle** : Base SQLAlchemy + session `sqlite:///./storage/reports.db` (`check_same_thread=False`).
- **Dépendances** : SQLAlchemy.
- **Statut** : FUSIONNER → `database.py`.

#### backend/app/models/report.py (4,3 Ko)

- **Rôle** : ORM complet (Report, Photo, Task, Signature + enums, relations, cascade, index sur number/status/photo_id/task_id).
- **Statut** : FUSIONNER → `models.py`.

#### backend/app/schemas/report.py (3 Ko)

- **Rôle** : Pydantic schemas (Photo, Task, Signature, Report, create/update/response).
- **Dépendances** : `pydantic`, enums `app.models.report`.
- **Statut** : FUSIONNER → `schemas.py`.

#### backend/app/api/reports.py (2,4 Ko)

- **Rôle** : CRUD rapports + génération PDF.
- **Statut** : FUSIONNER → `main.py` (routes API) + contrôleurs Jinja2 (nouveaux).

#### backend/app/api/photos.py (1,3 Ko)

- **Rôle** : Upload/suppression photo.
- **Statut** : FUSIONNER → `main.py` (ou blueprint unique).

#### backend/app/api/tasks.py (1,4 Ko) & backend/app/api/signatures.py (1,7 Ko)

- **Rôle** : CRUD tâches / signatures.
- **Statut** : FUSIONNER → `main.py`.

#### backend/app/services/photo_storage.py (2,6 Ko)

- **Rôle** : Service stockage (slugify, timestamp, `storage/photos/YYYY/MM`, miniatures PIL/fallback, delete).
- **Statut** : FUSIONNER → `storage.py`.

#### backend/app/services/pdf_service.py (1,2 Ko)

- **Rôle** : Service WeasyPrint (Jinja2 template + HTML→PDF).
- **Statut** : SUPPRIMER après migration ReportLab.
- **Remplacé par** : `pdf.py`.

#### backend/app/pdf/report.html (2,1 Ko)

- **Rôle** : Template Jinja2 (PDF WeasyPrint).
- **Statut** : SUPPRIMER (design converti en composants ReportLab ou archivé en `templates/pdf_template.html`).

---

### frontend/

Tous les fichiers React/Vite seront supprimés après migration Jinja2. Pour chacun :

- `frontend/Dockerfile` (193 o) → SUPPRIMER (plus de service Node).
- `frontend/package.json` (753 o) + `package-lock.json` (275 Ko) → SUPPRIMER.
- `frontend/tsconfig.json`, `tsconfig.node.json`, `vite.config.ts`, `vite-env.d.ts` → SUPPRIMER.
- `frontend/public/manifest.json`, `frontend/public/icons/*.svg` → SUPPRIMER (manifest PWA remplacé par manifest statique si besoin).
- `frontend/src/main.tsx`, `App.tsx`, `styles.css`, `types/report.ts`, `services/api.ts`, `hooks/useReports.ts`, `components/` (Header.tsx, MapView.tsx, PhotoCard.tsx, ShellLayout.tsx, Toolbar.tsx), `pages/` (DashboardPage.tsx, ReportPage.tsx, PhotosPage.tsx, TasksPage.tsx, ExportPage.tsx) → SUPPRIMER.
  - **Motif commun** : lecture seule, remplacée par templates Jinja2 + fetch server-side.
  - **Remplaçants** : `templates/*.html`, `static/js/*.js` (Vanilla) + Leaflet standard.
  - **Risques** : Moyen (perte temporaire de l’expérience SPA) → mitigé par réutilisation du design legacy.

---

## 2. Cartographie des futures fusions

| Fichier cible | Sources actuelles | Responsabilités fusionnées |
| --- | --- | --- |
| `main.py` | `backend/app/main.py`, `backend/app/api/*.py` | Configuration FastAPI (CORS, StaticFiles), routes API REST, nouvelles routes HTML (Dashboards, Photos, Tâches, PDF), montages `storage/` et `exports/` |
| `config.py` | `backend/app/core/config.py` | Chargement Settings Pydantic, définition `BASE_DIR`, `DATA_DIR`, `PHOTO_DIR`, `EXPORT_DIR`, configuration `Settings` unique |
| `database.py` | `backend/app/db/base.py`, `backend/app/db/session.py`, `backend/alembic/*` (référentiel d’informations) | Déclaration Base SQLAlchemy, engine `sqlite:///data/reports.db`, SessionLocal, création auto des tables |
| `models.py` | `backend/app/models/report.py` | ORM complet (Report, Photo, Task, Signature, enums, relations, indexes) |
| `schemas.py` | `backend/app/schemas/report.py` | Pydantic DTO pour API/Forms |
| `storage.py` | `backend/app/services/photo_storage.py` | Upload, slugification, structure de dossiers, suppression, miniatures |
| `pdf.py` | `generer_pdf.py`, `backend/app/services/pdf_service.py`, `backend/app/pdf/report.html` | Génération PDF ReportLab (couverture, sommaire, sections photos/tâches, QR code), suppression dépendance WeasyPrint |
| `templates/*.html` | `template_sans_images.html`, `frontend/src/**/*.tsx` | Découpage en templates modulaires (dashboard, report detail, photos, tasks, export) avec composants Jinja2 + JS Vanilla |
| `static/css/*`, `static/js/*`, `static/img/*` | `template_sans_images.html` (CSS/JS inline) + `frontend/src/styles.css` | Reconstitution des styles et scripts modulaires |

---

## 3. Plan de suppression React (frontend/)

| Fichier | Fonction actuelle | Remplaçant Jinja2/Vanilla | Complexité migration | Risque |
| --- | --- | --- | --- | --- |
| `frontend/src/App.tsx` | Shell + router React | `templates/base.html` + routes FastAPI | Moyenne (transposer layout) | Faible |
| `frontend/src/main.tsx` | Entrée Vite, render root | Suppression (FastAPI rend HTML) | Faible | Nul |
| `frontend/src/styles.css` | Style global (variables, cards) | `static/css/app.css` (copie adaptée) | Faible | Nul |
| `frontend/src/components/Header.tsx` | Bandeau résumé | `templates/report.html` (bloc Jinja) | Faible | Nul |
| `frontend/src/components/MapView.tsx` | Carte Leaflet (react-leaflet) | JS Vanilla Leaflet (template + `<div>`). | Moyenne (remplacer react-leaflet par Leaflet natif). | Faible |
| `frontend/src/components/PhotoCard.tsx` | Carte photo + tâches associées | Fragment Jinja `templates/_photo_card.html` | Moyenne | Faible |
| `frontend/src/components/ShellLayout.tsx` | Layout principal | `templates/base.html` | Faible | Faible |
| `frontend/src/components/Toolbar.tsx` | Navigation (tabs) | `templates/base.html` nav | Faible | Faible |
| `frontend/src/hooks/useReports.ts` | Fetch via React Query | Requêtes effectuées côté FastAPI (server render) | Faible | Nul |
| `frontend/src/services/api.ts` | Wrapper fetch | Remplacé par contrôleurs FastAPI | Faible | Nul |
| `frontend/src/pages/DashboardPage.tsx` | Liste des rapports (cartes) | `templates/reports.html` | Moyenne | Faible |
| `frontend/src/pages/ReportPage.tsx` | Vue détaillée + photos | `templates/report.html` | Moyenne | Faible |
| `frontend/src/pages/PhotosPage.tsx` | Grille photos globale | `templates/photos.html` | Faible | Faible |
| `frontend/src/pages/TasksPage.tsx` | Tableau des tâches | `templates/tasks.html` | Faible | Faible |
| `frontend/src/pages/ExportPage.tsx` | Actions export | `templates/export.html` (modal PDF) | Faible | Faible |
| `frontend/src/types/report.ts` | Typage TS | Structures Python / Pydantic | Faible | Nul |
| `frontend/Dockerfile` | Build SPA | N/A | Faible | Nul |
| `frontend/package*.json`, `tsconfig*.json`, `vite.config.ts`, `vite-env.d.ts` | Configuration toolchain | N/A | Faible | Nul |
| `frontend/public/manifest.json`, `icons/*` | PWA | Recréation facultative (Vanilla) | Faible | Nul |

Synthèse : tout le dossier `frontend/` sera supprimé après création des templates Jinja2 et JS Vanilla hérités du template legacy.

---

## 4. Plan de suppression WeasyPrint

### Fonctionnalités existantes (WeasyPrint)
- Fichier : `backend/app/services/pdf_service.py` + template `backend/app/pdf/report.html`.
- Mécanisme : charge un rapport via SQLAlchemy, rend un template Jinja2, convertit en PDF via `weasyprint.HTML.write_pdf`.
- Dépendances : `WeasyPrint`, `Jinja2`, stack native (GTK, Cairo, Pango) → difficile à packager uniformément sur Windows/Linux/Docker.

### Contraintes actuelles
- Nécessite installation de bibliothèques système (non fournies dans Docker/image Windows).
- Template HTML doit charger CSS/JS additionnels (Leaflet) → ressources externes indispensables.

### Migration vers ReportLab
- Réutiliser `generer_pdf.py` (ReportLab pur Python) pour : couverture, statistiques, sections photos, tâches, commentaires, signatures, pied de page.
- Ajouter QR code (module `reportlab.graphics.barcode.qr`), sommaire automatique (toc).
- `pdf.py` fournira une classe `PdfRenderer` exposant `render(report: Report) -> Path`.
- Les fonctions `compute_stats`, `build_styles`, `build_story`, `draw_cover`, `draw_footer` seront portées telles quelles (FUSIONNER).
- Fonctions à réécrire : chargement des images depuis stockage (chemins relatifs `storage/photos` → `BASE_DIR / storage`), injection des tâches depuis ORM plutôt que JSON, paramétrage du template (logo, couleurs) via settings.
- API `POST /reports/{id}/generate-pdf` pointera vers `pdf.py`.

---

## 5. Analyse des risques

### Critique

| Cause | Impact | Solution |
| --- | --- | --- |
| Perte de fonctionnalités lors de la migration UI (React + legacy) | Blocage utilisateur terrain | Approche incrémentale : migrer pages une par une, tests manuels + capture d’écran avant suppression React |
| Réécriture PDF (WeasyPrint → ReportLab) | PDF incomplet/invalide | Utiliser `generer_pdf.py` comme base, tests de non-régression visuelle, scripts comparatifs |

### Important

| Cause | Impact | Solution |
| --- | --- | --- |
| Changement d’emplacement DB (`storage/reports.db` → `data/reports.db`) | Perte de données si copie oubliée | Étape documentée dans DATABASE_MIGRATION.md + script de migration (copie + migration SQL) |
| Suppression Alembic | Difficulté d’évolution ultérieure | Documenter procédure future (pytest + script SQL) et prévoir adoption ultérieure de migrations Alembic après stabilisation |

### Mineur

| Cause | Impact | Solution |
| --- | --- | --- |
| Nettoyage CSS/JS du template legacy | Divergence visuelle temporaire | Auditer styles, extraire variables, vérifier sur desktop/mobile |
| Dépendances `requirements.txt` | Conflits pip | Fichier unique, pins versions, tests `pip check` |

---

## 6. Ordre exact de migration

1. **Créer la nouvelle arborescence** (`main.py`, `config.py`, `database.py`, `models.py`, `schemas.py`, `storage.py`, `pdf.py`, `templates/`, `static/`, `data/`, `storage/`).
2. **Migrer la base SQLite** (copie `storage/reports.db` → `data/reports.db`, mise à jour `DATABASE_URL`).
3. **Adapter `storage.py`** (upload photos, miniatures) et vérifier points de montage Docker (`./storage`).
4. **Intégrer ReportLab** (`pdf.py`), rebrancher l’endpoint `/generate-pdf`.
5. **Migrer les vues HTML** : conversion de `template_sans_images.html` en templates Jinja2 modulaires + JS Vanilla (Leaflet, EXIF, recap).
6. **Supprimer React/Vite** (`frontend/` complet) après validation des vues.
7. **Supprimer WeasyPrint** (`pdf_service.py`, template HTML) une fois ReportLab en place.
8. **Mettre à jour Docker Compose/Dockerfile** pour service unique FastAPI + volumes `./data`, `./storage`.
9. **Mettre à jour la documentation** (`README.md`, INSTALL, DEVELOPER_GUIDE, etc.).

---

Ce document complète ARCHITECTURE_AUDIT, PROJECT_MAP et MIGRATION_PLAN. Il sert de spécification détaillée avant toute modification de code.
