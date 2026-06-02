# FIELDREPORT_VISION

FieldReport — Vision produit
Date : 2026-06-02

---

## 1. Proposition de valeur

FieldReport est un outil de saisie et de restitution de rapports de visite technique sur le terrain. Il remplace les rapports papier et les fichiers Excel dispersés par une solution centralisée, accessible depuis n'importe quel navigateur.

---

## 2. Cible métier

### Secteurs

- Bâtiment et construction
- Inspection technique (électricité, plomberie, structure)
- Maintenance industrielle
- Audit immobilier

### Segment principal

Petites et moyennes structures (10 à 100 salariés) n'ayant pas les moyens d'acheter un ERP de maintenance ou une solution SaaS onéreuse.

---

## 3. Utilisateurs

| Persona | Rôle | Besoin principal | Fréquence |
|---------|------|-----------------|-----------|
| Inspecteur terrain | Crée les rapports sur chantier | Saisie rapide, offline, photos | Quotidien |
| Responsable bureau | Valide et relit les rapports | Vue d'ensemble, recherche, export | Hebdomadaire |
| Client final | Reçoit le rapport PDF | Clarté, traçabilité, signature | Par visite |
| Administrateur IT | Déploie et maintient l'outil | Simplicité Docker, backup | Mensuel |

---

## 4. Cas d'usage principaux

### UC-1 — Saisie d'un rapport sur chantier

1. Inspecteur ouvre FieldReport sur son smartphone
2. Il crée un nouveau rapport (numéro auto, date, client, site)
3. Il prend des photos directement depuis l'appareil
4. Il saisit les observations et recommandations
5. Il ajoute les tâches associées avec coût estimé
6. Il fait signer le client sur tablette
7. Il génère le PDF et l'envoie par email

**Valeur** : Remplacer 2h de saisie papier + transcription par 20 minutes de saisie directe.

### UC-2 — Suivi d'une intervention

1. Responsable bureau consulte le dashboard
2. Il filtre les rapports en attente de validation
3. Il ouvre un rapport, relit les photos et les tâches
4. Il approuve le rapport
5. Il génère le PDF final pour archivage

**Valeur** : Réduire le temps de relecture et éviter les oublis.

### UC-3 — Historique et recherche

1. Client appelle pour un problème sur un site
2. Responsable recherche "site X + fissure" dans l'historique
3. Il retrouve le rapport de l'année précédente avec photos
4. Il compare avec la visite actuelle

**Valeur** : Capitaliser le savoir, éviter les réinterventions inutiles.

---

## 5. Feuille de route

### v1.0.x — Stabilisation (actuel)

**Statut** : Release Candidate validée. Infrastructure nettoyée.

**Livrables** :
- Docker propre
- Dépendances cohérentes
- Code formaté (ruff)
- Tests passants

### v1.1 — Productivité terrain (Q3 2026)

**Objectif** : Rendre l'outil utilisable confortablement sur le terrain.

**Livrables** :
- Remplacement des `prompt()` par des modals HTML
- Capture photo native (`capture="environment"`)
- Géolocalisation automatique des photos
- Spinners et feedback sur toutes les actions
- Confirmation avant suppression
- Tableaux responsive

### v1.2 — Exploitation et recherche (Q4 2026)

**Objectif** : Permettre la gestion d'un volume croissant de rapports.

**Livrables** :
- Recherche full-text et filtres avancés
- Pagination API + UI
- Duplication de rapport
- Templates de rapport pré-remplis
- Export CSV
- Visionneuse photo lightbox

### v2.0 — Plateforme multi-utilisateur (H1 2027)

**Objectif** : Transformer FieldReport en plateforme utilisable par une équipe.

**Livrables** :
- Authentification JWT (inspecteur / responsable / client)
- Rôles et permissions
- Dashboard analytics (productivité, taux d'approbation)
- Partage lien public temporaire
- PWA complète (offline, sync, cache)
- Notifications email

---

## 6. Différenciation

| Critère | FieldReport | Excel + Photos | SaaS concurrent |
|---------|-------------|---------------|-----------------|
| Coût | Gratuit / auto-hébergé | Inclus dans Office | 30-100€/mois/utilisateur |
| Données | Chez le client (SQLite) | Fichiers dispersés | Chez l'éditeur (cloud) |
| Déploiement | `docker compose up` | Aucun | Inscription + configuration |
| Offline | Possible (PWA v2.0) | Oui (fichiers locaux) | Dépendant du réseau |
| Personnalisation | Code source ouvert | Aucune | Limitée |
| Photos liées au rapport | Oui (par rapport) | Non (dossier séparé) | Oui |
| Signature électronique | Oui (dessin) | Non | Payant |
| Export PDF | Oui (généré côté serveur) | Manuel | Oui |

---

## 7. Indicateurs de succès (KPIs)

| KPI | Cible v1.1 | Cible v2.0 |
|-----|-----------|-----------|
| Temps de saisie rapport | < 20 min | < 15 min |
| Temps de recherche rapport | < 30 s | < 10 s |
| Taux d'utilisation mobile | > 60 % | > 80 % |
| Rapports générés / mois | 100 | 500 |
| NPS utilisateur | > 40 | > 50 |

---

## 8. Risques produit

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|----------|
| Adoption mobile faible (UX desktop-first) | Moyenne | Haut | Prioriser les irritants mobiles en v1.1 |
| Concurrence SaaS à bas prix | Haute | Moyen | Vendre la souveraineté des données et le coût nul |
| Complexité technique PWA | Moyenne | Moyen | Phaser le offline (cache → sync → offline complet) |
| Besoin d'API tierces (carte, email) | Faible | Moyen | Garder le core indépendant, ajouter les intégrations en option |

---

## 9. Principes directeurs

1. **Terrain d'abord** : Chaque décision UX privilégie l'inspecteur sur le chantier
2. **Pas de vendor lock-in** : Les données restent chez le client (SQLite, fichiers locaux)
3. **Simplicité technique** : Pas de framework frontend lourd. Vanilla JS + Jinja2 suffisent.
4. **Itération rapide** : Des releases toutes les 6-8 semaines, pas de gros projets
5. **Zero-config** : `docker compose up -d` doit suffire à démarrer
