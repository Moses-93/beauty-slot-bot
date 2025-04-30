from aiogram import BaseMiddleware


class UserIDMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        data["user_id"] = event.from_user.id
        return await handler(event, data)
