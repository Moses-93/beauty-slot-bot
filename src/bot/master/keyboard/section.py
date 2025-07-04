from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


class SectionKeyboards:

    @staticmethod
    def main() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="📒 Записи"),
                    KeyboardButton(text="📖 Послуги"),
                ],
                [
                    KeyboardButton(text="📅 Віконця"),
                    KeyboardButton(text="📔 Контакти"),
                ],
            ],
            resize_keyboard=True,
        )

    @staticmethod
    def services() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="➕ Додати послугу"),
                    KeyboardButton(text="➖ Видалити послугу"),
                ],
                [
                    KeyboardButton(text="🔄 Оновити послугу"),
                    KeyboardButton(text="📋 Список послуг"),
                ],
                [KeyboardButton(text="🔙 Назад")],
            ],
            resize_keyboard=True,
        )

    @staticmethod
    def time_slots() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="➕ Нове віконце"),
                    KeyboardButton(text="➖ Прибрати віконце"),
                ],
                [KeyboardButton(text="📅 Всі віконця")],
                [KeyboardButton(text="🔙 Назад")],
            ],
            resize_keyboard=True,
        )

    @staticmethod
    def contacts() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="➕ Додати контакти"),
                ],
                [
                    KeyboardButton(text="✏️ Редагувати контакти"),
                    KeyboardButton(text="➖ Видалити контакти"),
                ],
                [KeyboardButton(text="📕 Мої контакти")],
                [KeyboardButton(text="🔙 Назад")],
            ],
            resize_keyboard=True,
        )
