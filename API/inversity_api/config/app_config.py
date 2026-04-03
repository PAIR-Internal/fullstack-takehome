from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_environment: str = "dev"
    cors_origins: list[str] = ["http://localhost:5173"]
    database_url: str = "postgresql://pair:pair@localhost:5432/pair_takehome"
    use_mock_data: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="PAIR_",
        extra="ignore",
    )


@lru_cache
def get_app_settings() -> AppSettings:
    return AppSettings()
