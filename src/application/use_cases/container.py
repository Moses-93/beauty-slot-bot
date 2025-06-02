from punq import Container

from . import date, service
from .booking import CreateBookingUseCase
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
    container.register(date.CreateDateUseCase)
    container.register(date.DeactivateDateUseCase)
    container.register(date.DeleteDateUseCase)
    container.register(date.GetAvailableDateUseCase)
    container.register(service.GetServicesUseCase)
    container.register(service.CreateServiceUseCase)
    container.register(service.EditServiceUseCase)
