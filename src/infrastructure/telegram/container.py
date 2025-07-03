from punq import Container

from src.application.abstractions.notifier import AbstractNotifier
from .notifier import TelegramNotifier


def register(container: Container) -> None:
    container.register(AbstractNotifier, TelegramNotifier)
