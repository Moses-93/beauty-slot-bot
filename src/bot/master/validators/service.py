from typing import Union
from datetime import timedelta


class ServiceValidators:

    @staticmethod
    def parse_title(title: str) -> Union[str, None]:

        normalized = title.strip()
        if 1 <= len(normalized) <= 100:
            return normalized
        return None

    @staticmethod
    def parse_price(price_str: str) -> Union[int, None]:

        try:
            price = float(price_str.replace(",", "."))
            if price >= 0:
                return int(round(price * 100))
        except ValueError:
            return None

    @staticmethod
    def parse_duration(duration_str: str) -> Union[timedelta, None]:

        duration_str = duration_str.strip()

        if ":" in duration_str:
            try:
                hours, minutes = map(int, duration_str.split(":"))
                total = timedelta(hours=hours, minutes=minutes)
                return total if total.total_seconds() > 0 else None
            except (ValueError, IndexError):
                return None
        else:
            try:
                minutes = int(duration_str)
                return timedelta(minutes=minutes) if minutes > 0 else None
            except ValueError:
                return None
