from punq import Container
from functools import lru_cache

from infrastructure import container as infra_di
from application import container as app_di


@lru_cache()
def get_container() -> Container:
    """
    Create the main container for dependency injection.
    """
    container = Container()

    infra_di.register(container)
    app_di.register(container)

    return container
