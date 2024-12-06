from aiocache import caches


caches.set_config(
    {
        "default": {  # Конфігурація для кешу за замовчуванням
            "cache": "aiocache.SimpleMemoryCache",
            "serializer": {"class": "aiocache.serializers.StringSerializer"},
        },
        "queries_cache": {  # Кеш для запитів
            "cache": "aiocache.SimpleMemoryCache",
            "serializer": {"class": "aiocache.serializers.StringSerializer"},
        },
        "users_cache": {  # Кеш для даних користувачів
            "cache": "aiocache.SimpleMemoryCache",
            "serializer": {"class": "aiocache.serializers.JsonSerializer"},
        },
    }
)
