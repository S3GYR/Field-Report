import React from "react";
import { Route, Routes, Navigate } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import ReportPage from "./pages/ReportPage";
import PhotosPage from "./pages/PhotosPage";
import TasksPage from "./pages/TasksPage";
import ExportPage from "./pages/ExportPage";
import ShellLayout from "./components/ShellLayout";

function App() {
  return (
    <ShellLayout>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/reports/:id" element={<ReportPage />} />
        <Route path="/photos" element={<PhotosPage />} />
        <Route path="/tasks" element={<TasksPage />} />
        <Route path="/export" element={<ExportPage />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </ShellLayout>
  );
}

export default App;
