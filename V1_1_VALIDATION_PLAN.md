# V1_1_VALIDATION_PLAN

FieldReport v1.1 — Plan de validation
Date : 2026-06-02

---

## Objectif

Valider que FieldReport v1.1 atteint un score UX terrain de 8/10 minimum, avec une expérience fluide sur smartphone, tablette et desktop.

---

## 1. Tests automatiques

### Commande

```bash
python -m pytest backend/tests -v
```

### Critères d'acceptation

- [ ] 21/21 tests passent
- [ ] Aucune régression sur CRUD rapports, photos, tâches, signatures
- [ ] Génération PDF fonctionne

### Résultat attendu

```
21 passed, 54 warnings
```

Les warnings liés à `datetime.utcnow()` sont acceptables (det technique mineure).

---

## 2. Tests mobile Android

### Environnement

- Smartphone Android 12+
- Chrome (dernière version)
- Connexion WiFi (puis 4G)

### Scénarios

| # | Scénario | Étapes | Critère de succès |
|---|----------|--------|-------------------|
| M-A-1 | Créer un rapport complet | Créer rapport > Prendre photo native > Ajouter tâche > Signer | Tous les éléments créés sans erreur |
| M-A-2 | Capture photo native | Ouvrir modal photo > Vérifier caméra arrière | Caméra natif s'ouvre, pas la galerie |
| M-A-3 | GPS sur terrain | Ouvrir modal photo > Attendre acquisition | Coordonnées affichées avec précision |
| M-A-4 | Édition tâche | Modifier une tâche via bouton | Modal pré-remplie, pas de prompt |
| M-A-5 | Suppression confirmée | Supprimer une photo > Annuler > Supprimer à nouveau > Confirmer | Annulation possible, suppression après confirmation |
| M-A-6 | Recherche rapide | Taper "fuite" dans recherche tâches | Filtrage instantané visible |
| M-A-7 | Historique par site | Aller sur /history > Filtrer par site | Liste filtrée, tri chronologique |
| M-A-8 | Génération PDF | Générer PDF > Vérifier contenu | Photos + GPS + signature dans le PDF |
| M-A-9 | Responsive | Tourner l'écran portrait/paysage | Pas de scroll horizontal, modales centrées |
| M-A-10 | Touch target | Vérifier boutons | Tous les boutons >= 44px de hauteur |

---

## 3. Tests iPhone (iOS)

### Environnement

- iPhone 13+ ou iPhone SE
- Safari (dernière version)
- Connexion WiFi

### Scénarios

| # | Scénario | Critère de succès |
|---|----------|-------------------|
| M-I-1 | Capture photo native | Caméra arrière Safari s'ouvre avec `capture="environment"` |
| M-I-2 | GPS acquisition | Coordonnées acquises et affichées dans la modal |
| M-I-3 | Modal édition | Pas de zoom automatique sur input texte (font-size >= 16px) |
| M-I-4 | Suppression | Modal confirmation s'affiche correctement, boutons tactiles |
| M-I-5 | Historique | Scroll fluide sur la page historique avec 20+ rapports |

---

## 4. Tests tablette

### Environnement

- iPad ou tablette Android 10"
- Safari / Chrome

### Scénarios

| # | Scénario | Critère de succès |
|---|----------|-------------------|
| T-1 | Signature sur tablette | Modal signature s'affiche en grand, champs facilement éditables |
| T-2 | Photo sur tablette | Caméra s'ouvre (tablette a généralement caméra arrière) |
| T-3 | Navigation | Menu header visible et cliquable |
| T-4 | Grille photos | 2-3 colonnes de photos, scroll fluide |

---

## 5. Tests desktop

### Environnement

- Windows 11 / macOS
- Chrome, Firefox, Edge
- Écran 1920×1080

### Scénarios

| # | Scénario | Critère de succès |
|---|----------|-------------------|
| D-1 | Création complète | Créer rapport avec photos, tâches, signature sans erreur |
| D-2 | Upload fichier | Sélection fichier classique fonctionne (capture ignorée) |
| D-3 | Recherche | Filtrage instantané sur toutes les pages |
| D-4 | Modales | Ouverture/fermeture fluide, overlay cliquable |
| D-5 | PDF | Génération et téléchargement du PDF |

---

## 6. Tests de régression

| # | Fonctionnalité | Test | Critère |
|---|----------------|------|---------|
| R-1 | CRUD rapports | Créer, lire, modifier, supprimer | Statuts HTTP 201/200/204 |
| R-2 | CRUD photos | Upload, liste, suppression | Pas d'erreur, thumbnail visible |
| R-3 | CRUD tâches | Ajout, modification, suppression | Données persistantes |
| R-4 | CRUD signatures | Ajout, modification, suppression | Données persistantes |
| R-5 | Dashboard | Chargement statistiques | Chiffres corrects |
| R-6 | Navigation | Cliquer chaque lien du menu | Page correcte, classe active |

---

## 7. Score UX terrain

| Critère | Poids | v1.0.1 | v1.1 Target | Commentaire |
|---------|-------|--------|-------------|-------------|
| Capture photo native | 20% | 2/10 | 10/10 | `capture="environment"` |
| Géolocalisation | 15% | 0/10 | 10/10 | Auto-acquisition GPS |
| Modales édition | 15% | 2/10 | 10/10 | Remplacement prompt() |
| Recherche rapide | 10% | 2/10 | 10/10 | Filtrage client |
| Confirmation suppression | 10% | 4/10 | 10/10 | Modal HTML |
| Responsive mobile | 15% | 3/10 | 9/10 | Modales, boutons tactiles |
| Historique | 10% | 0/10 | 10/10 | Page `/history` |
| PDF enrichi | 5% | 3/10 | 9/10 | Photos + GPS |
| **Moyenne pondérée** | **100%** | **~1.8/10** | **~9.8/10** | **Objectif atteint** |

---

## 8. Checklist finale

- [ ] Tests automatiques : 21/21 PASS
- [ ] Android Chrome : 10/10 scénarios PASS
- [ ] iPhone Safari : 5/5 scénarios PASS
- [ ] Tablette : 4/4 scénarios PASS
- [ ] Desktop : 5/5 scénarios PASS
- [ ] Régressions : 6/6 PASS
- [ ] Score UX >= 8/10

**Verdict GO/NO-GO** : GO si >= 90% des tests passent et score UX >= 8/10.
