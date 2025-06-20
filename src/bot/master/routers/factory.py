from aiogram import Router
from punq import Container

from .navigation import SectionRouter
from .date import CreateDateRouter, DeactivateDateRouter
from .service import CreateServiceRouter, EditServiceRouter, DeactivateServiceRouter
from .start import StartRouter


def build_master_router(container: Container) -> Router:
    router = Router("master")

    start_router = StartRouter().router
    navigation_router = SectionRouter(container).router

    service_routers = (
        CreateServiceRouter(container).router,
        EditServiceRouter(container).router,
        DeactivateServiceRouter(container).router,
    )

    date_routers = (
        CreateDateRouter(container).router,
        DeactivateDateRouter(container).router,
    )

    router.include_routers(
        navigation_router,
        start_router,
        *service_routers,
        *date_routers,
    )
    return router
