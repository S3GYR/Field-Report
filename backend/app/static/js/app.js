"use strict";

/* Field Report — Vanilla JS API Client */

const API = {
    reports: "/api/reports",
    photos:  "/api/photos",
    tasks:   "/api/tasks",
    signatures: "/api/signatures",
};

async function apiGet(url) {
    const r = await fetch(url);
    if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
    return r.json();
}
async function apiPost(url, body) {
    const r = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.detail || `${r.status} ${r.statusText}`);
    return data;
}
async function apiPut(url, body) {
    const r = await fetch(url, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.detail || `${r.status} ${r.statusText}`);
    return data;
}
async function apiDelete(url) {
    const r = await fetch(url, { method: "DELETE" });
    if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
    return true;
}
async function apiUpload(url, formData) {
    const r = await fetch(url, { method: "POST", body: formData });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.detail || `${r.status} ${r.statusText}`);
    return data;
}

/* Toast notifications */
function toast(msg, type = "info") {
    const c = document.getElementById("toast-container");
    const el = document.createElement("div");
    el.className = `toast ${type}`;
    el.textContent = msg;
    c.appendChild(el);
    setTimeout(() => el.remove(), 4000);
}

/* Utility DOM helpers */
function el(tag, attrs = {}, children = []) {
    const e = document.createElement(tag);
    Object.entries(attrs).forEach(([k, v]) => {
        if (k === "text") e.textContent = v;
        else if (k === "html") e.innerHTML = v;
        else e.setAttribute(k, v);
    });
    children.forEach(c => e.appendChild(typeof c === "string" ? document.createTextNode(c) : c));
    return e;
}

function formatDate(d) {
    if (!d) return "—";
    const date = new Date(d);
    return date.toLocaleDateString("fr-FR");
}

/* Modal helpers */
function openModal(id) { document.getElementById(id).classList.add("open"); }
function closeModal(id) { document.getElementById(id).classList.remove("open"); }

/* Global confirm delete */
window.confirmDelete = async function(label, apiUrl, onSuccess) {
    if (!confirm(`Supprimer ${label} ?`)) return;
    try {
        await apiDelete(apiUrl);
        toast("Supprimé", "info");
        if (onSuccess) onSuccess();
    } catch (err) {
        toast(err.message, "error");
    }
};
