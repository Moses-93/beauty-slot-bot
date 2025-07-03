from dataclasses import dataclass, field
from datetime import time as Time, datetime
from typing import Optional
from .service import Service
from .date import DateSlot


@dataclass(kw_only=True)
class Booking:
    id: Optional[int] = field(default=None)
    user_id: int
    service: Service
    date: DateSlot
    time: Time
    reminder_time: Optional[datetime] = field(default=None)
    is_active: bool = field(default=False)

    def should_schedule_reminder(self, now: datetime) -> bool:
        return self.reminder_time is not None and now < self.reminder_time

    def is_past(self, now: Optional[datetime] = None) -> bool:
        """
        Check if the booking is in the past, taking both date and time into account.
        """
        now = now or datetime.now()
        return datetime.combine(self.date.date, self.time) < now

    def confirm(self) -> None:
        """
        Confirm the booking if it is not in the past.
        """
        if self.is_past():
            raise ValueError("...")  # TODO: Add custom exception and message
        self.is_active = True

    def cancel(self) -> None:
        """Cancel the booking if it is active."""
        if not self.is_active:
            raise ValueError("...")  # TODO: Add custom exception and message
        self.is_active = False
