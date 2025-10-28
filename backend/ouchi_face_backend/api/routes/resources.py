from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from ...models.resource import ResourceKind
from ...schemas.resource import (
    RepoResourceCreate,
    ResourceCreateRequest,
    ResourceHealthResponse,
    ResourceListResponse,
    ResourceRead,
    SyncResponse,
)
from ...services.resource_service import ResourceService, to_read_model
from ..deps import get_db_session

router = APIRouter(prefix="/api/resources", tags=["resources"])


def get_service(session: AsyncSession = Depends(get_db_session)) -> ResourceService:
    return ResourceService(session)


@router.get("", response_model=ResourceListResponse)
async def list_resources(
    *,
    service: ResourceService = Depends(get_service),
    q: str | None = Query(default=None, description="Full text search query"),
    kind: ResourceKind | None = None,
    tag: str | None = None,
    owner: str | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> ResourceListResponse:
    resources, total = await service.list_resources(q=q, kind=kind, tag=tag, owner=owner, limit=limit, offset=offset)
    return ResourceListResponse(items=[await to_read_model(res) for res in resources], total=total)


@router.post("", response_model=ResourceRead)
async def create_resource(
    payload: ResourceCreateRequest,
    service: ResourceService = Depends(get_service),
) -> ResourceRead:
    resource = await service.create_or_update(payload)
    return await to_read_model(resource)


@router.get("/{resource_id}", response_model=ResourceRead)
async def read_resource(resource_id: int, service: ResourceService = Depends(get_service)) -> ResourceRead:
    resource = await service.get_resource(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return await to_read_model(resource)


@router.get("/slug/{slug}", response_model=ResourceRead)
async def read_resource_by_slug(slug: str, service: ResourceService = Depends(get_service)) -> ResourceRead:
    resource = await service.get_by_slug(slug)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return await to_read_model(resource)


@router.post("/{resource_id}/sync", response_model=SyncResponse)
async def sync_resource(resource_id: int, service: ResourceService = Depends(get_service)) -> SyncResponse:
    resource = await service.get_resource(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    if not resource.repo_url:
        raise HTTPException(status_code=400, detail="Resource does not have a repository source")

    payload = RepoResourceCreate(repo_url=resource.repo_url)
    refreshed = await service.create_or_update(payload)
    return SyncResponse(resource=await to_read_model(refreshed), refreshed=True)


@router.get("/{resource_id}/health", response_model=ResourceHealthResponse)
async def resource_health(resource_id: int, service: ResourceService = Depends(get_service)) -> ResourceHealthResponse:
    resource = await service.get_resource(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return ResourceHealthResponse(resource_id=resource.id, status=resource.health_status, checked_at=resource.health_checked_at)
