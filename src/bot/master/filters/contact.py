from typing import Union, Dict
from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.bot.master.validators.contact import ContactValidators


class LinkValidatorFilter(BaseFilter):

    async def __call__(self, message: Message) -> Union[bool, Dict[str, str]]:
        link = message.text.strip()
        if ContactValidators.is_valid_url(link):
            return {"link": link}
        return False


class PhoneValidatorFilter(BaseFilter):
    
    async def __call__(self, message: Message) -> Union[bool, Dict[str, str]]:
        parsed_phone = ContactValidators.parse_phone(message.text)
        if parsed_phone:
            return {"phone": parsed_phone}
        return False
