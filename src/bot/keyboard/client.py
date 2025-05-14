from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ClientKeyboard:
    """
    This class is responsible for generating the client keyboard for the bot.
    It provides methods to create different types of keyboards used in the bot.
    """

    @staticmethod
    def main() -> ReplyKeyboardMarkup:
        """
        Generates the main keyboard for the bot.
        :return: ReplyKeyboardMarkup object with the main keyboard buttons.
        """
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="📝 Записатися"),
                    KeyboardButton(text="📖 Мої записи"),
                ],
                [
                    KeyboardButton(text="📋 Послуги"),
                    KeyboardButton(text="🗓 Доступні дати"),
                ],
                [KeyboardButton(text="📕 Контакти")],
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

    @staticmethod
    def filter_booking() -> ReplyKeyboardMarkup:
        """
        Generates the keyboard for filtering bookings.
        :return: ReplyKeyboardMarkup object with the filter booking buttons.
        """
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Всі записи"),
                    KeyboardButton(text="Активні записи"),
                ],
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
