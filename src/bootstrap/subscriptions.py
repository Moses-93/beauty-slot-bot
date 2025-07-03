from punq import Container

from src.application.abstractions.event_bus import AbstractEventBus
from src.application.events.booking import BookingCreated
from src.application.event_handlers.booking import BookingCreatedHandler


def register_event_subscriptions(container: Container) -> None:
    event_bus: AbstractEventBus = container.resolve(AbstractEventBus)
    booking_created_handler: BookingCreatedHandler = container.resolve(
        BookingCreatedHandler
    )
    event_bus.subscribe(BookingCreated, booking_created_handler)
