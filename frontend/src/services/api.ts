import { Report } from "../types/report";

const API_URL = import.meta.env.VITE_API_URL || "/api";

async function handle<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "API error");
  }
  return response.json() as Promise<T>;
}

export const api = {
  async listReports(): Promise<Report[]> {
    const res = await fetch(`${API_URL}/reports`);
    return handle<Report[]>(res);
  },
  async getReport(id: number): Promise<Report> {
    const res = await fetch(`${API_URL}/reports/${id}`);
    return handle<Report>(res);
  },
};
