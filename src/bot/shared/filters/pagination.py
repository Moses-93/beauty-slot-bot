from aiogram.filters.callback_data import CallbackData


class PaginationCallback(CallbackData, prefix="paginate"):
    category: str
    offset: int
    limit: int
