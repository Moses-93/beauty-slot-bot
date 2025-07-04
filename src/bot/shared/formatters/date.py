from typing import Literal
from src.domain.entities.time import TimeSlot
from src.bot.shared.formatters.base import BaseFormatter


class TimeSlotFormatter(BaseFormatter):
    def __init__(self, parse_mode: Literal["Markdown", "HTML"]):
        super().__init__(
            header="📅 ВІЛЬНІ ВІКОНЦЯ",
            separator="\n" + "=" * 30 + "\n",
            parse_mode=parse_mode,
        )

    def _render_item(self, t: TimeSlot) -> str:

        return (
            f"📅 {self._bold("Дата:")} {t.date}\n" f"🕔 {self._bold("Час:")} {t.start}"
        )
