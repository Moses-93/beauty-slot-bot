from punq import Container
from src.application.abstractions.event_bus import AbstractEventBus
from .aiopubsub_event_bus import AiopubsubEventBus


def register(container: Container) -> None:
    container.register(AbstractEventBus, AiopubsubEventBus)
