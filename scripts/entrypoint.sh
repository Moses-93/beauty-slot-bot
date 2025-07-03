sleep 5

echo "Applying migrations..."

alembic upgrade head

python -m src.bootstrap.main