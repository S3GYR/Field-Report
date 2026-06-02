# OPERATIONS_MANUAL

FieldReport v1.1 — Manuel d'exploitation
Date : 2026-06-02

---

## 1. Création d'un rapport

### Via l'interface web

1. Se connecter à `https://fieldreport.example.com`
2. Cliquer sur **"Rapports"** dans le menu
3. Cliquer sur **"+ Nouveau rapport"**
4. Remplir le formulaire :
   - **Numéro** : identifiant unique (ex: `FR-2026-001`)
   - **Date de visite** : date du jour ou de l'intervention
   - **Client** : nom de la collectivité ou du maître d'ouvrage
   - **Site** : localisation précise (ex: `Cimetière Est — Allée principale`)
   - **Météo** : conditions observées
   - **Statut** : `Brouillon` par défaut
   - **Commentaires** : observations générales
5. Cliquer **"Créer"**
6. Le rapport apparaît dans la liste

### Via l'API

```bash
curl -X POST https://fieldreport.example.com/api/reports/ \
  -H "Content-Type: application/json" \
  -d '{
    "number": "FR-2026-001",
    "visit_date": "2026-06-02",
    "client": "Mairie de Demo",
    "site": "Cimetière Est",
    "weather": "sunny",
    "status": "draft",
    "comments": "Inspection annuelle des dalles"
  }'
```

---

## 2. Gestion des photos

### Ajouter une photo

1. Ouvrir le rapport détaillé (cliquer sur le numéro)
2. Cliquer **"+ Ajouter une photo"**
3. Sur mobile : l'appareil photo natif s'ouvre
4. Sur PC : sélectionner un fichier image
5. Attendre l'acquisition GPS (2-5 secondes)
6. Compléter le **commentaire** et la **priorité** si nécessaire
7. Cliquer **"Uploader"**
8. La photo apparaît dans la grille avec son lien GPS

### Supprimer une photo

1. Sur le rapport détaillé, trouver la photo
2. Cliquer **"Supprimer"**
3. Confirmer dans la modal

### Consulter toutes les photos

1. Aller sur **"Photos"** dans le menu
2. Utiliser la barre de recherche pour filtrer
3. Utiliser le select **"Filtrer par rapport"** pour ne voir qu'un rapport

---

## 3. Gestion des tâches

### Ajouter une tâche

1. Sur le rapport détaillé, section **"Tâches"**
2. Cliquer **"+ Ajouter une tâche"**
3. Remplir :
   - **Description** : action corrective à réaliser
   - **Coût estimé** : en euros
   - **Durée estimée** : en heures
   - **Statut** : `À faire` par défaut
4. Cliquer **"Créer"**

### Modifier une tâche

1. Cliquer **"Modifier"** sur la tâche
2. Modifier les champs
3. Cliquer **"Enregistrer"**

### Suivre les tâches globales

1. Aller sur **"Tâches"** dans le menu
2. Toutes les tâches de tous les rapports sont listées
3. Utiliser la barre de recherche pour filtrer
4. Cliquer sur le numéro de rapport pour accéder au détail

---

## 4. Historique des interventions

1. Aller sur **"Historique"** dans le menu
2. Les rapports sont regroupés et triés par date
3. Utiliser le select **"Filtrer par site"** pour ne voir qu'un site
4. Cliquer sur un numéro de rapport pour accéder au détail

**Usage** : Préparer un rendez-vous client en revoyant les interventions passées sur le même site.

---

## 5. Génération de PDF

### Depuis le rapport

1. Ouvrir le rapport détaillé
2. Cliquer **"Générer le PDF"**
3. Un toast confirme la génération avec le chemin du fichier
4. Le PDF est accessible à l'URL : `https://fieldreport.example.com/exports/report-{numero}.pdf`

### Contenu du PDF

- Page titre avec numéro et client
- Informations du rapport (site, date, météo, statut)
- Commentaires
- Tableau des tâches avec coûts et durées
- Photos avec coordonnées GPS
- Bloc signature

### Téléchargement

```bash
# Récupérer un PDF depuis le serveur
curl -O https://fieldreport.example.com/exports/report-FR-2026-001.pdf
```

---

## 6. Sauvegarde

### Automatique

La sauvegarde est exécutée quotidiennement à 2h du matin via cron.

Vérifier le statut :
```bash
sudo tail /var/log/fieldreport-backup.log
```

### Manuelle

```bash
cd /opt/fieldreport
sudo ./scripts/backup.sh
```

### Récupérer une sauvegarde

Les sauvegardes sont stockées dans :
- `/opt/fieldreport/backups/daily/` (7 jours)
- `/opt/fieldreport/backups/weekly/` (4 semaines)
- `/opt/fieldreport/backups/monthly/` (3 mois)

---

## 7. Maintenance

### Nettoyer les PDF obsolètes

```bash
# Supprimer les PDF de plus de 30 jours
find /opt/fieldreport/data/exports -name "report-*.pdf" -mtime +30 -delete
```

### Vérifier l'espace disque

```bash
df -h /opt/fieldreport/data
sudo du -sh /opt/fieldreport/data/*
```

### Vérifier les logs

```bash
# Logs application
sudo docker logs fieldreport-backend --tail 100

# Logs Nginx
sudo tail -f /var/log/nginx/fieldreport-access.log
```

### Redémarrer l'application

```bash
cd /opt/fieldreport
sudo docker compose restart
```

### Mise à jour

Voir `UPDATE_PROCEDURE.md` pour la procédure complète.

---

## 8. Procédures d'urgence

### Application hors ligne

1. Vérifier `sudo docker ps` — le conteneur est-il actif ?
2. Vérifier `sudo systemctl status nginx` — le reverse proxy tourne-t-il ?
3. Vérifier `curl http://127.0.0.1:8200/health` — l'application répond-elle ?
4. Consulter les logs : `sudo docker logs fieldreport-backend --tail 50`
5. Redémarrer : `sudo docker compose restart`

### Perte de données

1. Ne pas paniquer — les sauvegardes sont dans `/opt/fieldreport/backups/`
2. Identifier la dernière sauvegarde valide : `ls -lt backups/daily/`
3. Restaurer selon `BACKUP_STRATEGY.md`
4. Vérifier avec `curl https://fieldreport.example.com/health`

---

## 9. Contacts et support

| Rôle | Contact | Usage |
|------|---------|-------|
| Administrateur système | — | Problème serveur, Docker, réseau |
| Développeur | — | Bug application, évolution |
| Utilisateur terrain | — | Question fonctionnelle |
