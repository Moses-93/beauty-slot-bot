from punq import Container

from .services import container as services_di
from .use_cases import container as use_cases_di
from .event_handlers import container as event_handlers_di


def register(container: Container) -> None:
    """
    Register all services and use cases in the container.
    """
    services_di.register(container)
    use_cases_di.register(container)
    event_handlers_di.register(container)
