import type {
  LessonListResponse,
  LessonResponse,
  ProgressUpsertRequest,
  ProgressUpsertResponse,
} from "@/types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
const TENANT_ID = 1;
const USER_ID = 10;

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    const payload = (await response.json().catch(() => null)) as
      | { error?: { message?: string } }
      | null;
    throw new Error(payload?.error?.message ?? "Request failed");
  }

  return (await response.json()) as T;
}

export function fetchLessons(): Promise<LessonListResponse> {
  return request<LessonListResponse>(
    `/tenants/${TENANT_ID}/users/${USER_ID}/lessons`,
  );
}

export function fetchLesson(lessonId: number): Promise<LessonResponse> {
  return request<LessonResponse>(
    `/tenants/${TENANT_ID}/users/${USER_ID}/lessons/${lessonId}`,
  );
}

export function updateBlockProgress(
  lessonId: number,
  payload: ProgressUpsertRequest,
): Promise<ProgressUpsertResponse> {
  return request<ProgressUpsertResponse>(
    `/tenants/${TENANT_ID}/users/${USER_ID}/lessons/${lessonId}/progress`,
    {
      method: "PUT",
      body: JSON.stringify(payload),
    },
  );
}
