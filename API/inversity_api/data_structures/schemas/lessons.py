from typing import Any, Literal

from pydantic import BaseModel


ProgressStatus = Literal["seen", "completed"]
LessonStatus = Literal["not_started", "in_progress", "completed"]


class ProgressSummary(BaseModel):
    total_blocks: int
    seen_blocks: int
    completed_blocks: int
    last_seen_block_id: int | None
    completed: bool


class LessonListItem(BaseModel):
    id: int
    slug: str
    title: str
    status: LessonStatus
    next_block_id: int | None
    progress_summary: ProgressSummary


class LessonListResponse(BaseModel):
    lessons: list[LessonListItem]


class Variant(BaseModel):
    id: int
    tenant_id: int | None
    data: dict[str, Any]


class LessonBlock(BaseModel):
    id: int
    type: str
    position: int
    variant: Variant
    user_progress: ProgressStatus | None = None


class LessonMetadata(BaseModel):
    id: int
    slug: str
    title: str


class LessonResponse(BaseModel):
    lesson: LessonMetadata
    blocks: list[LessonBlock]
    progress_summary: ProgressSummary


class ProgressUpsertRequest(BaseModel):
    block_id: int
    status: ProgressStatus


class ProgressUpsertResponse(BaseModel):
    stored_status: ProgressStatus
    progress_summary: ProgressSummary
