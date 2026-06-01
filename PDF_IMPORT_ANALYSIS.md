# PDF_IMPORT_ANALYSIS

## Structure réelle des chemins

- `c:/Users/yoann/Desktop/Rapport/` (racine dépôt)
  - `generer_pdf.py` ← générateur ReportLab historique (fichier autonome à la racine).
  - `field-report/` (package utilitaire non standard, accessible via `sys.path.insert`)
    - `pdf.py` ← wrapper `PdfBuilder` qui importe `generer_pdf`.
  - `scripts/` ← contient `validate_pdf.py` exécuté par `validate.ps1`.
  - `tests/` ← les tests, dont `tests/test_pdf.py`, injectent `field-report/` dans `sys.path` pour importer `pdf.py`.

## Import actuel

- Dans `field-report/pdf.py` :

  ```python
  from generer_pdf import generate_pdf as legacy_generate_pdf
  ```

- Il s'agit d’un import absolu supposant que `generer_pdf.py` est trouvable via `sys.path` (dans l’un des répertoires listés).

## Répertoire de lancement des tests

- La commande de validation (`powershell ./validate.ps1 -Target pdf`) exécute `python scripts/validate_pdf.py`.
- Lorsqu’un script est lancé ainsi, **Python ajoute `c:/Users/yoann/Desktop/Rapport/scripts` en tête de `sys.path`** (et non la racine du dépôt).
- `tests/test_pdf.py` ajoute `field-report/` à `sys.path`, mais **n’ajoute jamais la racine du dépôt**.
- Résultat : le dossier contenant `generer_pdf.py` (`Rapport/`) n’est pas dans `sys.path` pendant l’import → `ModuleNotFoundError: No module named 'generer_pdf'`.

## Import recommandé

- Ajouter explicitement la racine du projet (`ROOT_DIR = Path(__file__).resolve().parents[1]`) au `sys.path` avant d’importer `pdf`. Exemple minimal :

  ```python
  ROOT_DIR = Path(__file__).resolve().parents[1]
  if str(ROOT_DIR) not in sys.path:
      sys.path.insert(0, str(ROOT_DIR))
  ```

- OU transformer `field-report` en package « propre » capable de réaliser des imports relatifs (`from .legacy.generer_pdf import ...`).

## Impact du changement

- Une fois la racine du dépôt (ou un package dédié) ajoutée au chemin, `field-report/pdf.py` résoudra `generer_pdf` correctement, permettant aux tests Pytest de poursuivre l’exécution. Cela débloque la génération ReportLab sans attendre un refactoring complet.

## Propositions

### Correction A — Minimum

- **Action** : Avant `from pdf import pdf_builder` dans `tests/test_pdf.py`, insérer `sys.path.insert(0, str(ROOT_DIR))` pour que la racine du dépôt soit dans le PYTHONPATH.
- **Avantages** : Correctif localisé, rapide, pas de refonte de modules.
- **Inconvénients** : Reste une bidouille de chemin, dépend des tests (les autres scripts doivent aussi dupliquer cette logique).

### Correction B — Propre

- **Action** : Déplacer `generer_pdf.py` dans `field-report/` (ex. `field-report/legacy/generer_pdf.py`) et modifier `field-report/pdf.py` pour utiliser un import relatif (`from .legacy.generer_pdf import generate_pdf`). Ajuster `sys.path` pour viser la racine (`Rapport/`) plutôt que `field-report/` et importer le module via un package explicite (`import field_report.pdf` avec un renommage éventuel du dossier en `field_report`).
- **Avantages** : Met fin aux imports flottants, facilite l’utilisation via `python -m`, prépare la librairie à être empaquetée.
- **Inconvénients** : Nécessite de toucher à l’arborescence (`field-report` contient un tiret, donc il faudrait probablement renommer en `field_report` pour respecter la convention), implique des ajustements supplémentaires (imports, références, documentation).

### Correction C — Architecture cible

- **Action** : Intégrer définitivement ReportLab dans la nouvelle application (ex. créer un module `field_report/pdf/reportlab_builder.py` ou migrer vers un service FastAPI dédié). `generer_pdf.py` deviendrait une classe/service importé depuis le package backend, et les tests importeraient `field_report.pdf.PdfBuilder` via un package installé (poetry/pip editable).
- **Avantages** : Aligné avec l’architecture cible (package unique, distribution propre, pas de fichiers orphelins à la racine). Simplifie l’intégration future avec FastAPI et la suppression complète de WeasyPrint.
- **Inconvénients** : Travail plus conséquent (packaging, refactor, potentielle migration du code legacy), nécessite coordination avec les autres chantiers (Docker, API, etc.).
