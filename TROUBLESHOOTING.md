# TROUBLESHOOTING

FieldReport v1.1 — Guide de dépannage
Date : 2026-06-02

---

## Application inaccessible

### Symptôme
Le navigateur affiche "Impossible de se connecter" ou erreur 502.

### Diagnostic

```bash
# Vérifier que le conteneur tourne
sudo docker ps --filter name=fieldreport

# Si le conteneur est absent
sudo docker compose -f /opt/fieldreport/docker-compose.yml up -d

# Vérifier le healthcheck
curl -s http://127.0.0.1:8200/health

# Vérifier les logs
sudo docker logs fieldreport-backend --tail 50
```

### Causes possibles

| Cause | Solution |
|-------|----------|
| Conteneur arrêté | `sudo docker compose up -d` |
| Port 8200 occupé | Modifier le port dans `docker-compose.yml` (`8201:8200`) |
| Erreur au démarrage (ImportError) | Reconstruire l'image : `docker compose up -d --build` |
| Nginx/Traefik arrêté | `sudo systemctl restart nginx` ou `docker compose restart traefik` |

---

## Docker arrêté

### Symptôme
`docker: Cannot connect to the Docker daemon`

### Solution

```bash
# Vérifier le statut
sudo systemctl status docker

# Démarrer Docker
sudo systemctl start docker
sudo systemctl enable docker

# Vérifier les permissions
sudo usermod -aG docker $USER
```

---

## Erreur base SQLite

### Symptôme
`no such table: reports` ou `sqlite3.OperationalError`

### Diagnostic

```bash
# Vérifier que le fichier existe
ls -la /opt/fieldreport/data/reports.db

# Vérifier l'intégrité
sqlite3 /opt/fieldreport/data/reports.db "PRAGMA integrity_check;"
```

### Solutions

```bash
# Initialiser la base (première installation)
sudo docker exec fieldreport-backend python -c \
  "from app.db.base import Base; from app.db.session import engine; \
   from app.models import Photo, Report, Signature, Task; \
   Base.metadata.create_all(engine)"

# Restaurer depuis la sauvegarde
sudo cp /opt/fieldreport/backups/daily/reports-YYYYMMDD.db /opt/fieldreport/data/reports.db
sudo docker compose restart
```

---

## Photos non accessibles

### Symptôme
Les photos s'affichent en casse (image brisée) ou retournent 404.

### Diagnostic

```bash
# Vérifier le volume Docker
sudo docker inspect fieldreport-backend | grep -A 5 Mounts

# Vérifier que les fichiers existent sur l'hôte
ls -la /opt/fieldreport/data/photos/

# Vérifier les permissions
sudo ls -la /opt/fieldreport/data/photos/2026/
```

### Solutions

```bash
# Corriger les permissions
sudo chown -R 1000:1000 /opt/fieldreport/data/photos
sudo chmod -R 755 /opt/fieldreport/data/photos

# Redémarrer le conteneur
sudo docker compose restart
```

---

## Génération PDF échoue

### Symptôme
Le bouton "Générer le PDF" retourne une erreur.

### Diagnostic

```bash
# Vérifier que ReportLab est installé
sudo docker exec fieldreport-backend python -c "import reportlab; print(reportlab.Version)"

# Vérifier les logs
sudo docker logs fieldreport-backend --tail 30 | grep -i pdf

# Vérifier le dossier exports
ls -la /opt/fieldreport/data/exports/
```

### Solutions

```bash
# Créer le dossier exports si manquant
mkdir -p /opt/fieldreport/data/exports
sudo docker compose restart

# Reconstruire l'image si ReportLab manquant
sudo docker compose up -d --build
```

---

## GPS indisponible

### Symptôme
"GPS : échec de l'acquisition" ou "GPS : non disponible"

### Diagnostic

| Contexte | Cause probable |
|----------|---------------|
| Sur PC desktop | Pas de module GPS hardware — comportement normal |
| Sur mobile avec GPS refusé | L'utilisateur a refusé la permission géolocalisation |
| Sur mobile avec GPS activé mais pas de fix | Intérieur, tunnel, ou première utilisation (cold start) |

### Solutions

- Sur mobile : activer la géolocalisation dans les paramètres système
- Sur mobile : accorder la permission au navigateur
- Attendre 10-15 secondes en extérieur dégagé pour le premier fix
- L'upload de photo est possible même sans GPS

---

## Problème de permissions

### Symptôme
Erreur 500 à l'upload de photo, ou `Permission denied` dans les logs.

### Solution

```bash
# Vérifier l'utilisateur exécutant le conteneur
sudo docker exec fieldreport-backend id

# Corriger les permissions du volume
sudo chown -R $(id -u):$(id -g) /opt/fieldreport/data
sudo chmod -R u+rwX /opt/fieldreport/data

# Si le conteneur tourne en root (par défaut), les permissions ne posent pas problème
# Mais il est recommandé de créer un utilisateur dédié (voir SECURITY_HARDENING.md)
```

---

## Logs à consulter

| Log | Commande | Quand consulter |
|-----|----------|-----------------|
| Application | `sudo docker logs fieldreport-backend --tail 100` | Erreurs 500, crash |
| Nginx access | `sudo tail -f /var/log/nginx/fieldreport-access.log` | Erreurs 404, 502, 503 |
| Nginx error | `sudo tail -f /var/log/nginx/fieldreport-error.log` | Erreurs proxy |
| Sauvegardes | `sudo tail -f /var/log/fieldreport-backup.log` | Échec de backup |
| Système | `sudo journalctl -u docker -f` | Problèmes Docker |

---

## Réinitialisation complète (données de test)

**ATTENTION** : Cette procédure supprime TOUTES les données.

```bash
cd /opt/fieldreport

# Arrêter
sudo docker compose down

# Supprimer les données
sudo rm -rf data/*
mkdir -p data/photos data/exports

# Recréer la base
sudo docker compose up -d
sudo docker exec fieldreport-backend python -c \
  "from app.db.base import Base; from app.db.session import engine; \
   from app.models import Photo, Report, Signature, Task; \
   Base.metadata.create_all(engine)"
```
