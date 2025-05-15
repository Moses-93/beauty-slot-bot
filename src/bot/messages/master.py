class MasterMessages:

    @staticmethod
    def start() -> str:
        return "👋 Привіт. Радий тебе бачити.\nПочнімо працювати!"

    @staticmethod
    def services_menu() -> str:
        return (
            "👋 Вітаю в розділі керування послугами!"
            "Тут ви можете створювати нові послуги, редагувати наявні або видаляти їх."
        )

    @staticmethod
    def dates_menu() -> str:
        return (
            "👋 Вітаю в розділі керування датами!"
            "Тут ви можете створювати нові дати, редагувати наявні або видаляти їх."
        )

    @staticmethod
    def bookings_menu() -> str:
        return (
            "👋 Вітаю в розділі керування записами!"
            "Тут ви можете переглядати записи ваших клієнтів."
        )
