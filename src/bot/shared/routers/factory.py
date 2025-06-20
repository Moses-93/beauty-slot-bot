from aiogram import Router
from punq import Container

from .date import DateDisplayRouter
from .booking import BookingDisplayRouter
from .services import ServiceDisplayRouter
from .contact import ContactDisplayRouter


def build_shared_router(container: Container) -> Router:
    router = Router("master")

    service_router = ServiceDisplayRouter(container).router
    booking_router = BookingDisplayRouter(container).router

    date_router = DateDisplayRouter(container).router
    contact_router = ContactDisplayRouter(container).router

    router.include_routers(
        service_router,
        booking_router,
        date_router,
        contact_router,
    )
    return router
