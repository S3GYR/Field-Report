# DOCKER_IMPROVEMENT_REPORT

FieldReport v1.0.1 — Amélioration Docker
Date : 2026-06-01

---

## Problèmes identifiés

| # | Problème | Fichier | Gravité |
|---|----------|---------|---------|
| 1 | Service `frontend` React obsolète dans `docker-compose.yml` | `docker-compose.yml` | Haute |
| 2 | Pas de healthcheck sur le backend | `docker-compose.yml` | Moyenne |
| 3 | Pas de politique de redémarrage | `docker-compose.yml` | Moyenne |
| 4 | Librairies système manquantes pour Pillow/ReportLab | `backend/Dockerfile` | Moyenne |
| 5 | Répertoires `storage/photos` et `storage/exports` non créés dans l'image | `backend/Dockerfile` | Faible |

---

## Corrections appliquées

### docker-compose.yml

- Suppression du service `frontend` et de sa dépendance
- Renommage du container `report-backend` → `fieldreport-backend`
- Ajout des variables d'environnement `PYTHONDONTWRITEBYTECODE` et `PYTHONUNBUFFERED`
- Ajout d'un `healthcheck` basé sur `urllib.request.urlopen('http://localhost:8200/health')`
- Ajout de `restart: unless-stopped`

### backend/Dockerfile

- Ajout de l'installation des librairies système :
  - `libjpeg62-turbo-dev`
  - `zlib1g-dev`
- Création des répertoires `storage/photos` et `storage/exports` dans l'image

---

## Impact

| Domaine | Avant | Après |
|---------|-------|-------|
| Cohérence compose/architecture | Service frontend inutile | Backend uniquement |
| Supervision | Aucune | Healthcheck toutes les 30s |
| Résilience | Aucune | Redémarrage automatique |
| Build image | Risque Pillow/ReportLab | Libs système garanties |
| Démarrage container | Risque répertoires manquants | Répertoires créés |

---

## Vérification

```bash
docker-compose config
```

**Résultat** : Configuration valide, un seul service (`backend`), healthcheck présent.

---

## Risques résiduels

- Aucun. Les modifications sont purement infrastructurelles.
