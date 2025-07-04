from typing import Union, Dict
from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.bot.master.validators.time_slot import TimeSlotValidators


class DateValidatorFilter(BaseFilter):

    async def __call__(self, message: Message) -> Union[bool, Dict[str, str]]:
        parsed_date = TimeSlotValidators.parse_date(message.text)
        if parsed_date:
            return {"date": parsed_date}
        return False


class TimeValidatorFilter(BaseFilter):

    async def __call__(self, message: Message) -> Union[bool, Dict[str, str]]:
        parsed_time = TimeSlotValidators.parse_time(message.text)
        if parsed_time:
            return {"time": parsed_time}
        return False
