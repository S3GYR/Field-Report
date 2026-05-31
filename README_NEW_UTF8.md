# Field Report Application – Documentation Technique

## 1. Présentation du projet

### Besoin métier
Application destinée aux équipes de terrain (BTP, maintenance, inspection) pour documenter une visite : collecte d’informations générales, photos géolocalisées, tâches associées, validations et génération d’un rapport PDF riche.

### Utilisateurs visés
- Conducteurs de travaux, chefs de chantier
- Techniciens de maintenance
- Chargés d’inspection ou de contrôle qualité

### Cas d’usage principaux
1. Préparer un rapport structuré avant une réunion client.
2. Suivre les anomalies détectées sur site via une liste de tâches priorisées.
3. Capitaliser les photos avec coordonnées GPS et commentaires terrain.
4. Fournir un PDF officiel signé et archivable.

### Fonctionnalités majeures
- Gestion complète des rapports (CRUD) via FastAPI + SQLite.
- Stockage local des photos dans `storage/photos/YYYY/MM` avec miniatures.
- Gestion des tâches, signatures, commentaires, météo, coordonnées.
- Génération PDF via Jinja2 + WeasyPrint (`backend/app/pdf/report.html`).
- Frontend React/Vite/TypeScript (PWA-ready) consommant l’API.
- Script historique `generer_pdf.py` pour générer un PDF depuis un JSON/HTML legacy.

## 2. Fonctionnement général

1. **Création du rapport**  
   - Le dashboard React (`frontend/src/pages/DashboardPage.tsx`) liste les rapports via `GET /api/reports`.  
   - `POST /api/reports` crée une entrée (numéro, site, date, météo, statut).

2. **Ajout des photos**  
   - Upload via `POST /api/photos/{report_id}` (multipart).  
   - `PhotoStorageService` range les fichiers dans `storage/photos/YYYY/MM` et crée une miniature `.thumb.jpg` (copie brute si Pillow indisponible).  
   - L’API retourne l’objet `Photo` (chemins relatifs, suppression sécurisée via `DELETE /api/photos/{photo_id}`).

3. **Gestion des tâches**  
   - `POST /api/tasks/{report_id}` crée une tâche liée (optionnellement associée à une photo).  
   - `PUT /api/tasks/{task_id}` et `DELETE /api/tasks/{task_id}` assurent la mise à jour.  
   - Les champs coût/durée sont validés par les schémas Pydantic (`backend/app/schemas/report.py`).

4. **Commentaires**  
   - `Report.comments` (commentaire global) et `Photo.comment` (commentaire local).  
   - Exposés dans le PDF via le template Jinja2.

5. **Coordonnées GPS**  
   - Champs `gps_lat`/`gps_lng` sur `Photo`.  
   - Exploités côté React via `MapView` (Leaflet).  
   - En legacy, `template_sans_images.html` extrait l’EXIF et effectue un géocodage Nominatim.

6. **Génération du PDF**  
   - Endpoint `POST /api/reports/{id}/generate-pdf` → `ReportPdfService`.  
   - Rendu du template `backend/app/pdf/report.html` puis génération via WeasyPrint dans `storage/exports/report-<number>.pdf`.  
   - Le script legacy `generer_pdf.py` (ReportLab) lit un JSON local.

7. **Exports**  
   - PDF via l’endpoint ci-dessus.  
   - Legacy HTML : export CSV et impression navigateur.  
   - Photos servies via `/storage/...`, PDF via `/exports/...` (montages configurés dans `app/main.py`).

### Schéma ASCII des flux

```
Utilisateur terrain
   ↓ saisie
Frontend React (Vite, Leaflet, React Query)
   ↓ REST /api
FastAPI / SQLAlchemy / SQLite
   ↓ services
PhotoStorage & PDF Service
   ↓
Fichiers storage/photos & storage/exports

Legacy HTML ─► localStorage/sessionStorage ─► generer_pdf.py ─► rapport.pdf
```

## 3. Architecture du projet

```
Rapport/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/config.py
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── photo_storage.py
│   │   │   └── pdf_service.py
│   │   ├── main.py
│   │   └── pdf/report.html
│   ├── alembic/
│   ├── tests/
│   └── Dockerfile
├── frontend/
│   ├── src/ (App, pages, components, hooks, services)
│   ├── public/ (manifest PWA, icônes)
│   ├── package.json, vite.config.ts
│   └── Dockerfile
├── storage/ (photos + exports, créé au runtime)
├── docker-compose.yml
├── template_sans_images.html
├── generer_pdf.py
└── README_NEW_UTF8.md
```

### Responsabilités & dépendances clés
- **backend/app/api/** : routers FastAPI, dépendent de `db.session`, `models`, `schemas`, `services`.
- **models/report.py** : définit Report, Photo, Task, Signature + enums `ReportStatus`, `PhotoPriority`, `TaskStatus`, `WeatherType`.
- **schemas/report.py** : Pydantic v2 avec `ConfigDict(from_attributes=True)` pour sérialiser les objets ORM.
- **services/photo_storage.py** : upload, miniatures, suppression ; dépend de Pillow (optionnel), `pathlib`, `unicodedata`, `shutil`.
- **services/pdf_service.py** : rendu Jinja2 + WeasyPrint (import différé pour éviter les erreurs pendant les tests).
- **frontend/src/** : React Router, React Query, Leaflet, fetch via `services/api.ts`.
- **template_sans_images.html** : application legacy autonome exploitant localStorage/sessionStorage, FileReader, Leaflet CDN, fetch Nominatim.
- **generer_pdf.py** : script ReportLab lisant `rapport_data.json` et produisant un PDF hors backend.

## 4. Analyse du générateur PDF legacy (`generer_pdf.py`)

- **Chargement des données** : `parse_args()` lit `--input/--output`, `load_data()` prépare `rapport_data.json`, `resolve_output_path()` définit le chemin final.
- **Statistiques** : `compute_stats()` calcule nombre de photos/tâches, statuts (`collections.Counter`), coût total (`normalize_cost()`), attributs dérivés (`photo_index`, `photo_name`).
- **Images** : `image_flowable()` détecte fichier local, base64 (`image_b64`) ou utilise `placeholder_image`.
- **Tâches** : `build_tasks_table()` garde les tâches significatives, produit un tableau `N°/Description/Statut/Date/Coût/Durée` stylé via `TableStyle`.
- **Coûts** : `normalize_cost()` nettoie les entrées (`€`, espaces, virgules), `format_currency()` et `format_cell_cost()` standardisent l’affichage.
- **Sections** : `build_info_section()`, `build_photos_section()` et `build_summary_section()` orchestrent la mise en page ReportLab.
- **Habillage** : `draw_cover()` dessine la couverture (bandeau, statistiques météo/photos/tâches), `draw_footer()` ajoute pagination et titre.
- **Helpers** : `build_styles()`, `build_comment_section()`, `build_signature_section()`, `escape_html()`, `text_or_dash()`, `format_date()`, `priority_label()`.

## 5. Analyse de l’interface HTML legacy (`template_sans_images.html`)

- **Structure** : layout complet (header sticky, toolbar, cartes photo, récapitulatif, commentaires, signature).
- **Styles** : CSS inline (typo DM Serif/DM Sans), responsive, règles `@media print`, palette beige/bleu.
- **JavaScript** : architecture monolithique sans bundler. Variables globales `photos`, `nextPhotoId`, `nextTaskId`. Gestion locale via `localStorage` (`rapport_meta5`, `rapport_gc5`, etc.) et `sessionStorage` (images base64).
- **Fonctionnalités clés** :
  - `init()` : initialisation depuis le stockage local, fallback `ORIG_IMAGES`.
  - `render()` : reconstruit entièrement le DOM (cartes, récap, commentaires, signature, boutons).
  - `handleFiles()` : import drag&drop/input fichier, conversion base64, extraction GPS (`autoExtractGpsFromFiles()`).
  - `geocodeAddress()` / `reverseGeocode()` : appels fetch à l’API Nominatim.
  - `renderTasks()` / `updateTask()` : édition instantanée avec feedback visuel.
  - `buildRecap()` : tableau synthèse coûts/durées/statuts.
  - `safePrint()` : supprime les iframes avant impression pour éviter les blocages.
  - `exportCSV()` : génère un CSV complet pour archivage.
- **Mode offline** : toutes les données résident côté navigateur ; aucune dépendance backend.
- **Cartes** : Leaflet intégré via iframe, synchronisation des coordonnées auto-extraites.

## 6. Structure des données

Exemple de payload API :

```json
{
  "id": 1,
  "number": "RPT-001",
  "visit_date": "2024-05-01",
  "client": "ACME",
  "site": "Paris",
  "weather": "sunny",
  "comments": "...",
  "status": "draft",
  "photos": [
    {
      "id": 10,
      "filename": "p.jpg",
      "filepath": "photos/2024/05/p.jpg",
      "thumbnail_path": "photos/2024/05/p.thumb.jpg",
      "gps_lat": 48.85,
      "gps_lng": 2.42,
      "comment": "Observation",
      "priority": "high"
    }
  ],
  "tasks": [
    {
      "id": 33,
      "description": "Fixer",
      "status": "todo",
      "estimated_cost": 1200.0,
      "estimated_duration": 4.0,
      "photo_id": 10
    }
  ],
  "signature": {
    "id": 5,
    "name": "Laura Dupont",
    "role": "Conductrice",
    "signed_on": "2024-05-02",
    "signature_image": null
  }
}
```

| Champ | Type | Obligatoire | Description |
| --- | --- | --- | --- |
| `number` | string | oui | Identifiant unique du rapport |
| `visit_date` | date ISO | oui | Date de visite |
| `client` | string | oui | Client |
| `site` | string | oui | Chantier / site |
| `weather` | enum (`sunny`, `cloudy`, `rain`, `storm`, `snow`, `fog`, `unknown`) | non | Condition météo |
| `comments` | string | non | Commentaire global |
| `status` | enum (`draft`, `in_review`, `approved`, `archived`) | non | Avancement |
| `photos[].priority` | enum (`high`, `medium`, `low`, `none`) | non | Priorité photo |
| `tasks[].status` | enum (`todo`, `in_progress`, `done`, `blocked`) | oui | Avancement tâche |
| `signature.signed_on` | date | non | Date de signature |

Legacy `rapport_data.json` suit la structure `info/photos/signature/global_comment` définie dans `generer_pdf.py`.

## 7. Fonctionnalités existantes

| Fonction | Description | État |
| --- | --- | --- |
| CRUD rapports | API FastAPI + SQLite | ✅ |
| Upload photo + stockage local | Téléversement + miniature + suppression | ✅ |
| Gestion des tâches | CRUD + lien optionnel vers photo | ✅ |
| Gestion signature | CRUD complet | ✅ |
| Génération PDF (WeasyPrint) | Endpoint `/generate-pdf` + template Jinja2 | ✅ |
| Tests backend (pytest) | Scénario CRUD principal | ✅ |
| Frontend React PWA | Pages Dashboard/Report/Photos/Tasks/Export | ✅ (MVP) |
| Legacy HTML offline | Application autonome | ✅ |
| Legacy PDF (ReportLab) | Script `generer_pdf.py` | ✅ |
| Docker Compose | Services frontend + backend | ⚠️ dépend de l’installation Docker locale |

## 8. Dépendances

### Python (backend)
- `fastapi`, `uvicorn[standard]`
- `SQLAlchemy 2.0`, `alembic`
- `pydantic 2`, `pydantic-settings`
- `python-multipart`
- `passlib[bcrypt]` (non exploité pour l’instant)
- `jinja2`, `weasyprint`
- `httpx`
- `pytest`
- (legacy) `reportlab` pour `generer_pdf.py`

### Frontend
- React 18, React Router DOM
- `@tanstack/react-query`
- Vite, TypeScript
- Leaflet + CSS
- `vite-plugin-pwa`

### APIs externes (legacy)
- OpenStreetMap / Nominatim pour géocodage et reverse geocode.

## 9. Installation

### Pré-requis
- Python ≥ 3.11 (WeasyPrint nécessite GTK/Cairo/ffi côté OS).
- Node.js ≥ 18.
- (Optionnel) Docker Desktop / Docker Engine.

### Mode manuel (Windows / Linux)

```bash
python -m venv .venv
# Windows : .\.venv\Scripts\Activate.ps1
# Linux/macOS : source .venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt

cd backend
alembic upgrade head
uvicorn backend.app.main:app --host 0.0.0.0 --port 8200 --reload
```

Dans un second terminal :

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 3200
```

Accès : frontend `http://localhost:3200`, API docs `http://localhost:8200/docs`.

### Docker

1. Installer Docker Desktop (Windows/macOS) ou Docker Engine + compose plugin (Linux).  
2. `docker compose build` à la racine du projet.  
3. `docker compose up -d`.  
4. Frontend accessible sur `http://localhost:3200`, backend sur `http://localhost:8200`.  
> Les images actuelles n’embarquent pas encore toutes les dépendances natives WeasyPrint.

## 10. Guide d’utilisation

1. Lancer backend + frontend (voir installation).  
2. Créer un rapport via `POST /api/reports` (UI à venir sur Dashboard).  
3. Ajouter des photos via `POST /api/photos/{report_id}` (en attendant un formulaire React, utiliser curl/Postman).  
4. Créer/mettre à jour des tâches via `POST/PUT/DELETE /api/tasks`.  
5. Renseigner les coordonnées GPS et les commentaires sur les photos (`PUT /api/photos/{photo_id}`).  
6. Ajouter signature et commentaire global (`POST /api/signatures/{report_id}`, `PUT /api/reports/{id}`).  
7. Générer le PDF final via `POST /api/reports/{id}/generate-pdf` puis récupérer le fichier dans `storage/exports`.  
8. Pour un usage offline rapide, ouvrir `template_sans_images.html`.

## 11. Limitations connues

- WeasyPrint requiert des bibliothèques natives (GTK, Cairo). Sans elles, la génération PDF échoue.
- Si Pillow est absent, les miniatures sont de simples copies (pas de réduction, risque disque).
- L’UI React n’inclut pas encore tous les formulaires (upload photo, édition complète).
- Aucune authentification ni gestion multi-utilisateurs.
- `docker compose` échoue si Docker n’est pas installé/configuré.
- Suite de tests limitée (un seul scénario CRUD).
- Pas de migration automatique des données legacy (localStorage → SQLite).
- Pas de compression ni quota pour les photos.

## 12. Pistes d’amélioration

### Critique
| Amélioration | Bénéfice | Difficulté |
| --- | --- | --- |
| Authentification + rôles | Sécurité et traçabilité | Haute |
| UI React complète (formulaires, upload, validations) | Adoption utilisateur | Moyenne |
| Image Docker avec dépendances WeasyPrint | Déploiement fiable | Moyenne |

### Important
| Amélioration | Bénéfice | Difficulté |
| --- | --- | --- |
| Migration automatique legacy → SQLite | Continuité utilisateur | Moyenne |
| Tests API/photos/tâches/PDF | Qualité et CI/CD | Moyenne |
| Compression/redimensionnement photo | Performance stockage | Faible à moyenne |

### Confort
| Amélioration | Bénéfice | Difficulté |
| --- | --- | --- |
| Export Excel/Word | Livrables clients | Moyenne |
| Notifications PWA | Feedback offline | Moyenne |
| Mode sombre / thèmes | Confort visuel | Faible |

## 13. Dette technique

- Double pile fonctionnelle (legacy HTML + nouvelle stack) → maintenance doublée.
- Fichiers monolithiques (`template_sans_images.html`, `generer_pdf.py`) difficiles à faire évoluer.
- Dépendances non utilisées (`passlib`, `httpx`) présentes dans `requirements`.
- Upload photo sans validation stricte (taille, format, antivirus).
- Couverture de tests minimale.
- Dockerfiles basiques (pas de multi-stage, pas de healthcheck).
- Gestion d’erreurs perfectible dans le service photo/PDF.

## 14. Roadmap recommandée

### Version 2.0 – Industrialisation
- UI React complète (forms, upload, carte interactive).
- Authentification JWT + rôles (admin/lecteur).
- Passage à PostgreSQL + migrations Alembic soignées.
- Pipeline CI/CD (pytest + lint + build frontend).
- Docker multi-stage avec dépendances natives WeasyPrint.

### Version 3.0 – Collaboration
- Multi-utilisateurs avec mentions/commentaires.
- Synchronisation offline (React Query persist, service worker riche).
- Cartes avancées (dessin de zones, import KML/GPX).
- Webhooks et notifications (mail/push).

### Version 4.0 – Exports & IA
- Export Word/Excel basés sur modèles.
- Analyse automatique des photos (IA) pour catégoriser les anomalies.
- Application mobile (React Native / Capacitor).
- Tableau de bord analytique multi-projets.

---

## Dépannage rapide

| Problème | Cause probable | Solution |
| --- | --- | --- |
| `ModuleNotFoundError: app` pendant `pytest` | `PYTHONPATH` incomplet | Garder `backend/tests/conftest.py` qui injecte la racine dans `sys.path`. |
| `docker: command not found` | Docker Desktop/Engine absent | Installer Docker ou suivre le guide manuel. |
| `weasyprint` introuvable | Dépendances natives manquantes | Installer GTK/Cairo ou utiliser une image docker adaptée. |
| Images absentes dans les PDF | Chemins statiques non servis | Vérifier que `app.mount("/storage", StaticFiles(...))` est actif et que les fichiers existent. |
| Tâches invisibles dans le recap legacy | Champs vides | Remplir au moins un champ (description, coût ou durée) pour qu’elles apparaissent. |

Cette documentation est encodée en UTF-8 (sans BOM) et constitue la référence officielle pour la maintenance, l’onboarding et les futures évolutions du projet.
