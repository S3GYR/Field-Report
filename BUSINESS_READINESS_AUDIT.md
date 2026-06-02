# BUSINESS_READINESS_AUDIT

FieldReport v1.1 RC1 — Audit de conformité métier
Date : 2026-06-02
Auditeur : Architecte logiciel senior

---

## 1. Méthodologie

L'audit évalue FieldReport v1.1 selon 4 personas métier et leurs usages terrain. Chaque fonctionnalité est notée : **Présent**, **Partiel**, **Absent**.

---

## 2. Persona : Agent communal (entretien, suivi interventions)

| Besoin | État | Justification | Priorité |
|--------|------|-------------|----------|
| Créer un rapport terrain | **Présent** | Formulaire modal sur `/reports`, champs complets | — |
| Prendre une photo sur site | **Présent** | `capture="environment"` sur mobile, upload avec GPS | — |
| Voir la position GPS de la photo | **Présent** | Coordonnées affichées, lien Google Maps | — |
| Ajouter une tâche corrective | **Présent** | Modal tâche avec description, coût, durée, statut | — |
| Signer le rapport | **Présent** | Modal signature (nom, rôle, date) | — |
| Générer un PDF pour la mairie | **Présent** | Bouton génération, fichier accessible `/exports/` | — |
| Rechercher un ancien rapport | **Présent** | Barre de recherche sur `/reports`, filtrage instantané | — |
| Voir l'historique d'un site | **Présent** | Page `/history`, filtre par site, tri chronologique | — |
| Supprimer une donnée avec confirmation | **Présent** | Modal confirmation sur toutes les suppressions | — |
| Travailler sans réseau | **Absent** | Pas de mode offline. Impossible hors couverture. | **CRITICAL** |

**Score agent communal : 9/10** (1 point bloquant : offline)

---

## 3. Persona : Chargé d'affaires (relevé chantier, réserves)

| Besoin | État | Justification | Priorité |
|--------|------|-------------|----------|
| Documenter des réserves avec photos | **Présent** | Photos + commentaires + priorité (haute/moyenne/basse) | — |
| Quantifier les corrections (coût, durée) | **Présent** | Champs `estimated_cost` et `estimated_duration` sur les tâches | — |
| Suivre l'état des réserves | **Présent** | Statuts tâche : `todo`, `in_progress`, `done`, `blocked` | — |
| Générer un compte-rendu client | **Présent** | PDF avec photos, GPS, tâches, signature | — |
| Filtrer les rapports par client | **Présent** | Recherche textuelle couvre le champ `client` | — |
| Ajouter plusieurs photos par réserve | **Présent** | N photos par rapport, chaque photo peut avoir des tâches | — |
| Relier une tâche à une photo spécifique | **Présent** | Modèle `Task` a un `photo_id` optionnel | — |
| Exporter en CSV | **Absent** | Pas d'export CSV. Uniquement PDF. | **IMPORTANT** |
| Dupliquer un rapport type | **Absent** | Pas de template / duplication. | **Amélioration** |

**Score chargé d'affaires : 8/10** (1 point manquant : export CSV)

---

## 4. Persona : Maintenance (anomalies, actions correctives)

| Besoin | État | Justification | Priorité |
|--------|------|-------------|----------|
| Enregistrer une anomalie | **Présent** | Report + photo + tâche = anomalie documentée | — |
| Planifier une intervention | **Partiel** | Tâches avec coût/durée mais pas de date d'échéance | **IMPORTANT** |
| Suivre le statut des corrections | **Présent** | `todo` → `in_progress` → `done` | — |
| Historique des interventions par site | **Présent** | `/history` filtré par site | — |
| Prioriser les anomalies | **Présent** | Photos avec priorité `high/medium/low/none` | — |
| Assigner une tâche à un technicien | **Absent** | Pas de champ "assigné à" sur les tâches. | **IMPORTANT** |
| Date prévue de correction | **Absent** | Pas de `due_date` sur les tâches. | **IMPORTANT** |
| Alertes tâches en retard | **Absent** | Pas de notification, pas de système d'alerte. | **Amélioration** |

**Score maintenance : 6/10** (points manquants : assignation, date prévue, échéance)

---

## 5. Persona : Inspection / Contrôle qualité

| Besoin | État | Justification | Priorité |
|--------|------|-------------|----------|
| Checklist de contrôle | **Absent** | Pas de modèle de checklist. | **IMPORTANT** |
| Scoring / note de conformité | **Absent** | Pas de champ score ou conformité. | **Amélioration** |
| Photos avant/après | **Partiel** | Possible via commentaires, pas de champ "type" photo. | **Amélioration** |
| Traçabilité (qui, quand) | **Partiel** | `created_at`/`updated_at` sur Report. Pas de champ `created_by`. | **IMPORTANT** |
| Validation par un tiers | **Présent** | Modal signature avec nom, rôle, date. | — |
| Compte-rendu formel | **Présent** | PDF avec toutes les données structurées. | — |
| Archivage long terme | **Partiel** | Fichiers stockés localement. Pas de GED. | **Amélioration** |

**Score inspection : 5/10** (points manquants : checklist, traçabilité utilisateur, scoring)

---

## 6. Fonctionnalités manquantes critiques

| # | Fonctionnalité | Impact | Piste v2 |
|---|----------------|--------|----------|
| 1 | **Mode offline** | Terrain sans réseau = blocage total | Service Worker + IndexedDB |
| 2 | **Authentification** | Multi-utilisateurs impossible, pas de traçabilité | JWT + rôles |
| 3 | **Assignation tâches** | Impossible de savoir qui fait quoi | Champ `assigned_to` sur Task |
| 4 | **Date d'échéance tâche** | Pas de planning des corrections | Champ `due_date` sur Task |
| 5 | **Export CSV/Excel** | Impossible d'exploiter les données dans un tableur | OpenPyXL / Pandas |

---

## 7. Points bloquants pour mise en production

| Bloquant | Description | Contournement immédiat |
|----------|-------------|------------------------|
| Pas d'offline | Zone rurale, parkings souterrains, zones blanches | Utilisation uniquement en zone couverte. Reporter la saisie. |
| Pas d'auth | Plusieurs agents sur le même serveur = confusion | Restreindre l'accès réseau (VPN, WiFi interne). Un seul agent connecté à la fois. |
| Pas d'assignation | Impossible de distribuer le travail | Convention de nommage dans les descriptions de tâches. |

---

## 8. Conclusion métier

| Persona | Note /10 | Bloquant majeur |
|-----------|----------|-----------------|
| Agent communal | 9 | Pas d'offline |
| Chargé d'affaires | 8 | Pas d'export CSV |
| Maintenance | 6 | Pas d'assignation/échéance |
| Inspection / CQ | 5 | Pas de checklist/traçabilité |

**Note moyenne métier : 7.0/10**

### Recommandations classées

**Critique**
- Planifier le mode offline en priorité absolue (v2.0)
- Ajouter authentification basique (même simple, sans complexité RBAC)

**Important**
- Ajouter `due_date` et `assigned_to` sur les tâches
- Ajouter export CSV/Excel des rapports
- Ajouter `created_by` / `updated_by` sur les entités

**Amélioration**
- Checklist de contrôle configurable par type de rapport
- Types de photo (avant/après/panne)
- Tableau de bord statistique (tâches en retard, coûts par site)
