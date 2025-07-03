from dataclasses import dataclass
from datetime import time as Time, datetime
from typing import Optional


@dataclass(frozen=True)
class BookingDTO:
    master_id: int
    client_id: int
    service_id: int
    date_id: int
    time: Time
    reminder_time: Optional[datetime] = None
