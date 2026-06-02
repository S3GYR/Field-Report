# FIELDREPORT_ROADMAP

Roadmap produit
Date : 2026-06-02

---

## V1.1.x — Stabilisation (Q2 2026)

### Objectif
Corrections et améliorations mineures suite au déploiement pilote.

| # | Fonctionnalité | Effort | Priorité |
|---|----------------|--------|----------|
| 1.1.1 | Vérification taille upload côté serveur | 1/2j | Critique |
| 1.1.1 | Vérification type MIME upload | 1/2j | Important |
| 1.1.1 | Limitation port Docker à 127.0.0.1 | 1/4j | Important |
| 1.1.2 | Correction `datetime.utcnow()` déprécié | 1/2j | Important |
| 1.1.2 | Création fichier `.env.example` | 1/4j | Amélioration |
| 1.1.3 | Utilisateur non-root dans Dockerfile | 1j | Important |
| 1.1.3 | Headers sécurité Nginx par défaut | 1/2j | Amélioration |

---

## V1.2 — Productivité (Q3 2026)

### Objectif
Améliorer la productivité terrain sans changer l'architecture.

| # | Fonctionnalité | Description | Effort |
|---|----------------|-------------|--------|
| 1 | Tableau de bord enrichi | Statistiques : tâches par statut, coûts par site, rapports par mois | 3j |
| 2 | Filtres avancés | Filtre par date, par statut, par client sur toutes les listes | 2j |
| 3 | Export CSV / Excel | Export des rapports, tâches, photos dans un tableur | 2j |
| 4 | Duplication de rapport | Cloner un rapport existant comme template | 1j |
| 5 | Commentaires riches | Éditeur simple (gras, listes) dans les commentaires | 2j |
| 6 | Favicon et PWA | Icône, manifest.json, service de base (pas encore offline) | 1j |

---

## V1.3 — Géolocalisation et analyse (Q4 2026)

### Objectif
Exploiter les données GPS et ajouter des outils d'analyse.

| # | Fonctionnalité | Description | Effort |
|---|----------------|-------------|--------|
| 1 | Cartographie | Carte Leaflet sur `/history` avec marqueurs des interventions | 4j |
| 2 | Cluster photos GPS | Regrouper les photos proches géographiquement | 2j |
| 3 | Statistiques terrain | Nombre d'interventions par zone, coûts moyens, durées | 2j |
| 4 | Filtrage géographique | Rechercher les rapports dans un rayon de X km | 2j |
| 5 | Export KML/GPX | Exporter les points GPS pour Google Earth / Garmin | 2j |

---

## V2.0 — Mode offline (Q1 2027)

### Objectif
Permettre l'utilisation terrain sans connexion réseau.

| # | Fonctionnalité | Description | Effort |
|---|----------------|-------------|--------|
| 1 | Service Worker | Intercepter les requêtes, cache des assets | 5j |
| 2 | IndexedDB | Stocker les rapports, photos (base64), tâches localement | 8j |
| 3 | Sync API | Synchronisation automatique lors du retour connexion | 10j |
| 4 | Gestion des conflits | Résolution si données modifiées sur serveur et localement | 5j |
| 5 | File API | Stockage temporaire des photos avant sync | 3j |
| 6 | Indicateur connexion | Icône en ligne/hors ligne visible en permanence | 1j |

**Impact** : Transformer FieldReport en PWA capable de fonctionner hors réseau. C'est la fonctionnalité la plus demandée par les utilisateurs terrain.

---

## V3.0 — Multi-utilisateurs et cloud (Q3 2027)

### Objectif
Passer à une application collaborative multi-agents.

| # | Fonctionnalité | Description | Effort |
|---|----------------|-------------|--------|
| 1 | Authentification JWT | Login / mot de passe, tokens sécurisés | 5j |
| 2 | Rôles | Admin, Agent, Lecteur | 3j |
| 3 | Traçabilité | `created_by`, `updated_by` sur toutes les entités | 2j |
| 4 | Assignation tâches | `assigned_to` sur Task avec notification | 3j |
| 5 | Date d'échéance | `due_date` sur Task, alertes visuelles | 2j |
| 6 | Synchronisation cloud | Multi-device, données centralisées | 8j |
| 7 | PostgreSQL optionnel | Remplacer SQLite pour la concurrence | 5j |
| 8 | Notifications push | Web Push API pour les tâches assignées | 4j |

**Impact** : Passage d'un outil mono-utilisateur à une plateforme collaborative pour les équipes.

---

## Planning synthétique

| Version | Période | Thème | Effort estimé |
|---------|---------|-------|---------------|
| v1.1.x | Q2 2026 | Stabilisation, sécurité | 1 semaine |
| v1.2 | Q3 2026 | Productivité, exports | 2 semaines |
| v1.3 | Q4 2026 | Géolocalisation, cartes | 2 semaines |
| v2.0 | Q1 2027 | Mode offline (PWA) | 6 semaines |
| v3.0 | Q3 2027 | Multi-utilisateurs, cloud | 5 semaines |

---

## Dépendances entre versions

```
v1.1.x (sécurité)
    ↓
v1.2 (productivité)
    ↓
v1.3 (cartographie)
    ↓
v2.0 (offline) ──→ v3.0 (multi-users)
    │                   │
    └─── IndexedDB ←──┘
```

v2.0 et v3.0 peuvent être développées en parallèle après v1.3, mais v3.0 requiert l'infrastructure IndexedDB de v2.0 pour le stockage local.
