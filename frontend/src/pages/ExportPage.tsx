import React from "react";

export default function ExportPage() {
  const [reportId, setReportId] = React.useState("");
  const [result, setResult] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  async function handleExport() {
    setError(null);
    setResult(null);
    try {
      const res = await fetch(`/api/reports/${reportId}/pdf`, { method: "POST" });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setResult(data.pdf);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <section className="card" style={{ maxWidth: 480, margin: "0 auto" }}>
      <h2>Exporter un rapport en PDF</h2>
      <label style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        Numéro de rapport ou ID
        <input value={reportId} onChange={(e) => setReportId(e.target.value)} />
      </label>
      <button className="btn" style={{ marginTop: 12 }} onClick={handleExport}>
        Générer le PDF
      </button>
      {result && (
        <p style={{ marginTop: 12 }}>
          PDF prêt : <a href={`/${result}`} target="_blank" rel="noreferrer">Télécharger</a>
        </p>
      )}
      {error && <p style={{ color: "tomato" }}>{error}</p>}
    </section>
  );
}
