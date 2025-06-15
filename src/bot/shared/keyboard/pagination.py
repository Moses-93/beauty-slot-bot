from typing import List, Sequence, Tuple, Type
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class Paginator:
    def __init__(self, limit: int, offset: int):
        self.limit = limit
        self.offset = offset

    def _calculate_pages(self, items: Sequence) -> Tuple[bool, bool]:
        has_next = len(items) > self.limit
        has_prev = self.offset > 0
        return (has_next, has_prev)

    def __call__(
        self,
        items: List,
        callback_factory: Type[CallbackData],
        category: str,
    ) -> InlineKeyboardMarkup:

        builder = InlineKeyboardBuilder()
        has_next, has_prev = self._calculate_pages(items)

        if has_prev:
            builder.button(
                text="⬅️ Назад",
                callback_data=callback_factory(
                    category=category, offset=self.offset - self.limit, limit=self.limit
                ).pack(),
            )

        builder.button(text=str(self.offset // self.limit + 1), callback_data="noop")

        if has_next:
            builder.button(
                text="Вперед ➡️",
                callback_data=callback_factory(
                    category=category, offset=self.offset + self.limit, limit=self.limit
                ).pack(),
            )

        return builder.as_markup()
