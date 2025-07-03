from src.application.abstractions.notifier import AbstractNotifier
from ..events.booking import BookingCreated


class BookingCreatedHandler:
    def __init__(self, notifier: AbstractNotifier):
        self.notifier = notifier

    async def __call__(
        self, event: BookingCreated
    ):  # TODO: Implement logic for formatting and sending messages
        pass
