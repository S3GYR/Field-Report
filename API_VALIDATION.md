# API_VALIDATION

Résultats réels après implémentation des CRUD (01/06/2026, `validate.ps1 -Target api`).

## Synthèse

- **Backend** : `backend/app/main.py` (FastAPI, SQLAlchemy 2, Pydantic v2)
- **Tests** : `backend/tests/test_api.py` + `backend/tests/test_reports_api.py`
- **Validation** : `scripts/validate_api.py` (pointe vers `backend/tests/`)
- **Résultat global** : **21 passed** — tous les endpoints CRUD sont opérationnels.

## Procédure de validation

```powershell
validate.ps1 -Target api
```

## Endpoints validés

| Ressource | Méthode | URL | Statut | Notes |
|-----------|---------|-----|--------|-------|
| reports | GET | `/api/reports/` | ✅ | Liste tous les rapports |
| reports | POST | `/api/reports/` | ✅ | Création d’un rapport |
| reports | GET | `/api/reports/{id}` | ✅ | Détail d’un rapport |
| reports | PUT | `/api/reports/{id}` | ✅ | Mise à jour partielle |
| reports | DELETE | `/api/reports/{id}` | ✅ | Suppression |
| photos | GET | `/api/photos/` | ✅ | Liste toutes les photos |
| photos | GET | `/api/photos/{id}` | ✅ | Détail d’une photo |
| photos | POST | `/api/photos/{report_id}` | ✅ | Upload fichier (fixture JPG) |
| photos | PUT | `/api/photos/{id}` | ✅ | Mise à jour métadonnées |
| photos | DELETE | `/api/photos/{id}` | ✅ | Suppression + nettoyage fichiers |
| tasks | GET | `/api/tasks/` | ✅ | Liste toutes les tâches |
| tasks | GET | `/api/tasks/{id}` | ✅ | Détail d’une tâche |
| tasks | POST | `/api/tasks/{report_id}` | ✅ | Création liée à un rapport |
| tasks | PUT | `/api/tasks/{id}` | ✅ | Mise à jour partielle |
| tasks | DELETE | `/api/tasks/{id}` | ✅ | Suppression |
| signatures | GET | `/api/signatures/` | ✅ | Liste toutes les signatures |
| signatures | GET | `/api/signatures/{report_id}` | ✅ | Détail par rapport |
| signatures | POST | `/api/signatures/{report_id}` | ✅ | Création liée à un rapport |
| signatures | PUT | `/api/signatures/{report_id}` | ✅ | Mise à jour partielle |
| signatures | DELETE | `/api/signatures/{report_id}` | ✅ | Suppression |

## Résultats des tests

```
backend/tests/test_api.py
  TestReportsCrud
    test_create_report PASSED
    test_list_reports PASSED
    test_get_report PASSED
    test_update_report PASSED
    test_delete_report PASSED
  TestPhotosCrud
    test_upload_photo PASSED
    test_list_photos PASSED
    test_get_photo PASSED
    test_update_photo PASSED
    test_delete_photo PASSED
  TestTasksCrud
    test_create_task PASSED
    test_list_tasks PASSED
    test_get_task PASSED
    test_update_task PASSED
    test_delete_task PASSED
  TestSignaturesCrud
    test_create_signature PASSED
    test_list_signatures PASSED
    test_get_signature PASSED
    test_update_signature PASSED
    test_delete_signature PASSED
  test_report_crud_flow PASSED (legacy test_reports_api.py)

21 passed, 54 warnings in 1.90s
```

## Warnings observés

- `DeprecationWarning: datetime.datetime.utcnow()` dans `app/models/report.py` et `app/services/photo_storage.py`. Non bloquant.

## Régressions

Aucune régression constatée.
