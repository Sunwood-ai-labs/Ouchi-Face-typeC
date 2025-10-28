from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import text
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncEngine, AsyncSession, create_async_engine

from ..core.config import settings


engine: AsyncEngine = create_async_engine(settings.database_url, echo=False, future=True)


async def init_db() -> None:
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


@asynccontextmanager
def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session
