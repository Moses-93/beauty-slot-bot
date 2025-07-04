from dataclasses import dataclass, field
from datetime import time, timedelta, datetime, date as Date
from typing import Optional

from src.domain.enums.time_slot import TimeSlotStatus


@dataclass(kw_only=True)
class TimeSlot:
    id: Optional[int] = field(default=None)
    master_id: int
    date: Date
    start: time
    end: time
    status: TimeSlotStatus = field(default=TimeSlotStatus.AVAILABLE)

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
