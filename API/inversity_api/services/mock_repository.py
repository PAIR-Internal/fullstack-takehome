from copy import deepcopy
from dataclasses import dataclass, field

from inversity_api.data_structures.schemas.lessons import (
    LessonBlock,
    LessonListItem,
    LessonListResponse,
    LessonMetadata,
    LessonResponse,
    ProgressUpsertRequest,
    ProgressUpsertResponse,
    Variant,
)
from inversity_api.services.lesson_progress import (
    build_progress_summary,
    derive_lesson_status,
    ensure,
)


@dataclass
class BlockVariantSeed:
    id: int
    tenant_id: int | None
    data: dict[str, object]


@dataclass
class BlockSeed:
    id: int
    block_type: str
    position: int
    variants: list[BlockVariantSeed]


@dataclass
class LessonSeed:
    id: int
    tenant_id: int
    slug: str
    title: str
    blocks: list[BlockSeed]


@dataclass
class MockLessonRepository:
    tenant_ids: set[int] = field(default_factory=lambda: {1, 2})
    user_tenant_map: dict[int, int] = field(
        default_factory=lambda: {
            10: 1,
            11: 1,
            20: 2,
        }
    )
    lessons: dict[int, LessonSeed] = field(default_factory=dict)
    progress_rows: dict[tuple[int, int, int], str] = field(
        default_factory=lambda: {
            (10, 100, 200): "completed",
            (10, 100, 201): "seen",
            (10, 101, 203): "seen",
        }
    )

    def __post_init__(self) -> None:
        if self.lessons:
            return

        self.lessons = {
            100: LessonSeed(
                id=100,
                tenant_id=1,
                slug="prompt-basics",
                title="Prompt Basics",
                blocks=[
                    BlockSeed(
                        id=200,
                        block_type="markdown",
                        position=1,
                        variants=[
                            BlockVariantSeed(
                                id=300,
                                tenant_id=None,
                                data={
                                    "heading": "Start with the task",
                                    "body": "Describe the outcome before you describe the tool or the technique.",
                                },
                            )
                        ],
                    ),
                    BlockSeed(
                        id=201,
                        block_type="markdown",
                        position=2,
                        variants=[
                            BlockVariantSeed(
                                id=301,
                                tenant_id=None,
                                data={
                                    "heading": "Give the model constraints",
                                    "body": "Be concrete about format, length, and the level of confidence you want back.",
                                },
                            ),
                            BlockVariantSeed(
                                id=302,
                                tenant_id=1,
                                data={
                                    "heading": "Give the learner constraints",
                                    "body": "PAIR-style prompt work is strongest when the request includes audience, tone, and success criteria.",
                                },
                            ),
                        ],
                    ),
                    BlockSeed(
                        id=202,
                        block_type="quiz",
                        position=3,
                        variants=[
                            BlockVariantSeed(
                                id=303,
                                tenant_id=None,
                                data={
                                    "heading": "Quick checkpoint",
                                    "body": "What is the clearest signal that a prompt has enough structure?",
                                },
                            )
                        ],
                    ),
                ],
            ),
            101: LessonSeed(
                id=101,
                tenant_id=1,
                slug="shipping-feedback",
                title="Shipping Feedback",
                blocks=[
                    BlockSeed(
                        id=203,
                        block_type="markdown",
                        position=1,
                        variants=[
                            BlockVariantSeed(
                                id=304,
                                tenant_id=None,
                                data={
                                    "heading": "Start with the risk",
                                    "body": "Lead with the issue, then explain why it matters, then offer the next action.",
                                },
                            )
                        ],
                    ),
                    BlockSeed(
                        id=204,
                        block_type="markdown",
                        position=2,
                        variants=[
                            BlockVariantSeed(
                                id=305,
                                tenant_id=None,
                                data={
                                    "heading": "Keep momentum",
                                    "body": "Good collaboration sounds calm, precise, and easy to act on.",
                                },
                            )
                        ],
                    ),
                ],
            ),
        }

    def list_lessons(self, tenant_id: int, user_id: int) -> LessonListResponse:
        self._validate_tenant_and_user(tenant_id=tenant_id, user_id=user_id)

        lessons = [
            lesson for lesson in self.lessons.values() if lesson.tenant_id == tenant_id
        ]
        items: list[LessonListItem] = []

        for lesson in sorted(lessons, key=lambda item: item.id):
            ordered_block_ids = [block.id for block in sorted(lesson.blocks, key=lambda item: item.position)]
            summary = build_progress_summary(
                ordered_block_ids=ordered_block_ids,
                progress_by_block_id=self._progress_for_lesson(
                    user_id=user_id,
                    lesson_id=lesson.id,
                ),
            )
            next_block_id = next(
                (
                    block_id
                    for block_id in ordered_block_ids
                    if self.progress_rows.get((user_id, lesson.id, block_id)) != "completed"
                ),
                None,
            )
            items.append(
                LessonListItem(
                    id=lesson.id,
                    slug=lesson.slug,
                    title=lesson.title,
                    status=derive_lesson_status(summary),
                    next_block_id=next_block_id,
                    progress_summary=summary,
                )
            )

        return LessonListResponse(lessons=items)

    def get_lesson(self, tenant_id: int, user_id: int, lesson_id: int) -> LessonResponse:
        lesson = self._validate_lesson_context(
            tenant_id=tenant_id,
            user_id=user_id,
            lesson_id=lesson_id,
        )
        blocks = sorted(lesson.blocks, key=lambda item: item.position)
        lesson_progress = self._progress_for_lesson(user_id=user_id, lesson_id=lesson_id)

        response_blocks = [
            LessonBlock(
                id=block.id,
                type=block.block_type,
                position=block.position,
                variant=self._select_variant(tenant_id=tenant_id, variants=block.variants),
                user_progress=lesson_progress.get(block.id),
            )
            for block in blocks
        ]

        progress_summary = build_progress_summary(
            ordered_block_ids=[block.id for block in blocks],
            progress_by_block_id=lesson_progress,
        )

        return LessonResponse(
            lesson=LessonMetadata(
                id=lesson.id,
                slug=lesson.slug,
                title=lesson.title,
            ),
            blocks=response_blocks,
            progress_summary=progress_summary,
        )

    def upsert_progress(
        self,
        tenant_id: int,
        user_id: int,
        lesson_id: int,
        payload: ProgressUpsertRequest,
    ) -> ProgressUpsertResponse:
        lesson = self._validate_lesson_context(
            tenant_id=tenant_id,
            user_id=user_id,
            lesson_id=lesson_id,
        )
        block_ids = {block.id for block in lesson.blocks}
        ensure(
            payload.block_id in block_ids,
            code="invalid_block",
            message="The provided block does not belong to this lesson.",
            status_code=400,
        )

        key = (user_id, lesson_id, payload.block_id)
        existing_status = self.progress_rows.get(key)

        if existing_status == "completed" and payload.status == "seen":
            stored_status = "completed"
        else:
            stored_status = payload.status

        self.progress_rows[key] = stored_status

        summary = build_progress_summary(
            ordered_block_ids=[block.id for block in sorted(lesson.blocks, key=lambda item: item.position)],
            progress_by_block_id=self._progress_for_lesson(user_id=user_id, lesson_id=lesson_id),
        )

        return ProgressUpsertResponse(
            stored_status=stored_status,
            progress_summary=summary,
        )

    def _validate_tenant_and_user(self, *, tenant_id: int, user_id: int) -> None:
        ensure(
            tenant_id in self.tenant_ids,
            code="tenant_not_found",
            message="Tenant not found.",
            status_code=404,
        )
        ensure(
            self.user_tenant_map.get(user_id) == tenant_id,
            code="user_not_found",
            message="User not found for tenant.",
            status_code=404,
        )

    def _validate_lesson_context(
        self,
        *,
        tenant_id: int,
        user_id: int,
        lesson_id: int,
    ) -> LessonSeed:
        self._validate_tenant_and_user(tenant_id=tenant_id, user_id=user_id)
        lesson = self.lessons.get(lesson_id)
        ensure(
            lesson is not None and lesson.tenant_id == tenant_id,
            code="lesson_not_found",
            message="Lesson not found for tenant.",
            status_code=404,
        )
        return lesson

    def _progress_for_lesson(self, *, user_id: int, lesson_id: int) -> dict[int, str]:
        lesson_progress: dict[int, str] = {}
        for (stored_user_id, stored_lesson_id, block_id), status in self.progress_rows.items():
            if stored_user_id == user_id and stored_lesson_id == lesson_id:
                lesson_progress[block_id] = status
        return lesson_progress

    def _select_variant(
        self,
        *,
        tenant_id: int,
        variants: list[BlockVariantSeed],
    ) -> Variant:
        selected = next((variant for variant in variants if variant.tenant_id == tenant_id), None)
        if selected is None:
            selected = next((variant for variant in variants if variant.tenant_id is None), None)

        ensure(
            selected is not None,
            code="variant_not_found",
            message="No variant was available for the requested block.",
            status_code=500,
        )

        return Variant(
            id=selected.id,
            tenant_id=selected.tenant_id,
            data=deepcopy(selected.data),
        )
