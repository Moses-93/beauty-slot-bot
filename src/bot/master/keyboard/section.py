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
                    KeyboardButton(text="📅 Дати"),
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
                [KeyboardButton(text="📋 Список послуг")],
                [KeyboardButton(text="🔙 Назад")],
            ],
            resize_keyboard=True,
        )

    @staticmethod
    def dates() -> ReplyKeyboardMarkup:
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
