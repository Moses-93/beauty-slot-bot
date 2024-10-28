from aiogram import BaseMiddleware


class UserIDMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        data["user_id"] = event.from_user.id
        return await handler(event, data)


class AdminMiddleware(BaseMiddleware):

    def __init__(self, admin_ids: list):
        super().__init__()
        self.admin_ids = admin_ids

    async def __call__(self, handler, event, data: dict):
        user_id = event.from_user.id
        data["is_admin"] = user_id in self.admin_ids
        return await handler(event, data)
