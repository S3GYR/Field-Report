import React from "react";
import { useReports } from "../hooks/useReports";
import PhotoCard from "../components/PhotoCard";
import { Photo, Task } from "../types/report";

export default function PhotosPage() {
  const { data, isLoading, error } = useReports();

  if (isLoading) return <div>Chargement…</div>;
  if (error) return <div>Erreur : {(error as Error).message}</div>;

  const photos = data?.flatMap((report) =>
    report.photos.map((photo: Photo) => ({
      photo,
      tasks: report.tasks.filter((task: Task) => task.photo_id === photo.id),
    }))
  );

  if (!photos || photos.length === 0) {
    return <p>Aucune photo disponible.</p>;
  }

  return (
    <section className="grid" style={{ gap: 20 }}>
      {photos.map(({ photo, tasks }) => (
        <PhotoCard key={photo.id} photo={photo} tasks={tasks} />
      ))}
    </section>
  );
}
