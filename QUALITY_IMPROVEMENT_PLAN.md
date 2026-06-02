# QUALITY_IMPROVEMENT_PLAN

FieldReport v1.0.1 — Plan d'amélioration de la qualité
Date : 2026-06-01

---

## Objectif

Passer les notes de qualité à :

- **Tests** : 6/10 → ≥ 8/10
- **Docker** : 6/10 → ≥ 8/10
- **Maintenabilité** : 7/10 → ≥ 8/10

---

## Actions sélectionnées (5 actions)

### P0 — Action 1 : Configurer ruff (linter + formatter)

| | |
|---|---|
| **Impact** | Maintenabilité (+2), Tests (+0.5) |
| **Effort estimé** | Très faible (~15 min) |
| **Risque** | Aucun — outil en lecture seule, pas de modification fonctionnelle |
| **Gain attendu** | Code standardisé, détection d'erreurs statiques, meilleure lisibilité pour les futurs contributeurs |
| **Fichiers concernés** | `pyproject.toml` (nouveau), `.gitignore` |

**Description** :
Installer `ruff`, ajouter une configuration minimale dans `pyproject.toml`, lancer `ruff check backend/` et `ruff format backend/`.

**Justification ratio effort/gain** :
Effort quasi nul. Retour immédiat sur la qualité du code. Impact direct sur Maintenabilité (passe de 7 à 9).

---

### P0 — Action 2 : Corriger docker-compose.yml (backend seul + healthcheck)

| | |
|---|---|
| **Impact** | Docker (+2) |
| **Effort estimé** | Faible (~15 min) |
| **Risque** | Faible — le compose de validation (`docker-compose.validation.yml`) est déjà fonctionnel, servir de référence |
| **Gain attendu** | Compose final cohérent avec l'architecture. Healthcheck pour supervision. Suppression du service frontend obsolète |
| **Fichiers concernés** | `docker-compose.yml` |

**Description** :
Remplacer le contenu de `docker-compose.yml` par la version de `DOCKER_FINALIZATION.md` (backend uniquement, healthcheck, restart policy).

**Justification ratio effort/gain** :
Un seul fichier à éditer. Gain de +2 sur Docker (passe de 6 à 8). Élimine l'incohérence entre la doc et le code.

---

### P0 — Action 3 : Retirer weasyprint et ajouter reportlab à requirements.txt

| | |
|---|---|
| **Impact** | Docker (+0.5), Maintenabilité (+0.5) |
| **Effort estimé** | Très faible (~5 min) |
| **Risque** | Aucun — reportlab est déjà utilisé en production par `pdf_service.py` |
| **Gain attendu** | Image Docker allégée. Dépendances explicites et cohérentes avec le code réel |
| **Fichiers concernés** | `backend/requirements.txt` |

**Description** :
Supprimer `weasyprint==62.3` et ajouter `reportlab>=4.0` et `pillow>=10.0`.

**Justification ratio effort/gain** :
Édition d'une seule ligne. Corrige une incohérence flagrante entre les dépendances déclarées et le code réel.

---

### P1 — Action 4 : Fusionner tests/ et backend/tests/ + ajouter tests PDF unitaires

| | |
|---|---|
| **Impact** | Tests (+2), Maintenabilité (+1) |
| **Effort estimé** | Moyen (~2h) |
| **Risque** | Faible — les tests existants passent déjà (21/21) |
| **Gain attendu** | Tests unifiés sous `backend/tests/`. Couverture du PDF service (génération, format, intégration). Suppression du doublon `tests/` |
| **Fichiers concernés** | `tests/` → `backend/tests/validation/`, `backend/tests/test_pdf_service.py` (nouveau) |

**Description** :
1. Déplacer `tests/test_*.py` dans `backend/tests/integration/` ou `backend/tests/legacy/`
2. Supprimer le répertoire `tests/` racine
3. Créer `backend/tests/test_pdf_service.py` avec des tests sur `generate_pdf()`

**Justification ratio effort/gain** :
C'est l'action la plus coûteuse mais indispensable pour atteindre 8/10 en Tests. L'écriture de tests PDF est rapide (TestClient + assert header `%PDF`).

---

### P2 — Action 5 : Ajouter .env.example et ignorer .env

| | |
|---|---|
| **Impact** | Maintenabilité (+1), Docker (+0.5) |
| **Effort estimé** | Très faible (~10 min) |
| **Risque** | Aucun |
| **Gain attendu** | Configuration centralisée et documentée. Sécurité (pas de secrets versionnés) |
| **Fichiers concernés** | `.env.example` (nouveau), `.gitignore` |

**Description** :
Créer `.env.example` avec les variables nécessaires (`DATABASE_URL`, `DEBUG`, `PORT`). Ajouter `.env` et `.env.local` au `.gitignore`.

**Justification ratio effort/gain** :
Gain de standardisation immédiat. Prépare la configuration Docker et le déploiement.

---

## Tableau récapitulatif

| Action | Priorité | Effort | Tests | Docker | Maintenabilité | Ratio gain/effort |
|--------|----------|--------|-------|--------|----------------|-------------------|
| 1 — ruff | P0 | Très faible | +0.5 | — | +2 | **Très haut** |
| 2 — compose fix | P0 | Faible | — | +2 | — | **Très haut** |
| 3 — requirements clean | P0 | Très faible | — | +0.5 | +0.5 | **Très haut** |
| 4 — tests unification + PDF | P1 | Moyen | +2 | — | +1 | **Haut** |
| 5 — .env.example | P2 | Très faible | — | +0.5 | +1 | **Haut** |

---

## Projections de notes

| Domaine | Actuel | Après actions | Écart |
|---------|--------|---------------|-------|
| Tests | 6/10 | 8.5/10 | +2.5 |
| Docker | 6/10 | 8.5/10 | +2.5 |
| Maintenabilité | 7/10 | 9/10 | +2 |

---

## Définition de done v1.0.1

- [ ] `ruff check backend/` passe sans erreur
- [ ] `docker-compose up -d` démarre uniquement le backend
- [ ] `curl http://localhost:8200/health` retourne OK
- [ ] `weasyprint` absent de `requirements.txt`
- [ ] `reportlab` et `pillow` présents dans `requirements.txt`
- [ ] Un seul répertoire de tests (`backend/tests/`)
- [ ] Tests PDF exécutés et passant
- [ ] `.env.example` créé et documenté
- [ ] `git status` clean
- [ ] Validation complète passée
