import logging
from typing import Any, Awaitable, Callable, Dict, Optional
from aiogram import BaseMiddleware
from aiogram.types import Update, User

from src.application.use_cases.user import EnsureUserExistsUseCase
from src.application.dto.user import UserDTO

logger = logging.getLogger(__name__)


class AttachUserMiddleware(BaseMiddleware):
    def __init__(self, ensure_user_uc: EnsureUserExistsUseCase):
        super().__init__()
        self._user_uc = ensure_user_uc

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        update: Update,
        data: Dict[str, Any],
    ) -> Any:
        tg_user = self._extract_user(update)

        if tg_user is None:
            return await handler(update, data)

        user_dto = UserDTO(
            name=tg_user.full_name,
            username=tg_user.username,
            chat_id=tg_user.id,
        )

        result = await self._user_uc(user_dto)
        if result.is_success:
            data["user"] = result.data
        else:
            logger.warning("Failed to create user: %s", user_dto)

        return await handler(update, data)

    def _extract_user(self, update: Update) -> Optional[User]:
        for event in (
            update.message,
            update.callback_query,
            update.inline_query,
            update.chat_join_request,
        ):
            if event and hasattr(event, "from_user"):
                return event.from_user
        return None
