class BookingMessage:

    @staticmethod
    def start() -> str:
        return (
            "Вітаю! Я ваш особистий асистент для запису на послуги.\n"
            "Щоб почати, виберіть послугу, на яку ви хочете записатися."
        )

    @staticmethod
    def select_date() -> str:
        return "📅 Чудово! Тепер оберіть бажану дату для запису:"

    @staticmethod
    def enter_time() -> str:
        return "🕒 Тепер введіть бажаний час для запису (формат: ГГ:ХХ):"

    @staticmethod
    def choose_reminder() -> str:
        return (
            "🌟 Відмінно!\n"
            "Тепер вкажіть, за скільки годин до запису ви бажаєте отримати нагадування. ⏰"
        )

    @staticmethod
    def success(service_title: str, date: str, time: str) -> str:
        return (
            f"🎉 Вітаю! Ви успішно записалися на послугу {service_title}./n"
            f"Я чекаю на вас {date} o {time}!"
        )

    @staticmethod
    def confirmation_prompt(service_title: str, date: str, time: str) -> str:
        return (
            "🎉 Чудово! Ми майже закінчили.\n\n"
            f"Ви обрали послугу: **{service_title}**\nДата: **{date}**\nЧас: **{time}**\n\n"
            f'Якщо все вірно, натисніть кнопку "Підтвердити". Якщо бажаєте скасувати, натисніть "Скасувати". ❓'
        )

    @staticmethod
    def cancelled_by_user() -> str:
        return (
            "😔 Мені шкода, що ви не записалися цього разу."
            "Але, я завжди рада вас бачити! Чекаю на вас знову! ❤️"
        )

    @staticmethod
    def select_booking_to_cancel() -> str:
        return "❗️ Будь ласка, виберіть запис, який ви хочете скасувати."

    @staticmethod
    def cancelled() -> str:
        return (
            "✅ Ваш запис успішно скасовано."
            "Дякуємо, що скористалися моїми послугами!"
        )

    @staticmethod
    def time_is_busy() -> str:
        return (
            "❗️ На жаль, обраний вами час вже зайнятий.\n"
            "Будь ласка, виберіть інший час або дату."
        )

    @staticmethod
    def not_found() -> str:
        return "❗️ На жаль, я не зміг знайти ваших записів"
