import React from "react";
import { useParams } from "react-router-dom";
import Header from "../components/Header";
import PhotoCard from "../components/PhotoCard";
import { useReport } from "../hooks/useReports";
import MapView from "../components/MapView";
import { Photo, Task } from "../types/report";

export default function ReportPage() {
  const { id } = useParams();
  const reportId = Number(id);

  if (!Number.isFinite(reportId)) {
    return <div>Rapport introuvable</div>;
  }

  const { data: report, isLoading, error } = useReport(reportId);

  if (isLoading) return <div>Chargement…</div>;
  if (error || !report) return <div>Rapport introuvable</div>;

  const firstPhotoWithGps = report.photos.find(
    (photo: Photo) => photo.gps_lat !== undefined && photo.gps_lng !== undefined
  );

  return (
    <>
      <Header report={report} />
      <section className="card" style={{ display: "grid", gap: 16 }}>
        <h2 style={{ fontFamily: "'DM Serif Display', serif" }}>Résumé</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))", gap: 12 }}>
          <div>
            <strong>Client</strong>
            <p>{report.client}</p>
          </div>
          <div>
            <strong>Site</strong>
            <p>{report.site}</p>
          </div>
          <div>
            <strong>Météo</strong>
            <p>{report.weather}</p>
          </div>
          <div>
            <strong>Statut</strong>
            <p>{report.status}</p>
          </div>
        </div>
        {report.comments && <p style={{ fontStyle: "italic" }}>{report.comments}</p>}
      </section>

      {firstPhotoWithGps && firstPhotoWithGps.gps_lat && firstPhotoWithGps.gps_lng && (
        <MapView lat={firstPhotoWithGps.gps_lat} lng={firstPhotoWithGps.gps_lng} />
      )}

      <section className="grid" style={{ gap: 20 }}>
        {report.photos.map((photo: Photo) => (
          <PhotoCard
            key={photo.id}
            photo={photo}
            tasks={report.tasks.filter((task: Task) => task.photo_id === photo.id)}
          />
        ))}
      </section>
    </>
  );
}
