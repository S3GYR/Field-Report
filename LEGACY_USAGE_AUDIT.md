# LEGACY_USAGE_AUDIT

## Objectif

Identifier pr&eacute;cis&eacute;ment quelles parties du code utilisent encore React et WeasyPrint, et quelles d&eacute;pendances sont devenues obsol&egrave;tes.

---

## 1. React — Utilisation actuelle

### 1.1 Arborescence `frontend/`

```
frontend/
  Dockerfile              -> Build image Node + Vite
  package.json            -> D&eacute;pendances React, Router, Query, Leaflet
  vite.config.ts          -> Config Vite + plugin React + PWA
  tsconfig.json           -> TypeScript React
  public/                 -> Assets statiques
  src/
    App.tsx               -> Root component React Router
    main.tsx              -> Entry point ReactDOM
    components/           -> Composants UI React
    pages/                -> Pages Dashboard, Reports, etc.
    hooks/                -> Hooks React Query
    services/             -> Client API Axios/fetch
    types/                -> D&eacute;finitions TypeScript
```

**Constat** : `frontend/` est une application React SPA compl&egrave;te. Elle n'est plus servie par le backend. Le backend FastAPI sert d&eacute;sormais les templates Jinja2 &agrave; la racine `/`.

### 1.2 R&eacute;f&eacute;rences React dans le backend

| Fichier | Ligne | Contenu | Impact |
|---------|-------|---------|--------|
| `docker-compose.yml` | 17–28 | Service `frontend` avec build Dockerfile + port 3200 | D&eacute;marrage Docker inclut encore React |
| `backend/requirements.txt` | aucune | Python ne d&eacute;pend pas de React | Aucun |

**Constat** : Aucune d&eacute;pendance runtime Python &agrave; React. Seul `docker-compose.yml` r&eacute;f&eacute;rence le service frontend.

### 1.3 R&eacute;f&eacute;rences React dans la documentation

| Fichier | Mentions | Contexte |
|---------|----------|----------|
| `README_NEW_UTF8.md` | 22 | Architecture legacy d&eacute;crite (React+Vite) |
| `REFACTOR_SPEC.md` | 35 | Spec originale mentionnant React |
| `ARCHITECTURE_AUDIT.md` | 16 | Audit d'architecture legacy |
| `PROJECT_MAP.md` | 13 | Mapping projet legacy |
| `MIGRATION_PLAN.md` | 6 | Plan de migration depuis React |
| `UI_VALIDATION.md` | 4 | Notes sur l'UI legacy |

**Constat** : Documentation historique &agrave; archiver, pas de r&eacute;f&eacute;rence fonctionnelle active.

---

## 2. WeasyPrint — Utilisation actuelle

### 2.1 Code Python

| Fichier | Ligne | Contenu | Statut |
|---------|-------|---------|--------|
| `backend/requirements.txt` | 10 | `weasyprint==62.3` | **Inutilis&eacute;** — remplac&eacute; par ReportLab |
| `backend/app/services/pdf_service.py` | ancien | Import `weasyprint.HTML` | **Remplac&eacute;** — r&eacute;&eacute;crit avec ReportLab |

**Constat** : WeasyPrint est import&eacute; dans `requirements.txt` mais le code l'utilisant a &eacute;t&eacute; r&eacute;&eacute;crit avec ReportLab. Le backend g&eacute;n&egrave;re des PDF via ReportLab (`reportlab.platypus`).

### 2.2 Documentation

| Fichier | Mentions | Contexte |
|---------|----------|----------|
| `PDF_COMPARISON.md` | 3 | Comparaison WeasyPrint vs ReportLab |
| `PDF_IMPORT_ANALYSIS.md` | 1 | Analyse des imports |
| `ARCHITECTURE_AUDIT.md` | 7 | Audit legacy |
| `README_NEW_UTF8.md` | 11 | Architecture legacy |
| `REFACTOR_SPEC.md` | 11 | Spec legacy |

**Constat** : Historique d'audit. WeasyPrint n'est plus dans le code fonctionnel.

---

## 3. D&eacute;pendances obsol&egrave;tes

| D&eacute;pendance | Fichier | Statut | Action |
|----------------|---------|--------|--------|
| `weasyprint==62.3` | `requirements.txt` | Inutilis&eacute;e | Retirer |
| `jinja2==3.1.4` | `requirements.txt` | Utilis&eacute;e (templates FastAPI) | **Conserver** |
| `react`, `react-dom` | `frontend/package.json` | UI legacy | Archiver avec frontend |
| `react-router-dom` | `frontend/package.json` | Routing legacy | Archiver |
| `@tanstack/react-query` | `frontend/package.json` | Data fetching legacy | Archiver |
| `leaflet` | `frontend/package.json` | Carte legacy | Archiver |
| `vite`, `@vitejs/plugin-react` | `frontend/package.json` | Build legacy | Archiver |
| `tailwindcss` | `frontend/package.json` | Styling legacy | Archiver |

---

## 4. Points d'entrée actifs

| Point d'entr&eacute;e | Stack | Statut |
|----------------------|-------|--------|
| `docker compose up` | Backend + Frontend | Frontend obsol&egrave;te |
| `uvicorn app.main:app` | Backend seul | **Recommand&eacute;** |
| `npm run dev` (frontend/) | React dev server | Obsol&egrave;te |
| `/` (port 8200) | Jinja2 dashboard | **Actif** |
| `/api/*` (port 8200) | FastAPI CRUD | **Actif** |

---

## 5. Synth&egrave;se

- **React** : isol&eacute; dans `frontend/`. Aucun impact runtime sur le backend. Seul `docker-compose.yml` le r&eacute;f&eacute;rence encore.
- **WeasyPrint** : r&eacute;f&eacute;renc&eacute; dans `requirements.txt` mais plus utilis&eacute; par le code. Le PDF service utilise ReportLab.
- **node_modules/** : peut &ecirc;tre supprim&eacute; apr&egrave;s archivage (r&eacute;g&eacute;n&eacute;rable via `npm install`).
