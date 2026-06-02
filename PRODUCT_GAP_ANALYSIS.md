# PRODUCT_GAP_ANALYSIS

FieldReport — Analyse des écarts produit / UX
Date : 2026-06-02

---

## 1. Vue d'ensemble de l'expérience actuelle

L'application FieldReport est une interface serveur-rendue (Jinja2) enrichie par du JavaScript vanilla. Elle permet :

- Dashboard avec compteurs temps réel
- CRUD rapports, photos, tâches, signatures
- Génération PDF côté serveur
- Upload de photos par rapport

---

## 2. Expérience utilisateur — Gaps identifiés

### 2.1 Parcours terrain (P0)

| Gap | Description | Impact utilisateur |
|-----|-------------|-------------------|
| Pas de mode hors-ligne | L'inspecteur sur chantier sans réseau ne peut rien saisir | Bloquant en terrain difficile |
| Pas d'application mobile dédiée | Interface web responsive mais pas optimisée tactile | Saisie fastidieuse sur smartphone |
| Pas de géolocalisation automatique | Coordonnées GPS non capturées automatiquement lors de la photo | Perte d'information terrain |
| Pas d'horodatage photo | Pas de metadata EXIF exploitée | Impossible de prouver quand la photo a été prise |

### 2.2 Saisie mobile (P0)

| Gap | Description | Impact |
|-----|-------------|--------|
| Édition via `prompt()` | Tâches et signatures utilisent `window.prompt()` pour l'édition | Expérience désastreuse sur mobile. Pas de validation. Pas de retour à la ligne. |
| Pas de prise de photo directe | L'upload passe par le sélecteur de fichiers du navigateur | Impossible de prendre une photo directement depuis l'appareil photo |
| Formulaires non validés côté client | Pas de feedback immédiat sur les champs obligatoires | Erreurs 400 du serveur après soumission |
| Pas d'autosave | Si le navigateur se recharge, la saisie en cours est perdue | Perte de données fréquente sur mobile |

### 2.3 Consultation rapport (P1)

| Gap | Description | Impact |
|-----|-------------|--------|
| Pas de recherche | Aucune barre de recherche dans la liste des rapports | Navigation difficile au-delà de 50 rapports |
| Pas de filtres | Pas de filtre par client, site, statut, date | Impossible d'isoler un sous-ensemble |
| Pas de pagination | Tous les rapports chargés en mémoire | Latence croissante avec le volume |
| Pas de tri personnalisé | Tri fixe par date de création | Difficile de retrouver un rapport ancien |
| Pas de vue calendrier | Pas de représentation temporelle des visites | Impossible de visualiser la charge hebdomadaire |

### 2.4 Gestion photos (P1)

| Gap | Description | Impact |
|-----|-------------|--------|
| Pas de visionneuse lightbox | Les photos s'ouvrent dans un nouvel onglet ou par URL brute | Mauvaise expérience de consultation |
| Pas de rotation / recadrage | Pas d'édition d'image côté client | Photos prises en portrait mal orientées |
| Pas de tags / catégories | Les photos ne sont classées que par rapport | Impossible de retrouver "toutes les photos de fissures" |
| Pas de comparaison avant/après | Pas de vue côte-à-côte | Moins efficace pour les rapports de suivi |

### 2.5 Génération PDF (P1)

| Gap | Description | Impact |
|-----|-------------|--------|
| Pas de template personnalisable | Un seul layout PDF | Incapacité d'adapter au branding client |
| Pas de génération par lot | Un PDF par rapport, un par un | Très lent pour les rapports mensuels |
| Pas de signature électronique avancée | Signature dessinée uniquement | Pas de certificat, pas de traçabilité juridique |
| Pas d'export Word/Excel | Seul format PDF disponible | Client demande souvent un format éditable |

---

## 3. Irritants utilisateur (gains rapides)

| # | Irritant | Correction rapide | Priorité |
|---|----------|-------------------|----------|
| 1 | `prompt()` pour l'édition | Remplacer par des modals HTML avec formulaires complets | P0 |
| 2 | Pas de feedback après action | Toast déjà implémenté mais pas sur toutes les pages | P0 |
| 3 | Pas de confirmation suppression | `confirm()` ou modal de confirmation avant delete | P0 |
| 4 | Tableaux non responsive | `overflow-x: auto` sur mobile pour les tables | P0 |
| 5 | Pas d'indicateur de chargement | Spinner sur les appels API lents (upload photo, génération PDF) | P0 |
| 6 | Pas de message d'erreur explicite | Erreurs réseau affichées en `alert()` ou silencieuses | P0 |
| 7 | Pas de focus automatique | Le premier champ des modals n'est pas autofocus | P1 |
| 8 | Pas de raccourcis clavier | `Escape` pour fermer modal, `Ctrl+S` pour sauvegarder | P1 |

---

## 4. Fonctionnalités manquantes

### P0 — Bloquant pour un usage terrain réel

- **Mode hors-ligne / PWA** : Service Worker + IndexedDB pour saisie sans réseau
- **Prise de photo native** : `<input type="file" accept="image/*" capture="environment">`
- **Géolocalisation auto** : `navigator.geolocation.getCurrentPosition()` + stockage GPS
- **Formulaires d'édition HTML** : Remplacer tous les `prompt()` par des modals

### P1 — Forte valeur métier

- **Recherche full-text** : Barre de recherche sur rapports (numéro, client, site, description)
- **Filtres avancés** : Par date range, client, statut, météo
- **Pagination API + UI** : `skip`/`limit` pour supporter des milliers de rapports
- **Visionneuse photo** : Lightbox côté client avec navigation clavier
- **Export CSV** : Export rapide des rapports pour Excel
- **Duplication rapport** : Cloner un rapport pour un site similaire
- **Modèles de rapport** : Templates pré-remplis (type d'inspection)

### P2 — Évolutions à valeur ajoutée

- **Carte Leaflet** : Affichage des rapports et photos sur une carte
- **Comparaison photo** : Vue avant/après côte-à-côte
- **Notifications email** : Rappel de rapport en retard
- **Partage lien public** : Lien temporaire pour un client sans compte
- **Dashboard analytics** : Graphiques de productivité (rapports/semaine, taux d'approbation)
- **Multi-utilisateur** : Rôles (admin, inspecteur, client)

---

## 5. Synthèse par domaine

| Domaine | Score UX actuel (1-10) | Écarts critiques | Écarts moyens | Gains rapides |
|---------|----------------------|------------------|---------------|---------------|
| Saisie terrain | 3/10 | 4 | 3 | 3 |
| Consultation rapport | 5/10 | 0 | 4 | 2 |
| Gestion photos | 5/10 | 0 | 4 | 2 |
| Génération PDF | 6/10 | 0 | 4 | 1 |
| Navigation globale | 6/10 | 0 | 2 | 2 |

---

## 6. Recommandations immédiates (v1.0.1)

1. **Remplacer tous les `prompt()`** par des modals HTML — impact maximal, effort faible
2. **Ajouter `capture="environment"`** sur l'input photo — une ligne de HTML
3. **Ajouter une barre de recherche** sur la page rapports — ~2h de dev
4. **Ajouter des spinners de chargement** sur les actions lentes — ~1h
5. **Ajouter des confirmations de suppression** — ~30 min

---

## 7. Feuille de route UX suggérée

| Version | Focus | Livrables |
|---------|-------|-----------|
| v1.0.1 | Irritants | Modals d'édition, capture photo native, spinners, confirmations |
| v1.1.0 | Productivité | Recherche, filtres, pagination, duplication rapport, export CSV |
| v1.2.0 | Terrain | PWA offline, géolocalisation, visionneuse photo, carte |
| v2.0.0 | Métier | Multi-utilisateur, rôles, analytics, partage client, API externe |
