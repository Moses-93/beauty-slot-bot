from aiogram import Router


class BaseRouter:
    def __init__(self, router: Router):
        self.router = router
        self._register()

    def _register(self):
        raise NotImplementedError("Subclasses should implement this method.")
