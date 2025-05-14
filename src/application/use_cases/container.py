from punq import Container

from .booking_creator import CreateBookingUseCase
from .time_checker import CheckBookingAvailabilityUseCase


def register(container: Container) -> None:
    """
    Register all use cases in the container.
    """
    container.register(
        CheckBookingAvailabilityUseCase,
    )
    container.register(
        CreateBookingUseCase,
    )
