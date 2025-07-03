import pytest
from aiogram.types import InlineKeyboardMarkup
from src.bot.shared.filters.pagination import PaginationCallback
from src.bot.shared.keyboard.pagination import Paginator
from src.bot.shared.enums.pagination import PaginationCategory


def extract_button_texts(markup: InlineKeyboardMarkup) -> list[str]:
    return [btn.text for row in markup.inline_keyboard for btn in row]


def extract_callback_data(markup: InlineKeyboardMarkup) -> list[str]:
    return [btn.callback_data for row in markup.inline_keyboard for btn in row]


def test_first_page():
    items = [f"item {i}" for i in range(6)]
    paginator = Paginator(limit=5, offset=0)
    markup = paginator(items, PaginationCallback, category=PaginationCategory.SERVICES)

    texts = extract_button_texts(markup)
    assert texts == ["1", "Вперед ➡️"]

    callbacks = extract_callback_data(markup)
    assert "paginate:services:5:5" in callbacks


def test_middle_page():
    items = [f"item {i}" for i in range(6)]
    paginator = Paginator(limit=5, offset=5)
    markup = paginator(items, PaginationCallback, category=PaginationCategory.SERVICES)

    texts = extract_button_texts(markup)
    assert texts == ["⬅️ Назад", "2", "Вперед ➡️"]

    callbacks = extract_callback_data(markup)
    assert "paginate:services:0:5" in callbacks
    assert "paginate:services:10:5" in callbacks


def test_last_page():
    items = [f"item {i}" for i in range(5)]
    paginator = Paginator(limit=5, offset=5)
    markup = paginator(items, PaginationCallback, category=PaginationCategory.SERVICES)

    texts = extract_button_texts(markup)
    assert texts == ["⬅️ Назад", "2"]

    callbacks = extract_callback_data(markup)
    assert "paginate:services:0:5" in callbacks
    assert all("10" not in cb for cb in callbacks)


def test_empty_page():
    items = []
    paginator = Paginator(limit=5, offset=0)
    markup = paginator(items, PaginationCallback, category=PaginationCategory.SERVICES)

    texts = extract_button_texts(markup)
    assert texts == ["1"]
    callbacks = extract_callback_data(markup)
    assert callbacks == ["noop"]
