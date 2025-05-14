from punq import Container
from .persistence.repositories import container as di_repo


def register(container: Container) -> None:
    """
    Register all repositories in the container.
    """
    di_repo.register(container)
