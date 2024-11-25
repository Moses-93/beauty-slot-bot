from datetime import datetime, time
from db.models import Notes
from cache.cache import request_cache, user_cache


class TemplateManager:

    @staticmethod
    def get_contacts_info():
        message = (
            "Адреса: [Вул. Перлинна 3](https://maps.app.goo.gl/coiRjcbFzwMTzppz8)\n"
            "Telegram: @chashurina\n"
            "Instagram: [chashurina_brows](https://www.instagram.com/chashurina_brows?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==)\n"
            "Телефон: +380934050798"
        )
        return message

    @staticmethod
    async def get_booking_confirmation(user_id: int, time: time):
        service, date = await user_cache.get_user_cache(user_id, "service", "date")
        message = (
            f"Ви щойно здійснили запис на послугу - {service.name}\n"
            f"Чекаю Вас {date.date} o {time}.\n"
            f"Будь ласка, зв'яжіться зі мною, коли будете знаходитись за моєю адресою. Я Вас зустріну\n"
            "Якщо Ви розумієте, що не прийдете або запізнюєтесь - будь ласка, скасуйте запис або повідомте про це мене"
        )
        return message

    @staticmethod
    async def message_to_the_master(
        username: str, service: str, date: datetime, time, booking_cancel=False
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
    def get_add_new_service(
        name=False, price=False, durations=False, success=False, service=None
    ):
        if name:
            message = (
                "Для того, щоб додати послугу - заповніть всі запропоновані поля.\n"
                "Введіть назву послуги:"
            )
            return message
        elif price:
            message = "Введіть ціну послуги:"
            return message
        elif durations:
            message = "Вкажіть тривалість послуги у хвилинах:"
            return message
        elif success:
            message = f"Послуга - {service} успішно додана!"
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
    def get_edit_service(choice=False, field=None, new_value=None):
        if field and new_value:
            message = f"Значення поля {field} успішно змінено на {new_value}!"
            return message
        elif choice:
            message = "Оберіть, яке поле Ви хочете редагувати"
            return message
        elif field:
            message = f"Введіть нове значення поля {field} {"в хвилинах:" if field == "durations" else":"}"
            return message
        else:
            message = "Оберіть, яку послугу Ви хочете редагувати"
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
    def get_cancel_notification():
        message = f"Запис скасовано"
        return message

    @staticmethod
    def elapsed_time_warning(time: datetime):
        message = f"Ви не можете обрати {time.time()}, оскільки він вже пройшов"
        return message

    @staticmethod
    def service_selection_info():
        message = "Оберіть дату, на яку бажаєте записатись"
        return message

    @staticmethod
    def busy_time_notification(time):
        message = f"На жаль, вказаний вами час зайнятий. Найближчий доступний час: {time}.\
        \nОберіть цей час, або вкажіть інший"
        return message

    @staticmethod
    def get_greeting_message():
        message = "Чим можу бути корисний?"
        return message

    @staticmethod
    def get_service_options():
        message = "Оберіть бажану послугу:"
        return message

    @staticmethod
    def get_entry_options():
        message = "Оберіть потрібні Вам записи:"
        return message

    @staticmethod
    def booking_not_found():
        message = "На жаль, я не зміг знайти жодних записів у обраній категорії("
        return message

    @staticmethod
    def date_selection_prompt():
        message = f"Напишіть час до 18:00 у форматі 'ГГ:ХХ'"
        return message

    @staticmethod
    async def successful_booking_notification(user_id: int, time: time):
        service, date = await user_cache.get_user_cache(user_id, "service", "date")
        message = f"Ви успішно записались на послугу - {service.name}. \nЧекаю на Вас {date.date} о {time}"
        return message

    @staticmethod
    def get_reminder(choice=False, hour=None, note: Notes = None):
        if choice:
            message = "Оберіть за скільки годин бажаєте отримати нагадування:"
            return message
        if note:
            message = (
                f"Нагадуємо, Ви записані на послугу - {note.service.name}\n"
                f"Дата: {note.free_date.date}\n"
                f"Час: {note.time}\n"
                "Адреса: вул. Перлинна 3. ЖК 5 Перлина\n"
            )
            return message

        else:
            message = f"Нагадування буде надіслано за {hour} год. до запису."
            return message


template_manager = TemplateManager()
