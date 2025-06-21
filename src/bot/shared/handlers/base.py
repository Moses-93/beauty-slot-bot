import logging
from typing import Any, Sequence
from punq import Container
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from src.bot.shared.formatters.base import BaseFormatter
from src.bot.shared.filters.pagination import PaginationCallback
from src.bot.shared.keyboard.pagination import Paginator
from src.bot.shared.enums.pagination import PaginationCategory

logger = logging.getLogger(__name__)


class BaseDisplayHandler:
    def __init__(
        self,
        container: Container,
        formatter: BaseFormatter,
    ):
        self._container = container
        self.formatter = formatter

    def resolve(self, service: Any, **kwargs):
        return self._container.resolve(service, **kwargs)

    def make_paginator(
        self, items: Sequence, category: PaginationCategory, limit: int, offset: int
    ) -> InlineKeyboardMarkup:
        paginator = Paginator(limit, offset)
        return paginator(items, PaginationCallback, category)

    async def send_page(
        self,
        message: Message,
        items: Sequence,
        category: PaginationCategory,
        limit: int,
        offset: int,
        **kwargs
    ) -> None:
        text = self.formatter.format(items[:limit])
        keyboard = self.make_paginator(items, category, limit, offset)
        await message.answer(text=text, reply_markup=keyboard, **kwargs)

    async def edit_page(
        self,
        callback: CallbackQuery,
        items: Sequence,
        category: PaginationCategory,
        limit: int,
        offset: int,
        **kwargs
    ) -> None:
        text = self.formatter.format(items[:limit])
        keyboard = self.make_paginator(items, category, limit, offset)
        await callback.message.edit_text(text=text, reply_markup=keyboard, **kwargs)
