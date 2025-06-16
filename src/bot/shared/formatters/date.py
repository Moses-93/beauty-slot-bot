from typing import Literal
from src.application.dto.date import DateDTO
from src.bot.shared.formatters.base import BaseFormatter


class DateFormatter(BaseFormatter):
    def __init__(self, parse_mode: Literal["Markdown", "HTML"]):
        super().__init__(
            header="📅 ДОСТУПНІ ДАТИ",
            separator="\n" + "=" * 30 + "\n",
            parse_mode=parse_mode,
        )

    def _render_item(self, d: DateDTO):

        return f"📅 {self._bold("Дата:")} {d.date}"
