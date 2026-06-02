# WEASYPRINT_DECOMMISSION_REPORT

FieldReport v1.0.1 — Retrait de WeasyPrint
Date : 2026-06-01

---

## Analyse préalable

### Recherche des références WeasyPrint dans le code source

```bash
grep -ri "weasyprint" backend/
```

**Résultat** :

- `backend/requirements.txt` : `weasyprint==62.3` (1 occurrence)
- Aucune occurrence dans les fichiers Python du backend

### Conclusion de l'analyse

WeasyPrint n'est **plus utilisé** dans le code source. La génération PDF est assurée par **ReportLab** (`backend/app/services/pdf_service.py`).

---

## Actions réalisées

### 1. Retrait de la dépendance

**Fichier** : `backend/requirements.txt`

**Avant** :

```
jinja2==3.1.4
weasyprint==62.3
httpx==0.27.0
```

**Après** :

```
jinja2==3.1.4
reportlab==4.4.0
pillow==10.3.0
httpx==0.27.0
```

### 2. Dépendances conservées

| Dépendance | Rôle | Justification |
|------------|------|---------------|
| `reportlab==4.4.0` | Génération PDF | Utilisé activement dans `pdf_service.py` |
| `pillow==10.3.0` | Manipulation d'images | Requis par ReportLab et le stockage photo |

---

## Risques éventuels

| Risque | Probabilité | Mitigation |
|--------|-------------|------------|
| Build Docker cassé si WeasyPrint fournissait des libs système implicites | Faible | Les libs système nécessaires (`libjpeg`, `zlib`) sont explicitement installées dans le Dockerfile |
| Documentation obsolète mentionnant WeasyPrint | Haute | Les documents historiques (.md) mentionnent encore WeasyPrint. Ils sont conservés à des fins d'audit. Le `README_PRODUCTION.md` sera mis à jour lors du merge vers `main`. |

---

## Vérification post-suppression

```bash
python -c "from app.main import create_app; app = create_app(); print('APP_OK')"
```

**Résultat** : `APP_OK` — L'application démarre correctement sans WeasyPrint.

```bash
pytest backend/tests/ -q
```

**Résultat** : `21 passed` — Tous les tests passent.

---

## Conclusion

WeasyPrint a été retiré sans impact fonctionnel. ReportLab et Pillow assurent la génération PDF et le traitement des photos. L'image Docker est allégée et les dépendances sont cohérentes avec le code source.
