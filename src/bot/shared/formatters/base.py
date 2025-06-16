from abc import ABC, abstractmethod
from typing import Sequence, Generic, TypeVar

T = TypeVar("T")


class BaseFormatter(ABC, Generic[T]):
    def __init__(
        self,
        header: str,
        separator: str = "\n",
        parse_mode: str = "Markdown",
    ):
        self.header = header
        self.separator = separator
        self.parse_mode = parse_mode

    @abstractmethod
    def _render_item(self, item: T) -> str:
        pass

    def _render_header(self) -> str:
        return self._bold(self.header) + "\n\n"

    def _bold(self, text: str) -> str:
        if self.parse_mode == "HTML":
            return f"<b>{text}</b>"
        return f"*{text}*"

    def format(self, items: Sequence[T]) -> str:
        lines = [self._render_item(item) for item in items]
        body = self.separator.join(lines)
        return self._render_header() + body
