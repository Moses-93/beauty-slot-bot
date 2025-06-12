from typing import Any, Awaitable, Callable, Dict, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from src.application.use_cases.user import EnsureUserExistsUseCase
from src.application.dto.user import UserDTO


class AttachUserMiddleware(BaseMiddleware):
    def __init__(self, ensure_user_uc: EnsureUserExistsUseCase):
        super().__init__()
        self._user_uc = ensure_user_uc

    async def __call__(
        self,
        handler: Callable[
            [Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]
        ],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any],
    ) -> Any:
        """Middleware to handle user authentication and creation.
        If the user does not exist, it creates a new user.
        """
        tg_user = event.from_user
        result = await self._user_uc(
            UserDTO(
                name=tg_user.full_name,
                username=tg_user.username,
                chat_id=tg_user.id,
            )
        )
        if result.is_success:
            data["user"] = result.data
            return await handler(event, data)
        else:
            return  # TODO: Add logging or error handling here
