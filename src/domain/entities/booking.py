from dataclasses import dataclass, field
from datetime import time as Time, datetime
from typing import Optional
from src.application.dto.date import DateDTO
from src.application.dto.service import ServiceDTO


@dataclass
class Booking:
    id: Optional[int] = field(default=None)
    user_id: int = field(default=None)
    service: ServiceDTO = field(default=None)
    date: DateDTO = field(default=None)
    time: Time = field(default=None)
    reminder_time: Optional[datetime] = field(default=None)
    is_active: bool = field(default=True)
