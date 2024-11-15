#!/bin/bash
echo "Current directory: $(pwd)"
cd /root || exit
echo "Changed to /root: $(pwd)"
cd app/chashurina-brows-bot/ || exit
echo "Changed to app directory: $(pwd)"
docker compose down
docker pull moses93/telegram-bot:latest
docker compose up -d --remove-orphans
