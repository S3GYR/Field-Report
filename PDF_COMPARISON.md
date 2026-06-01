# PDF_COMPARISON

Comparer ReportLab (`field-report/pdf.py` → `generer_pdf.py`) vs WeasyPrint (`backend/app/services/pdf_service.py`). Aucun résultat n’a été inventé ; ce template attend des mesures réelles.

| Critère | ReportLab | WeasyPrint | Notes |
| --- | --- | --- | --- |
| Taille fichier | NON TESTÉ | NON TESTÉ | Pytest stoppé : `generer_pdf.py` → `SyntaxError` (parenthèse ligne 509). |
| Temps génération | NON TESTÉ | NON TESTÉ | Collecte interrompue (erreur import ReportLab). |
| Qualité visuelle | NON TESTÉ | NON TESTÉ | Données non générées (erreur Python). |
| Pagination | NON TESTÉ | NON TESTÉ | Données non générées. |
| Images/photos | NON TESTÉ | NON TESTÉ | Données non générées. |
| GPS / métadonnées | NON TESTÉ | NON TESTÉ | Données non générées. |
| Tableaux tâches | NON TESTÉ | NON TESTÉ | Données non générées. |
| Signatures | NON TESTÉ | NON TESTÉ | Données non générées. |

## Procédure recommandée

1. Générer un rapport identique via endpoint WeasyPrint (`POST /api/reports/{id}/generate-pdf`).
2. Générer le même rapport via `PdfBuilder.build(...)` (ReportLab) avec données extraites du même rapport.
3. Mesurer taille (`ls -lh`), temps (`/usr/bin/time`, `Measure-Command` ou instrumentation interne), vérifier visuellement.
4. Remplir le tableau ci-dessus + consigner les chemins fichiers (ex : `storage/exports/report-wp.pdf`, `storage/exports/report-rl.pdf`).

> Marquer explicitement `NON TESTÉ` tant que les mesures n’ont pas été collectées.
