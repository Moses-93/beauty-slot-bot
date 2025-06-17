from datetime import datetime
from typing import Union


class DateValidators:

    @staticmethod
    def parse_date(date_str: str) -> Union[str, None]:
        try:
            date = datetime.strptime(date_str.strip(), "%d.%m.%Y")
            return date.strftime("%Y-%m-%d")
        except ValueError:
            return None

    @staticmethod
    def parse_time(time_str: str) -> Union[str, None]:
        try:
            time = datetime.strptime(time_str.strip(), "%H:%M")
            return time.strftime("%H:%M")
        except ValueError:
            return None
