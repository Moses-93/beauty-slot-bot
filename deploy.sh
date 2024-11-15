cd /root
cd app/chashurina-brows-bot/
docker pull moses93/telegram-bot:latest
docker compose down
docker compose up -d --remove-orphans
