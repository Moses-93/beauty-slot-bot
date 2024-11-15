if alembic history | grep 'Initial migration'; then
    echo "Міграції вже виконані"
    alembic upgrade head
else
    echo "Створюємо міграції"
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head
fi 
mkdir -p /app/logs && touch /app/logs/bot.log
python main.py