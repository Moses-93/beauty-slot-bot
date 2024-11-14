FROM python:3.12-slim

WORKDIR /app

# Копіюємо requirements.txt
COPY requirements.txt ./

RUN apt update
RUN pip install --upgrade pip
# Встановлюємо залежності з requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо решту файлів
COPY . .

# Запускаємо бота
CMD ["bash", "-c", "alembic revision --autogenerate -m 'Initial migration' && alembic upgrade head && python main.py"]
