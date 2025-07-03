from dataclasses import dataclass, field
from datetime import time, timedelta, datetime, date as Date
from typing import Optional


@dataclass(kw_only=True)
class TimeSlot:
    id: Optional[int] = field(default=None)
    date: Date
    start: time
    end: time
    is_active: bool = field(default=True)
    is_booked: bool = field(default=False)

    @classmethod
    def from_start_and_duration(
        cls, date: Date, start: time, duration: timedelta
    ) -> "TimeSlot":
        return cls(
            date=date,
            start=start,
            end=(datetime.combine(date, start) + duration).time(),
        )

    def can_fit(self, duration: timedelta) -> bool:
        full_start = datetime.combine(self.date, self.start)
        full_end = datetime.combine(self.date, self.end)
        return full_start + duration <= full_end

    def overlaps(self, other: "TimeSlot") -> bool:
        return self.start < other.end and other.start < self.end
