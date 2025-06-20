from aiogram import Router
from punq import Container

from src.bot.master.routers.factory import build_master_router
from src.bot.client.routers.factory import build_client_router
from src.bot.shared.routers.factory import build_shared_router


def build_bot_router(container: Container) -> Router:
    router = Router("bot")
    router.include_routers(
        build_master_router(container),
        build_client_router(container),
        build_shared_router(container),
    )
    return router
