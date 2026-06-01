# VALIDATION_GUIDE

Plan d’exécution de la chaîne de validation FieldReport (nouvelle architecture). Aucun test n’est exécuté automatiquement ici ; ce document décrit comment lancer les validations réelles.

## 1. Pré-requis

- Python 3.11+ (exécution locale).
- Dépendances installées : `pip install -r backend/requirements.txt` (FastAPI, SQLAlchemy, Pillow, ReportLab, Pytest…)
- Accès en écriture à `field-report/data` et `field-report/storage` (créés automatiquement au besoin).
- Optionnel : Docker / Docker Compose.

## 2. Structure tests/scripts

| Domaine | Pytest | Script helper | Makefile | PowerShell | Description |
| --- | --- | --- | --- | --- | --- |
| Base de données | `tests/test_database.py` | `python scripts/validate_database.py` | `make validate-db` | `./validate.ps1 -Target db` | Vérifie `init_db`, tables, indexes |
| Storage | `tests/test_storage.py` | `python scripts/validate_storage.py` | `make validate-storage` | `./validate.ps1 -Target storage` | Upload/miniature/suppression multi-format |
| PDF | `tests/test_pdf.py` | `python scripts/validate_pdf.py` | `make validate-pdf` | `./validate.ps1 -Target pdf` | Génération ReportLab (données factices) |
| API | `tests/test_api.py` | `python scripts/validate_api.py` | `make validate-api` | `./validate.ps1 -Target api` | Santé API + placeholders CRUD |

## 3. Exécution locale

```bash
# Exemple : validation complète
pip install -r backend/requirements.txt
make validate-all
```

Chaque cible `make validate-*` lance le script dédié (qui appelle Pytest). Exécution manuelle possible :

```bash
python scripts/validate_database.py
python scripts/validate_storage.py
python scripts/validate_pdf.py
python scripts/validate_api.py
```

## 4. Exécution PowerShell

```powershell
# Exécution globale
./validate.ps1 -Target all

# Exemple ciblé (storage uniquement)
./validate.ps1 -Target storage
```

## 5. Docker Compose validation

```bash
docker compose -f docker-compose.validation.yml up --build
```

Le service `validation` installe les dépendances puis exécute `pytest tests`. Monter les volumes permet de récupérer les rapports (fichiers `*.xml`, logs Pytest, etc.).

## 6. Résultats attendus / critères

- **DATABASE** : `tests/test_database.py` doit confirmer la présence des tables `reports/photos/tasks/signatures`. Toute erreur doit être consignée dans `MODEL_VALIDATION.md`.
- **STORAGE** : chaque format (`jpg`, `jpeg`, `png`, `webp`) doit produire un fichier et une miniature `.thumb.jpg`. Les échecs sont à reporter dans `STORAGE_VALIDATION.md`.
- **PDF** : `tests/test_pdf.py` doit générer un PDF non vide. Comparaison ReportLab vs WeasyPrint à documenter dans `PDF_COMPARISON.md`.
- **API** : le test `/health` doit réussir. Les tests CRUD sont pour l’instant marqués `pytest.skip` jusqu’à implémentation complète ; une fois prêts, mettre à jour `API_VALIDATION.md`.

## 7. Conservation des preuves

- Exporter les logs Pytest (`pytest -q --maxfail=1 --disable-warnings --log-cli-level=INFO`).
- Capturer la taille/horodatage des fichiers générés (PDF, images, base SQLite) pour alimenter les rapports `SQLITE_VALIDATION.md`, `MODEL_VALIDATION.md`, `STORAGE_VALIDATION.md`, `PDF_COMPARISON.md`, `API_VALIDATION.md` et `MIGRATION_READINESS_TEMPLATE.md`.

> Toute mesure non réalisée doit être explicitement notée comme `NON TESTÉ` dans les rapports.
