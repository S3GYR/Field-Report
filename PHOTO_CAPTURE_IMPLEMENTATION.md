# PHOTO_CAPTURE_IMPLEMENTATION

FieldReport v1.1 — Capture photo native mobile
Date : 2026-06-02

---

## Objectif

Permettre la prise de photo directe depuis l'appareil photo natif du smartphone/tablette, sans passer par la galerie, tout en conservant la possibilité de sélectionner depuis la galerie.

---

## Technique

### Attribut HTML5 `capture`

L'attribut `capture="environment"` sur un input de type `file` déclenche l'appareil photo arrière du device.

```html
<input type="file" name="file" accept="image/*" capture="environment" required>
```

| Attribut | Rôle |
|----------|------|
| `type="file"` | Input fichier standard |
| `accept="image/*"` | Limite aux fichiers image (JPEG, PNG, etc.) |
| `capture="environment"` | Force l'appareil photo arrière (mobile/tablette) |
| `required` | Empêche la soumission sans fichier |

### Comportement par device

| Device | `capture="environment"` | Fallback sans `capture` |
|--------|---------------------------|------------------------|
| Android Chrome | Ouvre appareil photo arrière | Galerie + appareil photo |
| iPhone Safari | Ouvre appareil photo arrière | Galerie + appareil photo |
| iPad Safari | Ouvre appareil photo arrière | Galerie + appareil photo |
| Desktop Chrome/Firefox | Ignoré, sélection fichier classique | Sélection fichier classique |

---

## Implémentation

### Fichier modifié

`backend/app/templates/report_detail.html`

```html
<!-- Modal: Photo upload -->
<div class="modal-overlay" id="modal-photo">
    <div class="modal">
        <div class="modal-header">
            <span class="modal-title">Ajouter une photo</span>
            <button class="modal-close" onclick="closeModal('modal-photo')">&times;</button>
        </div>
        <form id="form-photo">
            <div class="form-group">
                <label class="form-label">Fichier image</label>
                <input class="form-input" type="file" name="file" accept="image/*" capture="environment" required>
                <div id="gps-status" style="font-size:0.8rem;color:var(--muted);margin-top:4px;">GPS : acquisition en cours…</div>
            </div>
            <!-- … -->
        </form>
    </div>
</div>
```

### Soumission

```javascript
document.getElementById("form-photo").addEventListener("submit", async e => {
    e.preventDefault();
    const f = e.target;
    const fd = new FormData();
    fd.append("file", f.file.files[0]);
    if (f.gps_lat.value) fd.append("gps_lat", f.gps_lat.value);
    if (f.gps_lng.value) fd.append("gps_lng", f.gps_lng.value);
    if (f.gps_accuracy.value) fd.append("gps_accuracy", f.gps_accuracy.value);
    await apiUpload(API.photos + "/" + REPORT_ID, fd);
    // …
});
```

---

## Points d'attention

- Sur desktop, l'attribut `capture` est silencieusement ignoré — comportement standard de sélection fichier
- Sur iOS, l'utilisateur peut toujours basculer vers la galerie depuis l'interface caméra
- Le champ `accept="image/*"` est obligatoire pour que `capture` fonctionne correctement
- Le `FormData` conserve le type MIME natif du fichier (image/jpeg après capture caméra)

---

## Tests recommandés

| Test | Device | Résultat attendu |
|------|--------|------------------|
| Ouvrir modal photo sur Android | Smartphone Android | Caméra arrière s'ouvre |
| Ouvrir modal photo sur iPhone | iPhone | Caméra arrière s'ouvre |
| Ouvrir modal photo sur PC | Desktop | Sélecteur de fichier standard |
| Prendre photo + soumettre | Smartphone | Photo uploadée avec GPS |
