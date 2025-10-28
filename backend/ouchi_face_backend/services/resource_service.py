from __future__ import annotations

from datetime import datetime, date
from typing import Iterable, Sequence

from sqlalchemy import case, select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..db.fts import remove_resource_fts, search_resource_ids, upsert_resource_fts
from ..models.resource import Resource, ResourceKind, ResourceSource
from ..schemas.resource import (
    RepoResourceCreate,
    ResourceCreateRequest,
    ResourceMetadata,
    ResourceRead,
)
from ..utils.slugify import slugify
from .repo_sync import RepoSyncService


class ResourceService:
    def __init__(self, session: AsyncSession, repo_sync: RepoSyncService | None = None) -> None:
        self.session = session
        self.repo_sync = repo_sync or RepoSyncService()

    async def list_resources(
        self,
        *,
        q: str | None = None,
        kind: ResourceKind | None = None,
        tag: str | None = None,
        owner: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[Sequence[Resource], int]:
        query = select(Resource)
        if kind:
            query = query.where(Resource.kind == kind)
        if owner:
            query = query.where(Resource.owner == owner)
        if tag:
            query = query.where(Resource.tags.contains([tag]))

        id_order: Iterable[int] | None = None
        if q:
            ids = list(await search_resource_ids(self.session, q))
            if not ids:
                return [], 0
            id_order = ids
            query = query.where(Resource.id.in_(ids))

        count_result = await self.session.exec(query.with_only_columns(Resource.id))
        total = len(count_result.scalars().all())

        query = query.order_by(Resource.modified_at.desc())
        if id_order:
            ordering = case({rid: index for index, rid in enumerate(id_order)}, value=Resource.id)
            query = query.order_by(ordering)

        query = query.offset(offset).limit(limit)
        result = await self.session.exec(query)
        resources = result.scalars().all()
        return resources, total

    async def get_resource(self, resource_id: int) -> Resource | None:
        result = await self.session.exec(select(Resource).where(Resource.id == resource_id))
        return result.scalars().one_or_none()

    async def get_by_slug(self, slug: str) -> Resource | None:
        result = await self.session.exec(select(Resource).where(Resource.slug == slug))
        return result.scalars().one_or_none()

    async def get_by_repo(self, repo_url: str) -> Resource | None:
        result = await self.session.exec(select(Resource).where(Resource.repo_url == repo_url))
        return result.scalars().one_or_none()

    async def create_or_update(self, payload: ResourceCreateRequest) -> Resource:
        if isinstance(payload, RepoResourceCreate):
            sync_result = self.repo_sync.sync(payload.repo_url, payload.branch, payload.subpath)
            resource = await self._apply_metadata(sync_result.metadata, ResourceSource.REPOSITORY)
            resource.repo_url = str(payload.repo_url)
            resource.last_synced_at = datetime.utcnow()
            await self.session.commit()
            await self.session.refresh(resource)
            await upsert_resource_fts(self.session, resource)
            await self.session.commit()
            return resource

        resource = await self._apply_metadata(payload.metadata, ResourceSource.MANUAL)
        await self.session.commit()
        await self.session.refresh(resource)
        await upsert_resource_fts(self.session, resource)
        await self.session.commit()
        return resource

    async def delete(self, resource_id: int) -> None:
        resource = await self.get_resource(resource_id)
        if not resource:
            return
        await self.session.delete(resource)
        await remove_resource_fts(self.session, resource_id)
        await self.session.commit()

    async def _apply_metadata(self, metadata: ResourceMetadata, source: ResourceSource) -> Resource:
        base_slug = slugify(metadata.name)
        resource = await self.get_by_slug(base_slug)
        if metadata.repo and not resource:
            resource = await self.get_by_repo(str(metadata.repo))

        if resource:
            resource.kind = metadata.kind
            resource.name = metadata.name
            resource.slug = base_slug
            resource.description = metadata.description
            resource.tags = metadata.tags
            resource.url = str(metadata.url) if metadata.url else None
            resource.path = metadata.path
            resource.owner = metadata.owner
            resource.license = metadata.license
            resource.thumbnail_path = metadata.thumbnail
            resource.healthcheck_path = metadata.healthcheck
        else:
            slug = await self._ensure_unique_slug(base_slug)
            resource = Resource(
                kind=metadata.kind,
                name=metadata.name,
                slug=slug,
                description=metadata.description,
                tags=metadata.tags,
                url=str(metadata.url) if metadata.url else None,
                path=metadata.path,
                owner=metadata.owner,
                license=metadata.license,
                thumbnail_path=metadata.thumbnail,
                healthcheck_path=metadata.healthcheck,
                source=source,
            )
            self.session.add(resource)

        resource.source = source
        if metadata.repo:
            resource.repo_url = str(metadata.repo)
        if metadata.updated:
            if isinstance(metadata.updated, datetime):
                resource.updated_at = metadata.updated
            elif isinstance(metadata.updated, date):
                resource.updated_at = datetime.combine(metadata.updated, datetime.min.time())
        resource.touch()
        await self.session.flush()
        return resource

    async def _ensure_unique_slug(self, candidate: str) -> str:
        existing_slugs = await self.session.exec(select(Resource.slug))
        return slugify(candidate, existing_slugs.scalars().all())


async def to_read_model(resource: Resource) -> ResourceRead:
    return ResourceRead.model_validate(resource)
