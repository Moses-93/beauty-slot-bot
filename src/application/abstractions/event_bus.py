from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Awaitable, Type

from .events.base import Event


E = TypeVar("E", bound=Event)
Handler = Callable[[E], Awaitable[None]]


class AbstractEventBus(ABC):

    @abstractmethod
    def subscribe(self, event_type: Type[E], handler: Handler[E]) -> None:
        pass

    @abstractmethod
    def publish(self, event: E) -> None:
        pass
