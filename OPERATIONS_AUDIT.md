# OPERATIONS_AUDIT

FieldReport v1.1 RC1 — Audit exploitation
Date : 2026-06-02
Auditeur : Architecte DevOps senior

---

## 1. Installation

| Critère | État | Justification |
|---------|------|---------------|
| Procédure documentée | **PASS** | `INSTALLATION_DOCKER.md` détaille chaque étape : Docker Engine, Compose, clone, dossiers, lancement, vérification. |
| Commandes copiables | **PASS** | Toutes les commandes sont complètes et testables. |
| OS couverts | **PASS** | Ubuntu 24.04 et Debian 12 documentés. |
| Prérequis clairs | **PASS** | Docker Engine >= 24.0, Docker Compose >= 2.20. |
| Dépendances tierces | **PASS** | Aucune (pas de DB externe, pas de cache). |

**Temps estimé première installation** : 15-20 minutes sur un serveur neuf.

---

## 2. Sauvegardes

| Critère | État | Justification |
|---------|------|---------------|
| Script automatisé | **PASS** | `BACKUP_STRATEGY.md` fournit `backup.sh` complet. |
| Rotation intégrée | **PASS** | 7 jours / 4 semaines / 3 mois avec suppression auto. |
| Sauvegarde SQLite atomique | **PASS** | Utilise `.backup` de sqlite3 (pas `cp`). |
| Compression photos | **PASS** | tar.gz pour les dossiers. |
| Planification | **PASS** | Exemple cron fourni. |
| Hors site | **PARTIEL** | Documenté (rsync, S3) mais pas automatique dans le script de base. |

**Point de vigilance** : Le script de backup suppose que le conteneur est actif pour la sauvegarde SQLite. Si le conteneur est arrêté, la base est quand même accessible car c'est un fichier sur le volume hôte. Le `.backup` fonctionne hors ligne.

---

## 3. Restauration

| Critère | État | Justification |
|---------|------|---------------|
| Procédure documentée | **PASS** | `BACKUP_STRATEGY.md` détaille la restauration DB, photos, exports, complète. |
| Script de restauration | **PARTIEL** | Un exemple `restore.sh` est fourni mais pas de script paramétrable prêt à l'emploi. |
| Temps de restauration | **Non mesuré** | À tester sur un jeu de données réel. |
| Arrêt avant restauration | **Documenté** | Le conteneur doit être arrêté avant copie de la base. |

---

## 4. Mises à jour

| Critère | État | Justification |
|---------|------|---------------|
| Procédure documentée | **PASS** | `UPDATE_PROCEDURE.md` avec 6 étapes + rollback. |
| Sauvegarde pré-requise | **PASS** | Checklist explicite. |
| Rollback documenté | **PASS** | `git checkout` + restauration DB. |
| Zero-downtime | **NON** | `docker compose down` puis `up` = coupure de service. Pour un outil terrain asynchrone, acceptable. |
| Test post-mise à jour | **PASS** | Healthcheck + test API de création de rapport. |

---

## 5. Supervision

| Critère | État | Justification |
|---------|------|---------------|
| Healthcheck applicatif | **PASS** | Endpoint `/health` → `{"status":"ok"}`. |
| Healthcheck Docker | **PASS** | Configuré dans `docker-compose.yml` (interval 30s, 3 retries). |
| Métriques | **ABSENT** | Pas de Prometheus, pas de /metrics, pas de monitoring. |
| Alertes | **ABSENT** | Pas de PagerDuty, pas d'email, pas de webhook. |
| Logs centralisés | **ABSENT** | Logs sur stdout/stderr uniquement. Pas de ELK, Loki, ou syslog forward. |

**Recommandation** : Pour un déploiement pilote, la supervision minimale suffit. Pour la production pérenne, ajouter au minimum un check HTTP toutes les 5 minutes (UptimeRobot, Pingdom, ou cron interne).

---

## 6. Maintenance

| Critère | État | Justification |
|---------|------|---------------|
| Nettoyage PDF obsolètes | **PASS** | Documenté dans `OPERATIONS_MANUAL.md`. |
| Vérification espace disque | **PASS** | Commande `df` et `du` documentées. |
| Rotation logs Docker | **PARTIEL** | Par défaut Docker gère les logs (json-file driver). Pas de logrotate custom configuré. |
| Mises à jour système | **PASS** | `unattended-upgrades` documenté dans `SECURITY_HARDENING.md`. |

---

## 7. Conclusion exploitation

| Domaine | Note /10 | Justification |
|---------|----------|---------------|
| Installation | 8 | Procédure claire, commandes complètes |
| Sauvegardes | 8 | Script complet, rotation intégrée, manque hors-site auto |
| Restauration | 7 | Procédure claire, script exemple non paramétrable |
| Mises à jour | 7 | Procédure complète avec rollback, mais coupure de service |
| Supervision | 4 | Healthcheck OK mais pas de métriques ni d'alertes |
| Maintenance | 6 | Opérations documentées, pas de supervision proactive |

**Note moyenne exploitation : 6.7/10**

### Recommandations classées

**Critique**
- Mettre en place un check HTTP externe (UptimeRobot gratuit) pour alerter en cas de panne

**Important**
- Créer un script `restore.sh` paramétrable (date de backup en argument)
- Configurer logrotate pour les logs Docker si volume important

**Amélioration**
- Ajouter un dashboard de supervision minimal (ex: `docker stats` + cron)
- Automatiser la copie hors site (rsync vers NAS)
