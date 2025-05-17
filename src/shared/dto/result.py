from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


@dataclass
class ResultDTO(Generic[T]):
    is_success: bool
    data: Optional[T]
