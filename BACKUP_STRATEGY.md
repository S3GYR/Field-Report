# BACKUP_STRATEGY

FieldReport v1.1 — Stratégie de sauvegarde
Date : 2026-06-02

---

## Composants à sauvegarder

| Composant | Chemin | Type | Fréquence | Rétention |
|-----------|--------|------|-----------|-----------|
| Base SQLite | `/opt/fieldreport/data/reports.db` | Fichier | Quotidienne | 30 jours |
| Photos | `/opt/fieldreport/data/photos/` | Dossier | Quotidienne | 90 jours |
| Exports PDF | `/opt/fieldreport/data/exports/` | Dossier | Quotidienne | 30 jours |
| Code source | `/opt/fieldreport/` | Dossier | Hebdomadaire | 4 semaines |

---

## Script de sauvegarde

Créer `/opt/fieldreport/scripts/backup.sh` :

```bash
#!/bin/bash
set -euo pipefail

BACKUP_BASE="/opt/fieldreport/backups"
DATE=$(date +%Y%m%d_%H%M%S)
HOST=$(hostname)

# Dossiers source
DATA_DIR="/opt/fieldreport/data"
DB_FILE="$DATA_DIR/reports.db"
PHOTOS_DIR="$DATA_DIR/photos"
EXPORTS_DIR="$DATA_DIR/exports"

echo "[$(date)] Démarrage sauvegarde FieldReport $DATE"

# === Sauvegarde base SQLite (copie fichier) ===
if [ -f "$DB_FILE" ]; then
    sqlite3 "$DB_FILE" ".backup '$BACKUP_BASE/daily/reports-$DATE.db'"
    echo "[$(date)] Base SQLite sauvegardée"
else
    echo "[$(date)] AVERTISSEMENT : Base SQLite introuvable"
fi

# === Sauvegarde photos (tar.gz) ===
if [ -d "$PHOTOS_DIR" ] && [ "$(ls -A $PHOTOS_DIR)" ]; then
    tar czf "$BACKUP_BASE/daily/photos-$DATE.tar.gz" -C "$DATA_DIR" photos/
    echo "[$(date)] Photos sauvegardées"
else
    echo "[$(date)] AVERTISSEMENT : Dossier photos vide ou inexistant"
fi

# === Sauvegarde exports PDF (tar.gz) ===
if [ -d "$EXPORTS_DIR" ] && [ "$(ls -A $EXPORTS_DIR)" ]; then
    tar czf "$BACKUP_BASE/daily/exports-$DATE.tar.gz" -C "$DATA_DIR" exports/
    echo "[$(date)] Exports PDF sauvegardés"
fi

# === Rotation quotidienne (garde 7 jours) ===
find "$BACKUP_BASE/daily" -name "reports-*.db" -mtime +7 -delete
find "$BACKUP_BASE/daily" -name "photos-*.tar.gz" -mtime +7 -delete
find "$BACKUP_BASE/daily" -name "exports-*.tar.gz" -mtime +7 -delete

# === Copie hebdomadaire (garde 4 semaines) ===
if [ "$(date +%u)" == "7" ]; then
    cp "$BACKUP_BASE/daily/reports-$DATE.db" "$BACKUP_BASE/weekly/" 2>/dev/null || true
    cp "$BACKUP_BASE/daily/photos-$DATE.tar.gz" "$BACKUP_BASE/weekly/" 2>/dev/null || true
    find "$BACKUP_BASE/weekly" -mtime +28 -delete
    echo "[$(date)] Copie hebdomadaire effectuée"
fi

# === Copie mensuelle (garde 3 mois) ===
if [ "$(date +%d)" == "01" ]; then
    cp "$BACKUP_BASE/daily/reports-$DATE.db" "$BACKUP_BASE/monthly/" 2>/dev/null || true
    cp "$BACKUP_BASE/daily/photos-$DATE.tar.gz" "$BACKUP_BASE/monthly/" 2>/dev/null || true
    find "$BACKUP_BASE/monthly" -mtime +90 -delete
    echo "[$(date)] Copie mensuelle effectuée"
fi

echo "[$(date)] Sauvegarde terminée"
```

### Rendre exécutable

```bash
chmod +x /opt/fieldreport/scripts/backup.sh
```

---

## Configuration cron

```bash
# Éditer le crontab root
sudo crontab -e

# Ajouter la ligne suivante (exécution tous les jours à 2h du matin)
0 2 * * * /opt/fieldreport/scripts/backup.sh >> /var/log/fieldreport-backup.log 2>&1
```

---

## Rotation des sauvegardes

| Périodicité | Chemin | Rétention | Action |
|-------------|--------|-----------|--------|
| Quotidienne | `backups/daily/` | 7 jours | Suppression auto via script |
| Hebdomadaire | `backups/weekly/` | 4 semaines | Suppression auto via script |
| Mensuelle | `backups/monthly/` | 3 mois | Suppression auto via script |

---

## Restauration

### Base de données

```bash
# Arrêter l'application
sudo docker compose -f /opt/fieldreport/docker-compose.yml down

# Restaurer la base
sudo cp /opt/fieldreport/backups/daily/reports-YYYYMMDD_HHMMSS.db \
        /opt/fieldreport/data/reports.db

# Redémarrer
sudo docker compose -f /opt/fieldreport/docker-compose.yml up -d
```

### Photos

```bash
# Extraire l'archive
cd /opt/fieldreport/data
sudo tar xzf /opt/fieldreport/backups/daily/photos-YYYYMMDD_HHMMSS.tar.gz

# Redémarrer le conteneur si nécessaire
sudo docker compose -f /opt/fieldreport/docker-compose.yml restart
```

### Restauration complète

```bash
#!/bin/bash
# restore.sh — Restauration complète depuis une sauvegarde

BACKUP_DATE="20260601_020000"  # À adapter
BACKUP_BASE="/opt/fieldreport/backups/daily"
DATA_DIR="/opt/fieldreport/data"

echo "Restauration de la sauvegarde $BACKUP_DATE"

# Arrêter l'application
sudo docker compose -f /opt/fieldreport/docker-compose.yml down

# Restaurer la base
sudo cp "$BACKUP_BASE/reports-$BACKUP_DATE.db" "$DATA_DIR/reports.db"

# Restaurer les photos
sudo tar xzf "$BACKUP_BASE/photos-$BACKUP_DATE.tar.gz" -C "$DATA_DIR"

# Restaurer les exports
if [ -f "$BACKUP_BASE/exports-$BACKUP_DATE.tar.gz" ]; then
    sudo tar xzf "$BACKUP_BASE/exports-$BACKUP_DATE.tar.gz" -C "$DATA_DIR"
fi

# Redémarrer
sudo docker compose -f /opt/fieldreport/docker-compose.yml up -d

echo "Restauration terminée. Vérifiez avec : curl https://fieldreport.example.com/health"
```

---

## Sauvegarde hors site (recommandé)

Pour une protection contre la perte du serveur complet, copier les sauvegardes mensuelles vers un emplacement externe :

```bash
# Exemple avec rsync vers un NAS
rsync -avz /opt/fieldreport/backups/monthly/ admin@nas.local:/backups/fieldreport/

# Exemple avec AWS S3 (nécessite awscli)
aws s3 sync /opt/fieldreport/backups/monthly/ s3://my-backup-bucket/fieldreport/
```
