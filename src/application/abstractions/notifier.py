from abc import ABC, abstractmethod


class AbstractNotifier(ABC):

    @abstractmethod
    async def send_message(self, recipient_id: str, message: str, **kwargs):
        """
        Sends a message to a recipient.

        Args:
            recipient_id (str): A unique identifier of the recipient
            (e.g. Telegram chat ID, email address, phone number).
            message (str): The message content to send.
        """
        pass
