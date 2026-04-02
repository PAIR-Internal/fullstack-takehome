from functools import lru_cache

from inversity_api.config.app_config import get_app_settings
from inversity_api.services.lesson_progress import LessonProgressService
from inversity_api.services.mock_repository import MockLessonRepository
from inversity_api.services.postgres_repository import PostgresLessonRepository


@lru_cache
def get_lesson_progress_service() -> LessonProgressService:
    settings = get_app_settings()
    repository = MockLessonRepository() if settings.use_mock_data else PostgresLessonRepository()
    return LessonProgressService(repository=repository)
