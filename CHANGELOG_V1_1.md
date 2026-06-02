# CHANGELOG_V1_1

FieldReport — Version 1.1
Date : 2026-06-02

---

## Résumé

FieldReport v1.1 transforme l'application en véritable outil terrain mobile. Cette version apporte la capture photo native, la géolocalisation automatique, les modales d'édition responsive, l'historique des interventions par zone, la recherche rapide et les confirmations de suppression.

---

## P0 — Fonctionnalités critiques

### Capture photo native mobile

- **Fichier** : `backend/app/templates/report_detail.html`
- **Changement** : `capture="environment"` ajouté sur l'input file d'upload photo
- **Impact** : Sur smartphone, l'appareil photo natif s'ouvre directement sans passer par la galerie
- **Fallback** : La galerie reste accessible en retirant l'attribut capture

### Géolocalisation automatique

- **Fichiers** :
  - `backend/app/models/report.py` — ajout `gps_accuracy` (Float, nullable)
  - `backend/app/schemas/report.py` — ajout `gps_accuracy` dans PhotoBase, CreatePhoto, UpdatePhoto, PhotoResponse + `report_id` dans PhotoResponse
  - `backend/app/api/photos.py` — endpoint `upload_photo` accepte `gps_lat`, `gps_lng`, `gps_accuracy` en FormData
  - `backend/app/templates/report_detail.html` — acquisition JS via `navigator.geolocation.getCurrentPosition()` + affichage lien Google Maps
  - `backend/app/services/pdf_service.py` — export GPS dans le PDF
- **Impact** : Chaque photo est géolocalisée automatiquement avec précision

### Modales d'édition responsive

- **Fichiers** :
  - `backend/app/templates/report_detail.html` — modal task réutilisable création/édition
  - `backend/app/templates/tasks.html` — modal édition tâche
  - `backend/app/templates/signatures.html` — modal édition signature
- **Changement** : Remplacement de `window.prompt()` par des formulaires HTML complets dans des modals
- **Impact** : Utilisable sur smartphone, tablette et desktop

### Historique des interventions

- **Fichiers** :
  - `backend/app/templates/history.html` — nouvelle page
  - `backend/app/main.py` — route `/history`
  - `backend/app/templates/layout.html` — lien "Historique" dans la navigation
- **Changement** : Page listant tous les rapports par site, triés chronologiquement, avec un aperçu des photos et tâches
- **Impact** : Suivi des interventions sur une zone (cimetière, chantier, équipement)

---

## P1 — Fonctionnalités importantes

### Recherche rapports / photos / tâches / signatures

- **Fichiers** :
  - `backend/app/templates/reports.html` — barre de recherche + `filterReports()`
  - `backend/app/templates/photos.html` — barre de recherche + `filterPhotos()`
  - `backend/app/templates/tasks.html` — barre de recherche + `filterTasks()`
  - `backend/app/templates/signatures.html` — barre de recherche + `filterSignatures()`
- **Changement** : Filtrage côté client JavaScript sur les listes chargées
- **Impact** : Retrouver rapidement un élément sans pagination serveur

### Confirmation de suppression

- **Fichiers** :
  - `backend/app/templates/layout.html` — modal globale `modal-confirm-delete`
  - `backend/app/static/js/app.js` — `confirmDelete()` et `executeDelete()`
- **Changement** : Remplacement de `window.confirm()` par une modal HTML cohérente avec le design
- **Impact** : Suppression accidentelle impossible

---

## Corrections et améliorations

### Correction valeurs météo

- **Fichier** : `backend/app/templates/reports.html`
- **Problème** : Valeurs `rainy`, `windy` dans le select UI, mais `rain`, `storm` dans l'enum `WeatherType`
- **Correction** : Alignement des valeurs avec l'enum + ajout `snow`, `fog`

### Correction chemins static/templates

- **Fichier** : `backend/app/main.py`
- **Problème** : `settings.storage_root.parent` retournait un chemin incorrect selon le répertoire de travail
- **Correction** : Utilisation de `pathlib.Path(__file__).resolve().parent` pour un chemin absolu basé sur le fichier source

### Photos intégrées au PDF

- **Fichier** : `backend/app/services/pdf_service.py`
- **Changement** : `reportlab.platypus.Image` intégré pour inclure les photos dans le PDF
- **Impact** : Le PDF contient désormais les images réelles, pas seulement leur nom de fichier

### Correction encodage PDF

- **Fichier** : `backend/app/services/pdf_service.py`
- **Changement** : Remplacement des entités HTML (`&eacute;`, `&acirc;`, etc.) par des caractères Unicode directs
- **Impact** : ReportLab affiche correctement les accents

---

## Tests

- **Résultat** : 21 tests automatisés passent
- **Couverture** : CRUD rapports, photos, tâches, signatures
- **Warnings** : 54 warnings liés à `datetime.utcnow()` déprécié (det technique mineure)

---

## Fichiers créés

- `ANALYSE_ARCHITECTURE.md`
- `ANALYSE_METIER.md`
- `OFFLINE_V2_PREPARATION.md`
- `TEST_REPORT.md`
- `CHANGELOG_V1_1.md`
- `MIGRATION_NOTES.md`
- `backend/app/templates/history.html`

## Fichiers modifiés

| Fichier | Changement |
|---------|------------|
| `backend/app/models/report.py` | Ajout `gps_accuracy` |
| `backend/app/schemas/report.py` | Ajout `gps_accuracy`, `report_id` |
| `backend/app/api/photos.py` | GPS dans FormData |
| `backend/app/services/pdf_service.py` | Photos + GPS dans PDF, accents |
| `backend/app/main.py` | Route `/history`, chemins absolus |
| `backend/app/templates/layout.html` | Lien historique, modal confirm |
| `backend/app/templates/reports.html` | Météo corrigée, recherche |
| `backend/app/templates/report_detail.html` | Capture native, GPS, modal task |
| `backend/app/templates/tasks.html` | Modal édition, recherche |
| `backend/app/templates/signatures.html` | Modal édition, recherche |
| `backend/app/templates/photos.html` | Recherche |
| `backend/app/static/js/app.js` | Confirmation modal |
