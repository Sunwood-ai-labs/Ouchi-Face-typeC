from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from git import Repo

from ..core.config import settings
from ..schemas.resource import ResourceMetadata
from .ouchi_parser import OuchiMetadataError, load_ouchi_metadata


@dataclass
class RepoSyncResult:
    metadata: ResourceMetadata
    repo_path: Path
    metadata_root: Path
    readme: Optional[str]


class RepoSyncService:
    def __init__(self, storage_dir: Path | None = None) -> None:
        self.storage_dir = storage_dir or settings.repo_storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _resolve_repo_dir(self, repo_url: str) -> Path:
        parsed = urlparse(repo_url)
        repo_name = Path(parsed.path.rstrip("/")).stem or "repo"
        safe_name = repo_name.replace(" ", "-")
        return self.storage_dir / safe_name

    def sync(self, repo_url: str, branch: str | None = None, subpath: str | None = None) -> RepoSyncResult:
        repo_dir = self._resolve_repo_dir(repo_url)
        if repo_dir.exists() and (repo_dir / ".git").exists():
            repo = Repo(repo_dir)
            origin = repo.remotes.origin
            origin.fetch()
            checkout_branch = branch or repo.active_branch.name
            repo.git.checkout(checkout_branch)
            origin.pull()
        else:
            if repo_dir.exists():
                shutil.rmtree(repo_dir)
            repo = Repo.clone_from(repo_url, repo_dir)
            if branch:
                repo.git.checkout(branch)

        metadata_root = repo_dir / subpath if subpath else repo_dir
        metadata_root = metadata_root.resolve()
        metadata = load_ouchi_metadata(metadata_root)
        if not metadata.repo:
            metadata.repo = repo_url  # type: ignore[assignment]

        readme_path = None
        for candidate in ("README.md", "README.MD", "readme.md"):
            potential = metadata_root / candidate
            if potential.exists():
                readme_path = potential
                break
        readme = readme_path.read_text(encoding="utf-8") if readme_path else None

        return RepoSyncResult(metadata=metadata, repo_path=repo_dir, metadata_root=metadata_root, readme=readme)


__all__ = ["RepoSyncService", "RepoSyncResult", "OuchiMetadataError"]
