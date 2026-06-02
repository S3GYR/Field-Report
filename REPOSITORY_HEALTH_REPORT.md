# REPOSITORY_HEALTH_REPORT

FieldReport — Audit de santé du dépôt
Date : 2026-06-01

---

## 1. Structure du dépôt

```
fieldreport/
  .gitignore              -> Exclusions (Python, Node, IDE, storage)
  backend/
    app/
      api/                -> Routes FastAPI (reports, photos, tasks, signatures)
      db/                 -> Engine, session, base SQLAlchemy
      models/             -> ORM (Photo, Report, Signature, Task)
      schemas/            -> Pydantic
      services/           -> PDF (ReportLab), photo storage
      static/css/         -> Styles UI
      static/js/          -> Client API vanilla
      templates/          -> Jinja2 (dashboard, reports, photos, tasks, signatures)
      main.py             -> Point d'entrée FastAPI
    tests/                -> Tests pytest API + reports
    Dockerfile            -> Image backend
    requirements.txt      -> Dépendances Python
  frontend/               -> React legacy (non servi)
  field-report/           -> Code legacy (modèles, PDF, storage)
  legacy/                 -> Dirs préparés pour archivage
    frontend-react/
    weasyprint/
  scripts/                -> Scripts de validation
  storage/                -> SQLite + photos + exports
  tests/                  -> Tests validation (database, PDF, storage, API)
  docker-compose.yml      -> Backend + Frontend (legacy)
  docker-compose.validation.yml
  validate.ps1
  Makefile
  README_PRODUCTION.md
  (33 documents de planification/validation)
```

---

## 2. Qualité du .gitignore

| Règle | Présente | Efficace |
|-------|----------|----------|
| `__pycache__/` | Oui | Oui |
| `*.pyc` / `*.pyo` / `*.pyd` | Oui | Oui |
| `node_modules/` | Oui | Oui |
| `frontend/node_modules/` | Oui | Oui |
| `*.log` | Oui | Oui |
| `*.db` | Oui | Oui (mais empêche versionner une base seed) |
| `storage/photos/*` | Oui | Oui |
| `storage/exports/*` | Oui | Oui |
| `.gitkeep` conservés | Oui | Oui |

**Points faibles** :
- Pas de règle pour `.env` / `.env.local`
- Pas de règle pour `*.sqlite3`
- Pas de règle pour les artefacts de couverture `htmlcov/`

---

## 3. Organisation docs/

Pas de répertoire `docs/` dédié. Les documents sont à la racine.

| Type | Compte | Exemples |
|------|--------|----------|
| Validation | 7 | API_VALIDATION, UI_FUNCTIONAL_VALIDATION, END_TO_END_VALIDATION |
| Planification | 8 | MIGRATION_PLAN, DECOMMISSION_PLAN, CLEANUP_PLAN |
| Audit | 6 | ARCHITECTURE_AUDIT, LEGACY_USAGE_AUDIT, GIT_RELEASE_AUDIT |
| Rapports | 5 | RELEASE_CANDIDATE_REPORT, PDF_FIX_REPORT, STORAGE_FIX_REPORT |
| Guides | 5 | README_PRODUCTION, BACKUP_AND_RESTORE, DOCKER_FINALIZATION |
| Versioning | 3 | VERSION, CHANGELOG, GIT_RELEASE_REPORT |

**Constat** : ~35 documents à la racine. Difficile à naviguer. Un répertoire `docs/` serait préférable.

---

## 4. Organisation tests/

| Répertoire | Contenu | Qualité |
|------------|---------|---------|
| `backend/tests/` | `conftest.py`, `test_api.py`, `test_reports_api.py` | Bon (pytest, fixtures) |
| `tests/` | `test_api.py`, `test_database.py`, `test_pdf.py`, `test_storage.py` | Acceptable mais doublon partiel |

**Anomalies** :
- `tests/test_api.py` semble doublonner `backend/tests/test_api.py`
- Pas de tests pour l'UI Jinja2 (pas critique car c'est du rendu serveur)
- Pas de tests unitaires pour le PDF service

---

## 5. Organisation scripts/

| Script | Rôle | Qualité |
|--------|------|---------|
| `validate_api.py` | Wrapper pytest API | OK |
| `validate_database.py` | Wrapper pytest DB | OK |
| `validate_pdf.py` | Wrapper pytest PDF | OK |
| `validate_storage.py` | Wrapper pytest storage | OK |
| `validate_end_to_end.py` | Scénario E2E complet | Bien (testClient, assertions) |
| `validate_ui_functional.py` | Test UI fonctionnelle | Bien (TestClient + assert) |
| `pdf_layout_probe.py` | Debug layout PDF | OK (outil) |

**Constat** : Organisation cohérente. Les wrappers pourraient être factorisés en une CLI unique.

---

## 6. Cohérence Docker

| Élément | État | Note |
|---------|------|------|
| `backend/Dockerfile` | Fonctionnel | Image python:3.11-slim, UV, port 8200 |
| `docker-compose.yml` | **Legacy** | Contient encore le service `frontend` React |
| `docker-compose.validation.yml` | Fonctionnel | Backend seul pour validation |

**Anomalies** :
- `docker-compose.yml` (principal) inclut le service `frontend` obsolète. `DOCKER_FINALIZATION.md` préconise un compose sans frontend, mais le fichier n'a pas été modifié.
- `backend/Dockerfile` n'installe pas ReportLab (librairie système pour Pillow/ReportLab). Fonctionne si les libs sont suffisantes, mais fragile.
- `weasyprint==62.3` encore dans `requirements.txt`. Inutilisé mais installé dans l'image Docker.

---

## 7. Notes sur 10

| Domaine | Note | Justification |
|---------|------|---------------|
| **Architecture** | 8/10 | Clean separation API/services/templates. Points perdus : 2 storage dirs (racine + backend), duplication field-report/legacy, docker-compose legacy. |
| **Documentation** | 7/10 | Complète (~35 docs) mais dispersée à la racine. Pas de centralisation. Certains docs ont des encodages mixtes (entités HTML). |
| **Tests** | 6/10 | 21 tests API PASS. Doublon tests/. Pas de tests UI Jinja2, pas de tests PDF unitaires. Pas de CI/CD. |
| **Docker** | 6/10 | Dockerfile OK mais docker-compose.yml legacy. Pas de healthcheck dans le compose actuel. WeasyPrint encore installé. |
| **Git** | 7/10 | node_modules nettoyé. .gitignore correct. Mais .env non ignoré. Pas de branche `dev`. Commit RC1 non sur `main` (branche `v1.0.1-dev`). |
| **Maintenabilité** | 7/10 | Stack Python simple (FastAPI/SQLAlchemy). Code lisible. Mais : édition inline via `prompt()`, pas de pagination, pas d'auth, pas de linter/formatter configuré. |

**Moyenne globale** : **6.8 / 10**

---

## 8. Recommandations prioritaires

1. **Réorganiser les documents** dans un répertoire `docs/` par thème (validation, audit, guides)
2. **Corriger `docker-compose.yml`** pour retirer le service `frontend` (prendre celui de `DOCKER_FINALIZATION.md`)
3. **Retirer `weasyprint`** de `requirements.txt`
4. **Fusionner `tests/` et `backend/tests/`** ou clarifier la distinction
5. **Ajouter un `.env.example`** et ignorer `.env`
6. **Ajouter un healthcheck** au Dockerfile / docker-compose
7. **Configurer un linter** (ruff ou black) et un formatter
