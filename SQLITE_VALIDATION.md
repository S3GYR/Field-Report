# SQLITE_VALIDATION

## Contexte

- Nouvelle architecture : `field-report/` (configs centralisées).
- Objectif : basculer vers `data/reports.db` tout en conservant `storage/reports.db` pour rétrocompatibilité.

## Étapes réalisées

1. Ajout des constantes `BASE_DIR`, `DATA_DIR`, `DEFAULT_DB_PATH`, `LEGACY_DB_PATH` dans `field-report/config.py` @field-report/config.py#9-42.
2. Création automatique des dossiers (`data/`, `storage/`, `templates/`, `static/`).
3. Mécanisme d’auto-détection : si `storage/reports.db` existe et `data/reports.db` absent → `database_url` pointe vers la base legacy (aucune copie destructrice) @field-report/config.py#36-42.
4. `database.py` (nouveau) déclare `Base` et `init_db()` qui fait un `Base.metadata.create_all(bind=engine)` @field-report/database.py#5-25.
5. Compilation Python (`python -m compileall field-report`) pour s’assurer que les modules sont valides.
6. **Validation réelle** : `powershell ./validate.ps1 -Target db` (01/06/2026 01:20) → `tests/test_database.py ... 3 passed` (tables présentes, colonnes attendues, metadata complète).

## Vérifications

| Action | Résultat |
| --- | --- |
| Vérifier création auto `data/` | ✅ dossier present (avec `.gitkeep`). |
| Vérifier `storage/` existant | ✅ (hérite des données legacy, aucune suppression). |
| Vérifier `field-report/config.py` compile | ✅ par `python -m compileall`. |
| Vérifier `init_db()` | ✅ via `tests/test_database.py`. |

## Comparaison schéma

- Schéma SQLAlchemy `field-report/models.py` = copie conforme de `backend/app/models/report.py` (mêmes types, indexes, FK). @field-report/models.py#1-74.
- Aucun champ supprimé ou ajouté (conformité confirmée par lecture diff).  
- Index/contrainte identiques : `number` unique/index, `status` index, FK cascade.

## Points restants / TODO

- Exécuter `init_db()` sur un run FastAPI pour générer `data/reports.db` (sera validé pendant les tests CRUD).  
- Préparer script de migration si l’on veut copier `storage/reports.db` → `data/reports.db` (non implémenté, mentionné dans DATABASE_MIGRATION.md).  
- Documenter procédure dans README (à faire plus tard).

## Conclusion
La configuration SQLite côté nouvelle architecture est prête : `data/reports.db` devient la cible par défaut, tout en restant compatible avec la base legacy. Validation complète (création effective + tests CRUD) sera réalisée dans les étapes suivantes.
