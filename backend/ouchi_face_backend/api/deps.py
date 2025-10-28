from __future__ import annotations

from sqlmodel.ext.asyncio.session import AsyncSession

from ..db.session import get_session


async def get_db_session() -> AsyncSession:
    async with get_session() as session:
        yield session
