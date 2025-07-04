from punq import Container

from .time_finder import AvailableTimeFinder
from .booking_factory import BookingFactory


def register(container: Container) -> None:
    """
    Register all services in the container.
    """
    container.register(AvailableTimeFinder)
    container.register(BookingFactory)
