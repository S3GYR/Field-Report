# CHANGELOG

## [1.0.0-RC1] — 2026-06-01

### Release Candidate

FieldReport atteint le statut Production Candidate. Toutes les fonctionnalités métier sont validées.

---

### Évolutions

#### Audit & Architecture
- Audit complet de l'architecture legacy (React + WeasyPrint + SQLite)
- Identification des points de migration et des dépendances critiques
- Création de `ARCHITECTURE_AUDIT.md`

#### Migration SQLite
- Migration depuis PostgreSQL vers SQLite embarqué
- Suppression de la dépendance externe PostgreSQL
- Validation persistance : création, lecture, mise à jour, suppression
- Création de `SQLITE_VALIDATION.md`

#### Validation Storage
- Implémentation du service de stockage fichier (photos, thumbnails)
- Validation upload, lecture, suppression
- Support jpg, png, webp
- Création de `STORAGE_VALIDATION.md`

#### Validation PDF
- Analyse et correction du moteur PDF legacy
- Remplacement WeasyPrint par ReportLab
- Validation génération, téléchargement, intégration données métier
- Création de `PDF_FIX_REPORT.md`, `PDF_COMPARISON.md`

#### Migration API (CRUD)
- Implémentation endpoints REST complets : Reports, Photos, Tasks, Signatures
- Tests automatisés : 21/21 PASS
- Création de `API_IMPLEMENTATION_PLAN.md`, `API_VALIDATION.md`

#### Migration Jinja2 UI
- Création de l'interface utilisateur Jinja2
- Pages : Dashboard, Reports, Report Detail, Photos, Tasks, Signatures
- Design system CSS vanilla + JS vanilla
- Connexion aux endpoints CRUD via fetch API
- Validation fonctionnelle : 22/22 PASS
- Création de `UI_VALIDATION.md`, `UI_FUNCTIONAL_VALIDATION.md`

#### Validation End-to-End
- Scénario complet validé :
  1. Création rapport
  2. Ajout photo
  3. Ajout tâche
  4. Ajout signature
  5. Génération PDF
  6. Vérification des données
- Résultat : 6/6 PASS
- Création de `END_TO_END_VALIDATION.md`

#### Décommissionnement React
- Comparaison fonctionnelle React vs Jinja2 : couverture 100%
- Audit usage React : isolé dans `frontend/`, aucun impact runtime
- Plan d'archivage non destructif
- Création de `DECOMMISSION_PLAN.md`, `LEGACY_USAGE_AUDIT.md`

#### Décommissionnement WeasyPrint
- Remplacement effectif par ReportLab dans `pdf_service.py`
- WeasyPrint présent dans `requirements.txt` mais inutilisé
- Plan de retrait documenté

#### Production Readiness
- Configuration Docker optimisée (backend uniquement)
- Healthcheck et restart policy
- Documentation installation Windows, Linux, Docker
- Procédures de sauvegarde et restauration
- Création de `DOCKER_FINALIZATION.md`, `README_PRODUCTION.md`, `BACKUP_AND_RESTORE.md`

---

### Stack finale

- **Backend** : FastAPI 0.111 + SQLAlchemy 2.0 + Pydantic v2
- **Base de données** : SQLite (fichier embarqué)
- **UI** : Jinja2 + HTML5 + CSS3 + Vanilla JS
- **PDF** : ReportLab 4.4
- **Container** : Docker + Compose

---

### Dépendances retirées (à archiver)

- React, React DOM, React Router
- Tanstack Query
- Vite
- TailwindCSS
- Leaflet
- WeasyPrint

---

### Notes

Cette release candidate ne supprime aucun code legacy. Les composants React et WeasyPrint sont conservés dans `legacy/` et pourront être supprimés après validation du plan de décommissionnement.
