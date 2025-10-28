from __future__ import annotations

import asyncio
from datetime import date
from pathlib import Path

import pytest
from sqlalchemy import text
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession, create_async_engine

from ouchi_face_backend.models.resource import ResourceKind, ResourceSource
from ouchi_face_backend.schemas.resource import ManualResourceCreate, ResourceMetadata
from ouchi_face_backend.services.repo_sync import RepoSyncService
from ouchi_face_backend.services.resource_service import ResourceService


@pytest.fixture()
async def session(tmp_path: Path) -> AsyncSession:
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        await conn.execute(
            text(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS resources_fts USING fts5(
                    name, description, tags, content='', content_rowid='id'
                )
                """
            )
        )
    async_session = AsyncSession(engine)
    try:
        yield async_session
    finally:
        await async_session.close()
        await engine.dispose()


@pytest.mark.asyncio()
async def test_create_manual_resource(session: AsyncSession, tmp_path: Path) -> None:
    service = ResourceService(session, repo_sync=RepoSyncService(storage_dir=tmp_path))
    payload = ManualResourceCreate(
        metadata=ResourceMetadata(
            kind=ResourceKind.APP,
            name="Vector Dashboard",
            description="Self-hosted dashboard",
            tags=["dashboard", "internal"],
            url="http://localhost:9000",
            owner="@alice",
            license="MIT",
            healthcheck="/health",
            updated=date(2024, 5, 4),
        )
    )
    resource = await service.create_or_update(payload)

    assert resource.slug == "vector-dashboard"
    assert resource.source == ResourceSource.MANUAL
    assert resource.healthcheck_path == "/health"


@pytest.mark.asyncio()
async def test_search_resources(session: AsyncSession, tmp_path: Path) -> None:
    service = ResourceService(session, repo_sync=RepoSyncService(storage_dir=tmp_path))
    payload = ManualResourceCreate(
        metadata=ResourceMetadata(
            kind=ResourceKind.DATASET,
            name="Local Logs",
            description="System metrics dataset",
            tags=["metrics", "logs"],
        )
    )
    await service.create_or_update(payload)

    payload2 = ManualResourceCreate(
        metadata=ResourceMetadata(
            kind=ResourceKind.MODEL,
            name="Speech Model",
            description="Audio inference",
            tags=["audio"],
        )
    )
    await service.create_or_update(payload2)

    resources, total = await service.list_resources(q="metrics", limit=10)
    assert total == 1
    assert resources[0].name == "Local Logs"
