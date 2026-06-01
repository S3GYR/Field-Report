# ARCHITECTURE_AUDIT

## 1. Résumé exécutif

Le projet actuel repose sur **trois pipelines parallèles** :

1. **Backend FastAPI** (API REST + stockage fichiers) situé sous `backend/app`. Il implémente l’intégralité du modèle métier (rapports, photos, tâches, signatures) et expose aussi la génération PDF via un service WeasyPrint @backend/app/api/reports.py#16-70 @backend/app/services/pdf_service.py#15-36.
2. **Frontend React/Vite** (`frontend/`) consommant seulement `GET /reports` et `GET /reports/{id}` pour afficher des tableaux de bord lecture seule @frontend/src/services/api.ts#13-22 @frontend/src/pages/DashboardPage.tsx#6-29 @frontend/src/pages/ReportPage.tsx#17-64.
3. **Interface legacy HTML autonome** (`template_sans_images.html`) couvrant toutes les fonctionnalités interactives (upload photos, GPS EXIF, tâches, impression, export CSV) et un **script ReportLab** (`generer_pdf.py`) qui sait déjà produire des PDF complets offline @template_sans_images.html#1343-1415 @generer_pdf.py#1-200.

Ces couches redondantes compliquent la maintenance et la portabilité (WeasyPrint ⇒ dépendances natives, React ⇒ toolchain Node, legacy ⇒ duplication).

## 2. Périmètre technique détaillé

### 2.1 Backend FastAPI (`backend/app`)

- **API** : routes regroupées par ressource (rapports, photos, tâches, signatures) sous `backend/app/api/*.py` exploitent SQLAlchemy et valident les payloads via Pydantic @backend/app/api/photos.py#14-40 @backend/app/api/tasks.py#13-45.
- **Modèles** : `backend/app/models/report.py` définit les entités `Report`, `Photo`, `Task`, `Signature` avec cascades, énumérations métier et timestamps @backend/app/models/report.py#37-105.
- **Schemas** : `backend/app/schemas/report.py` expose les DTOs (Create/Update/Response) pour toutes les entités @backend/app/schemas/report.py#12-120.
- **Stockage fichiers** : `PhotoStorageService` gère slugification, hiérarchie `storage/photos/YYYY/MM`, miniatures Pillow ou fallback copie @backend/app/services/photo_storage.py#22-78.
- **Génération PDF** : `ReportPdfService` rend `backend/app/pdf/report.html` via Jinja2 et convertit en PDF avec WeasyPrint @backend/app/services/pdf_service.py#15-36. Cela impose Cairo/GTK côté OS.

### 2.2 Frontend React/Vite (`frontend/`)

- Application SPA (Vite, React Router, React Query) servant uniquement d’interface de consultation : Dashboard, Report, Photos, Tasks, Export @frontend/src/pages/TasksPage.tsx#5-44 @frontend/src/pages/PhotosPage.tsx#6-27.
- Les hooks `useReports` / `useReport` n’appellent que deux endpoints `GET` @frontend/src/hooks/useReports.ts#1-17.
- Aucun formulaire n’est implémenté côté React ; toutes les données proviennent de l’API existante. Cette couche est donc redondante si on adopte une UI server-side.

### 2.3 Interface legacy HTML (`template_sans_images.html`)

- Fichier unique (~75 Ko) combinant HTML/CSS/JS. Gère localStorage/sessionStorage, upload drag&drop, extraction EXIF GPS (`autoExtractGpsFromFiles`), lightbox, table de tâches, impression, export CSV @template_sans_images.html#1348-1415.
- Fonctionne entièrement offline, sans dépendance backend, et répond à la plupart des besoins métier (photos, tâches, recap, signature).

### 2.4 Génération PDF ReportLab (`generer_pdf.py`)

- Script CLI pur Python : lit `rapport_data.json`, calcule statistiques, construit une couverture, des sections photos/tâches et un pied de page @generer_pdf.py#94-200.
- Dépendances : `reportlab` uniquement (pas de librairies natives). Ce script constitue une excellente base pour le futur `pdf.py` côté FastAPI.

### 2.5 Infrastructure & dépendances

- **Docker Compose** lance deux services (frontend, backend) et monte seulement `./storage` dans le conteneur backend @docker-compose.yml#1-41. Aucune persistance pour SQLite (`storage/reports.db` par défaut dans `config.py` @backend/app/core/config.py#11-28).
- **Dépendances Python** (`backend/requirements.txt`) incluent FastAPI, SQLAlchemy, Pydantic, WeasyPrint, ReportLab (non listé), etc. @backend/requirements.txt#1-13.
- **Dépendances Node** (`frontend/package.json`, `package-lock.json`) ajoutent un poids significatif (React, React Query, Leaflet, Vite) @frontend/package.json#1-41.

## 3. Cartographie fonctionnelle (vue synthétique)

| Fonction métier | Implémentation principale | Observations |
| --- | --- | --- |
| CRUD rapports | API FastAPI (`backend/app/api/reports.py`) | Couverture complète via SQLAlchemy. Frontend React ne propose que la lecture. |
| Gestion photos | API `/photos` + `PhotoStorageService` | Upload effectif côté API, UI complète disponible uniquement dans `template_sans_images.html`. |
| Tâches | API `/tasks` | UI React lecture, UI legacy édition. |
| Signatures | API `/signatures` | Pas de composant React associé. |
| PDF | Service WeasyPrint + script ReportLab | Deux implémentations coexistent. |
| Cartographie (Leaflet) | React `MapView` + legacy iframe | Nécessite reproduction côté Jinja2. |

## 4. Dette technique & problèmes majeurs

1. **Duplication UI** (React vs HTML legacy) : double maintenance, comportements divergents, absence d’unicité de source de vérité.
2. **Dépendances lourdes** : WeasyPrint impose Cairo/GTK, difficile à packager identiquement sur Windows/Docker/Proxmox/CasaOS. ReportLab offre déjà une alternative portable.
3. **Portabilité limitée** : `database_url` pointe sur `sqlite:///./storage/reports.db` @backend/app/core/config.py#11-18 — pas de séparation `data/` vs `storage/`, montage Docker partiel.
4. **Arborescence complexe** : multi-dossiers (`backend/`, `frontend/`, `template_sans_images.html`, `generer_pdf.py`) vs cible souhaitée (monorepo simple `field-report/`).
5. **Tests insuffisants** : un seul test (`backend/tests/test_reports_api.py`) se concentre sur CRUD rapport, aucun test pour photos/tâches/PDF.
6. **Documentation hétérogène** : README récent documente l’état actuel mais pas la future architecture ; pas d’ARCHITECTURE.md ou INSTALL.md.

## 5. Risques si l’on conserve l’état actuel

| Risque | Impact | Probabilité |
| --- | --- | --- |
| Difficulté de déploiement multi-OS (WeasyPrint) | Blocage sur Windows/CasaOS | Élevée |
| Maintenance React (lecture seule) | Temps perdu sans bénéfice fonctionnel | Élevée |
| Divergence entre interface legacy et API | Données incohérentes / UX confuse | Moyenne |
| Perte de portabilité (chemins relatifs) | Restauration compliquée | Moyenne |

## 6. Opportunités d’amélioration

1. **Monolithe FastAPI + Jinja2** : servir toutes les pages via templates (réutiliser markup du legacy) et supprimer React.
2. **Génération PDF ReportLab** : intégrer `generer_pdf.py` dans un module `pdf.py` accessible via l’API (simplifie packaging).
3. **Réorganisation des dossiers** : adopter l’arborescence cible (`main.py`, `database.py`, etc.), stocker SQLite dans `data/reports.db`, normaliser les chemins via `Path`.
4. **Docker simplifié** : un seul service `web` avec volumes `./data` et `./storage` pour assurer la sauvegarde/ restauration par simple copie.
5. **Documentation complète** : produire ARCHITECTURE.md, INSTALL.md, DEVELOPER_GUIDE.md pour cadrer les futures évolutions et faciliter la maintenance par une seule personne.

---

Ce rapport se base uniquement sur les fichiers présents dans le dépôt au moment de l’analyse. Aucune modification de code n’a été effectuée.
