from __future__ import annotations

from typing import Iterable

from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.resource import Resource


async def upsert_resource_fts(session: AsyncSession, resource: Resource) -> None:
    await session.exec(text("DELETE FROM resources_fts WHERE rowid = :id").bindparams(id=resource.id))
    await session.exec(
        text(
            """
            INSERT INTO resources_fts(rowid, name, description, tags)
            VALUES (:id, :name, :description, :tags)
            """
        ).bindparams(
            id=resource.id,
            name=resource.name,
            description=resource.description or "",
            tags=" ".join(resource.tags or []),
        )
    )


async def remove_resource_fts(session: AsyncSession, resource_id: int) -> None:
    await session.exec(text("DELETE FROM resources_fts WHERE rowid = :id").bindparams(id=resource_id))


async def search_resource_ids(session: AsyncSession, query: str) -> Iterable[int]:
    result = await session.exec(
        text("SELECT rowid FROM resources_fts WHERE resources_fts MATCH :match").bindparams(match=query)
    )
    return [row for row in result.scalars().all()]
