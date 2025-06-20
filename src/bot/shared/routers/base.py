from aiogram import Router


class BaseRouter:
    def __init__(self, router: Router):
        self._router = router
        self._register()

    @property
    def router(self):
        return self._router

    def _register(self):
        raise NotImplementedError("Subclasses should implement this method.")
