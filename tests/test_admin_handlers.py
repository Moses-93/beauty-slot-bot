import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
from aiogram import types
from bot.admin.keyboards import admin_keyboards
from bot.admin.handlers import (
    general_handlers,
    dates_handlers,
    service_handlers,
    show_bookings,
)


@pytest.mark.asyncio
async def test_show_admin_panel_is_admin():
    message = AsyncMock(spec=types.Message)
    message.answer = AsyncMock()
    keyboard = AsyncMock(spec=types.ReplyKeyboardMarkup)
    admin_keyboards.main_keyboard = keyboard
    await general_handlers.show_admin_panel(message, is_admin=True)

    message.answer.assert_called_once_with(
        text="Ви перейшли в панель адміністратора", reply_markup=keyboard
    )


@pytest.mark.asyncio
async def test_show_admin_panel_not_admin():
    message = AsyncMock(spec=types.Message)
    message.answer = AsyncMock()
    keyboard = AsyncMock(spec=types.ReplyKeyboardMarkup)
    admin_keyboards.main_keyboard = keyboard
    await general_handlers.show_admin_panel(message, is_admin=False)
    message.answer.assert_called_once_with(text="У Вас немає доступу до адмін панелі.")
