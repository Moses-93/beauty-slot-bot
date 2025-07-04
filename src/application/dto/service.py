from dataclasses import dataclass, field
from datetime import timedelta


@dataclass(frozen=True)
class ServiceDTO:
    master_id: int
    title: str
    price: int
    duration: timedelta
    is_active: bool = field(default=True)
