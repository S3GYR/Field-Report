# API_IMPLEMENTATION_PLAN

## Contexte

Le moteur PDF ReportLab est validé. La priorité passe à l'API métier FastAPI (`backend/`).

L'objectif est de rendre opérationnels les CRUD complets (Reports, Photos, Tasks, Signatures) et de les valider via `validate.ps1 -Target api`.

## Architecture cible

- **Backend** : `backend/app/` — FastAPI, SQLAlchemy 2, Pydantic v2
- **Tests** : `tests/test_api.py` — pointe vers `backend/app/main.py`
- **Validation** : `scripts/validate_api.py` — exécute `tests/test_api.py`

## État actuel

### Routes existantes (`backend/app/api/`)

| Domaine | Endpoint | Méthode | Statut |
|---------|----------|---------|--------|
| Reports | `/api/reports/` | GET, POST | ✅ |
| Reports | `/api/reports/{id}` | GET, PUT, DELETE | ✅ |
| Reports | `/api/reports/{id}/generate-pdf` | POST | ✅ |
| Photos | `/api/photos/{report_id}` | POST | ✅ (upload) |
| Photos | `/api/photos/{photo_id}` | DELETE | ✅ |
| Photos | `/api/photos/` | GET | ❌ |
| Photos | `/api/photos/{photo_id}` | GET, PUT | ❌ |
| Tasks | `/api/tasks/{report_id}` | POST | ✅ |
| Tasks | `/api/tasks/{task_id}` | PUT, DELETE | ✅ |
| Tasks | `/api/tasks/` | GET | ❌ |
| Tasks | `/api/tasks/{task_id}` | GET | ❌ |
| Signatures | `/api/signatures/{report_id}` | POST, PUT, DELETE | ✅ |
| Signatures | `/api/signatures/` | GET | ❌ |
| Signatures | `/api/signatures/{signature_id}` | GET | ❌ |

### Tests actuels

- `backend/tests/test_reports_api.py` : test CRUD Reports (fonctionnel)
- `tests/test_api.py` : teste `field-report/main.py` (ancien backend, CRUD non implémentés)
- `scripts/validate_api.py` : exécute `tests/test_api.py`

## Plan d'implémentation

### Phase 1 — Reports

1. Vérifier que `backend/app/api/reports.py` est complet (déjà OK).
2. Créer / mettre à jour `tests/test_api.py` pour pointer vers `backend/app/main.py`.
3. Implémenter le test CRUD Reports dans `tests/test_api.py`.
4. Exécuter `validate.ps1 -Target api`.
5. Mettre à jour `API_VALIDATION.md`.

### Phase 2 — Photos

1. Compléter `backend/app/api/photos.py` :
   - `GET /api/photos/` — lister les photos
   - `GET /api/photos/{photo_id}` — récupérer une photo
   - `PUT /api/photos/{photo_id}` — mettre à jour une photo
2. Implémenter le test CRUD Photos dans `tests/test_api.py`.
3. Exécuter `validate.ps1 -Target api`.
4. Mettre à jour `API_VALIDATION.md`.

### Phase 3 — Tasks

1. Compléter `backend/app/api/tasks.py` :
   - `GET /api/tasks/` — lister les tâches
   - `GET /api/tasks/{task_id}` — récupérer une tâche
2. Implémenter le test CRUD Tasks dans `tests/test_api.py`.
3. Exécuter `validate.ps1 -Target api`.
4. Mettre à jour `API_VALIDATION.md`.

### Phase 4 — Signatures

1. Compléter `backend/app/api/signatures.py` :
   - `GET /api/signatures/` — lister les signatures
   - `GET /api/signatures/{signature_id}` — récupérer une signature
   (ou `GET /api/signatures/report/{report_id}` selon le pattern existant)
2. Implémenter le test CRUD Signatures dans `tests/test_api.py`.
3. Exécuter `validate.ps1 -Target api`.
4. Mettre à jour `API_VALIDATION.md`.

### Phase 5 — Validation globale

1. Exécuter `validate.ps1 -Target api` sur l'ensemble des tests.
2. Vérifier qu'aucun test n'est skipped.
3. Produire le résumé final dans `API_VALIDATION.md`.

## Contraintes

- Ne pas modifier `field-report/pdf.py` ni `legacy/generer_pdf.py` (sauf bug critique).
- Ne pas supprimer le frontend React pour l'instant.
- Conserver la compatibilité avec le schéma de base de données existant (`backend/app/models/report.py`).
- Les tests doivent utiliser une base SQLite en mémoire via `TestClient`.

## Livrables

- `API_IMPLEMENTATION_PLAN.md` (ce document)
- `tests/test_api.py` (mis à jour avec CRUD complets)
- `API_VALIDATION.md` (mis à jour après chaque phase)
