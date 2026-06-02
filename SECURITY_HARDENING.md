# SECURITY_HARDENING

FieldReport v1.1 — Durcissement sécurité
Date : 2026-06-02

---

## 1. HTTPS obligatoire

FieldReport v1.1 ne supporte pas le HTTPS natif. Déployez obligatoirement un reverse proxy avec SSL.

- Voir `REVERSE_PROXY.md` pour la configuration Nginx/Traefik + Let's Encrypt
- Redirection HTTP → HTTPS systématique
- Certificats renouvelés automatiquement

---

## 2. Pare-feu

### UFW (Ubuntu)

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing

# SSH (si administration distante)
sudo ufw allow 22/tcp

# HTTP/HTTPS (reverse proxy)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Bloquer le port 8200 directement (doit passer par le reverse proxy)
# Par défaut UFW bloque tout ce qui n'est pas explicitement autorisé

sudo ufw enable
```

### Vérification

```bash
sudo ufw status verbose
```

---

## 3. Sauvegardes

- Sauvegarde quotidienne automatique (voir `BACKUP_STRATEGY.md`)
- Stockage des backups hors site (NAS, S3, autre serveur)
- Test de restauration mensuel

---

## 4. Utilisateur non-root

Par défaut, le conteneur Docker tourne en root. Pour durcir :

### Modifier le Dockerfile

Ajouter dans `backend/Dockerfile` :

```dockerfile
# Créer un utilisateur non-root
RUN groupadd -r fieldreport && useradd -r -g fieldreport fieldreport

# Changer les permissions
RUN chown -R fieldreport:fieldreport /app/backend/storage

# Basculer vers l'utilisateur non-root
USER fieldreport
```

### Adapter les permissions du volume hôte

```bash
sudo chown -R 999:999 /opt/fieldreport/data
# (999 = UID/GID de l'utilisateur fieldreport dans le conteneur)
```

---

## 5. Protection reverse proxy

### En-têtes de sécurité (Nginx)

Ajouter dans `/etc/nginx/sites-available/fieldreport` :

```nginx
server {
    # ... configuration existante ...

    # Sécurité headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Limite upload (20 Mo pour les photos)
    client_max_body_size 20M;
}
```

---

## 6. Fail2ban

### Installation

```bash
sudo apt-get install -y fail2ban
```

### Configuration

Créer `/etc/fail2ban/jail.local` :

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[nginx-http-auth]
enabled = true

[nginx-limit-req]
enabled = true
```

### Activation

```bash
sudo systemctl enable fail2ban
sudo systemctl restart fail2ban
```

---

## 7. Mises à jour système

### Automatisation (unattended-upgrades)

```bash
sudo apt-get install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### Manuel

```bash
# Une fois par semaine minimum
sudo apt-get update
sudo apt-get upgrade -y

# Redémarrer si nécessaire
sudo reboot
```

---

## 8. Restrictions réseau additionnelles

### Accès SSH sécurisé

Éditer `/etc/ssh/sshd_config` :

```
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
```

```bash
sudo systemctl restart sshd
```

### Bloquer le port applicatif direct

S'assurer que le port 8200 n'est pas exposé sur l'interface publique :

```bash
# Vérifier
sudo ss -tlnp | grep 8200
# Attendu : 127.0.0.1:8200 uniquement

# Si 0.0.0.0:8200 apparaît, corriger docker-compose.yml :
# ports:
#   - "127.0.0.1:8200:8200"
```

---

## 9. Audit et monitoring

### Lister les conteneurs actifs

```bash
sudo docker ps
```

### Vérifier les images

```bash
sudo docker images
```

### Vérifier les volumes

```bash
sudo docker volume ls
```

---

## 10. Limitations de sécurité connues

FieldReport v1.1 présente les limitations suivantes qui seront corrigées en v2.0 :

- **Pas d'authentification** : L'application est accessible à toute personne connaissant l'URL. Déployer derrière un VPN ou un accès réseau restreint.
- **CORS ouvert** : `allow_origins=["*"]` accepte les requêtes de n'importe quel domaine.
- **Pas de rate limiting** : Aucune protection contre les requêtes répétées.
- **Pas de journalisation d'audit** : Aucun log des actions utilisateur.

---

## Checklist de sécurité pré-déploiement

- [ ] HTTPS activé avec certificat valide
- [ ] Redirection HTTP → HTTPS configurée
- [ ] Pare-feu UFW activé (ports 22, 80, 443 uniquement)
- [ ] Port 8200 non exposé sur 0.0.0.0
- [ ] Sauvegarde quotidienne configurée
- [ ] SSH sécurisé (pas de root, clé uniquement)
- [ ] Fail2ban activé
- [ ] Mises à jour automatiques configurées
- [ ] Headers de sécurité Nginx configurés
- [ ] Accès restreint au réseau local/VPN (si possible)
