# GIT_PRE_COMMIT_AUDIT

Date : 2026-06-01

---

## 1. Fichiers ajoutés (untracked)

### Documentation
- API_IMPLEMENTATION_PLAN.md
- API_VALIDATION.md
- ARCHITECTURE_AUDIT.md
- BACKUP_AND_RESTORE.md
- CHANGELOG.md
- CLEANUP_PLAN.md
- DATABASE_MIGRATION.md
- DECOMMISSION_PLAN.md
- DOCKER_FINALIZATION.md
- END_TO_END_VALIDATION.md
- GO_NO_GO_REPORT.md
- LEGACY_USAGE_AUDIT.md
- MIGRATION_PLAN.md
- MIGRATION_READINESS_TEMPLATE.md
- MODEL_VALIDATION.md
- PDF_COMPARISON.md
- PDF_FIX_REPORT.md
- PDF_IMPORT_ANALYSIS.md
- PDF_IMPORT_FIX_REPORT.md
- PDF_LAYOUT_ANALYSIS.md
- PDF_LAYOUT_FIX_REPORT.md
- PDF_LAYOUT_ROOTCAUSE.md
- PROJECT_MAP.md
- README_PRODUCTION.md
- REFACTOR_SPEC.md
- RELEASE_CANDIDATE_REPORT.md
- SQLITE_VALIDATION.md
- STORAGE_FIX_REPORT.md
- STORAGE_VALIDATION.md
- UI_FUNCTIONAL_VALIDATION.md
- UI_VALIDATION.md
- VALIDATION_GUIDE.md
- VERSION.md

### Nouveaux modules et code source
- Makefile
- validate.ps1
- docker-compose.validation.yml

### Templates Jinja2 et UI
- backend/app/static/
- backend/app/templates/

### Tests
- backend/tests/test_api.py
- tests/

### Scripts de validation
- scripts/
- backend/debug_pdf2.py

### Autres
- field-report/
- legacy/frontend-react/
- legacy/weasyprint/
- storage/
- backend/storage/
- .gitignore
- __pycache__/
- debug_pdf.log

---

## 2. Fichiers modifiés

- README_NEW_UTF8.md
- backend/app/api/photos.py
- backend/app/api/signatures.py
- backend/app/api/tasks.py
- backend/app/main.py
- backend/app/services/pdf_service.py
- backend/app/__pycache__/main.cpython-314.pyc
- backend/app/api/__pycache__/photos.cpython-314.pyc
- backend/app/api/__pycache__/signatures.cpython-314.pyc
- backend/app/api/__pycache__/tasks.cpython-314.pyc
- backend/app/services/__pycache__/pdf_service.cpython-314.pyc
- backend/tests/__pycache__/test_api.cpython-314-pytest-9.0.2.pyc

---

## 3. Fichiers supprimés

- generer_pdf.py
- template_sans_images.html

---

## 4. Fichiers ignorés (après mise à jour .gitignore)

- __pycache__/
- *.pyc, *.pyo, *.pyd
- debug_pdf.log
- legacy-backup.zip
- storage/photos/* (sauf .gitkeep)
- storage/exports/* (sauf .gitkeep)
- backend/storage/photos/* (sauf .gitkeep)
- backend/storage/exports/* (sauf .gitkeep)
- .pytest_cache/
- .coverage
- *.db

---

## 5. Anomalies identifiées

| Anomalie | Sévérité | Action |
|----------|----------|--------|
| __pycache__ présentes dans l'arbre | Mineure | Ignorées via .gitignore, non ajoutées au commit |
| debug_pdf.log présent | Mineure | Ignoré via .gitignore |
| legacy-backup.zip présent | Mineure | Ignoré via .gitignore |
| Deux répertoires storage (racine + backend) | Mineure | Les deux sont nécessaires ; backend/storage contient reports.db en dev |

---

## 6. Synthèse

| Catégorie | Compte |
|-----------|--------|
| Documents de validation / planification | 32 |
| Nouveaux modules / scripts | 8 |
| Templates Jinja2 + static | 2 répertoires |
| Tests | 2 répertoires |
| Modifications métier | 6 fichiers Python |
| Suppressions | 2 fichiers legacy |
| Ignorés | ~15 patterns |
