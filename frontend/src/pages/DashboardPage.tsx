import React from "react";
import { Link } from "react-router-dom";
import { useReports } from "../hooks/useReports";
import { Report } from "../types/report";

export default function DashboardPage() {
  const { data, isLoading, error } = useReports();

  if (isLoading) return <div>Chargement…</div>;
  if (error) return <div>Erreur : {(error as Error).message}</div>;

  return (
    <section className="card">
      <h2 style={{ fontFamily: "'DM Serif Display', serif", color: "var(--accent)" }}>Rapports récents</h2>
      <div className="grid" style={{ gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))" }}>
        {data?.map((report: Report) => (
          <article key={report.id} className="card" style={{ padding: 16, borderRadius: 12 }}>
            <p style={{ fontSize: "0.75rem", color: "var(--muted)", marginBottom: 4 }}>{report.number}</p>
            <h3 style={{ margin: "4px 0", fontSize: "1.1rem" }}>{report.client}</h3>
            <p style={{ margin: "4px 0" }}>{report.site}</p>
            <p style={{ fontSize: "0.8rem", color: "var(--muted)" }}>
              {new Date(report.visit_date).toLocaleDateString("fr-FR")}
            </p>
            <Link to={`/reports/${report.id}`} style={{ color: "var(--accent2)", fontWeight: 600 }}>
              Ouvrir →
            </Link>
          </article>
        ))}
      </div>
    </section>
  );
}
