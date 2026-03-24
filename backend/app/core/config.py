from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    app_name: str = "Media Server"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60 * 24

    sqlite_url: str = "sqlite:///./data/media_server.db"
    postgres_url: str | None = None

    media_dirs: str = "/media"
    config_dir: str = "/config"
    transcode_dir: str = "/transcode"

    tmdb_api_key: str = ""
    tmdb_base_url: str = "https://api.themoviedb.org/3"

    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    @property
    def database_url(self) -> str:
        return self.postgres_url or self.sqlite_url

    @property
    def media_paths(self) -> list[str]:
        return [p.strip() for p in self.media_dirs.split(",") if p.strip()]

    @property
    def cors_origin_list(self) -> list[str]:
        return [p.strip() for p in self.cors_origins.split(",") if p.strip()]

    @field_validator("secret_key")
    @classmethod
    def validate_secret(cls, v: str) -> str:
        if v == "change-me":
            return v
        if len(v) < 16:
            raise ValueError("secret_key must be at least 16 characters")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
