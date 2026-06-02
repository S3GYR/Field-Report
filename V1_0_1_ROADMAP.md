# V1_0_1_ROADMAP

FieldReport — Feuille de route v1.0.1

Date : 2026-06-01

---

## 1. Corrections (P0 — Bloquant)

| # | Tâche | Fichier concerné | Description |
|---|-------|-------------------|-------------|
| 1.1 | Retirer `weasyprint` de `requirements.txt` | `backend/requirements.txt` | Dépendance inutilisée. Allonge le build Docker sans raison. |
| 1.2 | Corriger `docker-compose.yml` | `docker-compose.yml` | Supprimer le service `frontend` obsolète. Utiliser la version de `DOCKER_FINALIZATION.md`. |
| 1.3 | Unifier les répertoires `storage/` | `storage/`, `backend/storage/` | Ne garder qu'un seul point de stockage. `backend/storage/` semble être le répertoire actif. |
| 1.4 | Ajouter `reportlab` à `requirements.txt` | `backend/requirements.txt` | ReportLab est utilisé mais absent de la liste. Fonctionne probablement via Pillow, mais explicite est préférable. |

---

## 2. Optimisations (P1 — Amélioration)

| # | Tâche | Impact | Description |
|---|-------|--------|-------------|
| 2.1 | Réorganiser les documents dans `docs/` | Navigation | Centraliser les 35+ fichiers `.md` en `docs/validation/`, `docs/audit/`, `docs/guides/`. |
| 2.2 | Fusionner `tests/` et `backend/tests/` | Qualité | Clarifier la frontière. `backend/tests/` = tests pytest. `tests/` = tests validation standalone. Renommer ou déplacer. |
| 2.3 | Ajouter `.env.example` + ignorer `.env` | Sécurité | Préparer la configuration d'environnement (port, DB path, debug). |
| 2.4 | Ajouter un healthcheck au compose | Docker | `healthcheck:` + `restart: unless-stopped` dans `docker-compose.yml`. |
| 2.5 | Optimiser le Dockerfile | Taille image | Installer uniquement les libs système nécessaires à Pillow/ReportLab. Multi-stage build optionnel. |
| 2.6 | Factoriser les scripts de validation | DX | `scripts/validate.py --target all` au lieu de 6 scripts séparés. |
| 2.7 | Configurer un linter/formatter | Qualité code | `ruff` ou `black` pour le backend. `pre-commit` hooks optionnels. |

---

## 3. Fonctionnalités futures (P2 — Évolution)

| # | Tâche | Priorité | Description |
|---|-------|----------|-------------|
| 3.1 | Authentification JWT/OAuth2 | Haute | Login/password. Nécessaire pour un déploiement production réel. |
| 3.2 | Pagination API + UI | Haute | `skip`/`limit` sur les endpoints listes. Éviter le chargement complet de grosses bases. |
| 3.3 | Formulaires d'édition dédiés | Moyenne | Remplacer `prompt()` par des modals HTML pour tâches et signatures. |
| 3.4 | Carte Leaflet dans Jinja2 | Moyenne | Afficher les coordonnées GPS des photos sur une carte. |
| 3.5 | Recherche full-text | Moyenne | Barre de recherche sur les rapports (numéro, client, site). |
| 3.6 | Export CSV | Moyenne | Bouton d'export CSV des rapports (fonctionnalité legacy réactivable). |
| 3.7 | Notifications toast | Faible | Remplacer `alert()` par des notifications non-bloquantes. |
| 3.8 | Thème sombre | Faible | Toggle dark/light mode CSS. |
| 3.9 | CI/CD GitHub Actions | Faible | Lancer les tests + build Docker sur push. |
| 3.10 | PostgreSQL optionnel | Faible | `DATABASE_URL` supportant SQLite ou PostgreSQL. Nécessaire pour multi-instance. |

---

## Planning suggéré

| Version | Livrables |
|---------|-----------|
| v1.0.1 | Corrections P0 + Optimisations 2.1 à 2.4 |
| v1.0.2 | Optimisations 2.5 à 2.7 + Auth JWT (3.1) |
| v1.1.0 | Pagination (3.2) + Formulaires d'édition (3.3) + Recherche (3.5) |
| v1.2.0 | Carte Leaflet (3.4) + Export CSV (3.6) + PostgreSQL (3.10) |

---

## Définition de done v1.0.1

- [ ] `weasyprint` retiré de `requirements.txt`
- [ ] `reportlab` ajouté à `requirements.txt`
- [ ] `docker-compose.yml` sans service `frontend`
- [ ] Un seul répertoire `storage/` actif
- [ ] `docs/` créé et documents déplacés
- [ ] `tests/` et `backend/tests/` clarifiés
- [ ] `.env.example` créé
- [ ] `git status` clean après toutes les modifications
- [ ] Validation complète passée (`validate.ps1 -Target all`)
