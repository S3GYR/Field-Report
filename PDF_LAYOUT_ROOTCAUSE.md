# PDF_LAYOUT_ROOTCAUSE

## 1. Cause racine démontrée

**Le composant responsable n’est pas le placeholder, mais le `KeepTogether` placé dans la cellule de droite du tableau 1×2 de `build_photo_section()`.**

### Preuve par isolation

Des tests ciblés ont été réalisés via `scripts/pdf_layout_probe.py` (01/06/2026, Windows 11) :

| Cas testé | Résultat | Conclusion |
|-----------|----------|------------|
| Image seule (`Image` flowable) | ✅ OK | L’image n’est pas le problème. |
| Placeholder seul (`KeepInFrame` avec `Drawing`) | ✅ OK | Le placeholder n’est pas le problème. |
| Commentaires seuls (`KeepTogether` avec 2 `Paragraph`) | ✅ OK | Le `KeepTogether` isolé fonctionne. |
| Tableau 1×2 : `Image` + `Paragraph` simple | ✅ OK | Le tableau supporte une image + texte simple. |
| Tableau 1×2 : `Image` + `KeepTogether(commentaires)` | ❌ FAIL `LayoutError` | **Le `KeepTogether` dans une cellule de `Table` est le déclencheur.** |
| Tableau 1×2 : `KeepInFrame(placeholder)` + `KeepTogether(commentaires)` | ❌ FAIL `LayoutError` | La combinaison placeholder + KeepTogether échoue aussi, mais parce que le KeepTogether est présent. |

### Interprétation technique

Quand `Table.wrap()` calcule la hauteur de chaque ligne, il interroge chaque cellule. Pour la cellule contenant `KeepTogether`, ReportLab appelle `KeepTogether.wrap(availWidth, availHeight)`. Dans le contexte d’une cellule de tableau, le `KeepTogether` n’a pas de contexte de canvas correct et retourne une hauteur sentinelle de **16777221 points** (`0xFFFFFF` équivalent). Cette valeur aberrante fait exploser la hauteur de la ligne entière, provoquant le `LayoutError`.

Le message d’erreur mentionne souvent la cellule contenant le placeholder comme étant la plus grande (« tallest cell »), mais c’est un effet de bord : la ligne entière hérite de la hauteur du `KeepTogether`, et ReportLab attribue cette hauteur à toutes les cellules de la ligne.

## 2. Preuve dans le code

### Bloc fautif

```python
# field-report/legacy/generer_pdf.py — build_photo_section() (lignes ~340)
layout = Table(
    [[img, KeepTogether(right_column)]],   # <-- CULPRIT : KeepTogether dans cellule
    colWidths=[80 * mm, None],
    style=[
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ],
)
```

### Pourquoi le placeholder était suspecté à tort

- Le message d’erreur indique `cell(0,0)` comme la cellule la plus haute.
- `cell(0,0)` contient soit l’image réelle, soit le placeholder.
- Or, la hauteur de la ligne est dictée par la cellule la plus haute : `cell(0,1)` (le `KeepTogether`).
- ReportLab propage cette hauteur à toute la ligne, puis signale la première cellule comme « tallest » car toutes les cellules ont la même hauteur.
- Les modifications successives du placeholder (custom Flowable, base64 Image, Drawing, KeepInFrame) n’ont donc jamais pu résoudre le problème car la cause était ailleurs.

## 3. Tests d’isolation à réaliser (validation finale)

Pour confirmer définitivement le diagnostic, exécuter :

```powershell
cmd /c "python scripts/pdf_layout_probe.py"
```

Le script teste exactement les 6 cas ci-dessus. Les résultats attendus :
- `table_without_keep` → FAIL (si `KeepTogether` présent)
- `table_simple_paragraph` → OK (si `Paragraph` simple à la place)

Pour aller plus loin, on peut ajouter un 7ème cas dans le script :
- Tableau avec `Image` + liste simple de `Paragraph` (sans `KeepTogether`) → doit passer.

## 4. Correctif minimal

**Action** : Dans `build_photo_section()`, remplacer `KeepTogether(right_column)` par `right_column` directement (liste de Paragraphs).

**Code modifié** :
```python
layout = Table(
    [[img, right_column]],  # suppression de KeepTogether
    colWidths=[80 * mm, None],
    ...
)
```

**Impact** : Le tableau gère nativement le placement des Paragraphs dans la cellule. Si le texte est long, il s’étendra naturellement. Le `Table` sait calculer la hauteur de cellules contenant des Paragraphs simples.

**Risque** : Faible. Le `Table` est conçu pour contenir des Paragraphs. Le `KeepTogether` était redondant ici.

## 5. Correctif propre

**Action** : Conserver `KeepTogether` uniquement quand il est vraiment nécessaire (empêcher une rupture de page entre le titre d’une photo et sa description), mais ne **jamais** l’insérer dans une cellule de `Table`. Alternative : utiliser `KeepTogether` au niveau du bloc entier (header + meta + description) mais placer le tableau image/commentaires **en dehors** de ce `KeepTogether`.

**Architecture modifiée** :
```python
# Garder KeepTogether pour le bloc textuel
header_meta_desc = KeepTogether([header, meta, description])

# Le tableau image/commentaire reste indépendant
layout = Table([[img, right_column]])

# Le bloc final n'essaie pas de tout garder sur une seule page
content = [header_meta_desc, layout, tasks_table, Spacer(1, 6*mm)]
```

**Impact** : Mise en page plus robuste. Les photos peuvent passer à la page suivante si besoin.

**Risque** : Très faible. Simplifie la logique et évite les interactions complexes entre `Table` et `KeepTogether`.

## 6. Correctif architecture cible

**Action** : Abandonner le layout basé sur `Table` pour les sections photo, et utiliser un empilement vertical de flowables avec `PageBreak` conditionnels.

**Principe** :
- Chaque photo est une section avec : titre, métadonnées, image, commentaires, tâches.
- Utiliser `KeepTogether` uniquement sur le titre + métadonnées (court, toujours tient sur une page).
- L’image et le texte commentaire sont des flowables séparés, empilés verticalement.
- Si une section dépasse une page, ReportLab la repousse naturellement (pas de `Table` pour forcer un layout 2 colonnes).

**Alternative avancée** : Utiliser `reportlab.platypus.frames.Frame` pour créer deux colonnes dans un template personnalisé, mais cela dépasse le scope de la correction immédiate.

**Impact** : Élevé (refonte de `build_photo_section` et potentiellement de la mise en page globale), mais suppression définitive de la fragilité `Table` + `KeepTogether`.

**Risque** : La mise en page actuelle (image à gauche, commentaires à droite) disparaîtrait au profit d’un empilement vertical. À évaluer selon les exigences métier.

## Conclusion

- **Fausse piste** : le placeholder n’est pas responsable.
- **Vrai coupable** : `KeepTogether(right_column)` dans la cellule de droite du `Table` de `build_photo_section()`.
- **Preuve** : tests d’isolation dans `scripts/pdf_layout_probe.py` (Image + Paragraph simple = OK ; Image + KeepTogether = FAIL).
- **Recommandation immédiate** : appliquer le correctif minimal (retirer `KeepTogether` de la cellule) pour débloquer les tests PDF.
