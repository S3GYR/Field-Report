# FINAL_ARCHITECTURE_REVIEW

FieldReport v1.1 RC1 — Audit architecture finale
Date : 2026-06-02
Auditeur : Architecte logiciel senior

---

## 1. Vue d'ensemble

FieldReport v1.1 est une application monolithique Python/FastAPI avec une base SQLite embarquée, servie via Jinja2 templates et une UI vanilla JS. Elle est conteneurisée avec Docker Compose.

---

## 2. Cohérence globale

| Critère | Évaluation | Justification |
|---------|------------|---------------|
| Stack cohérente | **PASS** | FastAPI + SQLAlchemy + Pydantic + Jinja2 + ReportLab + Pillow. Toutes les technologies sont compatibles et bien intégrées. |
| Séparation des couches | **PASS** | API (`backend/app/api/`), modèles (`models/`), schémas (`schemas/`), services (`services/`), templates (`templates/`). Séparation MVC respectée. |
| Cohérence navigation | **PASS** | Layout commun (`layout.html`), routing FastAPI cohérent (`/`, `/reports`, `/photos`, `/tasks`, `/signatures`, `/history`). |
| Données métier | **PASS** | 4 entités (Report, Photo, Task, Signature) avec relations SQLAlchemy correctes (`cascade="all, delete-orphan"`). |

---

## 3. Maintenabilité

### Points positifs

- **Code Python moderne** : annotations de type (`from __future__ import annotations`), SQLAlchemy 2.0 avec `Mapped`, Pydantic v2.
- **Chemins absolus** : `BASE_DIR = pathlib.Path(__file__).resolve().parent` dans `main.py` évite les erreurs de chemin.
- **Healthcheck** : endpoint `/health` intégré, utilisé par Docker.
- **Modularité** : chaque entité a son router API, son modèle, son schéma.

### Points de vigilance

| Problème | Fichier | Impact | Recommandation |
|----------|---------|--------|----------------|
| `datetime.utcnow()` déprécié | `backend/app/models/report.py:51-53`, `photo_storage.py:34,43` | Warnings pytest, risque de suppression future | Migrer vers `datetime.now(datetime.timezone.utc)` |
| Pas de typing strict sur certains retours API | `backend/app/api/photos.py:42` `list[PhotoResponse]` vs `List[PhotoResponse]` | Inconsistance mineure | Standardiser sur `list[]` (Python 3.9+) |
| CORS `allow_origins=["*"]` | `backend/app/main.py:23` | Pas de restriction domaine | Voir SECURITY_AUDIT_FINAL.md |
| Pas de middleware de logging des requêtes | — | Difficulté de traçabilité | Ajouter un middleware de log minimal |

---

## 4. Dette technique

| Élément | Sévérité | Fichier | Description |
|---------|----------|---------|-------------|
| `datetime.utcnow()` | **Low** | `models/report.py`, `photo_storage.py` | DeprecationWarning, non bloquant |
| Pas de `.env` exemple | **Low** | — | Variables dans `docker-compose.yml` et code, pas de surcharge facile |
| Pas de gestion de migrations auto | **Medium** | `alembic/` existe mais non documenté | La base est créée via `Base.metadata.create_all()` |
| Docker `restart: unless-stopped` | **Low** | `docker-compose.yml:24` | Le conteneur ne redémarre pas après un reboot si explicitement arrêté. `always` serait plus robuste. |
| Pas de limite mémoire/CPU Docker | **Low** | `docker-compose.yml` | Le conteneur peut consommer toutes les ressources |

---

## 5. Risques de panne

| Risque | Probabilité | Impact | Mitigation actuelle | Recommandation |
|--------|-------------|--------|---------------------|----------------|
| Corruption SQLite (accès concurrent) | Medium | **Critique** | `check_same_thread=False` | `HIGH` — Ne pas utiliser par >1 utilisateur simultané. Documenter clairement. |
| Perte volume Docker | Faible | **Critique** | Bind-mount `./storage` | `HIGH` — Documenter le chemin absolu en production. Backup quotidien. |
| Crash conteneur | Faible | Medium | `restart: unless-stopped` | `MEDIUM` — Passer à `always`. Configurer healthcheck alerte. |
| Fuite mémoire Pillow | Très faible | Faible | — | `LOW` — Monitorer `docker stats` |
| Dépendance ReportLab bloquante | Faible | Faible | Image Docker figée | `LOW` — Version fixée dans `requirements.txt` |

---

## 6. Dépendances critiques

| Package | Usage | Risque si indisponible | Mitigation |
|---------|-------|------------------------|------------|
| FastAPI 0.111.0 | Framework web | Application hors service | Version fixée, image Docker |
| SQLAlchemy 2.0.30 | ORM | Pas de persistance | Version fixée |
| ReportLab 4.4.0 | PDF | Pas de génération PDF | Version fixée |
| Pillow 10.3.0 | Images | Pas de thumbnails | Version fixée, fallback copie fichier |
| Uvicorn 0.30.0 | Serveur ASGI | Application inaccessible | Version fixée |

Aucune dépendance externe au runtime (pas de DB externe, pas de Redis, pas de message queue).

---

## 7. Gestion des erreurs

| Couche | Évaluation | Détail |
|--------|------------|--------|
| API (404) | **PASS** | Toutes les routes vérifient l'existence de l'entité avant opération (`db.get(...)`, `raise HTTPException(404, ...)`). |
| API (500) | **PARTIEL** | Pas de catch-all d'exception. Une erreur inattendue renvoie une stack trace brute en JSON (mode dev FastAPI par défaut). |
| Upload fichier | **PARTIEL** | Pas de validation de taille côté endpoint (`photo_max_size_mb` existe dans config mais n'est pas vérifié dans `upload_photo`). |
| UI JavaScript | **PASS** | `try/catch` sur tous les appels API, toast d'erreur affiché à l'utilisateur. |
| PDF génération | **PARTIEL** | `ValueError` catché et transformé en 404. Mais une erreur ReportLab inattendue crasherait le thread. |

---

## 8. Stockage

| Aspect | Évaluation | Justification |
|--------|------------|---------------|
| Organisation fichiers | **PASS** | Photos triées par `YYYY/MM/`, thumbnails co-localisés, noms slugifiés avec timestamp. |
| Nommage sécurisé | **PASS** | `_slugify()` supprime les caractères spéciaux, normalise Unicode, ajoute timestamp pour unicité. |
| Gestion suppression | **PASS** | `photo_storage.delete()` supprime l'original ET le thumbnail. |
| Taille max config | **PASS** | `photo_max_size_mb: int = 15` défini dans `config.py`. |
| Taille max appliquée | **FAIL** | Cette valeur n'est **pas** vérifiée dans l'endpoint `upload_photo`. L'utilisateur peut uploader un fichier de n'importe quelle taille. |

---

## 9. Conclusion architecture

| Domaine | Note /10 | Justification |
|---------|----------|---------------|
| Cohérence globale | 8 | Stack cohérente, séparation des couches respectée |
| Maintenabilité | 7 | Code moderne, mais `utcnow()` déprécié et manque de middleware logging |
| Dette technique | 7 | Peu de dette, mais migrations et `.env` manquants |
| Risques de panne | 6 | SQLite concurrent = risque majeur si multi-utilisateur |
| Gestion des erreurs | 6 | 404 bien gérés, mais pas de catch-all et pas de limite upload |
| Stockage | 7 | Bonne organisation, mais limite taille non appliquée |

**Note moyenne architecture : 6.8/10**

### Recommandations classées

**Critique**
- Documenter clairement que SQLite ne supporte pas l'accès concurrent en écriture
- Ajouter la vérification `photo_max_size_mb` dans l'endpoint upload

**Important**
- Migrer `datetime.utcnow()` vers `datetime.now(datetime.timezone.utc)`
- Ajouter un middleware de logging minimal
- Passer `restart: unless-stopped` à `always`

**Amélioration**
- Créer un fichier `.env.example`
- Ajouter des limits mémoire/CPU dans `docker-compose.yml`
