import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";

export function useReports() {
  return useQuery({ queryKey: ["reports"], queryFn: api.listReports });
}

export function useReport(reportId?: number) {
  return useQuery({
    queryKey: ["report", reportId],
    queryFn: () => {
      if (!reportId) throw new Error("Report id manquant");
      return api.getReport(reportId);
    },
    enabled: Boolean(reportId),
  });
}
