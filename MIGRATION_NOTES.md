# MIGRATION_NOTES

FieldReport v1.0.1 → v1.1
Date : 2026-06-02

---

## Résumé

Cette migration ajoute la géolocalisation aux photos, corrige les chemins statiques, améliore l'expérience mobile et enrichit le PDF.

**Complexité** : Faible
**Durée estimée** : 15 minutes
**Risque de régression** : Faible

---

## Prérequis

- Python 3.11+
- Dépendances à jour : `pip install -r backend/requirements.txt`
- Base de données SQLite existante (migrations automatiques avec Alembic)

---

## Étapes de migration

### 1. Mettre à jour le code

```bash
git pull origin main
```

### 2. Mettre à jour les dépendances

```bash
cd backend
pip install -r requirements.txt
```

### 3. Migration base de données

La migration Alembic ajoute la colonne `gps_accuracy` à la table `photos`.

```bash
cd backend
alembic revision --autogenerate -m "add gps_accuracy to photos"
alembic upgrade head
```

**Alternative sans Alembic** (si vous n'utilisez pas les migrations) :

```bash
# SQLite uniquement — la colonne sera créée automatiquement au prochain démarrage
# si vous supprimez/recréez la base. Sinon, exécutez :
sqlite3 storage/reports.db "ALTER TABLE photos ADD COLUMN gps_accuracy FLOAT;"
```

### 4. Redémarrer l'application

```bash
# Docker
docker-compose down
docker-compose up --build

# Ou directement
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8200
```

---

## Changements techniques

### Base de données

| Table | Changement | Type |
|-------|------------|------|
| `photos` | `gps_accuracy` | `FLOAT`, nullable |

### API

| Endpoint | Changement |
|----------|------------|
| `POST /api/photos/{report_id}` | Accepte `gps_lat`, `gps_lng`, `gps_accuracy` en FormData |

### Routes UI

| Route | Description |
|-------|-------------|
| `/history` | Nouvelle page : historique des interventions par site |

### Templates modifiés

- `layout.html` — Modal confirmation suppression + lien historique
- `reports.html` — Valeurs météo corrigées, recherche
- `report_detail.html` — Capture photo native, GPS, modal tâche
- `tasks.html` — Modal édition, recherche
- `signatures.html` — Modal édition, recherche
- `photos.html` — Recherche
- `history.html` — Nouveau

---

## Vérification post-migration

1. Ouvrir `http://localhost:8200/`
2. Créer un rapport
3. Ajouter une photo — vérifier que la capture native fonctionne sur mobile
4. Vérifier que les coordonnées GPS s'affichent sous la photo
5. Cliquer sur le lien GPS — vérifier l'ouverture Google Maps
6. Ajouter une tâche — vérifier la modal (pas de prompt)
7. Modifier une tâche — vérifier la modal pré-remplie
8. Supprimer une photo — vérifier la modal de confirmation
9. Générer le PDF — vérifier que les photos et GPS sont inclus
10. Consulter `/history` — vérifier le filtrage par site

---

## Rollback

En cas de problème :

```bash
# Revenir à v1.0.1
git checkout v1.0.1

# Restaurer la base de données depuis la sauvegarde
cp storage/reports.db.backup storage/reports.db
```

---

## Support

En cas d'anomalie, consulter :
- `ANALYSE_ARCHITECTURE.md` — architecture détaillée
- `TEST_REPORT.md` — résultats des tests
- `CHANGELOG_V1_1.md` — liste des changements
