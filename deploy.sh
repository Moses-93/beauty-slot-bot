cd /root
app/chashurina-brows-bot/deploy.sh
docker pull moses93/telegram-bot:latest
docker compose up -d --remove-orphans
