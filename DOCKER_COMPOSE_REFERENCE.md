# DOCKER_COMPOSE_REFERENCE

FieldReport v1.1 — Référence Docker Compose
Date : 2026-06-02

---

## Fichier source

`docker-compose.yml` (racine du projet)

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
      - ./storage:/app/backend/storage
    ports:
      - "8200:8200"
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8200/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    restart: unless-stopped
```

---

## Service `backend`

### Build

| Attribut | Valeur | Description |
|----------|--------|-------------|
| `context` | `.` | Répertoire de build = racine du projet |
| `dockerfile` | `backend/Dockerfile` | Chemin du Dockerfile relatif au contexte |

### Conteneur

| Attribut | Valeur | Description |
|----------|--------|-------------|
| `container_name` | `fieldreport-backend` | Nom fixe du conteneur |
| `command` | `uvicorn app.main:app --host 0.0.0.0 --port 8200` | Commande de démarrage (remplace le CMD du Dockerfile) |
| `restart` | `unless-stopped` | Redémarrage automatique sauf arrêt manuel |

### Environnement

| Variable | Valeur | Source | Rôle |
|----------|--------|--------|------|
| `DATABASE_URL` | `sqlite:///./storage/reports.db` | `docker-compose.yml` | Chemin base SQLite dans le conteneur |
| `PYTHONDONTWRITEBYTECODE` | `1` | `docker-compose.yml`, `Dockerfile` | Pas de fichiers `.pyc` |
| `PYTHONUNBUFFERED` | `1` | `docker-compose.yml`, `Dockerfile` | Logs immédiats sur stdout |

### Volumes

| Volume hôte | Volume conteneur | Type | Description |
|-------------|-------------------|------|-------------|
| `./storage` | `/app/backend/storage` | Bind mount | Données persistantes (DB + photos + exports) |

**En production** : Remplacer `./storage` par un chemin absolu (`/opt/fieldreport/data`).

### Ports

| Hôte | Conteneur | Protocole | Description |
|------|-----------|-----------|-------------|
| `8200` | `8200` | TCP | Port applicatif FastAPI/Uvicorn |

**En production** : Limiter à `127.0.0.1:8200:8200` pour forcer le passage par le reverse proxy.

### Healthcheck

| Attribut | Valeur | Description |
|----------|--------|-------------|
| `test` | `python -c "import urllib.request; urllib.request.urlopen('http://localhost:8200/health')"` | Requête HTTP vers `/health` |
| `interval` | `30s` | Intervalle entre deux tests |
| `timeout` | `10s` | Temps max pour considérer un test en échec |
| `retries` | `3` | Nombre d'échecs consécutifs avant état "unhealthy" |
| `start_period` | `10s` | Délai de grâce au démarrage |

---

## Dockerfile (`backend/Dockerfile`)

| Instruction | Valeur | Rôle |
|-------------|--------|------|
| `FROM` | `python:3.11-slim` | Image de base Python 3.11 légère |
| `WORKDIR` | `/app` | Répertoire de travail |
| `ENV` | `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUNBUFFERED=1` | Variables d'environnement |
| `RUN apt-get` | `libjpeg62-turbo-dev`, `zlib1g-dev` | Dépendances système pour Pillow |
| `COPY` | `requirements.txt` | Dépendances Python |
| `RUN pip` | `install -r requirements.txt` | Installation des packages |
| `COPY` | `backend ./backend` | Code source |
| `WORKDIR` | `/app/backend` | Changement de répertoire |
| `RUN mkdir` | `storage/photos storage/exports` | Création dossiers de stockage |
| `CMD` | `uvicorn app.main:app --host 0.0.0.0 --port 8200` | Commande par défaut |

---

## Commandes Docker Compose courantes

```bash
# Démarrer (première fois ou après modification)
docker compose up -d --build

# Démarrer (sans rebuild)
docker compose up -d

# Arrêter
docker compose down

# Redémarrer
docker compose restart

# Voir les logs
docker compose logs -f backend

# Voir les logs des 50 dernières lignes
docker compose logs --tail 50 backend

# Exécuter une commande dans le conteneur
docker compose exec backend python -c "print('OK')"

# Vérifier l'état des conteneurs
docker compose ps

# Vérifier l'état du healthcheck
docker inspect --format='{{.State.Health.Status}}' fieldreport-backend
```

---

## Dépendances fonctionnelles

Le service `backend` est **autonome**. Aucune dépendance externe n'est requise :

- Pas de base de données externe (SQLite embarqué)
- Pas de cache (Redis)
- Pas de queue (RabbitMQ, Celery)
- Pas de stockage objet (S3)

Cette architecture simplifie grandement le déploiement et la maintenance.
