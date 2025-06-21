from punq import Container

from .services import container as services_di
from .use_cases import container as use_cases_di


def register(container: Container) -> None:
    """
    Register all services and use cases in the container.
    """
    services_di.register(container)
    use_cases_di.register(container)
