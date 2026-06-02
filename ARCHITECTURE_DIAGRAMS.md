# ARCHITECTURE_DIAGRAMS

FieldReport v1.1 — Diagrammes d'architecture
Date : 2026-06-02

---

## 1. Diagramme logique

```
┌─────────────────┐
│   Utilisateur   │  Smartphone Android / iPhone / Tablette / PC Windows
│   Navigateur    │  Chrome, Safari, Firefox
└────────┬────────┘
         │ HTTPS (443)
         ▼
┌─────────────────────────┐
│    Reverse Proxy        │  Nginx ou Traefik
│    Terminaison SSL      │  Let's Encrypt
│    Port 80 → 443        │
└────────┬────────────────┘
         │ HTTP (127.0.0.1:8200)
         ▼
┌─────────────────────────┐
│   Docker Host           │  Ubuntu 24.04 LTS / Debian 12
│   Port 8200 local       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   Conteneur Docker      │  fieldreport-backend
│   FastAPI + Uvicorn     │  Python 3.11
│   Port 8200             │
│   Healthcheck /health   │
└────┬──────────────┬─────┘
     │              │
     ▼              ▼
┌──────────┐  ┌──────────┐
│  Jinja2  │  │  API     │
│  Templates│  │  REST    │
│  HTML UI │  │  /api/*  │
└────┬─────┘  └────┬─────┘
     │              │
     └──────┬───────┘
            │
            ▼
┌─────────────────────────┐
│   Services              │
│   • ReportLab (PDF)     │
│   • Pillow (thumbnails) │
│   • PhotoStorage        │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   Stockage persistant   │  Volume bind-mount ./storage → /app/backend/storage
│   ├── SQLite            │  reports.db
│   ├── Photos            │  photos/YYYY/MM/*.jpg
│   ├── Thumbnails        │  photos/YYYY/MM/*.thumb.jpg
│   └── Exports PDF       │  exports/report-*.pdf
└─────────────────────────┘
```

---

## 2. Diagramme réseau

```
Internet
    │
    ▼
┌──────────────────┐
│   Pare-feu UFW   │  Ports ouverts : 22 (SSH), 80 (HTTP), 443 (HTTPS)
│   DROP all other │  Port 8200 bloqué depuis l'extérieur
└────────┬─────────┘
         │
         ▼
┌──────────────────────────┐
│   Nginx / Traefik        │  443/tcp → backend:8200
│   80/tcp → redirect 443  │  Load balancing : N/A (mono-instance)
│   Let's Encrypt          │  SSL/TLS v1.2+
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│   Docker Bridge          │  docker0 / bridge
│   127.0.0.1:8200         │  Non exposé sur 0.0.0.0 en production
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│   fieldreport-backend    │  healthcheck → /health
│   0.0.0.0:8200           │  (interne au conteneur)
└──────────────────────────┘
```

### Tableau ports

| Source | Destination | Port | Protocole | Service |
|--------|-------------|------|-----------|---------|
| Internet | Serveur | 22/tcp | TCP | SSH (admin) |
| Internet | Serveur | 80/tcp | TCP | HTTP (redirect HTTPS) |
| Internet | Serveur | 443/tcp | TCP | HTTPS (application) |
| Serveur | Conteneur | 8200/tcp | TCP | FastAPI (local uniquement) |
| Conteneur | Internet | 53/udp | UDP | DNS (Let's Encrypt, updates) |
| Conteneur | Internet | 80/tcp | TCP | Let's Encrypt validation |

---

## 3. Diagramme stockage

```
/opt/fieldreport/data/  (hôte)
│
├── reports.db           ← SQLite (tables : reports, photos, tasks, signatures)
│                        Taille typique : < 50 Mo (1000 rapports)
│
├── photos/
│   └── 2026/
│       └── 06/
│           ├── photo-dalle-1234567890.jpg
│           ├── photo-dalle-1234567890.thumb.jpg
│           ├── fissure-1234567891.jpg
│           └── fissure-1234567891.thumb.jpg
│
└── exports/
    ├── report-FR-2026-001.pdf
    └── report-FR-2026-002.pdf
```

### Caractéristiques stockage

| Type | Taille typique | Facteur de croissance |
|------|---------------|----------------------|
| SQLite | < 50 Mo | Linéaire (~10 Ko/rapport) |
| Photos (originales) | ~3-5 Mo/photo | Linéaire, principal consommateur |
| Thumbnails | ~100-300 Ko/photo | Linéaire (~5% du poids original) |
| PDF exports | ~500 Ko-2 Mo/PDF | Linéaire, nettoyable |

**Projection** : 100 rapports/an × 10 photos/rapport × 4 Mo = **~4 Go/an**

---

## 4. Diagramme sauvegarde

```
┌─────────────────────────────┐
│   Serveur de production     │
│   /opt/fieldreport/         │
│   │                         │
│   ├── data/                 │
│   │   ├── reports.db        │ ← sqlite3 .backup
│   │   ├── photos/           │ ← tar czf
│   │   └── exports/          │ ← tar czf
│   │                         │
│   └── scripts/backup.sh     │ ← exécuté par cron à 02:00
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   /opt/fieldreport/backups/ │
│   │                         │
│   ├── daily/                │ ← 7 jours de rétention
│   │   ├── reports-20260601.db
│   │   ├── photos-20260601.tar.gz
│   │   └── exports-20260601.tar.gz
│   │                         │
│   ├── weekly/               │ ← 4 semaines (copie dimanche)
│   └── monthly/              │ ← 3 mois (copie 1er du mois)
└────────┬────────────────────┘
         │
         ▼ (optionnel)
┌─────────────────────────────┐
│   Stockage hors site        │
│   NAS / S3 / Serveur secondaire│
└─────────────────────────────┘
```

### Flux de restauration

```
┌─────────────────┐
│   Incident      │  Perte, corruption, erreur de mise à jour
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│   1. Arrêter le conteneur   │  docker compose down
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   2. Restaurer la base      │  cp backups/daily/reports-XXX.db data/
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   3. Restaurer les photos     │  tar xzf backups/daily/photos-XXX.tar.gz
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   4. Redémarrer               │  docker compose up -d
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   5. Vérifier               │  curl https://.../health
└─────────────────────────────┘
```
