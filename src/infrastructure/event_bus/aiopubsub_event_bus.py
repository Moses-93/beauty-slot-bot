import inspect
from aiopubsub import Hub, Key, Subscriber, Publisher
from typing import Type

from src.application.abstractions.event_bus import AbstractEventBus, E, Handler


class AiopubsubEventBus(AbstractEventBus):
    def __init__(self):
        self._hub = Hub()
        self._subscriber = Subscriber(self._hub, "main")
        self._publisher = Publisher(self._hub, "main")

    def _get_key(self, event_type: Type[E]) -> Key:
        return Key(f"{event_type.__module__}.{event_type.__name__}")

    def _adapt_handler(self, handler: Handler[E]):
        async def wrapper(_key: Key, event: Type[E]):
            return await handler(event)

        return wrapper

    def subscribe(self, event_type: Type[E], handler: Handler[E]):
        if not inspect.iscoroutinefunction(handler):
            raise TypeError(
                f"Handler for {event_type} must be async"
            )  # TODO: Add custom exception - InvalidEventHandlerTypeError
        key = self._get_key(event_type)
        self._subscriber.add_async_listener(key, self._adapt_handler(handler))

    def publish(self, event: E) -> None:
        key = self._get_key(type(event))
        self._publisher.publish(key, event)

    async def reset(self) -> None:
        await self._subscriber.remove_all_listeners()
