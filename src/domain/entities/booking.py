from dataclasses import dataclass, field
from datetime import time as Time, datetime
from typing import Dict, Optional


@dataclass
class Booking:
    id: Optional[int] = field(default=None)
    user_id: int = field(default=None)
    service_id: int = field(default=None)
    date_id: int = field(default=None)
    time: Time = field(default=None)
    reminder_time: Optional[datetime] = field(default=None)
    is_active: bool = field(default=True)

    def to_dict(self) -> Dict:
        """Convert the Booking object to a dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "service_id": self.service_id,
            "date_id": self.date_id,
            "time": self.time,
            "reminder_time": self.reminder_time,
            "is_active": self.is_active,
        }
