# INSTALLATION_DOCKER

FieldReport v1.1 — Guide d'installation pas à pas
Date : 2026-06-02

---

## 1. Installation Docker

### Ubuntu 24.04 LTS

```bash
# Mettre à jour les paquets
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

# Ajouter la clé GPG officielle Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Ajouter le repository Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Installer Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Vérifier l'installation
sudo docker --version
sudo docker compose version
```

### Debian 12

```bash
# Mettre à jour les paquets
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

# Ajouter la clé GPG officielle Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Ajouter le repository Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Installer Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Vérifier l'installation
sudo docker --version
sudo docker compose version
```

### Activer Docker sans sudo (optionnel)

```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

## 2. Téléchargement du projet

```bash
# Créer le répertoire d'installation
sudo mkdir -p /opt/fieldreport
sudo chown $USER:$USER /opt/fieldreport
cd /opt/fieldreport

# Cloner le repository (adapter l'URL)
git clone https://github.com/segyr/fieldreport.git .

# Ou transférer manuellement les fichiers (scp, rsync, etc.)
# scp -r ./fieldreport user@server:/opt/
```

---

## 3. Création des dossiers de données

```bash
cd /opt/fieldreport

# Créer les répertoires de stockage
mkdir -p data/photos data/exports backups/daily backups/weekly backups/monthly

# Permissions (l'utilisateur du conteneur Docker utilise uid 0 par défaut)
# Le bind-mount Docker utilise les permissions du système hôte
chmod 755 data data/photos data/exports backups
```

---

## 4. Configuration du docker-compose.yml de production

Le `docker-compose.yml` livré utilise `./storage` comme volume. En production, modifiez-le pour pointer vers `/opt/fieldreport/data`.

```yaml
version: "3.9"

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    container_name: fieldreport-backend
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8200"]
    environment:
      - DATABASE_URL=sqlite:///./storage/reports.db
      - PYTHONDONTWRITEBYTECODE=1
      - PYTHONUNBUFFERED=1
    volumes:
      - /opt/fieldreport/data:/app/backend/storage
    ports:
      - "127.0.0.1:8200:8200"
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8200/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    restart: unless-stopped
```

**Changements importants** :
- `volumes` pointe vers `/opt/fieldreport/data`
- `ports` écoute uniquement sur `127.0.0.1` (pas 0.0.0.0) pour forcer le passage par le reverse proxy

---

## 5. Lancement

```bash
cd /opt/fieldreport

# Construire et démarrer
sudo docker compose up -d --build

# Vérifier que le conteneur tourne
sudo docker ps

# Résultat attendu :
# CONTAINER ID   IMAGE                    COMMAND                  STATUS         PORTS
# xxxxxxx        fieldreport-backend      "uvicorn app.main:ap…"   Up 2 minutes   127.0.0.1:8200->8200/tcp
```

---

## 6. Initialisation de la base de données

```bash
# Créer les tables (une seule fois à la première installation)
sudo docker exec fieldreport-backend python -c \
  "from app.db.base import Base; from app.db.session import engine; \
   from app.models import Photo, Report, Signature, Task; \
   Base.metadata.create_all(engine)"
```

---

## 7. Vérifications

### Conteneur actif

```bash
sudo docker ps --filter name=fieldreport
```

### Logs

```bash
sudo docker logs fieldreport-backend --tail 50
```

### Healthcheck

```bash
curl http://127.0.0.1:8200/health
# Attendu : {"status":"ok"}
```

### Accès API

```bash
curl http://127.0.0.1:8200/api/reports/
# Attendu : [] (tableau vide si aucun rapport)
```

### Swagger UI

Ouvrir dans un navigateur (via tunnel SSH) :
```
http://127.0.0.1:8200/docs
```

---

## 8. Redémarrage et arrêt

```bash
# Redémarrer
sudo docker compose restart

# Arrêter
sudo docker compose down

# Arrêter et supprimer les volumes (ATTENTION : supprime la base SQLite)
sudo docker compose down -v
```

---

## 9. Mise à jour de l'image

```bash
cd /opt/fieldreport
sudo docker compose down
sudo docker compose up -d --build
```
