from dataclasses import dataclass
from datetime import time, timedelta, datetime, date


@dataclass(frozen=True)
class TimeSlot:
    start: time
    end: time

    @classmethod
    def create_with_duration(cls, start: time, duration: timedelta) -> "TimeSlot":
        return cls(
            start=start, end=(datetime.combine(date.today(), start) + duration).time()
        )

    def overlaps(self, other: "TimeSlot") -> bool:
        return self.start < other.end and other.start < self.end
