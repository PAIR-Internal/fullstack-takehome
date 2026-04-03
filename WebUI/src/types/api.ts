export type LessonStatus = "not_started" | "in_progress" | "completed";
export type UserProgressStatus = "seen" | "completed";

export interface ProgressSummary {
  total_blocks: number;
  seen_blocks: number;
  completed_blocks: number;
  last_seen_block_id: number | null;
  completed: boolean;
}

export interface LessonListItem {
  id: number;
  slug: string;
  title: string;
  status: LessonStatus;
  next_block_id: number | null;
  progress_summary: ProgressSummary;
}

export interface Variant {
  id: number;
  tenant_id: number | null;
  data: Record<string, unknown>;
}

export interface LessonBlock {
  id: number;
  type: string;
  position: number;
  variant: Variant;
  user_progress: UserProgressStatus | null;
}

export interface LessonResponse {
  lesson: {
    id: number;
    slug: string;
    title: string;
  };
  blocks: LessonBlock[];
  progress_summary: ProgressSummary;
}

export interface LessonListResponse {
  lessons: LessonListItem[];
}

export interface ProgressUpsertRequest {
  block_id: number;
  status: UserProgressStatus;
}

export interface ProgressUpsertResponse {
  stored_status: UserProgressStatus;
  progress_summary: ProgressSummary;
}
