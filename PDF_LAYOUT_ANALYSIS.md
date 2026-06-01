# PDF_LAYOUT_ANALYSIS

## 1. Cause exacte

- Le `LayoutError` provient du tableau 1x2 construit dans `build_photo_section()` @field-report/legacy/generer_pdf.py#332-345.
- La cellule (0,0) contient la table de remplacement produite par `placeholder_image()` @field-report/legacy/generer_pdf.py#507-522 (texte "Image indisponible").
- Ce tableau est inclus dans un `KeepTogether(content)` qui rend l’ensemble du bloc photo (en-tête, description, image, tableau des tâches) indivisible.
- Lorsque les tests sont exécutés sans fichiers photo réels (données `SAMPLE_DATA` dans `tests/test_pdf.py`), `image_flowable()` ne trouve aucun fichier/base64 et retourne la table de placeholder.
- Le bloc complet dépasse alors l’espace restant dans le frame `normal` de la page 4 (g gabarit "Later"). ReportLab tente de mesurer le tableau imbriqué, calcule une hauteur sentinelle (`16777221 pt`) et lève `LayoutError` car l’ensemble ne peut ni se scinder ni tenir dans une page.

## 2. Fonction concernée

- `build_photo_section()` : construit le `KeepTogether` et le tableau 1x2 (image + colonne de texte).
- `placeholder_image()` : crée la table interne 1x1 utilisée quand aucune image n’est disponible.

## 3. Données responsables

- `tests/test_pdf.py::SAMPLE_DATA` fournit une photo sans `image_path`, sans `image_b64` et sans fichier réel nommé `Photo_001.jpg`.
- `image_flowable()` échoue à ouvrir la ressource et utilise systématiquement le placeholder (`Table(... rowHeights=[60 * mm])`).
- Avec un vrai fichier ou un base64 valide, le `Image` ReportLab retournerait une hauteur finie et le bloc complet resterait en dessous des 716 pt disponibles; le cas de test amplifie l’erreur car tout repose sur le placeholder.

## 4. Pourquoi WeasyPrint n’est pas touché

- Le pipeline WeasyPrint (`backend/app/services/pdf_service.py`) génère un HTML/CSS paginé automatiquement. Les images manquantes sont rendues via `<img>` avec texte alternatif ou blocs auto-ajustés.
- HTML/CSS gère la pagination dynamiquement (pas de `KeepTogether` rigide), donc un bloc trop long est naturellement repoussé sur la page suivante sans provoquer d’exception.

## 5. Solutions possibles

### Correction A — Réduire le placeholder

- **Idée** : remplacer la table de placeholder par un `Spacer` ou un `Flowable` léger (ex. dessin vectoriel) avec `allowSplitting=1` pour garantir une hauteur calculable.
- **Impact** : localisé (uniquement quand l’image est absente). Mise en page quasi identique.
- **Difficulté** : faible (quelques lignes dans `placeholder_image()` / `image_flowable()`).
- **Risque** : faible ; seul le rendu d’une photo manquante change, aucun effet si les images existent.

### Correction B — Assouplir `KeepTogether`

- **Idée** : retirer `KeepTogether(content)` ou limiter son périmètre (ex. l’appliquer uniquement au titre + métadonnées, laisser le tableau image/texte et les tâches se fractionner). Eventuellement forcer un `FrameBreak` avant chaque photo.
- **Impact** : moyenne. Autorise ReportLab à répartir un bloc photo sur deux pages au lieu de lever une exception.
- **Difficulté** : moyenne (tester plusieurs combinaisons pour préserver une mise en page agréable).
- **Risque** : moyen ; la mise en page peut paraître moins compacte (image en bas d’une page, légende en haut de la suivante), mais les tests ne planteront plus.

### Correction C — Alignement architecture cible

- **Idée** : migrer la génération PDF legacy vers la même chaîne que l’API (WeasyPrint ou un service ReportLab refactorisé) et ne garder `generer_pdf.py` que comme script autonome optionnel.
- **Impact** : élevé (rationalisation complète, disparition des placeholders rigides, homogénéité avec l’API).
- **Difficulté** : élevée (refonte fonctionnelle, reprise des styles, ajout de tests d’intégration).
- **Risque** : élevé ; nécessite une validation approfondie avant de retirer le générateur legacy actuel.
