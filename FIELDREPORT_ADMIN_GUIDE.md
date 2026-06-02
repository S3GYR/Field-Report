# FIELDREPORT_ADMIN_GUIDE

FieldReport v1.1 — Guide de l'administrateur
Date : 2026-06-02

---

## 1. Démarrage

### Premier démarrage

```bash
cd /opt/fieldreport

# Construire et lancer
sudo docker compose up -d --build

# Initialiser la base de données (première installation uniquement)
sudo docker exec fieldreport-backend python -c \
  "from app.db.base import Base; from app.db.session import engine; \
   from app.models import Photo, Report, Signature, Task; \
   Base.metadata.create_all(engine)"

# Vérifier
sudo docker ps --filter name=fieldreport
curl -s http://127.0.0.1:8200/health
```

### Démarrage quotidien (redémarrage serveur)

Le conteneur démarre automatiquement grâce à `restart: unless-stopped`.

Si manuellement arrêté :
```bash
cd /opt/fieldreport
sudo docker compose up -d
```

---

## 2. Arrêt

```bash
cd /opt/fieldreport

# Arrêt normal
sudo docker compose down

# Arrêt d'urgence (kill immédiat)
sudo docker kill fieldreport-backend
```

---

## 3. Sauvegarde

### Automatique (cron)

La sauvegarde s'exécute quotidiennement à 2h si configurée :
```bash
sudo crontab -l | grep fieldreport
```

### Manuelle

```bash
cd /opt/fieldreport
sudo ./scripts/backup.sh
```

### Vérifier le succès

```bash
sudo tail -n 20 /var/log/fieldreport-backup.log
ls -lt /opt/fieldreport/backups/daily/
```

---

## 4. Restauration

### Restauration complète (base + photos)

```bash
#!/bin/bash
cd /opt/fieldreport

# Arrêter
sudo docker compose down

# Identifier la dernière backup
LAST_DB=$(ls -t backups/daily/reports-*.db | head -1)
LAST_PHOTOS=$(ls -t backups/daily/photos-*.tar.gz | head -1)

echo "Restauration depuis :"
echo "  DB : $LAST_DB"
echo "  Photos : $LAST_PHOTOS"

# Restaurer
sudo cp "$LAST_DB" data/reports.db
sudo tar xzf "$LAST_PHOTOS" -C data/

# Redémarrer
sudo docker compose up -d

# Vérifier
curl -s http://127.0.0.1:8200/health
```

---

## 5. Surveillance

### Conteneur actif

```bash
sudo docker ps --filter name=fieldreport
```

### Ressources

```bash
sudo docker stats fieldreport-backend --no-stream
```

### Healthcheck

```bash
curl -s http://127.0.0.1:8200/health | jq .
```

### Vérification rapide (toutes les heures)

```bash
#!/bin/bash
# /opt/fieldreport/scripts/healthcheck.sh
if ! curl -sf http://127.0.0.1:8200/health > /dev/null; then
    echo "[$(date)] ALERTE : FieldReport non réactif" | logger
    sudo docker compose -f /opt/fieldreport/docker-compose.yml restart
fi
```

Ajouter au cron :
```bash
0 * * * * /opt/fieldreport/scripts/healthcheck.sh
```

---

## 6. Logs

### Logs application

```bash
# En temps réel
sudo docker logs fieldreport-backend -f

# 100 dernières lignes
sudo docker logs fieldreport-backend --tail 100

# Depuis un moment précis
sudo docker logs fieldreport-backend --since 10m
```

### Logs Nginx

```bash
sudo tail -f /var/log/nginx/fieldreport-access.log
sudo tail -f /var/log/nginx/fieldreport-error.log
```

### Logs système Docker

```bash
sudo journalctl -u docker -f
```

### Nettoyer les logs Docker

```bash
# Vider les logs du conteneur
sudo sh -c 'truncate -s 0 /var/lib/docker/containers/*/local-logs/container.log'
```

---

## 7. Maintenance

### Mise à jour de l'application

Voir `UPDATE_PROCEDURE.md` pour la procédure complète.

Résumé :
```bash
cd /opt/fieldreport
sudo ./scripts/backup.sh
sudo docker compose down
git pull
sudo docker compose up -d --build
```

### Mise à jour du système

```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo reboot  # si nécessaire
```

### Nettoyage des exports PDF

```bash
# Supprimer les PDF de plus de 30 jours
find /opt/fieldreport/data/exports -name "report-*.pdf" -mtime +30 -delete
```

### Vérification espace disque

```bash
df -h /opt/fieldreport/data
du -sh /opt/fieldreport/data/*
```

### Redémarrage du conteneur

```bash
sudo docker compose -f /opt/fieldreport/docker-compose.yml restart
```

### Accès shell dans le conteneur

```bash
sudo docker exec -it fieldreport-backend bash
```

---

## 8. Commandes de référence

| Action | Commande |
|--------|----------|
| Démarrer | `sudo docker compose -f /opt/fieldreport/docker-compose.yml up -d` |
| Arrêter | `sudo docker compose -f /opt/fieldreport/docker-compose.yml down` |
| Redémarrer | `sudo docker compose -f /opt/fieldreport/docker-compose.yml restart` |
| Logs | `sudo docker logs fieldreport-backend -f` |
| Stats | `sudo docker stats fieldreport-backend` |
| Health | `curl -s http://127.0.0.1:8200/health` |
| Backup | `sudo /opt/fieldreport/scripts/backup.sh` |
| Shell | `sudo docker exec -it fieldreport-backend bash` |

---

## 9. Contact support

| Problème | Action |
|----------|--------|
| Serveur inaccessible | Vérifier `sudo docker ps`, `sudo systemctl status nginx` |
| Base corrompue | Restaurer depuis backup (voir DRP) |
| Erreur après mise à jour | Rollback (voir UPDATE_PROCEDURE.md) |
| Espace disque plein | `df -h`, supprimer vieux PDF, vérifier photos |
