class TemplateManager:

    @staticmethod
    async def message_to_the_master(
        username: str, service: str, date, time, booking_cancel=False
    ):
        message = (
            f"{"Скасований запис:\n" if booking_cancel else "Новий запис:\n"}"
            f"Користувач: {username}\n"
            f"Послуга: {service if service else None}\n"
            f"Дата: {date}\n"
            f"Час: {time}\n"
        )
        return message

    @staticmethod
    def get_delete_notification(date=False):
        message = (
            f"Шановний клієнте, на жаль, {"дата," if date else "послуга"} на яку ви були записані більше недоступна\n"
            f"Приносимо щирі вибачення та пропонуємо записатись на іншу {"дату" if date else "послугу"}"
        )
        return message

    @staticmethod
    def get_warning_del_date_or_service(date=False):
        message = (
            "ПОПЕРЕДЖЕННЯ!\n"
            f"На цю {"дату" if date else "послугу"} записані клієнти.\n"
            f"Видаливши цю {"дату" if date else "послугу"} ви скасуєте всі активні записи пов'язані з нею. \n"
            f"Клієнтам буде відправлено повідомлення про скасування запису."
        )
        return message

    @staticmethod
    def get_add_new_date(add=False, date=None):
        if add:
            message = "Введіть дату в форматі YYYY-MM-DD:"
            return message
        if date:
            message = f"Дата - {date} успішно додана!"
            return message

    @staticmethod
    def get_select_service_or_date_del(
        id=None, success=False, active=False, date=False
    ):
        if success:
            message = f"{"Дата" if date else "Послуга"} з ID: {id} успішно видалена!"
            return message
        elif active:
            message = (
                f"{"Дата" if date else "Послуга"} успішно видалена.\n"
                f"Записи клієнтів на цю {"дату" if date else "послугу"} скасовано.\n"
                "Клієнтам надіслано сповіщення."
            )
            return message
        else:
            message = (
                f"Оберіть, яку {"дату" if date else "послугу"} Ви хочете видалити:"
            )
            return message

    @staticmethod
    def elapsed_time_warning(time):
        message = f"Ви не можете обрати {time.time()}, оскільки він вже пройшов"
        return message

    @staticmethod
    def get_greeting_message():
        message = "Чим можу бути корисний?"
        return message
