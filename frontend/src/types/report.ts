export type ReportStatus = "draft" | "in_review" | "approved" | "archived";
export type WeatherType = "sunny" | "cloudy" | "rain" | "storm" | "snow" | "fog" | "unknown";
export type TaskStatus = "todo" | "in_progress" | "done" | "blocked";
export type PhotoPriority = "high" | "medium" | "low" | "none";

export interface Photo {
  id: number;
  report_id?: number;
  filename: string;
  filepath: string;
  thumbnail?: string;
  comment?: string;
  priority: PhotoPriority;
  gps_lat?: number;
  gps_lng?: number;
}

export interface Task {
  id: number;
  report_id?: number;
  photo_id?: number | null;
  description: string;
  status: TaskStatus;
  estimated_cost?: number | null;
  estimated_duration?: number | null;
}

export interface Signature {
  id: number;
  name: string;
  role?: string;
  signed_on?: string;
  signature_image?: string;
}

export interface Report {
  id: number;
  number: string;
  visit_date: string;
  client: string;
  site: string;
  weather: WeatherType;
  comments?: string;
  status: ReportStatus;
  created_at: string;
  updated_at: string;
  photos: Photo[];
  tasks: Task[];
  signature?: Signature | null;
}
