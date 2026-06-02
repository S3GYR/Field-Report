# README_DEPLOYMENT

FieldReport v1.1 — Guide de déploiement en production
Date : 2026-06-02
Auteur : SEGYR Technologies

---

## Présentation

FieldReport est une application métier de gestion de rapports terrain destinée aux collectivités, agents communaux, conducteurs de travaux, chargés d'affaires, techniciens de maintenance et bureaux d'études.

Elle permet :
- La création et gestion de rapports d'intervention
- La capture photo native avec géolocalisation GPS
- Le suivi des tâches correctives
- La collecte des signatures de validation
- La consultation de l'historique par site
- La génération de comptes-rendus PDF

---

## Architecture

```
Utilisateur (navigateur)
         │
         ▼
┌─────────────────────┐
│  Reverse Proxy      │  Nginx ou Traefik
│  HTTPS (443)        │  Certificat Let's Encrypt
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  Docker Host        │  Ubuntu 24.04 LTS / Debian 12
│  Port 8200          │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  Conteneur Docker   │  fieldreport-backend
│  FastAPI + Uvicorn  │  Python 3.11
│  Port 8200          │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  Volume ./storage   │  SQLite + photos + PDF
│  (bind-mount)       │
└─────────────────────┘
```

---

## Composants

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| Serveur web | Uvicorn (ASGI) | Serveur HTTP pour FastAPI |
| Framework API | FastAPI 0.111 | Routes REST + documentation auto |
| Moteur de templates | Jinja2 3.1.4 | Rendu HTML côté serveur |
| ORM | SQLAlchemy 2.0.30 | Modélisation base de données |
| Base de données | SQLite (fichier) | Stockage relationnel embarqué |
| Génération PDF | ReportLab 4.4.0 | Comptes-rendus PDF |
| Manipulation images | Pillow 10.3.0 | Thumbnails et redimensionnement |
| Conteneur | Docker + Compose | Packaging et déploiement |

---

## Prérequis système

### Système d'exploitation supporté

| OS | Version | Statut |
|----|---------|--------|
| Ubuntu Server | 22.04 LTS, 24.04 LTS | Supporté |
| Debian | 11, 12 | Supporté |
| CentOS/RHEL | 8, 9 | Supporté (Docker requis) |

### Logiciels requis

| Logiciel | Version minimale | Commande de vérification |
|----------|-------------------|--------------------------|
| Docker Engine | 24.0.0 | `docker --version` |
| Docker Compose | 2.20.0 | `docker compose version` |
| curl | (any) | `curl --version` |

### Ressources minimales

| Ressource | Valeur |
|-----------|--------|
| CPU | 1 cœur |
| RAM | 512 Mo |
| Disque | 2 Go (système + application) |

### Ressources recommandées

| Ressource | Valeur |
|-----------|--------|
| CPU | 2 cœurs |
| RAM | 1 Go |
| Disque | 20 Go SSD |
| Réseau | Connexion Internet pour HTTPS et GPS |

---

## Ports utilisés

| Port | Protocole | Direction | Service | Description |
|------|-----------|-----------|---------|-------------|
| 22 | TCP | Ingress | SSH | Administration serveur |
| 80 | TCP | Ingress | Nginx/Traefik | HTTP — redirection vers HTTPS |
| 443 | TCP | Ingress | Nginx/Traefik | HTTPS — accès utilisateurs |
| 8200 | TCP | Local | FieldReport | Port applicatif (non exposé directement) |

**Important** : Le port 8200 ne doit pas être exposé directement sur Internet. Il est accessible uniquement en local via le reverse proxy.

---

## Arborescence des données sur le serveur

```
/opt/fieldreport/                  # Répertoire d'installation
├── docker-compose.yml             # Orchestration Docker
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/                       # Code source
├── data/                          # Données persistantes (recommandé)
│   ├── photos/                    # Photos uploadées
│   │   └── 2026/
│   │       └── 06/
│   │           └── photo-123.jpg
│   ├── exports/                   # PDF générés
│   │   └── report-TEST-001.pdf
│   └── reports.db                 # Base SQLite
├── backups/                       # Sauvegardes
│   ├── daily/
│   ├── weekly/
│   └── monthly/
└── scripts/
    └── backup.sh                  # Script de sauvegarde
```

**Note** : Par défaut, le `docker-compose.yml` utilise `./storage` comme volume. En production, il est recommandé de mapper vers `/opt/fieldreport/data` pour une séparation claire entre code et données.

---

## Points d'accès

| URL | Description |
|-----|-------------|
| `https://fieldreport.example.com/` | Tableau de bord |
| `https://fieldreport.example.com/reports` | Liste des rapports |
| `https://fieldreport.example.com/reports/{id}` | Détail d'un rapport |
| `https://fieldreport.example.com/photos` | Galerie photos |
| `https://fieldreport.example.com/tasks` | Tâches |
| `https://fieldreport.example.com/signatures` | Signatures |
| `https://fieldreport.example.com/history` | Historique |
| `https://fieldreport.example.com/docs` | Documentation API (Swagger) |
| `https://fieldreport.example.com/health` | Healthcheck JSON |

---

## Sécurité — Avertissements

- **Pas d'authentification** : FieldReport v1.1 n'a pas de système de login. Déployez-le derrière un VPN ou un accès réseau restreint.
- **CORS ouvert** : L'application accepte les requêtes de n'importe quelle origine (`allow_origins=["*"]`).
- **HTTPS obligatoire** : En production, utilisez obligatoirement un reverse proxy avec HTTPS.
- **Mono-utilisateur** : SQLite ne supporte pas les écritures concurrentes. Un seul utilisateur à la fois.

---

## Support

Pour toute question de déploiement, consultez :
- `INSTALLATION_DOCKER.md` — Guide d'installation pas à pas
- `TROUBLESHOOTING.md` — Dépannage
- `SECURITY_HARDENING.md` — Durcissement sécurité
