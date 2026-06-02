# MOBILE_FIRST_STRATEGY

FieldReport — Stratégie multi-device et hors-ligne
Date : 2026-06-02

---

## 1. Philosophie

FieldReport est conçu pour l'inspecteur sur le terrain. Le smartphone est le device principal. La tablette est l'alternative pour la signature client. Le PC reste le poste de supervision et de relecture.

**Principe** : Mobile-first design. Chaque écran doit être utilisable avec un pouce, en plein soleil, sans zoom.

---

## 2. Utilisation smartphone

### Contexte d'usage

- En extérieur, mains sales ou gantées
- Écran lumineux, contrasté nécessaire
- Connexion 4G/5G instable ou inexistante
- Saisie au pouce, une main

### Exigences v1.1

| Exigence | Implémentation |
|----------|---------------|
| Boutons tactiles >= 44x44px | CSS `min-height: 44px; min-width: 44px` sur tous les boutons et liens |
| Texte lisible en plein soleil | Contraste >= 4.5:1, taille de base >= 16px |
| Saisie rapide | Champs réduits au minimum. Date picker natif. Client et site avec autocomplétion (localStorage) |
| Photo directe | `capture="environment"` sur l'input file |
| GPS auto | `navigator.geolocation.getCurrentPosition()` au moment de la photo |
| Feedback haptique visuel | Toasts non bloquants, spinner sur actions longues |
| Pas de zoom forcé sur input | `font-size: 16px` minimum sur tous les `<input>` (évite le zoom iOS) |
| Menu compact | Hamburger menu ou bottom navigation pour < 768px |
| Tableaux défilants horizontalement | `overflow-x: auto` sur toutes les tables |

### Parcours smartphone typique

1. Inspecteur arrive sur chantier, ouvre FieldReport
2. Dashboard → "Nouveau rapport" (bouton large, visible)
3. Saisie rapide : numéro (auto-incrémenté suggéré), date (aujourd'hui par défaut), client (autocomplete), site
4. Prend des photos directement depuis l'appareil photo (capture native)
5. Chaque photo est géolocalisée automatiquement
6. Ajoute 2-3 tâches via modals (pas de prompt)
7. Le client signe sur la tablette de l'inspecteur (écran plus grand)
8. Génère le PDF et l'envoie par email au client
9. Retour au dashboard, rapport marqué "validé"

---

## 3. Utilisation tablette

### Contexte d'usage

- Signature du client à la fin de la visite
- Relecture rapide du rapport sur un écran plus grand
- Saisie au salon de chantier (sous abri)

### Exigences v1.1

| Exigence | Implémentation |
|----------|---------------|
| Canvas de signature responsive | Le canvas de signature doit s'adapter à la largeur de l'écran. Pas de scroll pendant la signature. |
| Vue split-screen | Possibilité de voir le rapport et la signature côte-à-côte (non bloquant pour v1.1) |
| Orientation paysage recommandée | Message léger si l'utilisateur est en portrait : "Tournez la tablette pour une meilleure signature" |
| Touch targets plus larges | Même règle 44px que smartphone, mais avec plus d'espace disponible |

### Parcours tablette typique

1. Inspecteur ouvre le rapport en cours sur sa tablette
2. Il fait défiler les photos et les observations
3. Il présente la tablette au client
4. Le client lit le rapport, signe sur le canvas
5. L'inspecteur approuve le rapport
6. Génération PDF et envoi

---

## 4. Utilisation PC

### Contexte d'usage

- Bureau du responsable technique
- Relecture, validation, export
- Gestion des rapports sur plusieurs mois
- Administration et maintenance

### Exigences v1.1

| Exigence | Impléplementation |
|----------|-------------------|
| Layout multi-colonnes | Dashboard en 3 colonnes, tableaux avec toutes les colonnes visibles |
| Raccourcis clavier | `Escape` ferme les modals, `Ctrl+K` focus la barre de recherche |
| Vue détaillée | Report detail avec toutes les sections dépliées par défaut |
| Export facile | Boutons d'export CSV et PDF bien visibles |
| Multitâche | Plusieurs onglets navigateur possibles (reports, photos, tâches) |

### Parcours PC typique

1. Responsable ouvre FieldReport le lundi matin
2. Dashboard : 5 rapports en attente de validation
3. Clic sur le premier → report detail complet
4. Relecture des photos, des tâches, de la signature
5. Approuve le rapport
6. Génère le PDF final et l'archive
7. Passe au suivant

---

## 5. Fonctionnement hors connexion (vision future)

### Objectif v2.0

Permettre la saisie complète d'un rapport sans connexion réseau, avec synchronisation automatique dès que le réseau revient.

### Architecture envisagée

```
+-------------+     +------------------+     +-------------+
|   Client    +---->+  Service Worker  +---->+   IndexedDB  |
|  (PWA)      |     |  (cache, sync)   |     |  (données)   |
+-------------+     +------------------+     +-------------+
                            |
                            v
                     +------------------+
                     |  FastAPI Backend  |
                     |  (sync quand online)|
                     +------------------+
```

### Comportements offline

| Action | Online | Offline |
|--------|--------|---------|
| Créer rapport | API POST → SQLite | IndexedDB insert + flag `sync: false` |
| Modifier rapport | API PUT | IndexedDB update + flag `sync: false` |
| Prendre photo | API POST → storage | Blob IndexedDB + flag `sync: false` |
| Lister rapports | API GET | IndexedDB query |
| Générer PDF | API POST → ReportLab | ReportLab côté client (impossible, trop lourd) → PDF généré au retour online |
| Signature | Canvas + API POST | Canvas + IndexedDB blob |

### Stratégie de synchronisation

1. **Background Sync** (Service Worker) : dès que le réseau revient, envoyer les données en file d'attente
2. **Conflict resolution** : timestamp-based. La dernière modification gagne. Version côté serveur prioritaire si conflit.
3. **UI indication** : Badge "En attente de sync" avec compteur d'éléments non synchronisés
4. **Retry** : Exponential backoff en cas d'erreur réseau transitoire

### Implémentation progressive

| Phase | Fonctionnalité | Complexité |
|-------|---------------|------------|
| v1.1 | Cache des assets (CSS, JS) pour démarrage rapide | Faible (Service Worker basique) |
| v1.2 | Cache des données listes (rapports, tâches) pour lecture offline | Moyenne |
| v2.0 | Saisie complète offline avec sync bi-directionnelle | Haute |

### Risques

| Risque | Mitigation |
|--------|------------|
| IndexedDB limité à ~50MB sur iOS | Compresser les images, limiter la file d'attente, sync fréquente |
| Conflits de données | Timestamp + version. UI de résolution manuelle si conflit détecté |
| Service Worker non supporté sur vieux navigateurs | Graceful degradation. Message "Connectez-vous pour sauvegarder" |

---

## 6. Breakpoints CSS

| Breakpoint | Device | Layout |
|------------|--------|--------|
| < 576px | Smartphone portrait | Single column, bottom nav, large buttons |
| 576px - 768px | Smartphone paysage / tablette portrait | Single column, side nav possible |
| 768px - 992px | Tablette paysage / petit PC | 2 colonnes pour dashboard, tables visibles |
| > 992px | PC desktop | 3 colonnes, tables complètes, side nav fixe |

---

## 7. Tests multi-device

| Device | Navigateur | Tests prioritaires |
|--------|-----------|-------------------|
| iPhone 14 | Safari iOS | Capture photo, signature canvas, modals |
| Samsung Galaxy | Chrome Android | Capture photo, GPS, upload |
| iPad Pro | Safari iOS | Signature canvas, relecture rapport |
| Windows PC | Chrome | Recherche, validation, export |

---

## 8. Conclusion

La stratégie mobile-first de FieldReport repose sur trois piliers :

1. **Smartphone** : Saisie rapide, photo native, GPS, modals, feedback visuel
2. **Tablette** : Signature client, relecture confortable
3. **PC** : Supervision, recherche, validation, export

L'offline est une vision v2.0, décomposée en phases progressives pour maîtriser la complexité.
