from punq import Container

from . import date, service
from . import booking
from .user import EnsureUserExistsUseCase
from .time_checker import CheckBookingAvailabilityUseCase
from .contact import GetContactsUseCase


def register(container: Container) -> None:
    """
    Register all use cases in the container.
    """
    container.register(EnsureUserExistsUseCase)
    container.register(
        CheckBookingAvailabilityUseCase,
    )
    container.register(
        booking.CreateBookingUseCase,
    )
    container.register(
        booking.DeactivateBookingUseCase,
    )
    container.register(
        booking.GetBookingUseCase,
    )

    container.register(date.CreateDateUseCase)
    container.register(date.DeactivateDateUseCase)
    container.register(date.DeleteDateUseCase)
    container.register(date.GetAvailableDateUseCase)
    container.register(service.GetServicesUseCase)
    container.register(service.CreateServiceUseCase)
    container.register(service.EditServiceUseCase)
    container.register(GetContactsUseCase)
