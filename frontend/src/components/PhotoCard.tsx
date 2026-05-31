import React from "react";
import { Photo, Task } from "../types/report";

interface PhotoCardProps {
  photo: Photo;
  tasks?: Task[];
}

export default function PhotoCard({ photo, tasks = [] }: PhotoCardProps) {
  return (
    <article className="card" style={{ overflow: "hidden" }}>
      <header
        style={{
          background: "linear-gradient(135deg,#2d5016,#7a9e4e)",
          color: "white",
          padding: "10px 18px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <span style={{ fontFamily: "'DM Serif Display', serif", fontSize: "1.1rem" }}>{photo.filename}</span>
        <span style={{ fontSize: "0.8rem", opacity: 0.8 }}>{photo.priority.toUpperCase()}</span>
      </header>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", minHeight: 220 }}>
        <div style={{ position: "relative", background: "#111" }}>
          <img
            src={`/storage/${photo.filepath}`}
            alt={photo.filename}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        </div>
        <div style={{ borderLeft: "1px solid var(--border)", padding: 16 }}>
          <p style={{ fontSize: "0.85rem", color: "var(--muted)" }}>{photo.comment || "Aucun commentaire"}</p>
          <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: 8 }}>
            {tasks.length === 0 && <li style={{ color: "var(--muted)" }}>Aucune tâche liée</li>}
            {tasks.map((task) => (
              <li key={task.id} style={{ borderBottom: "1px solid #eee", paddingBottom: 8 }}>
                <strong>{task.description}</strong>
                <div style={{ fontSize: "0.75rem", color: "var(--muted)" }}>{task.status}</div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </article>
  );
}
