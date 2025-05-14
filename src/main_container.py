from punq import Container

from infrastructure import container as infra_di
from application import container as app_di


def create_container() -> Container:
    """
    Create the main container for dependency injection.
    """
    container = Container()

    infra_di.register(container)
    app_di.register(container)

    return container
