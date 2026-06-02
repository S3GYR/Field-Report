# V1_1_RELEASE_CHECKLIST

FieldReport v1.1 — Checklist finale avant publication
Date : 2026-06-02

---

## 1. Git

| # | Vérification | Statut |
|---|------------|--------|
| 1.1 | Toutes les modifications V1.1 sont commitées | [ ] |
| 1.2 | Message de commit descriptif : `feat: v1.1 mobile-first terrain` | [ ] |
| 1.3 | Branche `v1.0.1-dev` propre, pas de fichiers non-trackés | [ ] |
| 1.4 | Tag git créé : `git tag -a v1.1.0 -m "FieldReport v1.1.0"` | [ ] |
| 1.5 | Tag poussé : `git push origin v1.1.0` | [ ] |
| 1.6 | `.gitignore` à jour (pas de `storage/photos/`, pas de `*.db`) | [ ] |

---

## 2. Docker

| # | Vérification | Statut |
|---|------------|--------|
| 2.1 | `docker-compose build` réussit sans erreur | [ ] |
| 2.2 | `docker-compose up` démarre, health check `http://localhost:8200/health` renvoie `{"status":"ok"}` | [ ] |
| 2.3 | Volumes persistants configurés (`storage/`, `exports/`) | [ ] |
| 2.4 | Le conteneur redémarre proprement (`docker-compose restart`) | [ ] |
| 2.5 | Pas de fuite de mémoire après 1h de fonctionnement | [ ] |

---

## 3. Documentation

| # | Vérification | Statut |
|---|------------|--------|
| 3.1 | `CHANGELOG_V1_1.md` présent et complet | [ ] |
| 3.2 | `MIGRATION_NOTES.md` présent avec procédure de mise à jour | [ ] |
| 3.3 | `TEST_REPORT.md` avec résultats 21/21 PASS | [ ] |
| 3.4 | `PHOTO_CAPTURE_IMPLEMENTATION.md` créé | [ ] |
| 3.5 | `GPS_INTEGRATION_PLAN.md` créé | [ ] |
| 3.6 | `MODAL_REFACTOR_REPORT.md` créé | [ ] |
| 3.7 | `SEARCH_IMPLEMENTATION_PLAN.md` créé | [ ] |
| 3.8 | `DELETE_CONFIRMATION_REPORT.md` créé | [ ] |
| 3.9 | `V1_1_VALIDATION_PLAN.md` créé | [ ] |
| 3.10 | `FIELD_TEST_PROTOCOL.md` créé | [ ] |
| 3.11 | `USER_ACCEPTANCE_TEST.md` créé | [ ] |
| 3.12 | `KNOWN_LIMITATIONS.md` créé | [ ] |
| 3.13 | `OFFLINE_V2_PREPARATION.md` créé | [ ] |
| 3.14 | `README.md` mis à jour avec les nouvelles fonctionnalités | [ ] |

---

## 4. Sauvegardes

| # | Vérification | Statut |
|---|------------|--------|
| 4.1 | Base de données source (`storage/reports.db`) sauvegardée avant mise à jour | [ ] |
| 4.2 | Dossier `storage/photos/` sauvegardé | [ ] |
| 4.3 | Dossier `storage/exports/` sauvegardé | [ ] |
| 4.4 | Procédure de rollback testée (`git checkout v1.0.1` + restauration DB) | [ ] |

---

## 5. Tests

| # | Vérification | Statut |
|---|------------|--------|
| 5.1 | `python -m pytest backend/tests -v` → **21 passed** | [ ] |
| 5.2 | Aucune régression sur CRUD rapports | [ ] |
| 5.3 | Aucune régression sur CRUD photos | [ ] |
| 5.4 | Aucune régression sur CRUD tâches | [ ] |
| 5.5 | Aucune régression sur CRUD signatures | [ ] |
| 5.6 | Génération PDF fonctionne sur un rapport avec photo + GPS + signature | [ ] |
| 5.7 | Upload photo avec GPS fonctionne via API directe (`curl` ou Postman) | [ ] |
| 5.8 | Modal confirmation suppression fonctionne sur toutes les pages | [ ] |

---

## 6. UX Terrain

| # | Vérification | Statut |
|---|------------|--------|
| 6.1 | `capture="environment"` présent sur l'input file de `report_detail.html` | [ ] |
| 6.2 | Acquisition GPS déclenchée à l'ouverture de la modal photo | [ ] |
| 6.3 | Pas de `prompt()` dans tout le code source (`grep -r "prompt(" backend/app/templates/` doit être vide) | [ ] |
| 6.4 | Pas de `window.confirm()` pour la suppression (modal HTML utilisée) | [ ] |
| 6.5 | Barre de recherche présente sur reports, tasks, photos, signatures | [ ] |
| 6.6 | Page `/history` accessible et fonctionnelle | [ ] |
| 6.7 | Boutons >= 44px de hauteur tactile (vérifier CSS `.btn`) | [ ] |
| 6.8 | Input font-size >= 16px sur mobile (éviter zoom iOS) | [ ] |
| 6.9 | Lien Google Maps visible sous chaque photo géolocalisée | [ ] |
| 6.10 | Modal tâche supporte création ET édition | [ ] |

---

## 7. Sécurité et stabilité

| # | Vérification | Statut |
|---|------------|--------|
| 7.1 | Pas de secrets ou clés API hardcodées | [ ] |
| 7.2 | Pas de `DEBUG=True` en production | [ ] |
| 7.3 | CORS configuré restrictivement si exposé sur Internet | [ ] |
| 7.4 | Pas de fichiers temporaires ou scripts de debug (`fix_*.py`) dans le repo | [ ] |
| 7.5 | Chemins absolus utilisés dans `main.py` (pas de relatif fragile) | [ ] |

---

## 8. Décision GO / NO-GO

| Critère | Seuil | Statut |
|---------|-------|--------|
| Tests automatisés | 21/21 PASS | [ ] |
| Docker build | Sans erreur | [ ] |
| Documentation | 100% des docs créées | [ ] |
| Pas de régression | CRUD fonctionnels | [ ] |
| UX mobile | Capture photo + GPS testés manuellement | [ ] |

**Verdict** :

- [ ] **GO** — V1.1 prête pour release
- [ ] **CONDITIONNEL** — Corriger les points ci-dessous avant release :
  - ___
- [ ] **NO-GO** — Blocage majeur identifié :
  - ___

**Signataire** : _______________  **Date** : _______________
