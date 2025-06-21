from aiogram.filters.callback_data import CallbackData

from src.bot.shared.enums.pagination import PaginationCategory


class PaginationCallback(CallbackData, prefix="paginate"):
    category: PaginationCategory
    offset: int
    limit: int
