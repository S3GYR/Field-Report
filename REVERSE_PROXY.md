# REVERSE_PROXY

FieldReport v1.1 — Configuration reverse proxy
Date : 2026-06-02

---

## Principe

Le conteneur FieldReport écoute sur le port 8200 en local (`127.0.0.1:8200`). Il ne doit **jamais** être exposé directement sur Internet.

Un reverse proxy (Nginx ou Traefik) assure :
- Terminaison HTTPS
- Redirection HTTP → HTTPS
- Certificats SSL Let's Encrypt
- Accès unique point d'entrée

---

## Option A — Nginx

### Installation Nginx

```bash
sudo apt-get update
sudo apt-get install -y nginx
sudo systemctl enable nginx
```

### Configuration Let's Encrypt (Certbot)

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d fieldreport.example.com
```

### Fichier de configuration

`/etc/nginx/sites-available/fieldreport`

```nginx
server {
    listen 80;
    server_name fieldreport.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name fieldreport.example.com;

    ssl_certificate /etc/letsencrypt/live/fieldreport.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/fieldreport.example.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/fieldreport.example.com/chain.pem;

    # Sécurité SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;

    # Logs
    access_log /var/log/nginx/fieldreport-access.log;
    error_log /var/log/nginx/fieldreport-error.log;

    # Taille max upload (photos)
    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:8200;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
    }
}
```

### Activation

```bash
sudo ln -s /etc/nginx/sites-available/fieldreport /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Renouvellement automatique Let's Encrypt

```bash
sudo certbot renew --dry-run
# Le renouvellement est automatiquement configuré par certbot (cron/systemd timer)
```

---

## Option B — Traefik

### Docker Compose avec Traefik

Créer un `docker-compose.prod.yml` :

```yaml
version: "3.9"

services:
  traefik:
    image: traefik:v3.0
    container_name: traefik
    command:
      - "--api.dashboard=false"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.email=admin@example.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
      - "--entrypoints.web.http.redirections.entryPoint.to=websecure"
      - "--entrypoints.web.http.redirections.entryPoint.scheme=https"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /opt/fieldreport/letsencrypt:/letsencrypt
    restart: unless-stopped

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
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.fieldreport.rule=Host(`fieldreport.example.com`)"
      - "traefik.http.routers.fieldreport.entrypoints=websecure"
      - "traefik.http.routers.fieldreport.tls.certresolver=letsencrypt"
      - "traefik.http.services.fieldreport.loadbalancer.server.port=8200"
    restart: unless-stopped
```

### Lancement

```bash
cd /opt/fieldreport
sudo docker compose -f docker-compose.prod.yml up -d
```

---

## Vérification HTTPS

```bash
# Test redirection HTTP → HTTPS
curl -I http://fieldreport.example.com
# Attendu : HTTP/1.1 301 Moved Permanently

# Test HTTPS
curl -I https://fieldreport.example.com
# Attendu : HTTP/2 200

# Test certificat
openssl s_client -connect fieldreport.example.com:443 -servername fieldreport.example.com < /dev/null 2>/dev/null | openssl x509 -noout -dates
```
