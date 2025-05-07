from dataclasses import dataclass, field
from datetime import datetime, date as Date
from typing import Optional


@dataclass
class Date:
    id: Optional[int] = field(default=None)
    date: Date = field(default=None)
    deactivation_time: datetime = field(default=None)
    is_active: bool = field(default=True)
