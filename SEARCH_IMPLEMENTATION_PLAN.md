# SEARCH_IMPLEMENTATION_PLAN

FieldReport v1.1 — Recherche locale rapide
Date : 2026-06-02

---

## Objectif

Permettre la recherche instantanée dans les listes de rapports, photos, tâches et signatures sans requête serveur, en filtrant les éléments déjà chargés côté client.

---

## Stratégie

Recherche **client-side** sur les données déjà en mémoire JavaScript. Pas de pagination, pas de requête API supplémentaire. Le filtrage s'applique sur le `textContent` de chaque ligne/élément affiché.

---

## Implémentation par page

### Rapports — `reports.html`

```html
<div class="form-group" style="margin-bottom: 12px;">
    <input class="form-input" id="report-search" type="search" placeholder="Rechercher un rapport…" oninput="filterReports()">
</div>
```

```javascript
function filterReports() {
    const q = document.getElementById("report-search").value.toLowerCase();
    const rows = document.querySelectorAll("#reports-table tr");
    rows.forEach(row => {
        if (row.querySelector("td.empty-state")) return;
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(q) ? "" : "none";
    });
}
```

**Champs indexés** : numéro, date visite, client, site, météo, statut.

### Tâches — `tasks.html`

```html
<input class="form-input" id="task-search" type="search" placeholder="Rechercher une tâche…" oninput="filterTasks()">
```

```javascript
function filterTasks() {
    const q = document.getElementById("task-search").value.toLowerCase();
    const rows = document.querySelectorAll("#tasks-table tr");
    rows.forEach(row => {
        if (row.querySelector("td.empty-state")) return;
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(q) ? "" : "none";
    });
}
```

**Champs indexés** : description, rapport lié, statut, coût, durée.

### Photos — `photos.html`

```html
<input class="form-input" id="photo-search" type="search" placeholder="Rechercher une photo…" oninput="filterPhotos()">
```

```javascript
function filterPhotos() {
    const q = document.getElementById("photo-search").value.toLowerCase();
    const items = document.querySelectorAll("#photos-list .photo-item");
    items.forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(q) ? "" : "none";
    });
}
```

**Champs indexés** : nom de fichier, commentaire, rapport lié.

### Signatures — `signatures.html`

```html
<input class="form-input" id="signature-search" type="search" placeholder="Rechercher une signature…" oninput="filterSignatures()">
```

```javascript
function filterSignatures() {
    const q = document.getElementById("signature-search").value.toLowerCase();
    const rows = document.querySelectorAll("#signatures-table tr");
    rows.forEach(row => {
        if (row.querySelector("td.empty-state")) return;
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(q) ? "" : "none";
    });
}
```

**Champs indexés** : nom, rôle, date, rapport lié.

---

## Fichiers modifiés

| Fichier | Changement |
|---------|------------|
| `backend/app/templates/reports.html` | Barre recherche `#report-search` + `filterReports()` |
| `backend/app/templates/tasks.html` | Barre recherche `#task-search` + `filterTasks()` |
| `backend/app/templates/photos.html` | Barre recherche `#photo-search` + `filterPhotos()` |
| `backend/app/templates/signatures.html` | Barre recherche `#signature-search` + `filterSignatures()` |

---

## Caractéristiques

| Aspect | Valeur |
|--------|--------|
| Type | Filtrage client (DOM) |
| Performance | Instantané (< 1ms pour < 500 lignes) |
| Case sensitive | Non (`.toLowerCase()`) |
| Regex | Non (recherche simple `.includes()`) |
| Requête serveur | Aucune |
| Persistance | Aucune (effacé au rechargement) |

---

## Limitations connues

- La recherche s'applique uniquement aux données déjà chargées sur la page
- Pas de recherche cross-page (pas de recherche globale rapports + tâches + photos)
- Pas de recherche avancée (pas de filtres combinés, pas de dates)
- Pour des volumes > 1000 lignes par page, prévoir une pagination serveur
