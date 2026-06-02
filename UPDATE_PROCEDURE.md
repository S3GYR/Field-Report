# UPDATE_PROCEDURE

FieldReport v1.1 — Procédure de mise à jour
Date : 2026-06-02

---

## Principe

FieldReport étant conteneurisé, la mise à jour consiste à :
1. Sauvegarder les données
2. Arrêter le conteneur
3. Mettre à jour le code
4. Reconstruire l'image
5. Redémarrer
6. Valider

---

## Procédure pas à pas

### Étape 1 — Sauvegarde préalable

```bash
cd /opt/fieldreport

# Exécuter la sauvegarde manuellement
sudo ./scripts/backup.sh

# Vérifier que les fichiers de sauvegarde existent
ls -la backups/daily/
```

### Étape 2 — Arrêt de l'application

```bash
cd /opt/fieldreport
sudo docker compose down
```

### Étape 3 — Mise à jour du code

```bash
cd /opt/fieldreport

# Si déployé via git
git fetch origin
git pull origin main

# Ou si déployé manuellement
tar xzf fieldreport-v1.1.1.tar.gz --strip-components=1
```

### Étape 4 — Reconstruction de l'image

```bash
cd /opt/fieldreport
sudo docker compose up -d --build
```

### Étape 5 — Validation

```bash
# Vérifier que le conteneur est actif
sudo docker ps --filter name=fieldreport

# Healthcheck
curl -s http://127.0.0.1:8200/health | grep '"status":"ok"'

# Test rapide API
curl -s http://127.0.0.1:8200/api/reports/ | jq '. | length'

# Vérifier les logs (pas d'erreur au démarrage)
sudo docker logs fieldreport-backend --tail 20
```

### Étape 6 — Test fonctionnel (optionnel mais recommandé)

```bash
# Créer un rapport test via l'API
curl -X POST http://127.0.0.1:8200/api/reports/ \
  -H "Content-Type: application/json" \
  -d '{"number":"UPDATE-TEST-001","visit_date":"2026-06-02","client":"Test","site":"Test","weather":"sunny","status":"draft"}'

# Vérifier qu'il apparaît dans la liste
curl -s http://127.0.0.1:8200/api/reports/ | jq '.[] | select(.number=="UPDATE-TEST-001")'

# Supprimer le rapport test
curl -X DELETE http://127.0.0.1:8200/api/reports/1
```

---

## Rollback

Si la mise à jour échoue, restaurer la version précédente :

```bash
cd /opt/fieldreport

# 1. Arrêter le conteneur défectueux
sudo docker compose down

# 2. Restaurer le code (git)
git checkout v1.1.0

# 3. Restaurer la base de données depuis la sauvegarde
sudo cp backups/daily/reports-$(date +%Y%m%d)*.db data/reports.db

# 4. Reconstruire l'image de l'ancienne version
sudo docker compose up -d --build

# 5. Vérifier
curl -s http://127.0.0.1:8200/health
```

---

## Mise à jour Docker seule (pas de changement de code)

Si seule l'image de base Python ou les dépendances ont changé :

```bash
cd /opt/fieldreport
sudo docker compose down
sudo docker compose pull
sudo docker compose up -d --build
```

---

## Checklist post-mise à jour

- [ ] Sauvegarde effectuée avant la mise à jour
- [ ] Conteneur actif (`docker ps`)
- [ ] Healthcheck OK (`curl /health`)
- [ ] Accès HTTPS fonctionnel depuis le navigateur
- [ ] Création de rapport fonctionne
- [ ] Upload photo fonctionne
- [ ] Génération PDF fonctionne
- [ ] Aucune erreur dans les logs (`docker logs`)
