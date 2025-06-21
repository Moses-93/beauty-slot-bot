from aiogram import Dispatcher
from punq import Container

from src.application.use_cases.user import EnsureUserExistsUseCase
from src.bot.shared.middlewares.auth import AttachUserMiddleware


def setup_middlewares(dispatcher: Dispatcher, container: Container):

    ensure_user_uc = container.resolve(EnsureUserExistsUseCase)

    attach_user = AttachUserMiddleware(ensure_user_uc)

    dispatcher.update.outer_middleware(attach_user)
