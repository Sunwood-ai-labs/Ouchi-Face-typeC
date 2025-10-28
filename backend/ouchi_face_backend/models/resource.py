from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.types import JSON
from sqlmodel import Field, SQLModel


class ResourceKind(str, Enum):
    APP = "app"
    DATASET = "dataset"
    MODEL = "model"


class ResourceSource(str, Enum):
    MANUAL = "manual"
    REPOSITORY = "repository"


class Resource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    kind: ResourceKind
    name: str = Field(index=True)
    slug: str = Field(index=True, sa_column_kwargs={"unique": True})
    description: Optional[str] = None
    tags: list[str] = Field(default_factory=list, sa_column=Column(JSON, nullable=False))
    url: Optional[str] = None
    path: Optional[str] = None
    repo_url: Optional[str] = Field(default=None, index=True)
    owner: Optional[str] = None
    thumbnail_path: Optional[str] = None
    license: Optional[str] = None
    healthcheck_path: Optional[str] = None
    updated_at: Optional[datetime] = None
    last_synced_at: Optional[datetime] = None
    health_status: str = Field(default="unknown", index=True)
    health_checked_at: Optional[datetime] = None
    source: ResourceSource = Field(default=ResourceSource.MANUAL, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    modified_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    def touch(self) -> None:
        self.modified_at = datetime.utcnow()
