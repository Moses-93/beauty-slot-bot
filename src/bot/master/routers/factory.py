from aiogram import Router
from punq import Container

from .navigation import SectionRouter
from .date import DateRouter
from .service import ServiceRouter
from .start import StartRouter


def build_master_router(container: Container) -> Router:
    router = Router(name="master")

    start_router = StartRouter().router
    navigation_router = SectionRouter(container).router

    service_router = ServiceRouter(container).router

    date_router = DateRouter(container).router

    router.include_routers(
        navigation_router,
        start_router,
        service_router,
        date_router,
    )
    return router
