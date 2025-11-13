from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

class Device(SQLModel, table=True):
    """
    This is the SQLModel for the Device table.
    It defines the columns for the id, name, and created_at fields.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Reading(SQLModel, table=True):
    """
    This is the SQLModel for the Reading table.
    It defines the columns for the id, device_id, temperature_c, and timestamp fields.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    device_id: int = Field(index=True)
    temperature_c: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
