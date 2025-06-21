from punq import Container

from src.domain.repositories.abstract_booking_repository import (
    AbstractBookingRepository,
)
from src.domain.repositories.abstract_contact_repository import (
    AbstractContactRepository,
)
from src.domain.repositories.abstract_date_repository import AbstractDateRepository
from src.domain.repositories.abstract_service_repository import (
    AbstractServiceRepository,
)
from src.domain.repositories.abstract_user_repository import AbstractUserRepository
from .booking_repository import BookingRepository
from .date_repository import DateRepository
from .service_repository import ServiceRepository
from .contact_repository import ContactRepository
from .user_repository import UserRepository


def register(container: Container) -> None:
    """
    Register all repositories in the container.
    """
    container.register(AbstractBookingRepository, BookingRepository)
    container.register(AbstractServiceRepository, ServiceRepository)
    container.register(AbstractDateRepository, DateRepository)
    container.register(AbstractContactRepository, ContactRepository)
    container.register(AbstractUserRepository, UserRepository)
