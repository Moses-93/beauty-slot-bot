from typing import Literal
from src.bot.shared.formatters.base import BaseFormatter
from src.application.dto.service import ServiceDTO


class ServiceFormatter(BaseFormatter[ServiceDTO]):
    def __init__(self, parse_mode: Literal["Markdown", "HTML"]):
        super().__init__(
            header="📋 ДОСТУПНІ ПОСЛУГИ",
            separator="\n" + "=" * 30 + "\n",
            parse_mode=parse_mode,
        )

    def _render_item(self, s: ServiceDTO) -> str:
        duration = int(s.duration.total_seconds() // 60)

        return (
            f"🧴 {self._bold("Послуга:")} {s.title}\n"
            f"⏱ {self._bold("Тривалість:")} {duration} хв\n"
            f"💰 {self._bold("Ціна:")} {s.price} грн"
        )
