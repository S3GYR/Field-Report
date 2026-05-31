import React from "react";
import { useReports } from "../hooks/useReports";
import { Task, Report } from "../types/report";

export default function TasksPage() {
  const { data, isLoading, error } = useReports();

  if (isLoading) return <div>Chargement…</div>;
  if (error) return <div>Erreur : {(error as Error).message}</div>;

  const tasks = data?.flatMap((report: Report) =>
    report.tasks.map((task: Task) => ({ task, report }))
  );

  if (!tasks || tasks.length === 0) {
    return <p>Aucune tâche enregistrée.</p>;
  }

  return (
    <section className="card">
      <h2>Tâches</h2>
      <table className="recap-table">
        <thead>
          <tr>
            <th>Rapport</th>
            <th>Description</th>
            <th>Statut</th>
            <th>Coût estimé</th>
            <th>Durée</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map(({ task, report }) => (
            <tr key={task.id}>
              <td>{report.number}</td>
              <td>{task.description}</td>
              <td>{task.status}</td>
              <td>{task.estimated_cost ?? "—"}</td>
              <td>{task.estimated_duration ?? "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
