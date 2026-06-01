# MIGRATION_READINESS_TEMPLATE

## Backend

- **Status** : `NOT READY`
- **Notes** : Seule la route `/health` répond (tests CRUD inexistants, `pytest` interrompu avant toute validation fonctionnelle).

## SQLite

- **Status** : `PARTIAL`
- **Notes** : Initialisation automatique prête, mais tests CRUD non exécutés (collecte Pytest bloquée).

## Storage

- **Status** : `NOT READY`
- **Notes** : Tests `tests/test_storage.py` bloqués par `sample.jpg` Base64 invalide (aucune preuve d’upload/miniature).

## PDF

- **Status** : `NOT READY`
- **Notes** : `generer_pdf.py` contient une `SyntaxError` (ligne 509) empêchant toute génération ReportLab et comparaison avec WeasyPrint.

## API

- **Status** : `NOT READY`
- **Notes** : `/health` OK, mais routes CRUD absentes ou `pytest.skip`; aucune preuve de fonctionnement API métier.

> Mettre à jour chaque section uniquement après exécution complète des scripts/tests correspondants et en enregistrant les preuves (logs Pytest, captures, tailles de fichiers, etc.).
