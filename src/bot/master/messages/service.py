class ServiceMessage:

    @staticmethod
    def create() -> str:
        return "🎯 Створімо нову послугу!" "Яка буде її назва? Напишіть її, будь ласка."

    @staticmethod
    def edit() -> str:
        return "✏️ Хочете щось покращити? Оберіть послугу, яку бажаєте оновити."

    @staticmethod
    def deactivate() -> str:
        return "❌ Хочете видалити послугу? Оберіть її зі списку нижче."

    @staticmethod
    def enter_title() -> str:
        return "📝 Введіть назву послуги:"

    @staticmethod
    def enter_price() -> str:
        return (
            "💸 Супер! Тепер вкажіть вартість цієї послуги.\n"
            "Наприклад: 250 або 499.90 грн."
        )

    @staticmethod
    def enter_duration() -> str:
        return (
            "⏳ Чудово! Тепер вкажіть тривалість послуги в хвилинах цілим числом без секунд.\n"
            "Наприклад: 30 або 45"
        )

    def select_field() -> str:
        return "Оберіть поле, яке ви бажаєте оновити"

    def enter_new_value(field: str) -> str:
        return (
            f"Введіть нове значення для поля {field}.\n"
            "Наприклад: для ціни - 250 або 499.90 грн, "
            "для тривалості - 30 або 45 хвилин."
        )

    @staticmethod
    def success_create(title: str, price: int, duration: int) -> str:
        return (
            "🎉 Вітаю! Нова послуга успішно створена!\n"
            f"Назва: {title}\nЦіна: {price} грн\n Тривалість: {duration}\nТепер клієнти можуть нею скористатися!"
        )

    @staticmethod
    def success_edit(title: str, field: str, new_value: str) -> str:
        return (
            f"✅ Вітаю! Послуга {title} успішно оновлена!\n"
            f"Поле: {field}\nНовий запис: {new_value}"
        )

    @staticmethod
    def success_deactivate(title: str) -> str:
        return (
            f"❌ Послуга {title} успішно видалена!\n"
            "Тепер вона недоступна для запису."
        )

    @staticmethod
    def fail_create() -> str:
        return "Ой, не вдалося створити нову послугу 😢." "Спробуйте трохи пізніше!"

    @staticmethod
    def fail_edit() -> str:
        return "Упс, не вдалося оновити послугу 😢." "Спробуйте трохи пізніше!"
