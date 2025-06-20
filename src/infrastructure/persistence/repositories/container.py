from punq import Container

from .base_repository import BaseRepository
from .booking_repository import BookingRepository
from .date_repository import DateRepository
from .service_repository import ServiceRepository
from .contact_repository import ContactRepository


def register(container: Container) -> None:
    """
    Register all repositories in the container.
    """
    container.register(BaseRepository)
    container.register(BookingRepository)
    container.register(ServiceRepository)
    container.register(DateRepository)
    container.register(ContactRepository)
