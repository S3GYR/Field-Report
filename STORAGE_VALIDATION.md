# STORAGE_VALIDATION

Exécution réelle : `powershell ./validate.ps1 -Target storage` (01/06/2026 01:34, Windows 11). Résultat Pytest : `tests/test_storage.py ... 3 passed` (jpg/png/webp). Avertissements uniquement sur l’usage de `datetime.utcnow()`.

## Formats testés

| Format | Résultat | Notes |
| --- | --- | --- |
| jpg | ✅ | Upload + miniature + suppression OK (fixture `tests/assets/sample.jpg`). |
| png | ✅ | Upload + miniature + suppression OK (fixture `tests/assets/sample.png`). |
| webp | ✅ | Upload + miniature + suppression OK (fixture `tests/assets/sample.webp`). |

## Plateformes

| Plateforme | Résultat | Notes |
| --- | --- | --- |
| Windows 11 | ✅ | `validate.ps1 -Target storage` → Pytest 3/3 PASS. |
| Ubuntu/Debian/Fedora | NON TESTÉ | Tests non exécutés. |
| Docker Desktop/Engine | NON TESTÉ | Tests non exécutés. |

## Checklist

- Upload image ✅ (3 formats).
- Miniature générée ✅ (jpg/png/webp).
- Lecture image ✅ (vérification par lecture disque et métadonnées retournées).
- Suppression image ✅ (fichiers + miniatures supprimés).

> Cochez chaque case avec les résultats réels (et ajoutez les chemins/horodatages) dès que les scripts auront été exécutés.
