from dataclasses import dataclass, field
from datetime import datetime, timedelta, time, date
from typing import Optional


@dataclass(kw_only=True)
class Service:
    id: Optional[int] = field(default=None)
    master_id: int
    title: str
    price: int
    duration: timedelta

    @property
    def price_uah(self) -> float:
        return self.price / 100

    def end_time(self, start_time: time) -> time:
        dt = datetime.combine(date.today(), start_time) + self.duration
        return dt.time()
