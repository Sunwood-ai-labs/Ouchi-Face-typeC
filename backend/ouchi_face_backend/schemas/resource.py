from __future__ import annotations

from datetime import datetime, date
from typing import Literal, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator

from ..models.resource import ResourceKind, ResourceSource


class ResourceMetadata(BaseModel):
    kind: ResourceKind
    name: str
    description: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    url: Optional[HttpUrl] = None
    path: Optional[str] = None
    repo: Optional[HttpUrl] = None
    healthcheck: Optional[str] = None
    owner: Optional[str] = None
    license: Optional[str] = None
    thumbnail: Optional[str] = None
    updated: Optional[date | datetime] = None

    @field_validator("tags", mode="before")
    @classmethod
    def ensure_list(cls, value):
        if not value:
            return []
        if isinstance(value, str):
            return [value]
        return list(value)


class ManualResourceCreate(BaseModel):
    source_type: Literal["manual"] = "manual"
    metadata: ResourceMetadata


class RepoResourceCreate(BaseModel):
    source_type: Literal["repository"] = "repository"
    repo_url: HttpUrl
    branch: Optional[str] = None
    subpath: Optional[str] = None


ResourceCreateRequest = ManualResourceCreate | RepoResourceCreate


class ResourceRead(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    kind: ResourceKind
    name: str
    slug: str
    description: Optional[str]
    tags: list[str]
    url: Optional[str]
    path: Optional[str]
    repo_url: Optional[str]
    owner: Optional[str]
    thumbnail_path: Optional[str]
    license: Optional[str]
    healthcheck_path: Optional[str]
    updated_at: Optional[datetime]
    last_synced_at: Optional[datetime]
    health_status: str
    health_checked_at: Optional[datetime]
    source: ResourceSource
    created_at: datetime
    modified_at: datetime


class ResourceListResponse(BaseModel):
    items: list[ResourceRead]
    total: int


class SyncResponse(BaseModel):
    resource: ResourceRead
    refreshed: bool


class ResourceHealthResponse(BaseModel):
    resource_id: int
    status: str
    checked_at: Optional[datetime]
