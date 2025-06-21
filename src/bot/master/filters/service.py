from datetime import timedelta
from typing import Union, Dict
from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.bot.master.validators.service import ServiceValidators


class TitleValidatorFilter(BaseFilter):

    async def __call__(self, message: Message) -> Union[bool, Dict[str, str]]:
        parsed_title = ServiceValidators.parse_title(message.text)
        if parsed_title:
            return {"title": parsed_title}
        return False


class PriceValidatorFilter(BaseFilter):

    async def __call__(self, message: Message) -> Union[bool, Dict[str, str]]:
        parsed_price = ServiceValidators.parse_price(message.text)
        if parsed_price is not None:
            return {"price": parsed_price}
        return False


class DurationValidatorFilter(BaseFilter):

    async def __call__(self, message: Message) -> Union[bool, Dict[str, timedelta]]:
        parsed_duration = ServiceValidators.parse_duration(message.text)
        if parsed_duration:
            return {"duration": parsed_duration}
        return False
