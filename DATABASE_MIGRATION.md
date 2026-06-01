# DATABASE_MIGRATION

Documentation de référence pour la bascule SQLite → architecture cible, basée exclusivement sur les fichiers présents dans le dépôt (`backend/app/core/config.py`, `backend/app/models/report.py`, `backend/app/db/session.py`).

---

## 1. Analyse de la base actuelle

### Emplacement / configuration
- **URL** : `sqlite:///./storage/reports.db` (déclaré dans `backend/app/core/config.py`).
- **Chemin physique** : fichier `storage/reports.db` (non versionné, mais requis au démarrage FastAPI).
- **Initialisation** : SQLAlchemy `create_engine(..., connect_args={"check_same_thread": False})` dans `backend/app/db/session.py`.
- **Session** : `SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)`.
- **Migrations** : Alembic (fichiers `backend/alembic/*`) mais une seule version (`0001_init.py`).

### Tables effectives
D’après `backend/app/models/report.py` :
1. `reports`
2. `photos`
3. `tasks`
4. `signatures`

### Index & contraintes existantes
- `reports.number` : `unique=True`, `index=True` (identifiant métier).
- `reports.status` : `index=True`.
- `photos.report_id` : `ForeignKey` + `index=True`.
- `tasks.report_id`, `tasks.photo_id`, `tasks.status` : `index=True`.
- `signatures.report_id` : `unique=True` (relation 1‑1).
- Clés étrangères définies avec `ondelete="CASCADE"` (report → photo/task/signature) et `ondelete="SET NULL"` (task.photo_id).

---

## 2. Schéma actuel détaillé

### Table `reports`
| Champ | Type SQLAlchemy | Null | PK | Contraintes |
| --- | --- | --- | --- | --- |
| id | Integer | Non | Oui | Auto-incr. |
| number | String(50) | Non | Non | `unique=True`, `index=True` |
| visit_date | Date | Non | Non | — |
| client | String(120) | Non | Non | — |
| site | String(240) | Non | Non | — |
| weather | Enum(WeatherType) | Oui (default unknown) | Non | — |
| comments | Text | Oui | Non | — |
| status | Enum(ReportStatus) | Oui (default draft) | Non | `index=True` |
| created_at | DateTime | Non | Non | default `datetime.utcnow` |
| updated_at | DateTime | Non | Non | default + `onupdate` `datetime.utcnow` |

### Table `photos`
| Champ | Type | Null | PK | Contraintes |
| --- | --- | --- | --- | --- |
| id | Integer | Non | Oui | Auto-incr. |
| report_id | ForeignKey("reports.id") | Non | Non | `ondelete="CASCADE"`, `index=True` |
| filename | String(255) | Non | Non | — |
| filepath | String(500) | Non | Non | — |
| thumbnail_path | String(500) | Oui | Non | — |
| gps_lat | Float | Oui | Non | — |
| gps_lng | Float | Oui | Non | — |
| comment | Text | Oui | Non | — |
| priority | Enum(PhotoPriority) | Oui (default none) | Non | — |

### Table `tasks`
| Champ | Type | Null | PK | Contraintes |
| --- | --- | --- | --- | --- |
| id | Integer | Non | Oui | Auto-incr. |
| report_id | ForeignKey("reports.id") | Non | Non | `ondelete="CASCADE"`, `index=True` |
| photo_id | ForeignKey("photos.id") | Oui | Non | `ondelete="SET NULL"`, `index=True` |
| description | Text | Non | Non | — |
| status | Enum(TaskStatus) | Oui (default todo) | Non | `index=True` |
| estimated_cost | Numeric(12,2) | Oui | Non | — |
| estimated_duration | Float | Oui | Non | — |

### Table `signatures`
| Champ | Type | Null | PK | Contraintes |
| --- | --- | --- | --- | --- |
| id | Integer | Non | Oui | Auto-incr. |
| report_id | ForeignKey("reports.id") | Non | Non | `unique=True`, `ondelete="CASCADE"` |
| name | String(120) | Non | Non | — |
| role | String(120) | Oui | Non | — |
| signed_on | Date | Oui | Non | — |
| signature_image | String(500) | Oui | Non | — |

Relations :
- `Report.photos`, `Report.tasks`, `Report.signature` (cascade `all, delete-orphan`).
- `Photo.tasks` (cascade `all, delete-orphan`).

---

## 3. Schéma cible (SQLite `data/reports.db`)

Champs conservés : intégralité des colonnes actuelles pour Report, Photo, Task, Signature.

Champs ajoutés (prévision) :
- `reports.latitude` / `reports.longitude` : NON VÉRIFIÉ (à confirmer selon besoins).
- `reports.version` : NON VÉRIFIÉ (pour audit éventuel).

Champs supprimés : aucun prévu (continuité métier).

Modifications structurelles :
1. **Emplacement DB** : `sqlite:///data/reports.db` (utiliser `DATA_DIR = BASE_DIR / "data"`).
2. **Initialisation** : création automatique des répertoires `data/` / `storage/` via `pathlib` (cf. instructions target).
3. **Migrations futures** : script unique gérant `Base.metadata.create_all(bind=engine)` au premier démarrage.

---

## 4. Compatibilité future PostgreSQL

Objectif long terme : permettre `DATABASE_URL=postgresql+psycopg://...` sans réécriture métier.

Recommandations :
- Utiliser `sqlalchemy.URL` pour construire la chaîne (évite litteral string).
- Privilégier types génériques : `String`, `Text`, `Date`, `DateTime`, `Numeric` déjà compatibles PostgreSQL.
- Conserver `server_default` explicites (ex. `func.now()`) si ajoutés ultérieurement.
- Prévoir un script `alembic revision --autogenerate` une fois la refonte stabilisée pour basculer vers migrations réelles.
- Lors du passage SQLite → PostgreSQL :
  1. Export via `sqlite3 data/reports.db .dump > backup.sql`.
  2. Import dans PostgreSQL (adaptation `PRAGMA` -> `SET`, `AUTOINCREMENT` -> sequences).
  3. Tester via `pytest`/CI avant bascule.

---

## 5. Sauvegarde & restauration

### Données critiques
- `data/reports.db` (nouvel emplacement).
- `storage/photos/` (originaux + miniatures).
- `storage/exports/` (PDF générés).

### Procédure de sauvegarde
1. Arrêter l’application (`docker compose down` ou service FastAPI).
2. Copier les dossiers via OS ou script :
   ```bash
   tar czf backup-fieldreport-$(date +%Y%m%d).tar.gz data/ storage/
   ```
3. Stocker l’archive sur un support externe.

### Restauration / reprise après incident
1. Décompresser l’archive dans un dossier propre (`data/`, `storage/`).
2. Vérifier les permissions (FastAPI doit pouvoir écrire).
3. Relancer `docker compose up -d` (volumes montés sur `./data:/app/data`, `./storage:/app/storage`).
4. Vérifier l’accès aux rapports existants (consultation + génération PDF).

---

## 6. Validation

### Diagramme relationnel (ASCII)
```
Report (1)
  ├──< Photo (N)
  │       └──< Task (N) [optionnel via photo_id]
  ├──< Task (N)
  └─── Signature (1)
```

### Contraintes
- `reports.number` UNIQUE.
- `photos.report_id` FK CASCADE.
- `tasks.report_id` FK CASCADE.
- `tasks.photo_id` FK SET NULL.
- `signatures.report_id` FK CASCADE + UNIQUE (one-to-one).

### Index
- `reports.number` (unique index).
- `reports.status`.
- `photos.report_id`.
- `tasks.report_id`, `tasks.photo_id`, `tasks.status`.
- (Option) `reports.visit_date` → NON VÉRIFIÉ (index non défini actuellement).

Validation finale :
1. Lancer `Base.metadata.create_all(bind=engine)` sur un environnement propre (création tables dans `data/reports.db`).
2. Executer `pytest backend/tests/test_reports_api.py` pour vérifier CRUD.
3. Tester une génération PDF (nouveau service ReportLab) pour s’assurer que les relations fonctionnent (Report → Photo/Task/Signature).

---

Tout élément marqué **NON VÉRIFIÉ** nécessite confirmation pendant la mise en œuvre. Aucun fichier source n’a été modifié.
