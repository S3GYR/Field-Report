# CLEANUP_PLAN

## Principe

Aucune suppression pendant cette mission. Chaque &eacute;l&eacute;ment est class&eacute; selon 3 cat&eacute;gories avec justification, impact et risque.

---

## &Agrave; conserver

| &Eacute;l&eacute;ment | Justification | Impact | Risque |
|----------------|---------------|--------|--------|
| `backend/app/` | Application FastAPI production. Contient API, mod&egrave;les, services, templates, static. | Critique | Aucun |
| `backend/tests/` | Tests pytest valid&eacute;s (21 passed API, UI fonctionnelle). | Critique | Aucun |
| `backend/requirements.txt` (sans weasyprint) | D&eacute;pendances Python minimales. | Critique | N&eacute;cessite &eacute;dition pour retirer weasyprint |
| `backend/Dockerfile` | Image Docker backend valid&eacute;e. | Critique | Aucun |
| `backend/alembic/` | Migrations SQLAlchemy (m&ecirc;me si init manuel suffit). | Faible | Peut &ecirc;tre utilis&eacute; pour schema evolution |
| `field-report/legacy/generer_pdf.py` | Moteur PDF legacy ReportLab. R&eacute;f&eacute;rence valid&eacute;e. | Faible | Document historique |
| `scripts/validate_*.py` | Scripts de validation automatis&eacute;s. | Moyen | Aucun |
| `validate.ps1` | Point d'entr&eacute;e validation PowerShell. | Moyen | Aucun |
| `storage/` | Donn&eacute;es SQLite + photos + exports PDF. | Critique | Backup obligatoire avant toute op&eacute;ration |
| `.git/` | Historique source. | Critique | Aucun |
| `README_PRODUCTION.md` (ce doc) | Documentation production. | Moyen | Aucun |
| `UI_FUNCTIONAL_VALIDATION.md` | Preuve de validation UI. | Moyen | Aucun |
| `END_TO_END_VALIDATION.md` | Preuve E2E. | Moyen | Aucun |
| `API_VALIDATION.md` | Preuve API. | Moyen | Aucun |

---

## &Agrave; archiver

| &Eacute;l&eacute;ment | Destination | Justification | Impact | Risque |
|----------------|-------------|---------------|--------|--------|
| `frontend/` | `legacy/frontend-react/` | Application React compl&egrave;te. Plus servie mais code r&eacute;utilisable si rollback. | Faible | N&eacute;cessite Node.js pour rebuild ; node_modules est r&eacute;g&eacute;n&eacute;rable |
| `frontend/node_modules/` | `legacy/frontend-react/node_modules/` | D&eacute;pendances npm (275MB+). R&eacute;g&eacute;n&eacute;rables via `npm install`. | Faible | Peut &ecirc;tre exclu de l'archive pour gagner de la place |
| `docker-compose.yml` (actuel) | `legacy/docker-compose-legacy.yml` | Inclut service frontend. Nouveau compose sans frontend &agrave; cr&eacute;er. | Faible | Le nouveau compose doit monter les m&ecirc;mes volumes |
| `field-report/pdf.py` | `legacy/field-report-pdf-weasyprint.py` | Ancien service PDF WeasyPrint. ReportLab le remplace. | N&eacute;gligeable | Aucun si ReportLab valid&eacute; |
| `backend/app/services/pdf_service.py` (avant modif) | `legacy/pdf_service_weasyprint.py` | Version WeasyPrint du service. | N&eacute;gligeable | Version ReportLab est fonctionnelle |
| `backend/app/pdf/` (templates HTML) | `legacy/pdf-templates-weasyprint/` | Templates Jinja2 pour WeasyPrint. ReportLab ne les utilise pas. | N&eacute;gligeable | ReportLab g&eacute;n&egrave;re le HTML/PDF nativement |
| Documentation legacy (REFACTOR_SPEC, ARCHITECTURE_AUDIT, etc.) | `legacy/docs/` | Documents de planification de la migration. | N&eacute;gligeable | Aucun |

---

## &Agrave; supprimer (apr&egrave;s validation du plan)

| &Eacute;l&eacute;ment | Justification | Impact | Risque |
|----------------|---------------|--------|--------|
| `weasyprint==62.3` dans `requirements.txt` | Biblioth&egrave;que non utilis&eacute;e. R&eacute;duit la taille de l'image Docker. | Faible | S'assurer que ReportLab est install&eacute; |
| `frontend/Dockerfile` | Inutile si frontend archiv&eacute;. | Faible | Aucun |
| `frontend/vite.config.ts` | Build tool React. | N&eacute;gligeable | Aucun |
| `frontend/tsconfig*.json` | TypeScript config. | N&eacute;gligeable | Aucun |
| `.venv/` (si pr&eacute;sent) | Virtual env local. Ne pas versionner. | N&eacute;gligeable | Aucun si `.gitignore` correct |
| `__pycache__/` (racine) | Cache Python. | N&eacute;gligeable | Aucun si `.gitignore` correct |
| `debug_pdf.log` | Log de debug. | N&eacute;gligeable | Aucun |

---

## Proc&eacute;dure d'archivage (non destructive)

```bash
# 1. Cr&eacute;er le r&eacute;pertoire legacy
mkdir -p legacy

# 2. Archiver frontend React
mv frontend legacy/frontend-react

# 3. Archiver docker-compose legacy
cp docker-compose.yml legacy/docker-compose-legacy.yml

# 4. Cr&eacute;er le nouveau docker-compose (sans frontend)
cat > docker-compose.yml << 'EOF'
version: "3.9"
services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    container_name: report-backend
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8200"]
    environment:
      - DATABASE_URL=sqlite:///./storage/reports.db
    volumes:
      - ./storage:/app/backend/storage
    ports:
      - "8200:8200"
EOF

# 5. Nettoyer requirements.txt
sed -i '/weasyprint/d' backend/requirements.txt

# 6. Valider
validate.ps1 -Target all
```

---

## Checklist avant suppression d&e;finitive

- [ ] `legacy/frontend-react/` cr&eacute;&eacute; et contient l'int&eacute;gralit&eacute; de `frontend/`
- [ ] `docker-compose.yml` sans service `frontend` test&eacute; (`docker compose up -d`)
- [ ] `backend/requirements.txt` sans `weasyprint` test&eacute; (`pip install -r requirements.txt`)
- [ ] `validate.ps1 -Target all` passe (all green)
- [ ] Backup `storage/` r&eacute;alis&eacute;
- [ ] `README_PRODUCTION.md` mis &agrave; jour
