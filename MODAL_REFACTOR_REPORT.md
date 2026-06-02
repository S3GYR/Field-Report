# MODAL_REFACTOR_REPORT

FieldReport v1.1 — Remplacement des `prompt()` / `confirm()` / `alert()`
Date : 2026-06-02

---

## Objectif

Éliminer toutes les boîtes de dialogue natives bloquantes (`prompt()`, `confirm()`, `alert()`) qui posent problème sur mobile (affichage non adapté, blocage de l'UI, UX non cohérente) et les remplacer par des modales HTML cohérentes avec le design système existant.

---

## Inventaire pré-migration

| Page | Fonction | Dialogue natif | Élément modifié |
|------|----------|----------------|-----------------|
| `report_detail.html` | Créer tâche | — (déjà modal) | Modal réutilisée pour édition |
| `report_detail.html` | Éditer tâche | `prompt()` × 3 | `modal-task` réutilisé |
| `tasks.html` | Éditer tâche | `prompt()` × 3 | `modal-task-edit` ajouté |
| `signatures.html` | Éditer signature | `prompt()` × 3 | `modal-signature-edit` ajouté |
| `reports.html` | Créer/éditer rapport | — (déjà modals) | Aucun changement |
| Global | Suppression | `window.confirm()` | `modal-confirm-delete` global |

---

## Modales créées / modifiées

### 1. Modal tâche (création + édition) — `report_detail.html`

La modal existante a été refondue pour supporter à la fois la création et l'édition via un champ caché `task_id`.

```html
<div class="modal-overlay" id="modal-task">
    <div class="modal">
        <div class="modal-header">
            <span class="modal-title" id="modal-task-title">Nouvelle tâche</span>
            <button class="modal-close" onclick="closeModal('modal-task')">&times;</button>
        </div>
        <form id="form-task">
            <input type="hidden" name="task_id" id="task-id">
            <div class="form-group">
                <label class="form-label">Description</label>
                <input class="form-input" name="description" required>
            </div>
            <div class="grid-2">
                <div class="form-group">
                    <label class="form-label">Coût estimé (€)</label>
                    <input class="form-input" type="number" step="0.01" name="estimated_cost">
                </div>
                <div class="form-group">
                    <label class="form-label">Durée estimée (h)</label>
                    <input class="form-input" type="number" step="0.1" name="estimated_duration">
                </div>
            </div>
            <div class="form-group">
                <label class="form-label">Statut</label>
                <select class="form-select" name="status">
                    <option value="todo">À faire</option>
                    <option value="in_progress">En cours</option>
                    <option value="done">Terminée</option>
                    <option value="blocked">Bloquée</option>
                </select>
            </div>
            <div style="display:flex; gap: 8px; justify-content: flex-end;">
                <button type="button" class="btn btn-secondary" onclick="closeModal('modal-task')">Annuler</button>
                <button type="submit" class="btn btn-primary" id="btn-task-submit">Créer</button>
            </div>
        </form>
    </div>
</div>
```

**Logique de bascule création/édition** :

```javascript
function editTask(id) {
    const t = _report.tasks.find(x => x.id === id);
    if (!t) return;
    const f = document.getElementById("form-task");
    f.description.value = t.description;
    f.estimated_cost.value = t.estimated_cost || "";
    f.estimated_duration.value = t.estimated_duration || "";
    f.status.value = t.status;
    document.getElementById("task-id").value = t.id;
    document.getElementById("modal-task-title").textContent = "Modifier la tâche";
    document.getElementById("btn-task-submit").textContent = "Enregistrer";
    openModal("modal-task");
}

document.getElementById("form-task").addEventListener("submit", async e => {
    e.preventDefault();
    const f = e.target;
    const payload = Object.fromEntries(new FormData(f));
    delete payload.task_id;
    if (payload.estimated_cost) payload.estimated_cost = Number(payload.estimated_cost);
    if (payload.estimated_duration) payload.estimated_duration = Number(payload.estimated_duration);
    const taskId = document.getElementById("task-id").value;
    if (taskId) {
        await apiPut(API.tasks + "/" + taskId, payload);
        toast("Tâche mise à jour", "info");
    } else {
        await apiPost(API.tasks + "/" + REPORT_ID, payload);
        toast("Tâche créée", "info");
    }
    closeModal("modal-task");
    f.reset();
    document.getElementById("task-id").value = "";
    document.getElementById("modal-task-title").textContent = "Nouvelle tâche";
    document.getElementById("btn-task-submit").textContent = "Créer";
    loadReport();
});
```

### 2. Modal édition tâche — `tasks.html`

Modal dédiée identique à celle de `report_detail.html` mais avec un ID différent pour éviter les conflits de DOM.

### 3. Modal édition signature — `signatures.html`

```html
<div class="modal-overlay" id="modal-signature-edit">
    <div class="modal">
        <div class="modal-header">
            <span class="modal-title">Modifier la signature</span>
            <button class="modal-close" onclick="closeModal('modal-signature-edit')">&times;</button>
        </div>
        <form id="form-signature-edit">
            <input type="hidden" name="report_id" id="edit-sig-report-id">
            <div class="form-group">
                <label class="form-label">Nom</label>
                <input class="form-input" name="name" required>
            </div>
            <div class="form-group">
                <label class="form-label">Rôle</label>
                <input class="form-input" name="role">
            </div>
            <div class="form-group">
                <label class="form-label">Date de signature</label>
                <input class="form-input" type="date" name="signed_on">
            </div>
            <div style="display:flex; gap: 8px; justify-content: flex-end;">
                <button type="button" class="btn btn-secondary" onclick="closeModal('modal-signature-edit')">Annuler</button>
                <button type="submit" class="btn btn-primary">Enregistrer</button>
            </div>
        </form>
    </div>
</div>
```

---

## Fichiers modifiés

| Fichier | Changement |
|---------|------------|
| `backend/app/templates/report_detail.html` | Modal task réutilisable création/édition |
| `backend/app/templates/tasks.html` | Modal `modal-task-edit` ajoutée |
| `backend/app/templates/signatures.html` | Modal `modal-signature-edit` ajoutée |

---

## Gains UX

| Avant (`prompt()`) | Après (modal HTML) |
|-------------------|-------------------|
| Affichage OS natif, non stylable | Design cohérent avec FieldReport |
| Un seul champ par prompt | Formulaire complet en une seule modal |
| Bloque le thread JS | Asynchrone, UI responsive |
| Peu utilisable sur mobile | Adapté tactile, scrollable |
| Pas d'annulation propre | Bouton Annuler natif |
| Pas de validation HTML5 | `required`, `type="number"`, etc. |
