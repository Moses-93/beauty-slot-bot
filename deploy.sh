cd /root
cd app/chashurina-brows-bot/
docker compose down
docker pull moses93/telegram-bot:latest
docker compose up -d --remove-orphans
