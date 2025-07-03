from typing import Union
from punq import Container
from functools import lru_cache

from src.infrastructure import container as infra_di
from src.application import container as app_di

_container: Union[Container, None] = None


def initialize_container(container: Container) -> None:
    """
    Initialize the dependency injection container with all project dependencies.
    """
    global _container
    _container = container

    infra_di.register(container)
    app_di.register(container)


@lru_cache()
def get_container() -> Container:
    """
    Returns the initialized global dependency injection container.
    """
    if _container is None:
        raise RuntimeError("Container not initialized")
    return _container
