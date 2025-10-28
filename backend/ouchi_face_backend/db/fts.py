from __future__ import annotations

from typing import Iterable

from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.resource import Resource


async def upsert_resource_fts(session: AsyncSession, resource: Resource) -> None:
    await session.execute(text("DELETE FROM resources_fts WHERE rowid = :id"), {"id": resource.id})
    await session.execute(
        text(
            """
            INSERT INTO resources_fts(rowid, name, description, tags)
            VALUES (:id, :name, :description, :tags)
            """
        ),
        {
            "id": resource.id,
            "name": resource.name,
            "description": resource.description or "",
            "tags": " ".join(resource.tags or []),
        },
    )


async def remove_resource_fts(session: AsyncSession, resource_id: int) -> None:
    await session.execute(text("DELETE FROM resources_fts WHERE rowid = :id"), {"id": resource_id})


async def search_resource_ids(session: AsyncSession, query: str) -> Iterable[int]:
    result = await session.execute(
        text("SELECT rowid FROM resources_fts WHERE resources_fts MATCH :match"),
        {"match": query},
    )
    return [row[0] for row in result.fetchall()]
