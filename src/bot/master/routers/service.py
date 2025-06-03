from aiogram import Router, F

from src.bot.master.handlers import service

_service_router = Router(name="service")


class BaseServiceRouter:
    def __init__(self):
        self._router = _service_router
        self._register()

    @property
    def router(self):
        return self._router

    def _register(self):
        raise NotImplementedError("Subclasses should implement this method.")


class CreateServiceRouter(BaseServiceRouter):
    def __init__(self, handler: service.CreateServiceHandler):
        self._handler = handler
        super().__init__()

    def _register(self):
        pass


class DeactivateServiceRouter(BaseServiceRouter):
    def __init__(self, handler: service.DeactivateServiceHandler):
        self._handler = handler
        super().__init__()

    def _register(self):
        pass


class EditServiceRouter(BaseServiceRouter):
    def __init__(self, handler: service.EditServiceHandler):
        self._handler = handler
        super().__init__()

    def _register(self):
        pass
