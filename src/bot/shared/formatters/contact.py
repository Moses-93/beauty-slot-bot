from typing import Literal
from src.application.dto.contact import ContactDTO


class ContactFormatter:
    def __init__(self, parse_mode: Literal["Markdown", "HTML"]):
        self.parse_mode = parse_mode

    def _bold(self, text: str) -> str:
        if self.parse_mode == "HTML":
            return f"<b>{text}</b>"
        return f"*{text}*"

    def format(self, contact: ContactDTO) -> str:
        lines = [self._bold("📕 КОНТАКТНА ІНФОРМАЦІЯ"), ""]

        lines.append(f"📍 {self._bold('Адреса:')} {contact.address}")
        lines.append(f"📞 {self._bold('Телефон:')} {contact.phone_number}")
        lines.append(
            f"⏰ {self._bold('Години роботи:')} {contact.work_start_time} – {contact.work_end_time}"
        )

        if contact.google_maps_link:
            lines.append(f"🗺️ {self._bold('Google Maps:')} {contact.google_maps_link}")
        if contact.instagram_link:
            lines.append(f"📸 {self._bold('Instagram:')} {contact.instagram_link}")
        if contact.telegram_link:
            lines.append(f"✈️ {self._bold('Telegram:')} {contact.telegram_link}")
        if contact.about:
            lines.append(f"🧾 {self._bold('Про мене:')} {contact.about}")

        return "\n".join(lines)
