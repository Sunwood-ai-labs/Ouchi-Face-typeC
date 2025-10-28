from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import resources
from .core.config import settings
from .db.session import init_db
from .services.health_monitor import HealthMonitor

health_monitor = HealthMonitor()


def create_app() -> FastAPI:
    app = FastAPI(title="Ouchi Face API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(resources.router)

    @app.on_event("startup")
    async def on_startup() -> None:  # noqa: D401 - FastAPI hook
        await init_db()
        await health_monitor.start()

    @app.on_event("shutdown")
    async def on_shutdown() -> None:  # noqa: D401 - FastAPI hook
        await health_monitor.shutdown()

    return app


app = create_app()
