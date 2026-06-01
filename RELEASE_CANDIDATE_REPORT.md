# RELEASE_CANDIDATE_REPORT

FieldReport v1.0.0-RC1 — Rapport de Release Candidate

Date : 2026-06-01

---

## 1. Architecture finale

```
+-------------+     +------------------+     +-------------+
|   Client    +---->+  FastAPI + UV    +---->+   SQLite    |
|  Navigateur |     |  Jinja2 UI       |     |  (fichier)  |
|             |     |  ReportLab PDF   |     |  + photos   |
+-------------+     +------------------+     +-------------+
```

| Couche | Technologie | Rôle |
|--------|-------------|------|
| Backend | FastAPI 0.111 | API REST + SSR Jinja2 |
| ORM | SQLAlchemy 2.0 | Modèles + Migrations |
| Validation | Pydantic v2 | Schémas API |
| UI | Jinja2 + HTML5 + CSS3 + Vanilla JS | Pages serveur-rendered |
| PDF | ReportLab 4.4 | Génération PDF côté serveur |
| DB | SQLite | Stockage relationnel embarqué |
| Storage | Fichiers locaux | Photos, thumbnails, exports PDF |
| Container | Docker + Compose | Déploiement portable |

---

## 2. Fonctionnalités validées

### 2.1 Dashboard
- Compteurs temps réel (rapports, photos, tâches)
- Derniers rapports avec liens
- Navigation vers toutes les sections

### 2.2 Rapports (CRUD complet)
- Création avec formulaire modal
- Édition inline
- Suppression avec confirmation
- Filtres par statut
- Génération PDF

### 2.3 Photos
- Upload multipart (jpg, png, webp)
- Thumbnail automatique
- Affichage grille filtrable par rapport
- Suppression DB + fichiers

### 2.4 Tâches
- Création liée à un rapport
- Édition description + statut
- Suppression
- Affichage dans le détail rapport

### 2.5 Signatures
- Création liée à un rapport
- Édition nom + rôle + date
- Suppression
- Affichage dans le détail rapport

### 2.6 PDF
- Génération ReportLab depuis détail rapport
- Intégration données : infos, tâches, photos, signature
- Téléchargement via `/exports`

---

## 3. Couverture fonctionnelle

| Fonction | Couverture | Preuve |
|----------|------------|--------|
| Dashboard | 100% | `UI_FUNCTIONAL_VALIDATION.md` |
| Reports CRUD | 100% | `UI_FUNCTIONAL_VALIDATION.md` |
| Photos upload/affichage/suppression | 100% | `UI_FUNCTIONAL_VALIDATION.md` |
| Tasks CRUD | 100% | `UI_FUNCTIONAL_VALIDATION.md` |
| Signatures CRUD | 100% | `UI_FUNCTIONAL_VALIDATION.md` |
| PDF génération/téléchargement | 100% | `UI_FUNCTIONAL_VALIDATION.md` |
| End-to-End workflow | 100% | `END_TO_END_VALIDATION.md` |
| API CRUD | 100% | `API_VALIDATION.md` (21/21 tests) |
| SQLite persistence | 100% | `SQLITE_VALIDATION.md` |
| Storage fichiers | 100% | `STORAGE_VALIDATION.md` |

---

## 4. Résultats des tests

| Suite | Tests | Pass | Fail | Statut |
|-------|-------|------|------|--------|
| API CRUD (pytest) | 21 | 21 | 0 | PASS |
| UI Fonctionnelle | 22 | 22 | 0 | PASS |
| End-to-End | 6 | 6 | 0 | PASS |
| **Total** | **49** | **49** | **0** | **PASS** |

---

## 5. Dépendances conservées

| Package | Version | Usage |
|---------|---------|-------|
| fastapi | 0.111 | Framework web + API |
| uvicorn | 0.30 | Serveur ASGI |
| sqlalchemy | 2.0 | ORM |
| pydantic | 2.7 | Validation |
| jinja2 | 3.1 | Moteur templates |
| reportlab | 4.4 | Génération PDF |
| pillow | 10.3 | Manipulation images |
| python-multipart | 0.0.9 | Upload fichiers |
| alembic | 1.13 | Migrations DB |
| pytest | 8.2 | Tests |
| httpx | 0.27 | Client test |

---

## 6. Dépendances dépréciées

| Package | Raison | Action |
|---------|--------|--------|
| weasyprint | Remplacé par ReportLab | Retirer de `requirements.txt` |
| react | Remplacé par Jinja2 | Archiver dans `legacy/frontend-react/` |
| react-dom | Idem | Archiver |
| react-router-dom | Idem | Archiver |
| @tanstack/react-query | Idem | Archiver |
| leaflet | Carte non utilisée en Jinja2 | Archiver |
| vite | Build tool React | Archiver |
| tailwindcss | Styling React | Archiver |

---

## 7. Risques résiduels

| Risque | Sévérité | Mitigation |
|--------|----------|------------|
| Pas d'authentification | Moyenne | API publique en l'état ; ajouter OAuth2/JWT en v1.1 |
| Pas de pagination API | Moyenne | SQLite tiendra > 10K rapports ; pagination en v1.1 |
| SQLite mono-instance | Faible | Docker volume persistant ; migrer vers PostgreSQL pour multi-instance |
| Édition inline via `prompt()` | Faible | Suffisant pour MVP interne ; modals JS en v1.1 |
| Pas de carte Leaflet | Faible | Coordonnées GPS stockées ; affichage carte optionnel en v1.2 |
| WeasyPrint encore dans requirements | Faible | `pip install` plus long ; retirer après archivage frontend |

---

## 8. Livrables de la release

| Document | Description |
|----------|-------------|
| `VERSION.md` | Numéro de version et date |
| `RELEASE_CANDIDATE_REPORT.md` | Ce document |
| `CHANGELOG.md` | Historique des évolutions |
| `README_PRODUCTION.md` | Guide installation et maintenance |
| `BACKUP_AND_RESTORE.md` | Procédures de sauvegarde |
| `DECOMMISSION_PLAN.md` | Plan de retrait React/WeasyPrint |
| `LEGACY_USAGE_AUDIT.md` | Audit des dépendances legacy |
| `CLEANUP_PLAN.md` | Classification conserver/archiver/supprimer |
| `DOCKER_FINALIZATION.md` | Configuration Docker finale |
| `UI_FUNCTIONAL_VALIDATION.md` | Preuve UI fonctionnelle (22/22 PASS) |
| `END_TO_END_VALIDATION.md` | Preuve E2E (6/6 PASS) |
| `API_VALIDATION.md` | Preuve API (21/21 PASS) |

---

## 9. Décision Go/No-Go

| Critère | État | Décision |
|---------|------|----------|
| Toutes les features métier validées | PASS | GO |
| Tests automatisés verts | PASS | GO |
| Documentation complète | PASS | GO |
| Docker fonctionnel | PASS | GO |
| Stratégie legacy claire | PASS | GO |

**Verdict : GO pour la production.**

FieldReport v1.0.0-RC1 est candidate pour déploiement. Les suppressions de legacy (React, WeasyPrint) seront effectuées après validation finale du plan de décommissionnement.
