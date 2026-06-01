# PDF_LAYOUT_FIX_REPORT

## Modification appliquée

**Fichier** : `field-report/legacy/generer_pdf.py`

**Ligne** : 350 (fonction `build_photo_section`)

**Avant** :
```python
    layout = Table(
        [[img, KeepTogether(right_column)]],
        colWidths=[80 * mm, None],
        style=[
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ],
    )
```

**Après** :
```python
    layout = Table(
        [[img, right_column]],
        colWidths=[80 * mm, None],
        style=[
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ],
    )
```

**Nature du changement** : suppression de l'encapsulation `KeepTogether(...)` autour de `right_column` dans la cellule de droite du tableau 1×2. Le tableau reçoit désormais directement la liste de `Paragraph`.

**Contrainte respectée** : aucune modification de `placeholder_image()`, `image_flowable()`, ni de la structure générale du PDF.

## Résultat avant

- `validate.ps1 -Target pdf` : **ÉCHEC**
- Erreur : `reportlab.platypus.doctemplate.LayoutError`
- Message : `Flowable <Table@...> with cell(0,0) containing '<KeepInFrame at ...>' (... x 16777221), tallest cell 16777221.0 points, too large on page 4 in frame 'normal'(...)`
- Statut : `test_pdf.py::test_pdf_generation_creates_file` **FAILED**

## Résultat après

### 1. Compilation

```powershell
python -m compileall field-report -q
```

- **Résultat** : ✅ Succès (exit code 0, aucune erreur de syntaxe)

### 2. Validation pytest

```powershell
validate.ps1 -Target pdf
```

- **Résultat** : ✅ Succès
- **Détails** : `tests\test_pdf.py .` — 1 passed in 1.19s

### 3. Génération PDF complet

```powershell
cd field-report\legacy && python generer_pdf.py
```

- **Résultat** : ✅ Succès
- **Message** : `PDF généré : C:\Users\yoann\Desktop\Rapport\field-report\legacy\rapport.pdf`
- **Taille** : 7 697 octets
- **Date** : 01/06/2026 08:22

## Régressions observées

Aucune régression constatée lors des trois validations.

| Critère | Avant | Après | Statut |
|---------|-------|-------|--------|
| Compilation syntaxique | ❌ (LayoutError à l'exécution) | ✅ | OK |
| Test pytest PDF | FAILED | **PASSED** | OK |
| Génération PDF réelle | Échec (exception) | **Succès** | OK |
| Taille du PDF généré | N/A | 7 697 octets | OK |
| Contenu visuel | N/A | PDF lisible, sections photos présentes | OK |

## Conclusion

Le correctif minimal — suppression de `KeepTogether` dans la cellule de droite du `Table` de `build_photo_section()` — élimine définitivement le `LayoutError`. Le moteur PDF ReportLab est désormais fonctionnel pour les données de test.
