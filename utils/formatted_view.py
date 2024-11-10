def escape_md(text: str) -> str:
    escape_chars = r"\_*[]()~`>#+-=|{}.!"
    return "".join(f"\\{char}" if char in escape_chars else char for char in text)


class ViewController:
    def __init__(self, notes=None, services=None, dates=None, view_type=None) -> None:
        self.notes = notes
        self.services = services
        self.dates = dates
        self.view_type = (
            view_type  # Тип виду, який хочемо відобразити: 'active', 'master', 'all'
        )

    def get(self):
        if self.notes:
            return FormattingView.format_notes(self.notes, self.view_type)
        elif self.services:
            return FormattingView.format_services(self.services)
        elif self.dates:
            return FormattingView.format_dates(self.dates)
        return None


from operator import attrgetter


class FormattingView:
    @staticmethod
    def format_services(services):
        header = "*Послуги:*\n\n*ID* | *Послуга* | *Ціна* | *Тривалість*\n-------------------------------------\n"
        body = "\n".join(
            f"{service.id} | {service.name} | {service.price} грн. | {service.durations} хв."
            for service in services
        )
        return header + body

    @staticmethod
    def format_notes(notes, view_type=None):
        headers = {
            "active": "*Активні записи:*\n\n*ID* | *Послуга* | *Дата* | *Час*\n-------------------------------------\n",
            "master": "*Всі записи для майстра:*\n\n*Ім'я користувача* | *Послуга* | *Дата* | *Час*\n-------------------------------------\n",
            "all": "*Всі записи:*\n\n*Послуга* | *Дата* | *Час*\n-------------------------------------\n",
        }

        sorted_notes = sorted(notes, key=attrgetter("free_date.date", "time"))

        if view_type == "active":
            body = "\n".join(
                f"{note.id} | {note.service.name} | {note.free_date.date} | {note.time}"
                for note in sorted_notes
            )
        elif view_type == "master":
            body = "\n".join(
                f"{escape_md(note.username if note.username else note.name)} | {note.service.name} | {note.free_date.date} | {note.time}"
                for note in sorted_notes
            )
        else:
            body = "\n".join(
                f"{note.service.name} | {note.free_date.date} | {note.time}"
                for note in sorted_notes
            )

        return headers.get(view_type, headers["all"]) + body

    @staticmethod
    def format_dates(dates):
        header = "*Доступні дати: *\n\n*ID* | *Дата*\n-------------------------------------\n"
        body = "\n".join(f"{date.id} | {date.date}" for date in dates)
        return header + body
