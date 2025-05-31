from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


@dataclass
class ResultDTO(Generic[T]):
    is_success: bool
    data: Optional[T] = None

    @classmethod
    def success(cls, data: T) -> "ResultDTO[T]":
        return cls(is_success=True, data=data)

    @classmethod
    def fail(cls) -> "ResultDTO[None]":
        return cls(is_success=False)
