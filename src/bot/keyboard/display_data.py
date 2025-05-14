from typing import Dict, List, Tuple
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


class DisplayData:

    @staticmethod
    def generate_keyboard(
        data: List[Dict],
        text_keys: Tuple[str],
        callback_key: Tuple[str],
    ) -> InlineKeyboardMarkup:
        """
        Generates an InlineKeyboardMarkup from a list of dictionaries.
        Each dictionary represents a button, with the text and callback data
        specified by the keys in text_keys and callback_key respectively.
        :param data: List of dictionaries containing button data.
        :param text_keys: Tuple of keys to extract text for the buttons.
        :param callback_key: Tuple of keys to extract callback data for the buttons.
        :return: InlineKeyboardMarkup object with the generated buttons.
        """
        keyboard = [
            [
                InlineKeyboardButton(
                    text=" - ".join(str(i.get(key, "...")) for key in text_keys),
                    callback_data=f"{" ".join(str(i.get(key, "...")) for key in callback_key)}",
                )
            ]
            for i in data
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
