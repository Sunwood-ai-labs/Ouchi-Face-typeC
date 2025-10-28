from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

from ..schemas.resource import ResourceMetadata

_yaml = YAML(typ="safe")


class OuchiMetadataError(RuntimeError):
    pass


def load_ouchi_metadata(root: Path) -> ResourceMetadata:
    yaml_path = root / "ouchi.yaml"
    if not yaml_path.exists():
        raise OuchiMetadataError(f"ouchi.yaml not found in {root}")
    try:
        raw: dict[str, Any] = _yaml.load(yaml_path.read_text(encoding="utf-8")) or {}
    except Exception as exc:  # noqa: BLE001 - want to expose parse issues
        raise OuchiMetadataError(f"Failed to parse ouchi.yaml: {exc}") from exc

    if "kind" not in raw or "name" not in raw:
        raise OuchiMetadataError("ouchi.yaml must contain at least 'kind' and 'name'")

    updated_raw = raw.get("updated")
    updated = None
    if isinstance(updated_raw, datetime):
        updated = updated_raw
    elif isinstance(updated_raw, str):
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
            try:
                updated = datetime.strptime(updated_raw, fmt)
                break
            except ValueError:
                continue

    metadata = ResourceMetadata(
        kind=raw["kind"],
        name=raw["name"],
        description=raw.get("description"),
        tags=raw.get("tags", []),
        url=raw.get("url"),
        path=raw.get("path"),
        repo=raw.get("repo"),
        healthcheck=raw.get("healthcheck"),
        owner=raw.get("owner"),
        license=raw.get("license"),
        thumbnail=raw.get("thumbnail"),
        updated=updated,
    )
    return metadata
