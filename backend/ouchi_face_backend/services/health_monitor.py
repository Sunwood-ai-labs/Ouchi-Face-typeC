from __future__ import annotations

from datetime import datetime
from urllib.parse import urljoin

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from ..core.config import settings
from ..db.session import get_session
from ..models.resource import Resource


class HealthMonitor:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        self.client = httpx.AsyncClient(timeout=settings.health_request_timeout)

    async def start(self) -> None:
        self.scheduler.add_job(self._run_checks, "interval", seconds=settings.health_check_interval_seconds)
        self.scheduler.start()

    async def shutdown(self) -> None:
        await self.client.aclose()
        if self.scheduler.running:
            self.scheduler.shutdown()

    async def _run_checks(self) -> None:
        async with get_session() as session:
            result = await session.exec(select(Resource).where(Resource.url.is_not(None)))
            resources = result.all()
            for resource in resources:
                await self._check_resource(session, resource)
            await session.commit()

    async def _check_resource(self, session, resource: Resource) -> None:
        if not resource.url:
            return
        target = resource.url
        if resource.healthcheck_path:
            target = urljoin(resource.url.rstrip("/") + "/", resource.healthcheck_path.lstrip("/"))
        try:
            response = await self.client.get(target)
            resource.health_status = "up" if response.is_success else "down"
        except httpx.HTTPError:
            resource.health_status = "down"
        resource.health_checked_at = datetime.utcnow()
        await session.flush()
