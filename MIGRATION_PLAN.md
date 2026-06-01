# MIGRATION_PLAN

## 1. Sauvegarde préalable

- **Branche Git** : `legacy-backup` créée via `git checkout -b legacy-backup` (vérifié par `git status -sb`).
- **Archive** : `legacy-backup.zip` générée à la racine avec `Compress-Archive -Path * -DestinationPath legacy-backup.zip -Force`. L’archive capture l’intégralité du projet actuel (backend, frontend, scripts legacy, storage, etc.).

## 2. Fichiers / répertoires prévus pour suppression

| Élément | Rôle actuel | Justification | Statut |
| --- | --- | --- | --- |
| `frontend/` (React + Vite) | Client SPA lecture seule (Dashboard, Photos, Tasks, Report) | L’architecture cible impose FastAPI + Jinja2 + Vanilla JS, sans framework frontend. | **À supprimer** |
| `backend/app/pdf/report.html` | Template HTML consommé par WeasyPrint | Le PDF basculera vers ReportLab (`pdf.py`). | **À supprimer** |
| `backend/app/services/pdf_service.py` | Générateur PDF WeasyPrint | Remplacé par `pdf.py` basé sur ReportLab. | **À supprimer** |
| `template_sans_images.html` | Interface legacy autonome | Ses composants seront migrés dans les templates Jinja2 (`templates/*.html`). | **À supprimer après migration** |
| `backend/app/static/` (si présent) | Assets hérités | Les assets seront regroupés dans `static/` à la racine. | **À vérifier** |

## 3. Fichiers / modules prévus pour fusion

| Source actuelle | Futur fichier | Contenu fusionné | Notes |
| --- | --- | --- | --- |
| `backend/app/main.py` + `backend/app/api/*.py` | `main.py` | App FastAPI, routes (rapports, photos, tâches, signatures) et rendu des templates Jinja2. | Les endpoints REST restent disponibles. |
| `backend/app/db/base.py`, `backend/app/db/session.py`, `backend/alembic/` | `database.py` | Base SQLAlchemy + session + initialisation SQLite `data/reports.db`. | Création auto des tables à l’initialisation. |
| `backend/app/models/*.py` | `models.py` | Modèles Report/Photo/Task/Signature + enums. | Aucun champ supprimé. |
| `backend/app/schemas/*.py` | `schemas.py` | Schémas Pydantic (CRUD/API). | Réutilisés tels quels. |
| `backend/app/services/photo_storage.py` + helpers | `storage.py` | Gestion upload/miniatures/suppression (`storage/photos`). | Continue d’exploiter Pillow si présent. |
| `generer_pdf.py` + service actuel | `pdf.py` | Génération PDF via ReportLab (couverture, tâches, QR code). | Appelé depuis FastAPI. |

## 4. Fichiers prévus pour renommage / déplacement

| Chemin actuel | Nouveau chemin | Raison |
| --- | --- | --- |
| `backend/app/core/config.py` | `config.py` | Centraliser configuration + chemins `Path`. |
| `backend/app/main.py` | `main.py` | Point d’entrée unique FastAPI. |
| `backend/app/api/__init__.py` | `main.py` | Routes intégrées directement. |
| `backend/app/pdf/report.html` | `templates/pdf_template.html` (archive de design) | Sert de référence visuelle (non utilisé par ReportLab). |
| `storage/` (racine) | `storage/` (inchangé mais via `Path`) | Exploitation unifiée via `Path` + montages Docker. |

## 5. Fonctionnalités migrées

| Fonctionnalité | Source actuelle | Destination cible | Commentaire |
| --- | --- | --- | --- |
| Tableau de bord rapports | `frontend/src/pages/DashboardPage.tsx` | `templates/reports.html` rendu par FastAPI | Ajout de recherche/filtres server-side. |
| Vue rapport + Leaflet | `frontend/src/pages/ReportPage.tsx`, `components/MapView.tsx` | `templates/report.html` + JS Vanilla Leaflet | Réutilisation du markup legacy. |
| Pages Photos / Tâches | `frontend/src/pages/PhotosPage.tsx`, `TasksPage.tsx` | `templates/photos.html`, `templates/tasks.html` | Support CRUD complet. |
| Upload photo + GPS | API `/photos` + `template_sans_images.html` (JS) | Formulaires FastAPI + JS Vanilla (EXIF/GPS). | API inchangée. |
| Génération PDF | `backend/app/services/pdf_service.py` (WeasyPrint) | `pdf.py` (ReportLab) | Ajout QR code, sommaire, compatibilité Windows/Linux. |

## 6. Fonctionnalités abandonnées / suspendues

| Fonctionnalité | Statut | Justification |
| --- | --- | --- |
| SPA React/Vite | Abandonnée | Les écrans seront rendus côté serveur (FastAPI + Jinja2). Aucune perte fonctionnelle (React était lecture seule). |
| WeasyPrint | Abandonnée | Remplacée par ReportLab (pur Python, portable). |
| Build npm/PWA | Suspendu | Pourrait revenir plus tard en Vanilla JS si nécessaire. |

> Ce plan sera mis à jour à mesure que les suppressions/fusions/renommages seront réalisés.
