# DISASTER_RECOVERY_PLAN

FieldReport v1.1 — Plan de reprise après sinistre
Date : 2026-06-02

---

## Définitions

- **RTO** (Recovery Time Objective) : Temps maximum acceptable pour restaurer le service
- **RPO** (Recovery Point Objective) : Quantité maximale de données acceptables à perdre

---

## Scénario 1 — Perte du serveur complet

### Impact

- Indisponibilité totale de l'application
- Perte des données si les sauvegardes ne sont pas stockées hors site
- Impossibilité pour les agents de créer des rapports

### RTO

**4 heures** (avec un nouveau serveur + backups disponibles)

### RPO

**24 heures** (dernière sauvegarde quotidienne)

### Procédure

```bash
# 1. Provisionner un nouveau serveur (VPS, cloud, ou physique)
# 2. Installer Docker (voir INSTALLATION_DOCKER.md)

# 3. Restaurer le code
sudo mkdir -p /opt/fieldreport
sudo chown $USER:$USER /opt/fieldreport
cd /opt/fieldreport
git clone https://github.com/segyr/fieldreport.git .

# 4. Restaurer les données depuis la dernière backup
sudo mkdir -p /opt/fieldreport/data/photos /opt/fieldreport/data/exports
# Récupérer les fichiers depuis le stockage hors site (NAS, S3, etc.)
# Exemple avec rsync depuis un NAS :
rsync -avz admin@nas:/backups/fieldreport/latest/ /tmp/fieldreport-restore/

# Restaurer la base
sudo cp /tmp/fieldreport-restore/reports-*.db /opt/fieldreport/data/reports.db

# Restaurer les photos
sudo tar xzf /tmp/fieldreport-restore/photos-*.tar.gz -C /opt/fieldreport/data

# Restaurer les exports
sudo tar xzf /tmp/fieldreport-restore/exports-*.tar.gz -C /opt/fieldreport/data

# 5. Lancer l'application
sudo docker compose up -d --build

# 6. Vérifier
curl -s http://127.0.0.1:8200/health
```

### Prévention

- Sauvegardes quotidiennes copiées vers un NAS ou un service cloud
- Documentation de l'installation complète et testée
- Liste des dépendances système (Docker version, OS)

---

## Scénario 2 — Panne disque (données corrompues)

### Impact

- SQLite corrompue ou illisible
- Photos potentiellement intactes (si sur partition séparée)
- Exports PDF à regénérer

### RTO

**1 heure**

### RPO

**24 heures**

### Procédure

```bash
# 1. Arrêter l'application
sudo docker compose -f /opt/fieldreport/docker-compose.yml down

# 2. Vérifier l'intégrité de la base actuelle
sqlite3 /opt/fieldreport/data/reports.db "PRAGMA integrity_check;"
# Si "ok" → ne pas restaurer, chercher une autre cause
# Si "error" → restaurer

# 3. Restaurer la base depuis la dernière backup valide
LAST_GOOD=$(ls -t /opt/fieldreport/backups/daily/reports-*.db | head -1)
sudo cp "$LAST_GOOD" /opt/fieldreport/data/reports.db

# 4. Vérifier la restauration
sqlite3 /opt/fieldreport/data/reports.db "SELECT COUNT(*) FROM reports;"

# 5. Redémarrer
sudo docker compose -f /opt/fieldreport/docker-compose.yml up -d

# 6. Regénérer les PDF si nécessaire (optionnel, les PDF peuvent être regénérés à la demande)
```

### Prévention

- `PRAGMA integrity_check` mensuel
- Surveillance espace disque (`df -h`)
- Partition séparée pour les données si possible

---

## Scénario 3 — Corruption SQLite

### Impact

- Base de données illisible
- Perte des rapports, tâches, signatures
- Photos sur disque potentiellement intactes mais orphelines

### RTO

**30 minutes**

### RPO

**24 heures** (ou 0 si corruption détectée immédiatement après backup)

### Procédure

```bash
# 1. Arrêter le conteneur
sudo docker compose down

# 2. Sauvegarder la base corrompue (pour analyse)
sudo cp /opt/fieldreport/data/reports.db /opt/fieldreport/data/reports-corrupted.db

# 3. Essayer de récupérer avec sqlite3
sqlite3 /opt/fieldreport/data/reports-corrupted.db ".dump" > /tmp/recovery.sql
sqlite3 /opt/fieldreport/data/reports.db < /tmp/recovery.sql
# Si échec → restaurer depuis backup

# 4. Si dump échoue, restaurer depuis backup
LAST_GOOD=$(ls -t /opt/fieldreport/backups/daily/reports-*.db | head -1)
sudo cp "$LAST_GOOD" /opt/fieldreport/data/reports.db

# 5. Redémarrer
sudo docker compose up -d
```

### Prévention

- Utiliser `.backup` (atomic) plutôt que `cp`
- Ne jamais copier le `.db` pendant une écriture
- Éviter l'accès concurrent SQLite

---

## Scénario 4 — Suppression accidentelle (rapport, photo, ou base)

### Impact

- Données supprimées par erreur utilisateur
- Pas de corbeille / undo dans l'application

### RTO

**15 minutes**

### RPO

**0** (si suppression détectée avant la prochaine backup, sinon 24h)

### Procédure

```bash
# CAS A : Suppression d'un rapport
# Pas de récupération unitaire possible sans backup.
# Restaurer la base complète depuis la dernière backup.
# Les rapports créés depuis la backup seront perdus.

# CAS B : Suppression d'une photo
# Restaurer les photos depuis le tar.gz
sudo tar xzf /opt/fieldreport/backups/daily/photos-20260601.tar.gz -C /tmp/
# Récupérer manuellement le fichier depuis /tmp/photos/YYYY/MM/
sudo cp /tmp/photos/YYYY/MM/fichier.jpg /opt/fieldreport/data/photos/YYYY/MM/

# CAS C : Suppression de la base entière
# Restaurer immédiatement depuis la dernière backup
sudo cp /opt/fieldreport/backups/daily/reports-$(date +%Y%m%d)*.db /opt/fieldreport/data/reports.db
sudo docker compose restart
```

### Prévention

- Confirmer les suppressions (modal HTML — déjà implémenté)
- Backup plus fréquent si activité intense
- Export PDF régulier comme archive read-only

---

## Scénario 5 — Erreur de mise à jour

### Impact

- Application ne démarre pas
- Erreur 500 sur certaines routes
- Nouvelle version incompatible avec la base existante

### RTO

**30 minutes**

### RPO

**0** (la backup pré-mise à jour est faite juste avant)

### Procédure

```bash
cd /opt/fieldreport

# 1. Arrêter
sudo docker compose down

# 2. Restaurer le code
git checkout v1.1.0  # ou le dernier tag stable

# 3. Restaurer la base (pré-mise à jour)
sudo cp backups/daily/reports-$(date +%Y%m%d)*.db data/reports.db

# 4. Reconstruire
sudo docker compose up -d --build

# 5. Vérifier
curl -s http://127.0.0.1:8200/health
```

### Prévention

- Toujours sauvegarder avant mise à jour (checklist UPDATE_PROCEDURE.md)
- Tester la mise à jour sur un environnement de recette
- Taguer les versions stables (`git tag`)

---

## Récapitulatif

| Scénario | RTO | RPO | Procédure principale |
|----------|-----|-----|---------------------|
| Perte serveur complet | 4h | 24h | Nouveau serveur + restore code + données |
| Panne disque | 1h | 24h | Restore base depuis backup, photos intactes |
| Corruption SQLite | 30 min | 24h | `.dump` recovery ou restore backup |
| Suppression accidentelle | 15 min | 0-24h | Restore fichier ou base selon cas |
| Erreur mise à jour | 30 min | 0 | Checkout version stable + restore base |

---

## Checklist DRP annuel (à planifier)

- [ ] Tester la restauration complète sur un serveur vierge
- [ ] Vérifier l'intégrité SQLite (`PRAGMA integrity_check`)
- [ ] Contrôler l'espace disque disponible
- [ ] Vérifier que les backups hors site sont accessibles
- [ ] Mettre à jour la procédure si l'architecture a changé
