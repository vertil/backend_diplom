import redis
from settings import settings

redis_client = redis.Redis.from_url(settings.redis_url)


def get_redis_session() -> redis.Redis:
    try:
        return redis_client
    finally:
        redis_client.close()
