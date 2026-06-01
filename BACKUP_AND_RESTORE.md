# BACKUP_AND_RESTORE

## Préambule

FieldReport utilise **SQLite** (base fichier unique) et **stockage local** (photos + exports PDF). La sauvegarde est donc simple : copier des fichiers.

---

## 1. Sauvegarde SQLite

### 1.1 Windows (natif)

```powershell
# Backup avec timestamp
$date = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item storage\reports.db -Destination "storage\reports-backup-$date.db"
Write-Host "Backup created: storage\reports-backup-$date.db"

# Backup compressé
Compress-Archive -Path storage\reports.db -DestinationPath "storage\reports-backup-$date.zip"
```

### 1.2 Linux / macOS (natif)

```bash
# Backup avec timestamp
date_str=$(date +%Y%m%d_%H%M%S)
cp storage/reports.db "storage/reports-backup-${date_str}.db"
echo "Backup created: storage/reports-backup-${date_str}.db"

# Backup compressé
tar czf "storage/reports-backup-${date_str}.tar.gz" storage/reports.db
```

### 1.3 Docker

```bash
# Backup depuis le conteneur
docker cp fieldreport-backend:/app/backend/storage/reports.db \
  ./reports-backup-$(date +%Y%m%d_%H%M%S).db

# Backup via exec (le conteneur doit tourner)
docker exec fieldreport-backend \
  sh -c 'cp /app/backend/storage/reports.db /app/backend/storage/reports-backup-$(date +%Y%m%d_%H%M%S).db'
```

### 1.4 Automatisation (cron Linux)

```bash
# Crontab : backup quotidien à 2h du matin
0 2 * * * /bin/bash -c 'cd /opt/fieldreport && cp storage/reports.db storage/reports-backup-$(date +\%Y\%m\%d).db && find storage -name "reports-backup-*.db" -mtime +30 -delete'
```

---

## 2. Sauvegarde Photos

### 2.1 Windows (natif)

```powershell
$date = Get-Date -Format "yyyyMMdd"
Compress-Archive -Path storage\photos\* -DestinationPath "storage\photos-backup-$date.zip"
```

### 2.2 Linux / macOS (natif)

```bash
date_str=$(date +%Y%m%d)
tar czf "storage/photos-backup-${date_str}.tar.gz" -C storage photos/
```

### 2.3 Docker

```bash
docker cp fieldreport-backend:/app/backend/storage/photos \
  ./photos-backup-$(date +%Y%m%d)
```

---

## 3. Sauvegarde Complète (Base + Photos + Exports)

### 3.1 Script Windows (`scripts/backup.ps1`)

```powershell
param(
    [string]$Destination = ".\backups",
    [int]$KeepDays = 30
)

$date = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = Join-Path $Destination "backup-$date"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

# Copier la base
Copy-Item storage\reports.db (Join-Path $backupDir "reports.db")

# Copier les photos
if (Test-Path storage\photos) {
    Copy-Item -Recurse storage\photos (Join-Path $backupDir "photos")
}

# Copier les exports PDF
if (Test-Path storage\exports) {
    Copy-Item -Recurse storage\exports (Join-Path $backupDir "exports")
}

# Compresser
Compress-Archive -Path $backupDir -DestinationPath "$backupDir.zip"
Remove-Item -Recurse $backupDir

# Nettoyer les vieux backups
Get-ChildItem $Destination -Filter "backup-*.zip" |
  Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$KeepDays) } |
  Remove-Item

Write-Host "Backup created: $backupDir.zip"
```

### 3.2 Script Linux (`scripts/backup.sh`)

```bash
#!/bin/bash
DEST="${1:-./backups}"
KEEP_DAYS="${2:-30}"
DATE_STR=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$DEST/backup-$DATE_STR"

mkdir -p "$BACKUP_DIR"

cp storage/reports.db "$BACKUP_DIR/"
[ -d storage/photos ] && cp -r storage/photos "$BACKUP_DIR/"
[ -d storage/exports ] && cp -r storage/exports "$BACKUP_DIR/"

tar czf "$BACKUP_DIR.tar.gz" -C "$DEST" "backup-$DATE_STR"
rm -rf "$BACKUP_DIR"

# Nettoyer les vieux backups
find "$DEST" -name "backup-*.tar.gz" -mtime +$KEEP_DAYS -delete

echo "Backup created: $BACKUP_DIR.tar.gz"
```

---

## 4. Restauration Complète

### 4.1 Arrêter l'application

```bash
# Docker
docker compose down

# Natif (Ctrl+C ou kill du process uvicorn)
```

### 4.2 Restaurer les fichiers

```bash
# Extraire le backup
tar xzf backups/backup-20260601_120000.tar.gz

# Restaurer la base
cp backups/backup-20260601_120000/reports.db storage/reports.db

# Restaurer les photos
rm -rf storage/photos
cp -r backups/backup-20260601_120000/photos storage/

# Restaurer les exports
rm -rf storage/exports
cp -r backups/backup-20260601_120000/exports storage/
```

### 4.3 Redémarrer

```bash
# Docker
docker compose up -d

# Natif
cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8200
```

### 4.4 Vérification post-restauration

```bash
# Vérifier la santé
curl http://localhost:8200/health

# Vérifier le nombre de rapports
curl http://localhost:8200/api/reports/ | python -m json.tool | grep -c "id"

# Vérifier les photos
ls storage/photos/ | wc -l
```

---

## 5. Reprise après Incident (DR)

### Scénario 1 : Corruption SQLite

```bash
# 1. Arrêter l'application
docker compose down

# 2. Renommer la base corrompue
mv storage/reports.db storage/reports-corrupted.db

# 3. Restaurer depuis le dernier backup
cp backups/backup-$(date +%Y%m%d)/reports.db storage/reports.db

# 4. Redémarrer
docker compose up -d
```

### Scénario 2 : Perte totale des données

```bash
# 1. Recréer le répertoire storage
mkdir -p storage/photos storage/exports

# 2. Restaurer le dernier backup complet
tar xzf backups/backup-YYYYMMDD_HHMMSS.tar.gz -C /tmp/
cp /tmp/backup-*/reports.db storage/
cp -r /tmp/backup-*/photos storage/
cp -r /tmp/backup-*/exports storage/

# 3. Recréer les tables si nécessaire (schema)
docker exec fieldreport-backend python -c \
  "from app.db.base import Base; from app.db.session import engine; \
   from app.models import Photo, Report, Signature, Task; \
   Base.metadata.create_all(engine)"

# 4. Redémarrer
docker compose up -d
```

### Scénario 3 : Fichiers photos manquants (DB OK)

```bash
# Restaurer uniquement les photos depuis le backup
tar xzf backups/backup-YYYYMMDD_HHMMSS.tar.gz -C /tmp/
rm -rf storage/photos
cp -r /tmp/backup-*/photos storage/
# Pas besoin de redémarrer, les fichiers sont servis via StaticFiles
```

---

## 6. Checklist Sauvegarde Quotidienne

- [ ] Backup SQLite créé avec timestamp
- [ ] Backup photos créé (si photos modifiées)
- [ ] Backups compressés et stockés hors site (optionnel)
- [ ] Rotation des vieux backups (> 30 jours supprimés)
- [ ] Test de restauration mensuel effectué

---

## 7. Espace disque estimé

| Élément | Taille typique | Notes |
|---------|---------------|-------|
| SQLite (reports.db) | 10–100 MB | Dépend du nombre de rapports et de photos |
| Photos (storage/photos) | 1–10 MB par photo | Thumbnails générés automatiquement |
| Exports PDF | 100 KB – 2 MB par PDF | Dépend du contenu |
| Backup quotidien | Base + Photos + PDF | Compressé ~30–50% |

**Recommandation** : prévoir au minimum 5x l'espace de la base + photos en stockage backup.
