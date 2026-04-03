from dataclasses import dataclass
from typing import Protocol

from inversity_api.data_structures.schemas.lessons import (
    LessonListResponse,
    LessonResponse,
    ProgressSummary,
    ProgressUpsertRequest,
    ProgressUpsertResponse,
)
from inversity_api.services.exceptions import ApiError


class LessonRepository(Protocol):
    def list_lessons(self, tenant_id: int, user_id: int) -> LessonListResponse: ...

    def get_lesson(
        self,
        tenant_id: int,
        user_id: int,
        lesson_id: int,
    ) -> LessonResponse: ...

    def upsert_progress(
        self,
        tenant_id: int,
        user_id: int,
        lesson_id: int,
        payload: ProgressUpsertRequest,
    ) -> ProgressUpsertResponse: ...


@dataclass
class LessonProgressService:
    repository: LessonRepository

    def list_lessons(self, tenant_id: int, user_id: int) -> LessonListResponse:
        return self.repository.list_lessons(tenant_id=tenant_id, user_id=user_id)

    def get_lesson(
        self,
        tenant_id: int,
        user_id: int,
        lesson_id: int,
    ) -> LessonResponse:
        return self.repository.get_lesson(
            tenant_id=tenant_id,
            user_id=user_id,
            lesson_id=lesson_id,
        )

    def upsert_progress(
        self,
        tenant_id: int,
        user_id: int,
        lesson_id: int,
        payload: ProgressUpsertRequest,
    ) -> ProgressUpsertResponse:
        return self.repository.upsert_progress(
            tenant_id=tenant_id,
            user_id=user_id,
            lesson_id=lesson_id,
            payload=payload,
        )


def build_progress_summary(
    *,
    ordered_block_ids: list[int],
    progress_by_block_id: dict[int, str],
) -> ProgressSummary:
    seen_blocks = 0
    completed_blocks = 0
    last_seen_block_id: int | None = None

    for block_id in ordered_block_ids:
        status = progress_by_block_id.get(block_id)
        if status is None:
            continue

        last_seen_block_id = block_id
        if status in {"seen", "completed"}:
            seen_blocks += 1
        if status == "completed":
            completed_blocks += 1

    total_blocks = len(ordered_block_ids)
    return ProgressSummary(
        total_blocks=total_blocks,
        seen_blocks=seen_blocks,
        completed_blocks=completed_blocks,
        last_seen_block_id=last_seen_block_id,
        completed=total_blocks > 0 and completed_blocks == total_blocks,
    )


def derive_lesson_status(summary: ProgressSummary) -> str:
    if summary.completed:
        return "completed"
    if summary.seen_blocks > 0:
        return "in_progress"
    return "not_started"


def ensure(condition: bool, *, code: str, message: str, status_code: int) -> None:
    if not condition:
        raise ApiError(code=code, message=message, status_code=status_code)
