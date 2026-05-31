import React from "react";
import { Report } from "../types/report";

interface HeaderProps {
  report?: Report;
}

const statStyle: React.CSSProperties = {
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  justifyContent: "center",
  padding: "0 22px",
  borderRight: "1px solid rgba(255,255,255,0.15)",
};

export default function Header({ report }: HeaderProps) {
  const infoLabel = report
    ? `${report.client} — ${new Date(report.visit_date).toLocaleDateString("fr-FR")}`
    : "Sélectionnez un rapport";

  return (
    <header style={{ background: "var(--accent)", color: "white", boxShadow: "0 2px 24px rgba(0,0,0,0.3)" }}>
      <div style={{ display: "flex", alignItems: "stretch", minHeight: 58 }}>
        <div style={{ padding: "0 22px", display: "flex", alignItems: "center", borderRight: "1px solid rgba(255,255,255,0.2)" }}>
          📋
        </div>
        <div style={{ flex: 1, display: "flex", flexDirection: "column", justifyContent: "center", padding: "10px 24px" }}>
          <h1 style={{ fontFamily: "'DM Serif Display', serif", fontWeight: 400, margin: 0 }}>Rapport de terrain</h1>
          <span style={{ fontSize: "0.7rem", opacity: 0.7 }}>{infoLabel}</span>
        </div>
        <div style={{ display: "flex", borderLeft: "1px solid rgba(255,255,255,0.2)" }}>
          <div style={statStyle}>
            <span style={{ fontFamily: "'DM Serif Display', serif", fontSize: "1.2rem" }}>{report?.photos.length ?? "—"}</span>
            <span style={{ fontSize: "0.6rem", textTransform: "uppercase", opacity: 0.7 }}>Photos</span>
          </div>
          <div style={{ ...statStyle, borderRight: "none" }}>
            <span style={{ fontFamily: "'DM Serif Display', serif", fontSize: "1.2rem" }}>{report?.tasks.length ?? "—"}</span>
            <span style={{ fontSize: "0.6rem", textTransform: "uppercase", opacity: 0.7 }}>Tâches</span>
          </div>
        </div>
      </div>
    </header>
  );
}
