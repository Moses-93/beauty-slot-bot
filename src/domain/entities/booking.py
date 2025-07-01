from dataclasses import dataclass, field
from datetime import time as Time, datetime
from typing import Optional
from .service import Service
from .date import DateSlot


@dataclass
class Booking:
    id: Optional[int] = field(default=None)
    user_id: int
    service: Service
    date: DateSlot
    time: Time
    reminder_time: Optional[datetime] = field(default=None)
    is_active: bool = field(default=True)
