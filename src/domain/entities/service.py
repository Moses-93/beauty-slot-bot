from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Service:
    id: Optional[int] = field(default=None)
    title: str = field(default=None)
    price: int = field(default=None)
    duration: int = field(default=None)
    is_active: bool = field(default=True)
