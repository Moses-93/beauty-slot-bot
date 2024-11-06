from datetime import datetime, time
from db.models import Notes, Service, FreeDate


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
    def get_booking_confirmation(service: Service, date: FreeDate, time: time):
        message = (
            f"Ви щойно здійснили запис на послугу - {service.name}\n"
            f"Чекаю Вас {date.date} o {time}.\n"
            f"Будь ласка, зв'яжіться зі мною, коли будете знаходитись за моєю адресою. Я Вас зустріну\n"
            "Якщо Ви розумієте, що не прийдете або запізнюєтесь - будь ласка, скасуйте запис або повідомте про це мене"
        )
        return message

    @staticmethod
    def message_to_the_master(username: str, service: Service, date: FreeDate, time):
        message = (
            f"Новий запис:\n"
            f"Користувач: {username}\n"
            f"Послуга: {service.name}\n"
            f"Дата: {date.date}\n"
            f"Час: {time}\n"
        )

        return message

    @staticmethod
    def get_cancel_notification():
        message = f"Запис скасовано"
        return message

    @staticmethod
    def elapsed_time_warning(time:datetime):
        message = f"Ви не можете обрати {time.time()}, оскільки він вже пройшов"
        return message

    @staticmethod
    def service_selection_info(service: Service):
        message = f"Ви обрали '{service.name}'. Вартість: {service.price} грн.\
            \nОберіть дату, на яку бажаєте записатись"
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
    def no_entries_found():
        message = "На жаль, я не зміг знайти жодних записів у обраній категорії("
        return message

    @staticmethod
    def date_selection_prompt(date: FreeDate):
        message = f"Ви обрали {date.date}. Напишіть час до 18:00 у форматі 'ГГ:ХХ'"
        return message

    @staticmethod
    def successful_booking_notification(service: Service, date: FreeDate, time):
        message = f"Ви успішно записались на послугу - {service.name}. \nЧекаю на Вас {date.date} о {time}"
        return message

    @staticmethod
    def get_reminder():
        message = "Оберіть за скільки годин бажаєте отримати нагадування:"
        return message

    @staticmethod
    def get_reminder_notification(hour: int):
        message = f"Нагадування буде надіслано за {hour} год. до запису."
        return message

    @staticmethod
    def recording_reminder(note: Notes):
        message = (
            f"Нагадуємо, Ви записані на послугу - {note.service.name}\n"
            f"Дата: {note.free_date.date}\n"
            f"Час: {note.time}\n"
            "Адреса: вул. Перлинна 3. ЖК 5 Перлина\n"
        )
        return message

    @staticmethod
    def get_booking_cancellation(note: Notes):
        message = (
            f"Користувач {note.username} скасував запис:\n"
            f"Послуга: {note.service.name} \n"
            f"Дата: {note.free_date.date} \n"
            f"Час: {note.time}"
        )
        return message

    @staticmethod
    def booking_not_found():
        message = "На жаль, такого запису не знайдено"
        return message


template_manager = TemplateManager()
