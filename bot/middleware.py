from aiogram import BaseMiddleware


class UserIDMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        data["user_id"] = event.from_user.id
        return await handler(event, data)


# class UserNameMiddleware(BaseMiddleware):
#     async def __call__(self, handler, event, data: dict):
#         user_id = event.from_user.id
#         user_data[user_id] = {
#             "name": event.from_user.full_name,
#             "username": event.from_user.username
#         }
#         return await handler(event, data)
