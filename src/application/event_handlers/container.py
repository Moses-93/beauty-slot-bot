from punq import Container

from .booking import BookingCreatedHandler


def register(container: Container) -> None:
    """
    Register all event handlers in the container.
    """
    container.register(BookingCreatedHandler)
