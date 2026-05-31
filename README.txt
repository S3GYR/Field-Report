═══════════════════════════════════════════════════════════
  RAPPORT DE TERRAIN - Guide d'utilisation
═══════════════════════════════════════════════════════════

FICHIERS INCLUS
───────────────
• rapport_photos.html       → Le rapport complet (ouvrir dans Chrome/Edge)
• template_sans_images.html → Template vide sans photos (pour régénérer)
• generer_pdf.py            → Script Python pour générer le PDF
• README.txt                → Ce fichier

═══════════════════════════════════════════════════════════
UTILISATION NORMALE (rapport avec photos intégrées)
═══════════════════════════════════════════════════════════

1. Ouvrir "rapport_photos.html" dans Chrome ou Edge
2. Remplir la fiche de saisie (panneau vert "Saisie du rapport")
   - Projet, commune, intervenant, date, météo, GPS
3. Pour chaque photo :
   - Saisir le numéro de tâche, description, date, statut
   - Ajouter des tâches avec le bouton "+ Ajouter une tâche"
   - Saisir les coordonnées GPS → la carte s'affiche automatiquement
   - Ajouter un commentaire sur la photo
4. Exporter en CSV avec le bouton "Exporter CSV"

⚠️  Les données sont sauvegardées automatiquement dans le navigateur
    (localStorage). Toujours ouvrir le MÊME fichier HTML pour retrouver
    les données saisies.

═══════════════════════════════════════════════════════════
AJOUTER DE NOUVELLES PHOTOS
═══════════════════════════════════════════════════════════

Option A : Dans le rapport ouvert
  → Cliquer "+ Ajouter photo(s)" dans la barre d'outils
  → Les photos s'ajoutent à la fin du rapport

Option B : Nouveau rapport avec nouvelles photos
  → Envoyer les photos à Claude avec ce message :
    "Génère un nouveau rapport terrain avec ces photos"
  → Claude régénère un rapport_photos.html complet

═══════════════════════════════════════════════════════════
GÉNÉRER LE PDF (sans passer par le navigateur)
═══════════════════════════════════════════════════════════

Pré-requis : Python 3 + dépendances
  pip install reportlab

Lancer :
  python generer_pdf.py            # utilise rapport_data.json
  python generer_pdf.py -i mes_donnees.json -o sortie.pdf

Fonctionnement :
• le script lit un fichier JSON (par défaut rapport_data.json). S’il n’existe pas, un exemple est créé automatiquement.
• complétez les sections "info", "photos", "global_comment" et "signature" dans ce JSON.
  - Chaque photo peut définir image_path (chemin local), image_b64 (base64) ou simplement name.
  - Les tâches acceptent numero, description, statut (todo/inprogress/done), date, cout, duree.
• Le PDF paginé reprend : page de couverture, fiches photos avec commentaires, récapitulatif des tâches, commentaire global et bloc de signature.

═══════════════════════════════════════════════════════════
FONCTIONNALITÉS
═══════════════════════════════════════════════════════════

✅ Page de couverture professionnelle (commune, date, intervenant)
✅ Carte GPS de localisation du rapport (OpenStreetMap)
✅ 20 photos intégrées (auto-redimensionnées)
✅ Plusieurs tâches par photo (N°, description, date, statut, coût, durée)
✅ Priorité par photo (Haute / Moyenne / Basse)
✅ Localisation GPS par photo + mini-carte automatique
✅ Commentaire par photo
✅ Commentaire général du rapport
✅ Récapitulatif automatique de toutes les tâches
✅ Totaux (coût, durée, statut)
✅ Signature et validation du rapport
✅ Export CSV
✅ Miniatures de navigation
✅ Filtres par statut et priorité
✅ Extraction GPS automatique depuis EXIF des photos
✅ Sauvegarde automatique (localStorage navigateur)
✅ Thème professionnel vert forêt

═══════════════════════════════════════════════════════════
POUR RÉGÉNÉRER UN RAPPORT AVEC D'AUTRES PHOTOS
═══════════════════════════════════════════════════════════

Envoyer ce message à Claude (claude.ai) avec vos nouvelles photos :

"J'ai un rapport terrain existant. Génère un nouveau rapport_photos.html
avec ces nouvelles photos. Voici le template : [joindre template_sans_images.html]"

═══════════════════════════════════════════════════════════
