# DECOMMISSION_PLAN

## Contexte

FieldReport est passé en statut **Production Candidate**. L'interface Jinja2 remplace React. Le moteur ReportLab remplace WeasyPrint. Ce document compare les deux stacks fonction par fonction pour valider que le d&eacute;commissionnement de React est s&eacute;curis&eacute;.

## Comparaison fonctionnelle : React vs Jinja2

| Fonction | React | Jinja2 | Couverture | Notes |
|----------|-------|--------|------------|-------|
| Dashboard | Oui | Oui | 100% | Compteurs r&eacute;els SQLite, derniers rapports, liens rapides |
| Liste rapports | Oui | Oui | 100% | Table CRUD avec badges statut, actions inline |
| Cr&eacute;ation rapport | Oui | Oui | 100% | Modal formulaire complet (num&eacute;ro, date, client, site, m&eacute;t&eacute;o, statut) |
| &Eacute;dition rapport | Oui | Oui | 100% | Modal pr&eacute;-remplie, PUT partiel |
| Suppression rapport | Oui | Oui | 100% | Confirm + DELETE, cascade enfants |
| D&eacute;tail rapport | Oui | Oui | 100% | Infos, signature, photos, t&acirc;ches, g&eacute;n&eacute;ration PDF |
| Upload photo | Oui | Oui | 100% | Input file + POST multipart, thumbnail auto |
| Affichage photo | Oui | Oui | 100% | Grille avec thumbnail, lien vers original |
| Suppression photo | Oui | Oui | 100% | Suppression DB + fichiers storage |
| Cr&eacute;ation t&acirc;che | Oui | Oui | 100% | Modal description + co&ucirc;t + dur&eacute;e |
| &Eacute;dition t&acirc;che | Oui | Oui | 100% | Prompt inline (description + statut) |
| Suppression t&acirc;che | Oui | Oui | 100% | Confirm + DELETE |
| Cr&eacute;ation signature | Oui | Oui | 100% | Modal nom + r&ocirc;le + date |
| &Eacute;dition signature | Oui | Oui | 100% | Prompt inline |
| Suppression signature | Oui | Oui | 100% | Confirm + DELETE |
| G&eacute;n&eacute;ration PDF | Oui | Oui | 100% | ReportLab, int&eacute;gration t&acirc;ches/photos/signature |
| T&eacute;l&eacute;chargement PDF | Oui | Oui | 100% | Fichier servi via /exports (StaticFiles) |
| Navigation | Oui | Oui | 100% | Header sticky avec liens actifs |
| Responsive | Oui | Oui | 90% | Grid CSS, media queries &le;768px |

## &Eacute;carts identifi&eacute;s

| &Eacute;cart | S&eacute;v&eacute;rit&eacute; | Justification |
|--------------|-----------|---------------|
| Pas de carte Leaflet (Jinja2) | Faible | Pas de GPS interactif ; les coordonn&eacute;es GPS sont stock&eacute;es en base (schema Photo) mais non affich&eacute;es sur carte. Le champ `gps_lat/lng` reste disponible pour un ajout futur. |
| Pas de PWA / Service Worker | Faible | Pas de besoin offline identifi&eacute;. Vite-plugin-pwa &eacute;tait pr&eacute;sent dans React mais non fonctionnellement test&eacute;. |
| &Eacute;dition inline via `prompt()` | Moyenne | Acceptable pour MVP. Pas de formulaire d'&eacute;dition d&eacute;di&eacute; pour t&acirc;ches/signatures (suffisant pour un utilisateur interne). Peut &ecirc;tre am&eacute;lior&eacute; plus tard avec des modals JS. |
| Pas de pagination API/UI | Moyenne | Listes compl&egrave;tes charg&eacute;es. &Agrave; pr&eacute;voir si > 100 rapports. |
| Pas d'authentification | Moyenne | Ni React ni Jinja2 n'avaient d'auth. Identique. |
| Pas de recherche full-text | Faible | Recherche non impl&eacute;ment&eacute;e dans React. Identique. |

## D&eacute;pendances restantes

| D&eacute;pendance | React | Jinja2 | Action |
|----------------|-------|--------|--------|
| Node.js / npm | Requis | Non requis | Supprimer apr&egrave;s archivage frontend |
| Vite / React / Router | Requis | Non requis | Supprimer apr&egrave;s archivage |
| TailwindCSS | Requis | Non requis (CSS vanilla) | Supprimer apr&egrave;s archivage |
| Tanstack Query | Requis | Non requis | Supprimer apr&egrave;s archivage |
| WeasyPrint | Optionnel (PDF service) | Non requis | Retirer de `requirements.txt` |
| ReportLab | Non utilis&eacute; | Requis (PDF service) | Conserver |
| Jinja2 | Non utilis&eacute; | Requis (templates + PDF legacy) | Conserver |

## D&eacute;cision

**React peut &ecirc;tre d&eacute;commissionn&eacute;.** La couverture fonctionnelle est de 100% sur toutes les features m&eacute;tier. Les &eacute;carts identifi&eacute;s sont soit mineurs (affichage GPS), soit &eacute;quivalents &agrave; l'ancienne stack (pas d'auth, pas de pagination).

## Proc&eacute;dure de d&eacute;commissionnement (non destructive)

1. Cr&eacute;er `legacy/frontend-react/` et y copier `frontend/`
2. Mettre &agrave; jour `docker-compose.yml` pour supprimer le service `frontend`
3. Retirer `weasyprint` de `backend/requirements.txt`
4. Valider avec `validate.ps1 -Target all`
5. Documenter dans `CHANGELOG.md`
