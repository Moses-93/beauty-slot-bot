from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


class Sections:

    @staticmethod
    def main_section() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📒 Записи")],
                [
                    KeyboardButton(text="📖 Послуги"),
                    KeyboardButton(text="📅 Дати"),
                ],
            ],
            resize_keyboard=True,
        )

    @staticmethod
    def services_section() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="➕ Додати послугу"),
                    KeyboardButton(text="➖ Видалити послугу"),
                ],
                [KeyboardButton(text="📋 Список послуг")],
                [KeyboardButton(text="🔙 Назад")],
            ],
            resize_keyboard=True,
        )

    @staticmethod
    def dates_section() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="➕ Додати дату"),
                    KeyboardButton(text="➖ Видалити дату"),
                ],
                [KeyboardButton(text="📅 Список дат")],
                [KeyboardButton(text="🔙 Назад")],
            ],
            resize_keyboard=True,
        )

    @staticmethod
    def bookings_section() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Активні записи"),
                    KeyboardButton(text="Всі записи"),
                ],
                [KeyboardButton(text="🔙 Назад")],
            ],
            resize_keyboard=True,
        )
