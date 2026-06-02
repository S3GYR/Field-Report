# KNOWN_LIMITATIONS

FieldReport v1.1 — Limitations connues
Date : 2026-06-02

---

## 1. Limitations mobiles

### Capture photo native

| Limitation | Détail | Mitigation |
|------------|--------|------------|
| `capture="environment"` ignoré sur certains navigateurs | Firefox mobile, vieux Android WebView | L'utilisateur peut toujours choisir la galerie manuellement |
| iOS : pas de contrôle sur la résolution | La photo est prise à la résolution maximale de l'appareil | Compression côté serveur via Pillow thumbnail |
| Android : comportement variable selon OEM | Samsung, Xiaomi, Huawei peuvent ouvrir leur appareil photo natif différemment | `accept="image/*"` garantit toujours le fallback galerie |
| Pas de prévisualition en direct | L'utilisateur ne voit la photo qu'après capture | Acceptable pour un outil terrain simple |

### Interface responsive

| Limitation | Détail | Mitigation |
|------------|--------|------------|
| Tables non optimisées pour < 360px | Les colonnes des tableaux de tâches et rapports peuvent nécessiter un scroll horizontal | `overflow-x: auto` sur les tables, cards pour historique |
| Header navigation sur mobile | Tous les liens ne tiennent pas sur une ligne < 375px | Pas de menu hamburger (v1.1), scroll horizontal implicite du nav |
| Input font-size | `.form-input { font-size: 0.95rem }` risque de provoquer un zoom iOS si < 16px | À vérifier sur device réel, augmenter à `1rem` si nécessaire |

---

## 2. Limitations GPS

| Limitation | Détail | Mitigation |
|------------|--------|------------|
| Précision variable | 5-20m en extérieur dégagé, 50-200m en intérieur / urbain dense | Champ `gps_accuracy` affiché à l'utilisateur |
| Premier fix lent | Le premier GPS fix peut prendre 5-15s sur cold start | Acquisition déclenchée dès l'ouverture de la modal |
| Pas de GPS sur PC desktop | Pas de coordonnées si l'ordinateur n'a pas de module GPS | Upload possible sans GPS, comportement normal |
| Refus de permission | Si l'utilisateur refuse la géolocalisation, aucune coordonnée n'est acquise | Message clair "GPS : échec de l'acquisition", upload sans GPS possible |
| Pas de suivi en temps réel | `getCurrentPosition()` = position ponctuelle, pas de trajectoire | Hors scope v1.1 (v2.0 offline pourrait ajouter watchPosition) |
| Coordonnées peuvent être faussées | Réseau WiFi, VPN, mock GPS peuvent fausser la position | Affichage de la précision pour information |

---

## 3. Limitations SQLite

| Limitation | Détail | Mitigation |
|------------|--------|------------|
| Mono-utilisateur | SQLite ne supporte pas les écritures concurrentes | Usage prévu : un seul utilisateur terrain à la fois |
| Pas de réplication native | Pas de sync automatique entre devices | Export PDF manuel pour transmission |
| Taille fichier | La base grandit avec les photos (stockées en fichier, pas en BLOB) | Photos stockées dans `storage/photos/`, pas dans SQLite |
| Pas de backup automatique | Aucune sauvegarde planifiée | Recommandation : copier `storage/reports.db` régulièrement |
| Pas de recherche full-text | Recherche par `LIKE` uniquement si implémentée côté API | Recherche v1.1 est client-side sur les données chargées |
| Verrouillage fichier | Si le fichier `.db` est ouvert par un autre processus, écriture impossible | Docker garantit un seul processus |

---

## 4. Limitations Docker

| Limitation | Détail | Mitigation |
|------------|--------|------------|
| Volumes persistants requis | Sans `volumes` dans `docker-compose.yml`, les données disparaissent au `docker-compose down` | `docker-compose.yml` configuré avec `volumes` |
| Hot reload uniquement en dev | En production, recompilation du conteneur nécessaire | Utiliser `docker-compose.prod.yml` distinct |
| Pas de HTTPS natif | Le conteneur expose HTTP uniquement | Reverse proxy Nginx / Traefik en amont pour HTTPS |
| Pas de scaling horizontal | SQLite empêche le multi-instance | Architecture mono-instance par design |
| Image taille | Python + Pillow + ReportLab = ~500MB | Acceptable pour un déploiement local/serveur dédié |

---

## 5. Limitations PDF

| Limitation | Détail | Mitigation |
|------------|--------|------------|
| Photos en basse résolution dans le PDF | ReportLab `Image` charge l'image originale, pas la miniature | `keepRatio=True` et largeur max 120mm |
| Pas de texte OCR sur les photos | Les photos ne sont pas analysées pour extraction de texte | Hors scope, possible v2 avec Tesseract |
| Pas de mise en page avancée | Pas de colonnes multiples, pas de styles conditionnels | Template simple ReportLab, suffisant pour un compte-rendu |
| Signature image non intégrée si manquante | Si le fichier image de signature n'existe pas, seul le texte apparaît | Vérification existence fichier avant `Image()` |
| Pas de PDF/A pour archivage | Le PDF généré n'est pas conforme PDF/A | ReportLab standard, hors scope v1.1 |

---

## 6. Limitations fonctionnelles v1.1

| Limitation | Détail | Piste v2 |
|------------|--------|--------|
| Pas de mode hors ligne | Sans réseau, aucune saisie possible | Service Worker + IndexedDB |
| Pas de synchronisation multi-device | Les données restent sur le serveur unique | Sync API avec conflits |
| Pas d'authentification | Pas de login, pas de rôles | JWT + rôles (admin, agent) |
| Pas de notifications push | Pas d'alerte tâche en retard | Web Push API |
| Pas d'export CSV/Excel | Uniquement PDF | OpenPyXL / Pandas |
| Pas de dashboard cartographique | Historique en liste texte, pas sur carte | Leaflet + tuiles OpenStreetMap |

---

## Résumé

FieldReport v1.1 est un outil terrain **connecté** optimisé pour smartphone/tablette avec les contraintes suivantes :

- Nécessite une connexion réseau permanente
- Mono-utilisateur SQLite
- Pas de fonctionnalités collaboratives
- Pas de mode hors ligne

Ces limitations sont **acceptées et documentées** pour la v1.1. La feuille de route v2.0 (OFFLINE_V2_PREPARATION.md) adresse les points critiques.
