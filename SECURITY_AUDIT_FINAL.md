# SECURITY_AUDIT_FINAL

FieldReport v1.1 RC1 — Audit sécurité
Date : 2026-06-02
Auditeur : Architecte logiciel senior

---

## 1. Résumé exécutif

FieldReport v1.1 n'a **pas de système d'authentification**. C'est une architecture "trust the network" : toute personne ayant accès à l'URL a un accès complet en lecture/écriture/suppression. Le déploiement doit impérativement s'accompagner d'une restriction réseau (VPN, IP whitelist, ou accès LAN uniquement).

---

## 2. Exposition réseau

| Élément | État | Risque | Justification |
|---------|------|--------|---------------|
| CORS | `allow_origins=["*"]` | **HIGH** | `backend/app/main.py:21-27` : Toute origine peut appeler l'API. Facilite les attaques CSRF si un utilisateur visitant un site malveillant est authentifié... mais comme il n'y a pas d'auth, le risque CSRF est limité. Le risque principal est le scraping. |
| Port exposé | `8200:8200` (0.0.0.0) | **HIGH** | `docker-compose.yml:16-17` : Le port 8200 est exposé sur toutes les interfaces. Doit être `127.0.0.1:8200:8200` en production. |
| HTTPS natif | Absent | **HIGH** | Le conteneur ne supporte pas le HTTPS. Un reverse proxy est obligatoire en production. |

---

## 3. Docker

| Élément | État | Risque | Justification |
|---------|------|--------|---------------|
| Image de base | `python:3.11-slim` | **LOW** | Image officielle Docker Hub, maintenue. |
| User conteneur | `root` (par défaut) | **MEDIUM** | Le conteneur tourne en root. Si compromis, l'attaquant a accès root sur le host (risque limité par les namespaces Docker mais non nul). |
| Secrets | Aucun | **LOW** | Pas de clé API, pas de token, pas de mot de passe. L'application n'utilise pas de secret. |
| Capabilities | Par défaut | **LOW** | Pas de `CAP_SYS_ADMIN` ou capabilities dangereuses demandées. |

---

## 4. Reverse proxy

| Élément | État | Risque | Recommandation |
|---------|------|--------|----------------|
| Documentation proxy | Présente | **LOW** | `REVERSE_PROXY.md` couvre Nginx et Traefik avec Let's Encrypt. |
| Headers sécurité | Documentés | **LOW** | `SECURITY_HARDENING.md` liste les headers à ajouter. |
| Rate limiting | Absent | **MEDIUM** | Pas de limite de requêtes. Un bot peut spammer l'API. Ajouter `limit_req` Nginx ou middleware FastAPI. |

---

## 5. HTTPS

| Élément | État | Risque | Recommandation |
|---------|------|--------|----------------|
| Certificat | Via Let's Encrypt | **LOW** | Automatique, gratuit, reconnu. |
| Renouvellement | Automatique (Certbot/Traefik) | **LOW** | Cron/systemd timer configuré par Certbot. |
| Redirection | Documentée | **LOW** | HTTP → HTTPS configuré dans `REVERSE_PROXY.md`. |

---

## 6. SQLite

| Élément | État | Risque | Justification |
|---------|------|--------|---------------|
| Injection SQL | Protégé | **LOW** | SQLAlchemy ORM avec paramètres bindés. Pas de requêtes brutes. |
| Fichier DB | `storage/reports.db` | **MEDIUM** | Si le volume est exposé ou mal protégé, le fichier peut être copié. Pas de chiffrement. |
| Backup | Scripté | **LOW** | `BACKUP_STRATEGY.md` utilise `sqlite3 .backup` (atomic copy). |

---

## 7. Permissions

| Élément | État | Risque | Justification |
|---------|------|--------|---------------|
| Volume hôte | `755` | **LOW** | Lecture/écriture/exécution pour owner, lecture/exécution pour group/autres. Acceptable si le serveur est mono-utilisateur. |
| Fichiers uploadés | `644` (défaut umask) | **LOW** | Photos lisibles par tous sur le système hôte. Acceptable dans un contexte restreint. |

---

## 8. Uploads

| Élément | État | Risque | Justification |
|---------|------|--------|---------------|
| Type MIME | `accept="image/*"` côté client | **MEDIUM** | Côté serveur, l'endpoint `upload_photo` ne vérifie PAS le type MIME. N'importe quel fichier peut être uploadé. |
| Extension | Vérifiée (slugify) | **LOW** | L'extension du fichier original est conservée. Mais pas de filtrage `.jpg`, `.png`, etc. |
| Taille max | Configurée (15 Mo) | **HIGH** | `photo_max_size_mb` existe dans `config.py` mais **n'est pas vérifiée** dans l'endpoint. Un upload de plusieurs Go est théoriquement possible. |
| Traversée de répertoire | Protégé | **LOW** | Le chemin est construit côté serveur (`target_dir / final_name`), pas à partir de l'input utilisateur. |
| Exécution fichier uploadé | Impossible | **LOW** | Les fichiers sont servis via `StaticFiles` (download), jamais exécutés. |

### Vulnérabilité upload

```python
# backend/app/api/photos.py:14-39
# Aucune vérification de taille ni de type MIME
```

**Recommandation critique** : Ajouter dans `upload_photo` :
```python
from app.core.config import get_settings
settings = get_settings()

# Vérifier taille
if file.size and file.size > settings.photo_max_size_mb * 1024 * 1024:
    raise HTTPException(413, detail="File too large")

# Vérifier type MIME
if file.content_type and not file.content_type.startswith("image/"):
    raise HTTPException(415, detail="Only image files allowed")
```

---

## 9. Génération PDF

| Élément | État | Risque | Justification |
|---------|------|--------|---------------|
| Injection contenu | Partiel | **MEDIUM** | Les commentaires et descriptions sont injectés dans `Paragraph()` sans échappement HTML. ReportLab interprète un sous-ensemble de balises HTML (`<b>`, `<i>`, etc.). Un commentaire `<script>` serait inoffensif, mais une balise malformée pourrait casser le PDF. |
| Path traversal | Protégé | **LOW** | Les chemins de photo sont résolus via `settings.storage_root / photo.filepath` (Path sécurisé). |
| Ressources | Sans limite | **LOW** | Un rapport avec 100 photos génère un PDF très lourd. Pas de limite de pages. |

---

## 10. Vulnérabilités identifiées

| ID | Vulnérabilité | Sévérité | Fichier | Exploitation |
|----|---------------|----------|---------|--------------|
| SEC-001 | Pas d'authentification | **CRITICAL** | Global | N'importe qui avec l'URL peut créer, modifier, supprimer tout. |
| SEC-002 | CORS ouvert `*` | **HIGH** | `main.py:23` | Scraping API, requêtes cross-origin non contrôlées. |
| SEC-003 | Port 8200 exposé 0.0.0.0 | **HIGH** | `docker-compose.yml:16` | Contournement possible du reverse proxy. |
| SEC-004 | Upload sans limite de taille | **HIGH** | `api/photos.py:14` | Remplissage disque (DoS). |
| SEC-005 | Upload sans vérification type MIME | **MEDIUM** | `api/photos.py:14` | Upload de fichiers non-image possibles. |
| SEC-006 | Conteneur root | **MEDIUM** | `Dockerfile` | Élévation de privilèges si escape conteneur. |
| SEC-007 | Pas de rate limiting | **MEDIUM** | Global | Spam API, brute force (futur si auth ajoutée). |
| SEC-008 | Stack trace exposée | **LOW** | Global | FastAPI mode dev expose les stack traces en JSON (pas de `debug=False` explicite). |

---

## 11. Bonnes pratiques manquantes

| Pratique | Priorité | Impact |
|----------|----------|--------|
| Authentification JWT ou session | **CRITICAL** | Blocage pour usage multi-utilisateur |
| Rate limiting middleware | **HIGH** | DoS, spam |
| Validation taille upload | **HIGH** | Remplissage disque |
| Validation type MIME upload | **MEDIUM** | Fichiers malveillants |
| Utilisateur non-root conteneur | **MEDIUM** | Privilege escalation |
| `X-Content-Type-Options` etc. | **LOW** | Headers sécurité navigateur |

---

## 12. Conclusion sécurité

| Domaine | Note /10 | Justification |
|---------|----------|---------------|
| Exposition réseau | 3 | CORS *, port 0.0.0.0, pas d'HTTPS natif |
| Docker | 6 | Image officielle mais root, pas de capabilities restreintes |
| SQLite | 7 | ORM protège des injections, mais pas de chiffrement |
| Uploads | 4 | Pas de limite taille, pas de vérification type MIME |
| Reverse proxy / HTTPS | 8 | Bien documenté mais pas appliqué par défaut |

**Note moyenne sécurité : 5.6/10**

### Recommandations classées

**Critique**
- Ajouter authentification avant tout usage multi-utilisateur
- Limiter le port Docker à `127.0.0.1:8200`
- Vérifier la taille des uploads côté serveur

**Important**
- Restreindre CORS aux domaines de production
- Ajouter rate limiting middleware
- Créer utilisateur non-root dans le Dockerfile

**Amélioration**
- Activer `debug=False` en production
- Ajouter validation type MIME upload
- Headers de sécurité HTTP
