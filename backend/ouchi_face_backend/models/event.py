from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    resource_id: int = Field(foreign_key="resource.id")
    type: str
    data: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
