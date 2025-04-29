import logging
from aiogram import BaseMiddleware
from db.crud import admins_manager

logger = logging.getLogger(__name__)


class AdminMiddleware(BaseMiddleware):

    def __init__(self):
        super().__init__()

    async def __call__(self, handler, event, data: dict):
        user_id = event.from_user.id
        admin = await admins_manager.read(chat_id=user_id)
        data["is_admin"] = True if admin else False
        return await handler(event, data)
