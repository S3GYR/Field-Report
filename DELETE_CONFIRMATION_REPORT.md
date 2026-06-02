# DELETE_CONFIRMATION_REPORT

FieldReport v1.1 — Confirmations de suppression
Date : 2026-06-02

---

## Objectif

Remplacer le `window.confirm()` natif par une modal HTML cohérente avec le design système, applicable à tous les points de suppression de l'application : rapport, photo, tâche, signature.

---

## Problème des dialogues natifs

| Problème | Impact mobile |
|----------|---------------|
| Style OS, non personnalisable | Incohérence visuelle |
| Petit bouton OK/Annuler | Difficile à toucher |
| Bloque le thread JS | UI figée |
| Pas d'intégration CSS | Non responsive |

---

## Architecture

Une seule modal globale définie dans `layout.html`, utilisée par toutes les pages via la fonction JS `confirmDelete()`.

### Modal globale — `layout.html`

```html
<div class="modal-overlay" id="modal-confirm-delete">
    <div class="modal" style="max-width: 420px;">
        <div class="modal-header">
            <span class="modal-title">Confirmer la suppression</span>
            <button class="modal-close" onclick="closeModal('modal-confirm-delete')">&times;</button>
        </div>
        <p id="confirm-delete-msg" style="margin-bottom: 20px;"></p>
        <div style="display:flex; gap: 8px; justify-content: flex-end;">
            <button type="button" class="btn btn-secondary" onclick="closeModal('modal-confirm-delete')">Annuler</button>
            <button type="button" class="btn btn-danger" id="btn-confirm-delete" onclick="executeDelete()">Supprimer</button>
        </div>
    </div>
</div>
```

### Logique JavaScript — `app.js`

```javascript
let _pendingDelete = { url: null, onSuccess: null };

window.confirmDelete = function(label, apiUrl, onSuccess) {
    _pendingDelete = { url: apiUrl, onSuccess };
    document.getElementById("confirm-delete-msg").textContent = `Supprimer ${label} ?`;
    openModal("modal-confirm-delete");
};

window.executeDelete = async function() {
    closeModal("modal-confirm-delete");
    if (!_pendingDelete.url) return;
    try {
        await apiDelete(_pendingDelete.url);
        toast("Supprimé", "info");
        if (_pendingDelete.onSuccess) _pendingDelete.onSuccess();
        _pendingDelete = { url: null, onSuccess: null };
    } catch (err) {
        toast(err.message, "error");
    }
};
```

---

## Points d'utilisation

| Page | Élément | Label passé | Callback |
|------|---------|-------------|----------|
| `reports.html` | Rapport | `le rapport ${r.number}` | `loadReports()` |
| `report_detail.html` | Rapport | `"ce rapport"` | redirection `/reports` |
| `report_detail.html` | Photo | `"cette photo"` | `loadReport()` |
| `report_detail.html` | Tâche | `"cette tâche"` | `loadReport()` |
| `tasks.html` | Tâche | `la tâche "${t.description}"` | `loadTasks()` |
| `photos.html` | Photo | `"cette photo"` | `loadPhotos()` |
| `signatures.html` | Signature | `la signature de ${s.name}` | `loadSignatures()` |

### Exemple d'appel

```javascript
function deleteReport(id) {
    const r = _reports.find(x => x.id === id);
    confirmDelete(`le rapport ${r.number}`, API.reports + "/" + id, loadReports);
}
```

---

## Gains UX

| Avant (`window.confirm()`) | Après (modal HTML) |
|---------------------------|-------------------|
| Style OS natif | Design FieldReport cohérent |
| Petit texte | Message personnalisé avec le nom de l'élément |
| Boutons minuscules | Boutons `.btn` >= 44px, tactile |
| Thread bloqué | Asynchrone, pas de blocage |
| Non annulable proprement | Bouton Annuler + croix + clic overlay |
