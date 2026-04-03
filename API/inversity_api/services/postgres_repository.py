from inversity_api.data_structures.schemas.lessons import (
    LessonListResponse,
    LessonResponse,
    ProgressUpsertRequest,
    ProgressUpsertResponse,
)


class PostgresLessonRepository:
    """
    Swap the mock repository for SQL-backed queries here when moving from scaffold to
    exercise implementation.

    Suggested next step:
    - validate tenant / user / lesson ownership up front
    - assemble variants with tenant override > default
    - derive summaries from lesson block order plus user_block_progress
    """

    def list_lessons(self, tenant_id: int, user_id: int) -> LessonListResponse:
        raise NotImplementedError("Implement lesson list queries against Postgres.")

    def get_lesson(
        self,
        tenant_id: int,
        user_id: int,
        lesson_id: int,
    ) -> LessonResponse:
        raise NotImplementedError("Implement lesson assembly queries against Postgres.")

    def upsert_progress(
        self,
        tenant_id: int,
        user_id: int,
        lesson_id: int,
        payload: ProgressUpsertRequest,
    ) -> ProgressUpsertResponse:
        raise NotImplementedError("Implement progress upsert queries against Postgres.")
