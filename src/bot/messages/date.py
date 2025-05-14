class DateMessage:

    @staticmethod
    def start() -> str:
        return (
            "👋 Вітаю в розділі керування датами."
            "Тут ви можете додавати, видаляти та переглядати ваші вільні дати!"
        )

    @staticmethod
    def enter_date() -> str:
        return (
            "Почнімо! 🚀 Введіть нову дату у форматі DD.MM.YYYY, і ми все налаштуємо!"
        )

    @staticmethod
    def enter_deactivation_time(date: str) -> str:
        return (
            "Чудово! 🕒 Тепер вкажіть час, коли дата має автоматично видалитися."
            f"Наприклад, якщо ви введете 17:00, дата зникне {date} о 17:00:00."
        )

    @staticmethod
    def deactivate() -> str:
        return "Окей! 📅 Оберіть дату, яку ви хочете видалити."

    @staticmethod
    def success_create(date: str) -> str:
        return (
            f"Супер! 🎁 Дата: {date} успішно створена!"
            "Ваші клієнти вже можуть записуватися!"
        )

    @staticmethod
    def success_deactivate(date: str) -> str:
        return f"Послуга {date} успішно видалена! ❌\nТепер вона недоступна для запису."
