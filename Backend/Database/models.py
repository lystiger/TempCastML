from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

class Device(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Reading(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    device_id: int = Field(index=True)
    temperature_c: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
