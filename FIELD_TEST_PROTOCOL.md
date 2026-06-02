# FIELD_TEST_PROTOCOL

FieldReport v1.1 — Protocole de test terrain
Date : 2026-06-02

---

## 1. Informations générales

| Champ | Valeur |
|-------|--------|
| Version testée | v1.1.0 |
| Environnement | Terrain réel (extérieur, couverture réseau variable) |
| Durée estimée | 45 min par device |
| Nombre de scénarios | 10 |
| Nombre de devices | 5 |

---

## 2. Matériel requis

| Device | OS minimum | Navigateur | Quantité |
|--------|-----------|------------|----------|
| Smartphone Android | Android 12+ | Chrome 120+ | 1 |
| Smartphone iPhone | iOS 16+ | Safari 16+ | 1 |
| Tablette Android | Android 12+ | Chrome 120+ | 1 |
| Tablette iPad | iPadOS 16+ | Safari 16+ | 1 |
| PC Windows | Windows 11 | Chrome 120+ | 1 |

### Prérequis terrain

- [ ] Serveur FieldReport accessible (WiFi ou 4G)
- [ ] GPS activé sur les devices mobiles
- [ ] Permission caméra accordée dans le navigateur
- [ ] Permission géolocalisation accordée dans le navigateur
- [ ] Au moins 2 rapports préexistants en base (pour test historique)

---

## 3. Scénarios de test

### Scénario 1 — Création de rapport

**Objectif** : Créer un rapport d'intervention complet depuis le terrain.

| Étape | Action | Résultat attendu |
|-------|--------|------------------|
| 1.1 | Naviguer vers `/reports` | Page rapports chargée, barre de recherche visible |
| 1.2 | Cliquer "+ Nouveau rapport" | Modal création s'ouvre |
| 1.3 | Remplir : Numéro `TEST-001`, Date `2026-06-02`, Client `Mairie Test`, Site `Cimetière Est`, Météo `Ensoleillé`, Statut `Brouillon`, Commentaires `Inspection annuelle` | Champs remplis |
| 1.4 | Cliquer "Créer" | Modal fermée, rapport apparaît dans la liste |
| 1.5 | Vérifier le rapport dans la liste | `TEST-001` visible avec badge `draft` |

**Device** : Tous
**Temps max** : 2 min

---

### Scénario 2 — Capture photo native

**Objectif** : Prendre une photo directement avec l'appareil photo du device.

| Étape | Action | Résultat attendu |
|-------|--------|------------------|
| 2.1 | Ouvrir le rapport créé en S1 | Page détail chargée |
| 2.2 | Cliquer "+ Ajouter une photo" | Modal photo s'ouvre |
| 2.3 | Sur mobile/tablette : vérifier que l'appareil photo s'ouvre (pas la galerie) | Caméra natif visible |
| 2.4 | Sur PC : vérifier que le sélecteur de fichier s'ouvre | Sélecteur fichier standard |
| 2.5 | Prendre / sélectionner une photo | Photo affichée dans l'input |
| 2.6 | Cliquer "Uploader" | Modal fermée, photo apparaît dans la grille |
| 2.7 | Sur mobile : vérifier possibilité de basculer galerie si besoin | Basculer possible (iOS) ou capture directe (Android) |

**Device** : Mobiles + tablettes (prioritaire), PC (fallback)
**Temps max** : 3 min

---

### Scénario 3 — Géolocalisation GPS

**Objectif** : Acquérir automatiquement les coordonnées GPS d'une photo.

| Étape | Action | Résultat attendu |
|-------|--------|------------------|
| 3.1 | Ouvrir modal photo (S2.2) | Modal ouverte |
| 3.2 | Attendre 2-3 secondes | Texte "GPS : lat, lng (±Xm)" affiché |
| 3.3 | Si GPS refusé : vérifier message | "GPS : échec de l'acquisition" visible, upload possible |
| 3.4 | Uploader la photo | Photo affichée avec lien GPS sous l'image |
| 3.5 | Cliquer le lien GPS | Google Maps s'ouvre à la position exacte |
| 3.6 | Sur PC : vérifier que l'upload sans GPS fonctionne | Photo uploadée, pas de lien GPS (normal) |

**Device** : Mobiles + tablettes (GPS requis), PC (optionnel)
**Temps max** : 3 min
**Conditions** : Extérieur, ciel dégagé ou partiellement couvert

---

### Scénario 4 — Ajout de tâche

**Objectif** : Ajouter et modifier une tâche via la modal (pas de prompt).

| Étape | Action | Résultat attendu |
|-------|--------|------------------|
| 4.1 | Sur page rapport détail, cliquer "+ Ajouter une tâche" | Modal tâche s'ouvre, titre "Nouvelle tâche" |
| 4.2 | Remplir : Description `Remplacer dalles allée`, Coût `450`, Durée `2.5`, Statut `À faire` | Champs remplis |
| 4.3 | Cliquer "Créer" | Modal fermée, tâche apparaît dans le tableau |
| 4.4 | Cliquer "Modifier" sur la tâche | Modal réouvre, titre "Modifier la tâche", champs pré-remplis |
| 4.5 | Changer statut en "En cours", cliquer "Enregistrer" | Tâche mise à jour, badge `in_progress` visible |
| 4.6 | Sur `/tasks`, vérifier que la tâche apparaît | Tâche visible avec lien vers le rapport |

**Device** : Tous
**Temps max** : 3 min

---

### Scénario 5 — Ajout de signature

**Objectif** : Ajouter une signature au rapport.

| Étape | Action | Résultat attendu |
|-------|--------|------------------|
| 5.1 | Sur page rapport détail, cliquer "Ajouter / Modifier" signature | Modal signature s'ouvre |
| 5.2 | Remplir : Nom `Jean Dupont`, Rôle `Responsable technique`, Date `2026-06-02` | Champs remplis |
| 5.3 | Cliquer "Enregistrer" | Modal fermée, signature affichée dans la carte |
| 5.4 | Sur `/signatures`, vérifier la signature | Signature visible avec nom, rôle, date, lien rapport |

**Device** : Tous
**Temps max** : 2 min

---

### Scénario 6 — Recherche

**Objectif** : Retrouver rapidement un élément via la recherche.

| Étape | Action | Résultat attendu |
|-------|--------|------------------|
| 6.1 | Sur `/reports`, taper `TEST` dans la barre de recherche | Uniquement le rapport `TEST-001` visible |
| 6.2 | Effacer la recherche | Tous les rapports réapparaissent |
| 6.3 | Sur `/tasks`, taper `dalles` | Tâche `Remplacer dalles allée` visible |
| 6.4 | Sur `/photos`, taper `TEST` ou nom de fichier | Photo du rapport TEST-001 visible |
| 6.5 | Sur `/signatures`, taper `Dupont` | Signature Jean Dupont visible |

**Device** : Tous
**Temps max** : 2 min

---

### Scénario 7 — Génération PDF

**Objectif** : Générer un PDF complet avec photos et GPS.

| Étape | Action | Résultat attendu |
|-------|--------|------------------|
| 7.1 | Sur page rapport détail, cliquer "Générer le PDF" | Toast "PDF généré" apparaît |
| 7.2 | Sur PC : télécharger et ouvrir le PDF | PDF contient : info rapport, tâches, photos (images réelles), coordonnées GPS, signature |
| 7.3 | Sur mobile : vérifier que le toast indique le chemin du fichier | Chemin `/exports/...` affiché |

**Device** : Tous (PC pour vérification visuelle prioritaire)
**Temps max** : 2 min

---

### Scénario 8 — Consultation historique

**Objectif** : Consulter l'historique des interventions par site.

| Étape | Action | Résultat attendu |
|-------|--------|------------------|
| 8.1 | Naviguer vers `/history` | Page historique chargée, select "Filtrer par site" visible |
| 8.2 | Sélectionner le site `Cimetière Est` | Liste filtrée, rapport `TEST-001` visible |
| 8.3 | Vérifier les infos affichées | Numéro, date, client, statut, nombre photos/tâches visibles |
| 8.4 | Cliquer sur le numéro du rapport | Redirection vers `/reports/{id}` |

**Device** : Tous
**Temps max** : 2 min

---

### Scénario 9 — Suppression avec confirmation

**Objectif** : Supprimer des éléments avec confirmation modal.

| Étape | Action | Résultat attendu |
|-------|--------|------------------|
| 9.1 | Sur page rapport détail, cliquer "Supprimer" sur la photo | Modal confirmation s'ouvre, message "Supprimer cette photo ?" |
| 9.2 | Cliquer "Annuler" | Modal fermée, photo toujours présente |
| 9.3 | Cliquer à nouveau "Supprimer" puis "Supprimer" | Photo supprimée, toast "Supprimé" |
| 9.4 | Répéter pour la tâche | Même comportement |
| 9.5 | Sur `/reports`, cliquer "Supprimer" sur `TEST-001` | Modal confirmation "Supprimer le rapport TEST-001 ?" |
| 9.6 | Confirmer | Rapport supprimé, redirection ou liste mise à jour |

**Device** : Tous
**Temps max** : 3 min

---

### Scénario 10 — Sauvegarde / restauration

**Objectif** : Vérifier la persistance des données.

| Étape | Action | Résultat attendu |
|-------|--------|------------------|
| 10.1 | Créer un second rapport `TEST-002` avec photo, tâche, signature | Rapport créé |
| 10.2 | Rafraîchir la page (F5 / pull-to-refresh) | Données toujours présentes |
| 10.3 | Fermer le navigateur, rouvrir, retourner sur `/reports` | Rapports `TEST-001` et `TEST-002` visibles |
| 10.4 | Sur serveur : vérifier que le fichier SQLite existe | `storage/reports.db` présent |
| 10.5 | Sur serveur : vérifier les photos dans `storage/photos/` | Fichiers images présents |

**Device** : Tous
**Temps max** : 3 min

---

## 4. Grille de test par device

### Smartphone Android

| Scénario | Résultat | Heure | Remarques |
|----------|----------|-------|-----------|
| S1 — Création rapport | | | |
| S2 — Capture photo native | | | |
| S3 — GPS | | | |
| S4 — Tâche | | | |
| S5 — Signature | | | |
| S6 — Recherche | | | |
| S7 — PDF | | | |
| S8 — Historique | | | |
| S9 — Suppression | | | |
| S10 — Sauvegarde | | | |

### Smartphone iPhone

| Scénario | Résultat | Heure | Remarques |
|----------|----------|-------|-----------|
| S1 — Création rapport | | | |
| S2 — Capture photo native | | | |
| S3 — GPS | | | |
| S4 — Tâche | | | |
| S5 — Signature | | | |
| S6 — Recherche | | | |
| S7 — PDF | | | |
| S8 — Historique | | | |
| S9 — Suppression | | | |
| S10 — Sauvegarde | | | |

### Tablette Android

| Scénario | Résultat | Heure | Remarques |
|----------|----------|-------|-----------|
| S1 — Création rapport | | | |
| S2 — Capture photo native | | | |
| S3 — GPS | | | |
| S4 — Tâche | | | |
| S5 — Signature | | | |
| S6 — Recherche | | | |
| S7 — PDF | | | |
| S8 — Historique | | | |
| S9 — Suppression | | | |
| S10 — Sauvegarde | | | |

### Tablette iPad

| Scénario | Résultat | Heure | Remarques |
|----------|----------|-------|-----------|
| S1 — Création rapport | | | |
| S2 — Capture photo native | | | |
| S3 — GPS | | | |
| S4 — Tâche | | | |
| S5 — Signature | | | |
| S6 — Recherche | | | |
| S7 — PDF | | | |
| S8 — Historique | | | |
| S9 — Suppression | | | |
| S10 — Sauvegarde | | | |

### PC Windows

| Scénario | Résultat | Heure | Remarques |
|----------|----------|-------|-----------|
| S1 — Création rapport | | | |
| S2 — Upload fichier (pas capture) | | | |
| S4 — Tâche | | | |
| S5 — Signature | | | |
| S6 — Recherche | | | |
| S7 — PDF (vérification visuelle) | | | |
| S8 — Historique | | | |
| S9 — Suppression | | | |
| S10 — Sauvegarde | | | |

---

## 5. Critères de réussite globaux

- [ ] >= 80% des scénarios PASS sur chaque device
- [ ] Scénarios S2 (capture photo) et S3 (GPS) PASS sur au moins Android + iPhone
- [ ] Aucun crash navigateur
- [ ] Aucune perte de données
- [ ] Temps total < 45 min par device
