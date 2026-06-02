# USER_ACCEPTANCE_TEST

FieldReport v1.1 — Tests d'acceptance utilisateur
Date : 2026-06-02

---

## 1. Informations du testeur

| Champ | Valeur |
|-------|--------|
| Nom | |
| Fonction | |
| Device utilisé | |
| OS / Version | |
| Navigateur / Version | |
| Date du test | |
| Durée totale | |

---

## 2. Scénarios avec critères

### Scénario 1 — Création d'un rapport depuis le terrain

**Contexte** : Je suis sur le site d'un cimetière, je dois créer un rapport d'inspection.

| Étape | Action | Temps max | Critère de réussite | Critère d'échec |
|-------|--------|-----------|---------------------|-----------------|
| 1.1 | Ouvrir la page Rapports | 5s | Page chargée, barre recherche visible | Erreur 500, page blanche |
| 1.2 | Cliquer "Nouveau rapport" | 2s | Modal s'ouvre, champs vides | Pas de réaction, modal vide |
| 1.3 | Remplir le formulaire | 30s | Tous les champs accessibles, clavier ne cache pas les inputs | Inputs inaccessibles, zoom involontaire (iOS) |
| 1.4 | Soumettre | 3s | Rapport créé, apparaît dans la liste | Erreur réseau, données non sauvegardées |

**Temps de réalisation** : ___ min ___ s
**Résultat** : PASS / FAIL / PARTIEL
**Remarques utilisateur** :

---

### Scénario 2 — Prendre une photo de la fissure

**Contexte** : J'ai constaté une fissure, je dois la photographier.

| Étape | Action | Temps max | Critère de réussite | Critère d'échec |
|-------|--------|-----------|---------------------|-----------------|
| 2.1 | Ouvrir le rapport | 5s | Page détail chargée | Page blanche |
| 2.2 | Cliquer "+ Ajouter une photo" | 2s | Modal photo s'ouvre | Pas de réaction |
| 2.3 | Vérifier l'appareil photo | 3s | Caméra natif s'ouvre (mobile) ou sélecteur fichier (PC) | Galerie s'ouvre au lieu de la caméra |
| 2.4 | Prendre la photo | 5s | Photo visible dans l'input | Photo floue, format non supporté |
| 2.5 | Uploader | 10s | Photo apparaît dans la grille du rapport | Timeout, erreur serveur |

**Temps de réalisation** : ___ min ___ s
**Résultat** : PASS / FAIL / PARTIEL
**Remarques utilisateur** :

---

### Scénario 3 — Vérifier la géolocalisation de la photo

**Contexte** : Je veux prouver que la photo a été prise sur le site.

| Étape | Action | Temps max | Critère de réussite | Critère d'échec |
|-------|--------|-----------|---------------------|-----------------|
| 3.1 | Ouvrir modal photo | 2s | Modal ouverte | — |
| 3.2 | Attendre l'acquisition GPS | 5s | Coordonnées affichées avec précision en mètres | "GPS : échec" persistant |
| 3.3 | Uploader la photo | 10s | Photo avec lien GPS visible | Pas de lien GPS |
| 3.4 | Cliquer le lien GPS | 5s | Google Maps s'ouvre à la bonne position | Position erronée ou carte vide |

**Temps de réalisation** : ___ min ___ s
**Résultat** : PASS / FAIL / PARTIEL
**Remarques utilisateur** :

---

### Scénario 4 — Ajouter une tâche corrective

**Contexte :** Je dois noter une intervention à prévoir.

| Étape | Action | Temps max | Critère de réussite | Critère d'échec |
|-------|--------|-----------|---------------------|-----------------|
| 4.1 | Cliquer "+ Ajouter une tâche" | 2s | Modal tâche s'ouvre | Pas de réaction |
| 4.2 | Remplir description, coût, durée | 20s | Champs clairs, keyboard numérique pour coût/durée | Keyboard texte pour champs numériques |
| 4.3 | Créer | 3s | Tâche visible dans le tableau | Erreur, tâche non créée |
| 4.4 | Modifier la tâche | 15s | Modal pré-remplie, modification sans re-saisie totale | Champs vides, perte de données |

**Temps de réalisation** : ___ min ___ s
**Résultat** : PASS / FAIL / PARTIEL
**Remarques utilisateur** :

---

### Scénario 5 — Signer le rapport

**Contexte :** Le responsable signe la fin de l'inspection.

| Étape | Action | Temps max | Critère de réussite | Critère d'échec |
|-------|--------|-----------|---------------------|-----------------|
| 5.1 | Cliquer "Ajouter / Modifier signature" | 2s | Modal signature s'ouvre | Pas de réaction |
| 5.2 | Saisir nom, rôle, date | 20s | Champs accessibles, date picker natif | Date manuelle, format ambigu |
| 5.3 | Enregistrer | 3s | Signature affichée dans la carte | Erreur, signature non sauvegardée |

**Temps de réalisation** : ___ min ___ s
**Résultat** : PASS / FAIL / PARTIEL
**Remarques utilisateur** :

---

### Scénario 6 — Retrouver rapidement un ancien rapport

**Contexte :** Je cherche le rapport du cimetière Nord de l'année dernière.

| Étape | Action | Temps max | Critère de réussite | Critère d'échec |
|-------|--------|-----------|---------------------|-----------------|
| 6.1 | Aller sur /reports | 3s | Liste chargée | Page blanche |
| 6.2 | Taper "Nord" dans recherche | 2s | Filtrage instantané, rapports "Nord" visibles | Délai > 2s, aucun résultat |
| 6.3 | Effacer la recherche | 1s | Tous les rapports réapparaissent | Liste vide, rechargement nécessaire |

**Temps de réalisation** : ___ min ___ s
**Résultat** : PASS / FAIL / PARTIEL
**Remarques utilisateur** :

---

### Scénario 7 — Générer le PDF pour la mairie

**Contexte :** Le client demande le compte-rendu en PDF.

| Étape | Action | Temps max | Critère de réussite | Critère d'échec |
|-------|--------|-----------|---------------------|-----------------|
| 7.1 | Cliquer "Générer le PDF" | 2s | Toast de confirmation | Erreur serveur |
| 7.2 | Sur PC : télécharger et ouvrir le PDF | 10s | PDF lisible, photos visibles, GPS inclus | PDF vide, photos manquantes, texte coupé |

**Temps de réalisation** : ___ min ___ s
**Résultat** : PASS / FAIL / PARTIEL
**Remarques utilisateur** :

---

### Scénario 8 — Consulter l'historique du site

**Contexte :** Je veux voir toutes les interventions sur le cimetière Est.

| Étape | Action | Temps max | Critère de réussite | Critère d'échec |
|-------|--------|-----------|---------------------|-----------------|
| 8.1 | Aller sur /history | 5s | Page historique chargée | Page blanche |
| 8.2 | Sélectionner le site "Cimetière Est" | 2s | Liste filtrée, tri chronologique | Pas de sites dans le select, ordre erroné |
| 8.3 | Cliquer sur un rapport | 3s | Redirection vers le détail | Lien mort, erreur 404 |

**Temps de réalisation** : ___ min ___ s
**Résultat** : PASS / FAIL / PARTIEL
**Remarques utilisateur** :

---

### Scénario 9 — Supprimer une photo par erreur (annulation)

**Contexte :** Je veux vérifier que la suppression est sécurisée.

| Étape | Action | Temps max | Critère de réussite | Critère d'échec |
|-------|--------|-----------|---------------------|-----------------|
| 9.1 | Cliquer "Supprimer" sur une photo | 2s | Modal confirmation s'ouvre avec message clair | Suppression immédiate sans confirmation |
| 9.2 | Cliquer "Annuler" | 1s | Modal fermée, photo intacte | Photo supprimée malgré tout |
| 9.3 | Re-cliquer "Supprimer" puis confirmer | 2s | Photo supprimée, toast "Supprimé" | Erreur, photo toujours présente |

**Temps de réalisation** : ___ min ___ s
**Résultat** : PASS / FAIL / PARTIEL
**Remarques utilisateur** :

---

### Scénario 10 — Retrouver ses données après fermeture du navigateur

**Contexte :** Je ferme le navigateur et rouvre plus tard.

| Étape | Action | Temps max | Critère de réussite | Critère d'échec |
|-------|--------|-----------|---------------------|-----------------|
| 10.1 | Créer un rapport avec photo et tâche | 3 min | Rapport créé | — |
| 10.2 | Fermer le navigateur | 2s | Navigateur fermé | — |
| 10.3 | Rouvrir le navigateur, retourner sur FieldReport | 10s | Toutes les données présentes | Rapport perdu, base réinitialisée |
| 10.4 | Rafraîchir la page (F5) | 5s | Données toujours là | Erreur 404, données manquantes |

**Temps de réalisation** : ___ min ___ s
**Résultat** : PASS / FAIL / PARTIEL
**Remarques utilisateur** :

---

## 3. Synthèse globale

### Score par scénario

| Scénario | Résultat | Temps réalisé | Remarques |
|----------|----------|---------------|-----------|
| S1 — Création rapport | | | |
| S2 — Capture photo | | | |
| S3 — GPS | | | |
| S4 — Ajout tâche | | | |
| S5 — Signature | | | |
| S6 — Recherche | | | |
| S7 — PDF | | | |
| S8 — Historique | | | |
| S9 — Suppression | | | |
| S10 — Persistance | | | |

### Calcul du score

- PASS = 1 point
- PARTIEL = 0.5 point
- FAIL = 0 point

**Total** : ___ / 10

### Appréciation globale

| Critère | Note /10 |
|---------|----------|
| Facilité d'utilisation | |
| Rapidité | |
| Fiabilité (pas de perte de données) | |
| Adaptation mobile | |
| Clarté des informations | |

**Note moyenne** : ___ / 10

### Remarques libres

Qu'est-ce qui vous a le plus surpris (positif ou négatif) ?

Y a-t-il une fonctionnalité manquante indispensable ?

Recommanderiez-vous FieldReport à un collègue ?

---

## 4. Décision

| Option | Coche |
|--------|-------|
| **GO** — V1.1 validée pour mise en production | |
| **CONDITIONNEL** — Corriger les points bloquants avant release | |
| **NO-GO** — Refonte nécessaire avant toute release | |

**Points bloquants identifiés** :

**Recommandation du testeur** :
