# V1_1_IMPLEMENTATION_PLAN

FieldReport v1.1 — Plan d'implémentation Product Sprint
Date : 2026-06-02

---

## Contexte

FieldReport v1.0.1 est techniquement stabilisé. L'objectif de v1.1 est de transformer l'outil en véritable solution terrain mobile en traitant les 5 irritants les plus critiques identifiés dans `PRODUCT_GAP_ANALYSIS.md`.

---

## 1. Capture photo native mobile

| | |
|---|---|
| **Description** | Permettre la prise de photo directement depuis l'appareil photo du smartphone via l'attribut HTML `capture="environment"` sur l'input file |
| **Impact métier** | **Très haut** — Réduit le temps de saisie terrain de 30 %. Élimine le besoin de quitter l'application pour prendre une photo. |
| **Complexité technique** | **Très faible** — Attribut HTML natif, aucun JS nécessaire |
| **Dépendances** | Aucune |
| **Estimation temps** | 15 min |
| **Risque** | Aucun — API HTML5 standard supportée par tous les navigateurs mobiles modernes |
| **Priorité** | **P0** |

**Détail technique** :

```html
<!-- Actuel -->
<input type="file" name="file" accept="image/*">

<!-- Cible -->
<input type="file" name="file" accept="image/*" capture="environment">
```

**Fichiers concernés** :
- `backend/app/templates/photos.html` (formulaire d'upload)
- `backend/app/templates/report_detail.html` (si upload inline)

---

## 2. Géolocalisation automatique

| | |
|---|---|
| **Description** | Capturer les coordonnées GPS (`latitude`, `longitude`) lors de la prise de photo ou de la création de rapport via `navigator.geolocation` |
| **Impact métier** | **Haut** — Preuve de localisation pour les rapports. Capitalisation du patrimoine terrain. |
| **Complexité technique** | **Faible** — API `navigator.geolocation.getCurrentPosition()` native. Stockage dans la base via champs `latitude`/`longitude` existants ou nouveaux. |
| **Dépendances** | Permission navigateur `geolocation`. Connexion réseau initiale pour obtenir la position (peut être longue si pas de GPS intégré). |
| **Estimation temps** | 2h |
| **Risque** | **Faible** — L'utilisateur peut refuser la permission. Fallback : saisie manuelle ou absence de données. |
| **Priorité** | **P0** |

**Détail technique** :

- Ajouter `latitude`/`longitude` au modèle `Photo` et/ou `Report`
- Côté JS : `navigator.geolocation.getCurrentPosition()` avant l'upload photo
- Envoyer les coordonnées en plus du fichier dans le FormData
- Afficher une petite carte statique ou les coordonnées textuelles dans le détail photo

**Fichiers concernés** :
- `backend/app/models/photo.py` (nouveaux champs)
- `backend/app/schemas/photo.py` (champs dans le schéma)
- `backend/app/api/photos.py` (endpoint upload)
- `backend/app/templates/photos.html` (JS + affichage)
- `backend/app/static/js/app.js` (helper géoloc)

---

## 3. Modales d'édition

| | |
|---|---|
| **Description** | Remplacer tous les appels `window.prompt()` par des modals HTML contenant des formulaires complets avec validation. Concerne les pages Tâches et Signatures. |
| **Impact métier** | **Très haut** — `prompt()` est inutilisable sur mobile. C'est l'irritant numéro 1 signalé dans l'audit UX. |
| **Complexité technique** | **Moyenne** — Requiers la création de modals HTML (le système modal existe déjà), validation côté client, et mise à jour du JS pour envoyer les données via API. |
| **Dépendances** | Modal system déjà en place (`openModal`, `closeModal`, CSS modal existant) |
| **Estimation temps** | 4h |
| **Risque** | **Faible** — Le système de modal est déjà fonctionnel (reports.html). Il faut le répliquer pour tasks.html et signatures.html. |
| **Priorité** | **P0** |

**Détail technique** :

- Créer des modals d'édition dans `tasks.html` et `signatures.html` (inspirer de `reports.html`)
- Chaque modal contient un `<form>` avec les champs nécessaires
- Validation HTML5 (`required`, `min`, `max`) + feedback visuel
- JS : `apiPut` à la place de `prompt()` + `apiPut`

**Fichiers concernés** :
- `backend/app/templates/tasks.html`
- `backend/app/templates/signatures.html`
- `backend/app/static/js/app.js` (si helpers partagés)

---

## 4. Recherche rapports/photos/tâches

| | |
|---|---|
| **Description** | Ajouter une barre de recherche en haut des pages de liste (rapports, photos, tâches) filtrant les résultats côté client sur le texte visible. |
| **Impact métier** | **Haut** — Indispensable au-delà de 50 éléments. Réduit le temps de recherche de 2 min à 5 s. |
| **Complexité technique** | **Faible** — Filtrage côté client en JS vanilla sur les données déjà chargées. Pas besoin de nouvel endpoint API pour v1.1. |
| **Dépendances** | Les données doivent déjà être chargées dans le DOM (c'est le cas actuellement) |
| **Estimation temps** | 2h |
| **Risque** | **Aucun** — Filtrage client, pas d'impact serveur |
| **Priorité** | **P1** |

**Détail technique** :

```javascript
function filterTable(query) {
    const rows = document.querySelectorAll("#reports-table tr");
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(query.toLowerCase()) ? "" : "none";
    });
}
```

**Fichiers concernés** :
- `backend/app/templates/reports.html`
- `backend/app/templates/photos.html`
- `backend/app/templates/tasks.html`
- `backend/app/templates/signatures.html`

---

## 5. Confirmation de suppression

| | |
|---|---|
| **Description** | Ajouter une modal de confirmation avant chaque suppression (rapport, photo, tâche, signature) pour éviter les suppressions accidentelles. |
| **Impact métier** | **Moyen** — Sécurise les données. Un rapport supprimé par erreur est irrécupérable. |
| **Complexité technique** | **Très faible** — Réutiliser le système de modal existant. Une modal générique suffit. |
| **Dépendances** | Système de modal |
| **Estimation temps** | 1h |
| **Risque** | **Aucun** |
| **Priorité** | **P1** |

**Détail technique** :

- Modal générique `modal-confirm` avec message dynamique et callback
- Affiché avant chaque appel `apiDelete`
- Boutons "Annuler" (ferme la modal) / "Confirmer la suppression" (exécute le delete)

---

## Tableau récapitulatif

| # | Fonctionnalité | P | Impact | Complexité | Dépendances | Estimation |
|---|----------------|---|--------|-----------|-------------|------------|
| 1 | Capture photo native | P0 | Très haut | Très faible | Aucune | 15 min |
| 2 | Géolocalisation auto | P0 | Haut | Faible | Permission GPS | 2h |
| 3 | Modales d'édition | P0 | Très haut | Moyenne | Modals existants | 4h |
| 4 | Recherche rapports | P1 | Haut | Faible | Données chargées | 2h |
| 5 | Confirmation suppression | P1 | Moyen | Très faible | Modals existants | 1h |

**Total estimé** : ~9h30 de développement

---

## Planning suggéré

| Jour | Tâches |
|------|--------|
| J1 matin | Capture photo native + Géolocalisation |
| J1 après-midi | Modales d'édition (tasks + signatures) |
| J2 matin | Recherche rapports/photos/tâches/signatures |
| J2 après-midi | Confirmation suppression + tests manuels mobile |
| J3 | Validation complète (pytest, E2E, UI functional) |

---

## Définition of done v1.1

- [ ] Prise de photo directe fonctionne sur smartphone (Chrome Android, Safari iOS)
- [ ] Coordonnées GPS affichées sur les photos détail
- [ ] Plus aucun `window.prompt()` dans l'application
- [ ] Barre de recherche fonctionnelle sur toutes les pages de liste
- [ ] Confirmation avant suppression sur tous les boutons "Supprimer"
- [ ] `pytest backend/tests/` : 21 pass
- [ ] `validate_ui_functional.py` : 22 pass
- [ ] `ruff check backend/` : clean
- [ ] Test manuel sur smartphone (Chrome DevTools mobile + vrai device si possible)
