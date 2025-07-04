from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class BookingDTO:
    master_id: int
    client_id: int
    service_id: int
    time_slot_id: int
    reminder_time: Optional[datetime] = None
