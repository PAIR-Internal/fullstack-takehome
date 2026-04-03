from fastapi import APIRouter, Depends

from inversity_api.data_structures.schemas.lessons import (
    LessonListResponse,
    LessonResponse,
    ProgressUpsertRequest,
    ProgressUpsertResponse,
)
from inversity_api.dependencies import get_lesson_progress_service
from inversity_api.services.lesson_progress import LessonProgressService

router = APIRouter(prefix="/tenants/{tenant_id}/users/{user_id}/lessons", tags=["lessons"])


@router.get("")
def list_lessons(
    tenant_id: int,
    user_id: int,
    lesson_progress_service: LessonProgressService = Depends(get_lesson_progress_service),
) -> LessonListResponse:
    return lesson_progress_service.list_lessons(tenant_id=tenant_id, user_id=user_id)


@router.get("/{lesson_id}")
def get_lesson(
    tenant_id: int,
    user_id: int,
    lesson_id: int,
    lesson_progress_service: LessonProgressService = Depends(get_lesson_progress_service),
) -> LessonResponse:
    return lesson_progress_service.get_lesson(
        tenant_id=tenant_id,
        user_id=user_id,
        lesson_id=lesson_id,
    )


@router.put("/{lesson_id}/progress")
def upsert_progress(
    tenant_id: int,
    user_id: int,
    lesson_id: int,
    payload: ProgressUpsertRequest,
    lesson_progress_service: LessonProgressService = Depends(get_lesson_progress_service),
) -> ProgressUpsertResponse:
    return lesson_progress_service.upsert_progress(
        tenant_id=tenant_id,
        user_id=user_id,
        lesson_id=lesson_id,
        payload=payload,
    )
