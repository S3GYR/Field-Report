# MODEL_VALIDATION

Ce document sera rempli après exécution réelle des tests CRUD (rapports, photos, tâches, signatures). Aucune donnée n’a été inventée.

## Configuration utilisée

- Application : FieldReport (nouvelle architecture).
- Base : `data/reports.db` (ou fallback `storage/reports.db`).
- Procédures exécutées :
  1. `powershell ./validate.ps1 -Target db` (01/06/2026 01:20) → `tests/test_database.py ... 3 passed` (validation du schéma, tables, metadata).
  2. `python -m pytest tests -v` (01/06/2026 01:13) → échec pendant la collecte :
     - `tests/test_pdf.py` → import `generer_pdf.py` lève `SyntaxError` (parenthèse fermante `)` ne correspondant pas au `[` ligne 509).
     - `tests/test_storage.py` → échantillon `sample.jpg` Base64 invalide (`number of data characters (469) cannot be 1 more than a multiple of 4`).
     → Collecte interrompue, aucun test CRUD lancé.

## Report

| Opération | Résultat | Notes |
| --- | --- | --- |
| Create | NON TESTÉ | Bloqué par `SyntaxError` dans `generer_pdf.py`. |
| Read | NON TESTÉ | Bloqué par `SyntaxError` dans `generer_pdf.py`. |
| Update | NON TESTÉ | Bloqué par `SyntaxError` dans `generer_pdf.py`. |
| Delete | NON TESTÉ | Bloqué par `SyntaxError` dans `generer_pdf.py`. |

## Photo

| Opération | Résultat | Notes |
| --- | --- | --- |
| Create | NON TESTÉ | Collecte Pytest interrompue (erreurs PDF/Storage). |
| Read | NON TESTÉ | Collecte Pytest interrompue (erreurs PDF/Storage). |
| Update | NON TESTÉ | Collecte Pytest interrompue (erreurs PDF/Storage). |
| Delete | NON TESTÉ | Collecte Pytest interrompue (erreurs PDF/Storage). |

## Task

| Opération | Résultat | Notes |
| --- | --- | --- |
| Create | NON TESTÉ | Collecte Pytest interrompue (erreurs PDF/Storage). |
| Read | NON TESTÉ | Collecte Pytest interrompue (erreurs PDF/Storage). |
| Update | NON TESTÉ | Collecte Pytest interrompue (erreurs PDF/Storage). |
| Delete | NON TESTÉ | Collecte Pytest interrompue (erreurs PDF/Storage). |

## Signature

| Opération | Résultat | Notes |
| --- | --- | --- |
| Create | NON TESTÉ | Collecte Pytest interrompue (erreurs PDF/Storage). |
| Read | NON TESTÉ | Collecte Pytest interrompue (erreurs PDF/Storage). |
| Update | NON TESTÉ | Collecte Pytest interrompue (erreurs PDF/Storage). |
| Delete | NON TESTÉ | Collecte Pytest interrompue (erreurs PDF/Storage). |

> Compléter chaque cellule avec les logs réels (horodatage, ID, éventuelles erreurs) lorsque les tests CRUD auront été exécutés via l’API ou Pytest.
