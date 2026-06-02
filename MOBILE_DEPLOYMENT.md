# MOBILE_DEPLOYMENT

FieldReport v1.1 — Guide d'utilisation mobile
Date : 2026-06-02

---

## 1. Android

### Accès navigateur

1. Ouvrir Chrome (recommandé) ou Firefox
2. Saisir l'URL de l'application : `https://fieldreport.example.com`
3. L'interface s'adapte automatiquement à l'écran

### Ajout à l'écran d'accueil (PWA-like)

1. Dans Chrome, appuyer sur le menu `⋮` (trois points)
2. Sélectionner **"Ajouter à l'écran d'accueil"**
3. Nommer le raccourci : **FieldReport**
4. Confirmer avec **"Ajouter"**

L'icône apparaît sur l'écran d'accueil. L'application s'ouvre en plein écran sans la barre d'adresse.

### Mode application

- L'application fonctionne comme une application native
- Pas besoin de taper l'URL à chaque fois
- Le raccourci utilise l'icône du site (favicon)

---

## 2. iPhone (iOS)

### Accès navigateur

1. Ouvrir **Safari** (obligatoire pour le mode PWA)
2. Saisir l'URL : `https://fieldreport.example.com`

### Ajout à l'écran d'accueil

1. Appuyer sur le bouton **Partager** (carré avec flèche vers le haut)
2. Faire défiler et sélectionner **"Sur l'écran d'accueil"**
3. Nommer le raccourci : **FieldReport**
4. Confirmer avec **"Ajouter"**

### Mode application

- Safari crée une application autonome
- L'interface occupe tout l'écran
- Pas de barre de navigation Safari

---

## 3. Tablette (Android et iPad)

### Utilisation recommandée

La tablette est le **device optimal** pour FieldReport :
- Écran plus grand pour la saisie et la lecture des rapports
- Appareil photo disponible (iPad Pro, tablettes Android)
- GPS intégré (cellulaire) ou via WiFi
- Autonomie suffisante pour une journée de terrain

### Configuration recommandée

- Garder le chargeur ou une batterie externe pour les longues journées
- Configurer le verrouillage d'écran pour éviter les manipulations accidentelles en poche
- Désactiver la rotation automatique si nécessaire pour une utilisation stable

---

## 4. Fonctionnement GPS

### Prérequis

- GPS activé dans les paramètres système du device
- Permission de géolocalisation accordée au navigateur
- Connexion réseau (WiFi ou 4G/5G) — optionnel mais recommandée

### Fonctionnement

1. Ouvrir la modal **"+ Ajouter une photo"**
2. Attendre 2-5 secondes
3. Les coordonnées s'affichent : `GPS : 48.85670, 2.35220 (±5m)`
4. Si le GPS échoue : le message `GPS : échec de l'acquisition` apparaît
5. L'upload est possible même sans coordonnées

### Précision attendue

| Environnement | Précision typique |
|---------------|-------------------|
| Extérieur dégagé | 3-10 mètres |
| Zone urbaine | 10-30 mètres |
| Forêt / vallée | 20-100 mètres |
| Intérieur | Non disponible |

### Dépannage GPS

| Problème | Solution |
|----------|----------|
| "GPS : non disponible" | Activer la localisation dans les paramètres système |
| "échec de l'acquisition" | Sortir à l'extérieur, attendre 15 secondes, réessayer |
| Précision > 50m | Attendre le "fix" précis, bouger légèrement |
| Permission refusée | Aller dans Paramètres > Safari/Chrome > Autorisations > Localisation > Autoriser |

---

## 5. Fonctionnement photo

### Capture native

Sur **smartphone et tablette** :
1. Ouvrir la modal photo
2. L'appareil photo natif du device s'ouvre automatiquement
3. Prendre la photo
4. La photo apparaît dans le formulaire
5. Compléter le commentaire et la priorité si besoin
6. Uploader

**Note iOS** : Safari offre toujours la possibilité de basculer vers la galerie depuis l'interface caméra.

### Sur PC

- Le sélecteur de fichier classique s'ouvre
- Sélectionner une image depuis l'ordinateur
- Pas de GPS (comportement normal)

---

## 6. Permissions requises

| Permission | Navigateur | Android | iOS | Usage |
|------------|-----------|---------|-----|-------|
| Caméra | Chrome, Safari | Oui | Oui | Prise de photo native |
| Géolocalisation | Chrome, Safari | Oui | Oui | Acquisition GPS |
| Stockage | Chrome, Safari | Non | Non | Pas nécessaire (serveur) |
| Notifications | Chrome, Safari | Optionnel | Optionnel | Pas utilisé v1.1 |

### Comment accorder les permissions

**Android (Chrome)** :
1. Appuyer sur l'icône `i` dans la barre d'adresse
2. Permissions > Autoriser la caméra / la localisation

**iOS (Safari)** :
1. Paramètres > Safari > Confidentialité et sécurité
2. Ou directement depuis la demande de permission lors de l'usage

---

## 7. Conseils d'utilisation terrain

### Avant de partir

- [ ] Vérifier que le device est chargé (> 80%)
- [ ] Tester l'accès à l'URL depuis le site
- [ ] Vérifier que le GPS fonctionne (prendre une photo test)
- [ ] Ajouter le raccourci à l'écran d'accueil

### Pendant l'intervention

- Prendre les photos immédiatement après constatation (mémoire fraîche)
- Vérifier les coordonnées GPS affichées sous la photo
- Ajouter les tâches au fur et à mesure
- Signer le rapport avant de quitter le site

### Retour au bureau

- Générer le PDF depuis un PC pour vérification visuelle
- Télécharger le PDF pour transmission au client
- Consulter l'historique pour le prochain rendez-vous
