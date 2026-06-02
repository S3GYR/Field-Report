# OFFLINE_V2_PREPARATION

FieldReport — Préparation architecture hors connexion v2.0
Date : 2026-06-02

---

## 1. Objectif

Permettre la saisie complète d'un rapport sans connexion réseau, avec synchronisation automatique dès que le réseau revient.

---

## 2. Architecture cible

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Smartphones   │────▶│  Service Worker  │────▶│   IndexedDB     │
│   / Tablettes   │     │  (cache, sync)   │     │  (données)      │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │  FastAPI Backend │
                        │  (sync online)   │
                        └──────────────────┘
```

---

## 3. Composants

### 3.1 Service Worker

**Rôle** :
- Intercepter les requêtes HTTP
- Servir les assets (CSS, JS, HTML) depuis le cache
- Mettre en file d'attente les requêtes POST/PUT/DELETE en cas d'absence de réseau
- Déclencher la synchronisation dès que le réseau revient

**Implémentation** :

```javascript
// sw.js
const CACHE_NAME = 'fieldreport-v1';
const STATIC_ASSETS = [
  '/',
  '/static/css/main.css',
  '/static/js/app.js',
  '/reports',
  '/history',
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS)));
});

self.addEventListener('fetch', e => {
  if (e.request.method === 'GET') {
    e.respondWith(caches.match(e.request).then(resp => resp || fetch(e.request)));
  } else {
    e.respondWith(
      fetch(e.request).catch(() => {
        // Queue for background sync
        return queueRequest(e.request);
      })
    );
  }
});

self.addEventListener('sync', e => {
  if (e.tag === 'sync-reports') {
    e.waitUntil(syncPendingRequests());
  }
});
```

### 3.2 IndexedDB

**Schéma** :

| Store | Clé | Index | Description |
|-------|-----|-------|-------------|
| reports | id (auto) | site, status | Rapports en attente de sync |
| photos | id (auto) | report_id | Photos (blob) en attente |
| tasks | id (auto) | report_id | Tâches en attente |
| signatures | report_id | — | Signatures en attente |
| sync_queue | id (auto) | timestamp | File d'attente des requêtes API |

**Implémentation** :

```javascript
// db.js
const DB_NAME = 'FieldReportDB';
const DB_VERSION = 1;

function openDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onerror = () => reject(req.error);
    req.onsuccess = () => resolve(req.result);
    req.onupgradeneeded = e => {
      const db = e.target.result;
      db.createObjectStore('reports', { keyPath: 'id', autoIncrement: true });
      db.createObjectStore('photos', { keyPath: 'id', autoIncrement: true });
      db.createObjectStore('tasks', { keyPath: 'id', autoIncrement: true });
      db.createObjectStore('signatures', { keyPath: 'report_id' });
      db.createObjectStore('sync_queue', { keyPath: 'id', autoIncrement: true });
    };
  });
}
```

### 3.3 Stratégie de synchronisation

**File d'attente** :

1. Chaque action utilisateur (créer rapport, ajouter photo, etc.) génère une entrée dans `sync_queue`
2. La requête est d'abord envoyée au backend
3. Si le backend répond 2xx, l'entrée est supprimée
4. Si le backend ne répond pas (offline), l'entrée reste en file d'attente
5. Dès que le réseau revient (`sync` event ou `online` event), la file est traitée

**Ordre de synchronisation** :

1. Rapports (création)
2. Photos (upload après création du rapport)
3. Tâches
4. Signatures

**Gestion des conflits** :

- Timestamp-based : la dernière modification gagne
- Si conflit détecté (statut différent côté serveur), afficher une UI de résolution
- Version côté serveur prioritaire si conflit non résolu

### 3.4 UI hors ligne

**Indicateurs** :

- Badge "Hors ligne" dans le header quand `navigator.onLine === false`
- Compteur "En attente de sync" avec le nombre d'éléments dans `sync_queue`
- Bouton "Forcer la synchronisation" manuel

**Limitations offline** :

| Action | Online | Offline |
|--------|--------|---------|
| Créer rapport | API POST | IndexedDB insert + queue |
| Prendre photo | API POST | Blob IndexedDB + queue |
| Lister rapports | API GET | IndexedDB query |
| Générer PDF | API POST | PDF généré au retour online |
| Signature | API POST | Blob IndexedDB + queue |

---

## 4. Estimation

| Phase | Durée | Complexité |
|-------|-------|------------|
| Service Worker basique (cache assets) | 4h | Faible |
| IndexedDB + schémas | 6h | Moyenne |
| Queue de synchronisation | 8h | Moyenne |
| Gestion des conflits | 6h | Moyenne |
| UI offline (indicateurs) | 4h | Faible |
| Tests offline | 4h | Moyenne |
| **Total** | **~32h** | **Moyenne** |

---

## 5. Risques

| Risque | Mitigation |
|--------|------------|
| IndexedDB limité à ~50MB sur iOS | Compresser images, sync fréquente, limite 20 photos en queue |
| Service Worker non supporté (vieux navigateurs) | Graceful degradation : message "Connectez-vous pour sauvegarder" |
| Conflits de données | Timestamp + UI résolution manuelle |
| Sync interrompue | Retry avec exponential backoff, persistance queue |
| Photos trop volumineuses | Redimensionner côté client avant stockage |

---

## 6. Prérequis v1.1

Les modifications v1.1 préparent le terrain :

- **Modales responsive** : fonctionnent offline sans rechargement
- **Capture photo native** : les photos peuvent être stockées localement avant sync
- **GPS** : coordonnées attachées aux photos pour preuve terrain
- **Historique** : consultation de données historiques en cache

---

## 7. Phases d'implémentation

| Version | Objectif |
|---------|----------|
| v1.1 | Cache assets (Service Worker basique) — **préparation** |
| v1.2 | Cache données lectures (rapports, tâches, photos) — **lecture offline** |
| v2.0 | Saisie complète offline avec sync bidirectionnelle — **écriture offline** |
