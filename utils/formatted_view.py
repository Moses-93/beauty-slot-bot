def format_services(services):
    # Формат заголовка
    result = "*Послуги:*\n\n"
    result += "*ID* | *Послуга* | *Ціна* | *Тривалість*\n"
    result += "-------------------------------------\n"

    for service in services:
        # Форматування рядка для кожної послуги
        result += f"{service.id} | {service.name} | {service.price} грн. | {service.durations} хв.\n"

    return result

def format_notes(notes, active_notes=False):
    # Збираємо заголовок
    if active_notes:
        result = "*Активні записи:*\n\n"
        result += "*ID* | *Послуга* | *Дата* | *Час*\n"
        result += "-------------------------------------\n"

        for note in notes:
            result += f"{note.id} | {note.service.name} | {note.free_date.date} | {note.time}\n"
        return result
        
    result = "*Всі записи:*\n\n"
    result += "*Послуга* | *Дата* | *Час*\n"
    result += "-------------------------------------\n"

    # Додаємо записи
    for note in notes:
        result += f"{note.service.name} | {note.free_date.date} | {note.time}\n"

    return result

def format_dates(dates):
    result = "*Доступні дати: *\n\n"
    result += "*ID* | *Дата*\n"
    result += "-------------------------------------\n"

    for date in dates:
        result += f"{date.id} | {date.date}\n"
    
    return result