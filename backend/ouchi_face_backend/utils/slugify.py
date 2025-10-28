from __future__ import annotations

import re
from typing import Iterable


_slug_re = re.compile(r"[^a-z0-9]+")


def slugify(value: str, existing: Iterable[str] | None = None) -> str:
    base = _slug_re.sub("-", value.lower()).strip("-")
    if not base:
        base = "resource"
    if existing is None:
        return base
    candidate = base
    suffix = 2
    existing_set = set(existing)
    while candidate in existing_set:
        candidate = f"{base}-{suffix}"
        suffix += 1
    return candidate
