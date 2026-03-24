from functools import lru_cache
from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="Media Server", validation_alias=AliasChoices("APP_NAME", "app_name"))
    secret_key: str = Field(default="change-me", validation_alias=AliasChoices("SECRET_KEY", "secret_key"))
    access_token_expire_minutes: int = Field(
        default=60 * 24,
        validation_alias=AliasChoices("ACCESS_TOKEN_EXPIRE_MINUTES", "access_token_expire_minutes"),
    )

    sqlite_url: str = Field(
        default="sqlite:///./data/media_server.db",
        validation_alias=AliasChoices("SQLITE_URL", "sqlite_url"),
    )
    postgres_url: str | None = Field(default=None, validation_alias=AliasChoices("POSTGRES_URL", "postgres_url"))

    media_dirs: str = Field(default="/media", validation_alias=AliasChoices("MEDIA_DIRS", "media_dirs"))
    config_dir: str = Field(default="/config", validation_alias=AliasChoices("CONFIG_DIR", "config_dir"))
    transcode_dir: str = Field(default="/transcode", validation_alias=AliasChoices("TRANSCODE_DIR", "transcode_dir"))

    tmdb_api_key: str = Field(default="", validation_alias=AliasChoices("TMDB_API_KEY", "tmdb_api_key"))
    tmdb_base_url: str = Field(
        default="https://api.themoviedb.org/3",
        validation_alias=AliasChoices("TMDB_BASE_URL", "tmdb_base_url"),
    )

    cors_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        validation_alias=AliasChoices("CORS_ORIGINS", "cors_origins"),
    )

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


@lru_cache
def get_settings() -> Settings:
    return Settings()
