from aiogram import Router
from punq import Container

from .booking import BookingRouter
from .start import StartRouter


def build_client_router(container: Container) -> Router:
    router = Router(name="client")

    booking_router = BookingRouter(container).router
    start_router = StartRouter().router

    router.include_routers(booking_router, start_router)
    return router
