# ANALYSE_METIER

FieldReport — Analyse métier et cas d'usage
Date : 2026-06-02

---

## 1. Cibles métiers identifiées

| Persona | Activité | Besoin principal | Fréquence |
|---------|----------|-----------------|-----------|
| Conducteur de travaux | Suivi de chantier | Rapport quotidien, photos, réserves | Quotidien |
| Chargé d'affaires | Relevé client | Rapport structuré, signature, PDF | Par visite |
| Technicien de maintenance | Anomalies et actions correctives | Suivi interventions, historique | Quotidien |
| Agent communal | Espaces verts, cimetières, voirie | Relevé terrain simple, suivi annuel | Hebdomadaire |
| Inspecteur qualité | Contrôle et non-conformités | Photos preuves, tâches correctives | Par mission |
| Bureau d'études | Relevé technique | Observations détaillées, planification | Par projet |

---

## 2. Cas d'usage par persona

### 2.1 Agent communal — Entretien cimetière

**Scénario** : M. Dupont, agent communal, fait sa tournée hebdomadaire du cimetière. Il constate que le talus nord n'a pas été débroussaillé.

**Parcours actuel FieldReport** :

1. Ouvre FieldReport sur son smartphone
2. Crée un rapport "CIM-2026-001" — Client : Commune d'Imbleville — Site : Cimetière municipal
3. Prend une photo du talus non traité
4. Ajoute une tâche : "Débroussailler talus nord — Estimé : 2h"
5. Génère le PDF pour le responsable

**Gaps identifiés** :

| # | Gap | Impact |
|---|-----|--------|
| 1 | Pas d'historique par zone | Impossible de voir que le 15/05 la tonte a été faite, le 28/05 le débroussaillage était partiel |
| 2 | Pas de géolocalisation | Impossible de situer précisément le talus sur une carte |
| 3 | Photo via galerie | Doit quitter l'app, prendre la photo, revenir — fastidieux |
| 4 | Pas de modèle pré-rempli | Doit saisir client/site à chaque fois |

### 2.2 Chargé d'affaires — Relevé chantier

**Scénario** : Mme Martin, chargée d'affaires chez SEGYR Technologies, visite un chantier de construction. Elle doit constater des réserves et faire signer le client.

**Parcours actuel** :

1. Crée un rapport "SEGYR-2026-045"
2. Prend 12 photos des réserves (fissures, non-conformités)
3. Rédige les observations dans "Commentaires"
4. Ajoute 5 tâches correctives avec coûts estimés
5. Le client signe sur la tablette
6. Génère le PDF et l'envoie

**Gaps identifiés** :

| # | Gap | Impact |
|---|-----|--------|
| 1 | `prompt()` pour l'édition tâche | Impossible de modifier une tâche correctement sur mobile |
| 2 | Pas de recherche dans l'historique | Retrouver le rapport du chantier de janvier est difficile |
| 3 | Pas de lien Google Maps | Le client ne sait pas exactement où se situe la réserve |
| 4 | Pas de confirmation suppression | Risque de supprimer un rapport signé par erreur |

### 2.3 Technicien de maintenance — Anomalies

**Scénario** : Un technicien dépanne une chaudière. Il doit documenter l'anomalie et les actions réalisées.

**Parcours actuel** :

1. Crée un rapport "MAINT-2026-112"
2. Prend une photo de l'anomalie
3. Ajoute une tâche : "Remplacer sonde température"
4. Modifie le statut en "done"
5. Génère le PDF pour l'archive

**Gaps identifiés** :

| # | Gap | Impact |
|---|-----|--------|
| 1 | Pas d'historique des interventions sur un même équipement | Impossible de voir que la même panne est revenue 3 fois |
| 2 | Pas de recherche par équipement/site | Retrouver les interventions sur "Chaudière A" est manuel |
| 3 | Tableau non responsive sur mobile | Difficile à lire les tâches sur smartphone |

### 2.4 Inspecteur qualité — Contrôle

**Scénario** : Un inspecteur contrôle la conformité d'un ouvrage. Il doit établir un PV avec photos, mesures et signature.

**Parcours actuel** :

1. Crée un rapport "QC-2026-003"
2. Prend des photos de non-conformités
3. Saisit les observations
4. Ajoute des tâches de correction
5. Fait signer le responsable chantier
6. Génère le PDF

**Gaps identifiés** :

| # | Gap | Impact |
|---|-----|--------|
| 1 | Pas de catégorisation des photos | Impossible de taguer "fissure", "humidité", "non-conformité" |
| 2 | Pas de priorité visible dans le PDF | Les tâches urgentes ne ressortent pas |
| 3 | Pas de coordonnées GPS dans le PDF | Pas de preuve de localisation juridiquement utilisable |

---

## 3. Fonctionnalités couvertes par FieldReport v1.0.1

| Fonctionnalité | Couverture | Qualité |
|----------------|-----------|---------|
| Création rapport | Complète | Bonne (modal HTML) |
| Modification rapport | Complète | Bonne (modal HTML) |
| Suppression rapport | Complète | Moyenne (pas de confirmation modal) |
| Upload photo | Complète | Moyenne (pas de capture native) |
| Visualisation photo | Complète | Moyenne (pas de lightbox) |
| Suppression photo | Complète | Moyenne (pas de confirmation modal) |
| Gestion tâches | Complète | Mauvaise (`prompt()` édition) |
| Gestion signatures | Complète | Mauvaise (`prompt()` édition) |
| Génération PDF | Complète | Moyenne (photos non intégrées, pas de GPS) |
| Dashboard | Complète | Bonne |

---

## 4. Fonctionnalités manquantes critiques (P0)

### 4.1 Historique des interventions par zone

**Besoin** : Pour un site donné (ex: "Cimetière municipal"), voir chronologiquement toutes les interventions passées.

**Actuellement** : Les rapports sont indépendants. Aucun lien chronologique entre eux.

**Solution proposée** : Ajouter une page "Historique" qui liste tous les rapports pour un site donné, triés par date, avec un résumé des tâches et photos.

**Implémentation** :
- Nouveau endpoint API : `GET /api/reports?site={site}` (filtre existant, juste exposer le paramètre)
- Nouvelle page UI : `/history?site={site}`
- Affichage chronologique : date, statut, nombre de photos, nombre de tâches, commentaires

### 4.2 Géolocalisation automatique

**Besoin** : Attacher automatiquement les coordonnées GPS à chaque photo et rapport.

**Actuellement** : Champs `gps_lat`/`gps_lng` existent dans la base mais ne sont jamais remplis.

**Solution proposée** :
- Côté client : `navigator.geolocation.getCurrentPosition()` avant l'upload
- Transmettre lat/lng/accuracy dans le FormData
- Stocker côté serveur
- Afficher un lien Google Maps dans le détail photo
- Exporter dans le PDF

### 4.3 Capture photo native

**Besoin** : Prendre une photo directement depuis l'appareil photo du smartphone sans passer par la galerie.

**Solution proposée** : `capture="environment"` sur l'input file.

### 4.4 Modales d'édition responsive

**Besoin** : Éditer tâches et signatures via des formulaires HTML complets sur mobile.

**Actuellement** : `window.prompt()` est utilisé, ce qui est inutilisable sur mobile.

**Solution proposée** : Remplacer par des modals HTML identiques à celles des rapports.

---

## 5. Fonctionnalités manquantes importantes (P1)

### 5.1 Recherche rapports

**Besoin** : Trouver rapidement un rapport par numéro, client, site ou contenu d'observation.

**Solution** : Barre de recherche côté client filtrant la liste chargée.

### 5.2 Confirmation de suppression

**Besoin** : Éviter les suppressions accidentelles de rapports, photos, tâches, signatures.

**Actuellement** : `confirmDelete` utilise `window.confirm()` natif du navigateur.

**Solution** : Modal de confirmation HTML cohérente avec le design.

### 5.3 Photos intégrées au PDF

**Besoin** : Le PDF final doit contenir les images des photos, pas seulement leur nom.

**Actuellement** : `pdf_service.py` affiche `Paragraph(photo.filename)`.

**Solution** : Utiliser `reportlab.platypus.Image` pour intégrer les photos.

### 5.4 Catégories / Tags

**Besoin** : Classer les photos par type (fissure, humidité, avant/après, etc.).

**Solution** : Ajouter un champ `category` au modèle Photo.

---

## 6. Fonctionnalités futures (P2)

| Fonctionnalité | Description |
|----------------|-------------|
| PWA offline | Service Worker + IndexedDB pour saisie sans réseau |
| Carte interactive | Leaflet avec markers pour chaque rapport/photo |
| Notifications | Rappel de rapports en retard |
| Multi-utilisateur | Rôles (admin, inspecteur, client) |
| Partage lien public | Lien temporaire pour un client |
| Duplication rapport | Cloner un rapport pour un site similaire |
| Modèles de rapport | Templates pré-remplis par type d'inspection |

---

## 7. Synthèse des manques par persona

| Persona | P0 (bloquant) | P1 (important) | P2 (valorisation) |
|---------|-------------|--------------|-----------------|
| Agent communal | Historique zone, GPS, photo native | Recherche, catégories | Carte, modèles |
| Chargé d'affaires | Modales édition, GPS, confirmation suppression | Recherche, photos dans PDF | Partage client, duplication |
| Technicien maintenance | Historique équipement, modales édition | Recherche, photos dans PDF | Notifications, analytics |
| Inspecteur qualité | GPS dans PDF, modales édition | Photos dans PDF, catégories | Multi-signataires, checklist |

---

## 8. Recommandations prioritaires

1. **P0 — Capture photo native** : 1 ligne de HTML, impact maximal sur terrain
2. **P0 — Géolocalisation** : Champs DB prêts, 2h de dev côté API + client
3. **P0 — Modales d'édition** : Remplacer les `prompt()` sur tasks.html, signatures.html, report_detail.html
4. **P0 — Historique par zone** : Nouvelle page UI filtrant par site, tri chronologique
5. **P1 — Recherche client** : Filtrage JS sur les listes existantes
6. **P1 — Confirmation modal** : Remplacer `confirm()` par une modal HTML
