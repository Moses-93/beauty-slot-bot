from aiogram import Router, F

from src.bot.shared.handlers.display import DisplayHandler


class DisplayRouter:
    def __init__(self, display_handler: DisplayHandler):
        self._router = Router(name="display_router")
        self._handler = display_handler
        self._register()

    def _register(self):
        self._router.message.register(
            self._handler.show_contacts,
            F.text.in_(["📕 Контакти", "📕 Мої контакти"]),
        )
        self._router.message.register(
            self._handler.show_services,
            F.text.in_("📋 Послуги", "📋 Список послуг"),
        )
        self._router.message.register(
            self._handler.show_dates,
            F.text.in_("🗓 Доступні дати", "📅 Список дат"),
        )

        self._router.callback_query.register(
            self._handler.show_active_bookings,
            F.data == "active_bookings",
        )
        self._router.callback_query.register(
            self._handler.show_all_bookings,
            F.data == "all_bookings",
        )

    @property
    def router(self) -> Router:
        return self._router
