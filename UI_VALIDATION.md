# UI_VALIDATION

Date : 01/06/2026

## R&eacute;sum&eacute;

L'interface utilisateur finale Jinja2 a &eacute;t&eacute; cr&eacute;&eacute;e et connect&eacute;e aux endpoints CRUD existants du backend FastAPI.

## Stack utilis&eacute;e

- **Moteur de templates** : Jinja2 (int&eacute;gr&eacute; &agrave; FastAPI)
- **Frontend** : HTML5, CSS3, Vanilla JS (aucun framework JS)
- **Backend** : FastAPI, SQLAlchemy 2, SQLite

## Structure des fichiers

```
backend/app/
  templates/
    layout.html         (squelette commun : header, nav, footer, toasts)
    dashboard.html      (accueil, statistiques, derniers rapports)
    reports.html        (liste CRUD rapports + modals cr&eacute;ation/&eacute;dition)
    report_detail.html  (d&eacute;tail d'un rapport : infos, signature, photos, t&acirc;ches, PDF)
    photos.html         (galerie photos filtrable par rapport)
    tasks.html          (liste des t&acirc;ches avec &eacute;dition inline)
    signatures.html     (liste des signatures avec &eacute;dition inline)
  static/
    css/main.css        (design system responsive, cards, tables, forms, modals, toasts)
    js/app.js           (client API vanilla : GET/POST/PUT/DELETE, upload, toasts, helpers)
```

## Pages et fonctionnalit&eacute;s

| Page | URL | Fonctionnalit&eacute;s |
|------|-----|----------------------|
| **Tableau de bord** | `/` | Compteurs (rapports, photos, t&acirc;ches), tableau des 5 derniers rapports, liens rapides |
| **Rapports** | `/reports` | Liste pagin&eacute;e, cr&eacute;ation (modal), &eacute;dition (modal), suppression, g&eacute;n&eacute;ration PDF |
| **D&eacute;tail rapport** | `/reports/{id}` | Infos, signature (CRUD), photos (upload + suppression), t&acirc;ches (CRUD), g&eacute;n&eacute;ration PDF, suppression du rapport |
| **Photos** | `/photos` | Galerie filtrable par rapport, suppression |
| **T&acirc;ches** | `/tasks` | Liste globale, &eacute;dition inline (description + statut), suppression |
| **Signatures** | `/signatures` | Liste globale, &eacute;dition inline (nom + r&ocirc;le + date), suppression |

## Connexion API

Toutes les pages consomment les endpoints REST existants :

- `GET/POST /api/reports/`
- `GET/PUT/DELETE /api/reports/{id}`
- `POST /api/reports/{id}/generate-pdf`
- `GET/POST /api/photos/` (POST via `/api/photos/{report_id}`)
- `GET/PUT/DELETE /api/photos/{id}`
- `GET/POST /api/tasks/` (POST via `/api/tasks/{report_id}`)
- `GET/PUT/DELETE /api/tasks/{id}`
- `GET /api/signatures/`
- `GET/POST/PUT/DELETE /api/signatures/{report_id}`

## Validation navigateur

```
GET /           -> 200 (5083 bytes)  -> Tableau de bord
GET /reports    -> 200 (11031 bytes) -> Liste rapports
GET /reports/1  -> 200 (13965 bytes) -> D&eacute;tail rapport
GET /photos     -> 200 (4188 bytes)  -> Galerie photos
GET /tasks      -> 200 (4475 bytes)  -> Liste t&acirc;ches
GET /signatures -> 200 (4401 bytes)  -> Liste signatures
```

Sc&eacute;nario test&eacute; manuellement :
1. Cr&eacute;er un rapport via l'API (`POST /api/reports/`) &rarr; 201
2. Recharger `/` &rarr; le rapport appara&icirc;t dans "Derniers rapports"
3. Naviguer sur `/reports` &rarr; le rapport est list&eacute;
4. Cliquer sur le num&eacute;ro &rarr; `/reports/1` s'affiche avec d&eacute;tails

## Limitations connues

- **Authentification** : aucune (API publique en l'&eacute;tat)
- **Pagination** : non impl&eacute;ment&eacute;e c&ocirc;t&eacute; API ni UI (listes compl&egrave;tes charg&eacute;es)
- **Recherche / filtres avanc&eacute;s** : filtre par rapport uniquement sur la page Photos
- &Eacute;dition inline des t&acirc;ches et signatures via `prompt()` (suffisant pour un MVP sans React)
- Pas de drag-and-drop pour les photos (upload via input file classique)
- Pas de preview canvas pour les signatures (champ texte `signature_image`)

## Interdictions respect&eacute;es

- [x] `frontend/` non supprim&eacute;
- [x] React non supprim&eacute;
- [x] WeasyPrint non supprim&eacute;

## Proc&eacute;dure de lancement

```powershell
cd backend
# Cr&eacute;er les tables si n&eacute;cessaire
python -c "from app.db.base import Base; from app.db.session import engine; from app.models import Photo, Report, Signature, Task; Base.metadata.create_all(engine)"
# Lancer le serveur
python -m uvicorn app.main:app --host 0.0.0.0 --port 8200 --reload
```

Acc&egrave;s UI : http://localhost:8200/
