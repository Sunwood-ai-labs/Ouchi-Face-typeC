from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration sourced from environment variables."""

    model_config = SettingsConfigDict(env_prefix="OUCHI_", env_file=('.env',), case_sensitive=False)

    database_url: str = Field(default="sqlite+aiosqlite:///./data/ouchi_face.db")
    repo_storage_dir: Path = Field(default=Path("data/repos"))
    health_check_interval_seconds: int = Field(default=120, ge=30)
    health_request_timeout: int = Field(default=10, ge=1)
    allow_origins: list[str] = Field(default_factory=lambda: ["*"])
    github_client_id: Optional[str] = None
    github_client_secret: Optional[str] = None
    forgejo_base_url: Optional[AnyUrl] = None


settings = Settings()
settings.repo_storage_dir.mkdir(parents=True, exist_ok=True)
