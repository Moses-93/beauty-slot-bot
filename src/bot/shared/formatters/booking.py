from typing import Literal
from src.domain.entities.booking import Booking
from src.bot.shared.formatters.base import BaseFormatter


class BookingFormatter(BaseFormatter[Booking]):
    def __init__(self, parse_mode: Literal["Markdown", "HTML"]):
        super().__init__(
            header="📋 ЗАПИСИ",
            separator="\n" + "=" * 30 + "\n",
            parse_mode=parse_mode,
        )

    def _render_item(self, b: Booking) -> str:

        return (
            f"📌 {self._bold("Послуга:")} {b.service.title}\n"
            f"📅 {self._bold("Дата:")} {b.time_slot.date}\n"
            f"⏰ {self._bold("Час:")} {b.time_slot.start}\n"
            f"💵 {self._bold("Ціна:")} {b.service.price} грн"
        )
