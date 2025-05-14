from punq import Container

from .time_finder import AvailableTimeFinder


def register(container: Container) -> None:
    """
    Register all services in the container.
    """
    container.register(AvailableTimeFinder)
