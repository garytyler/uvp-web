import aioredis
from app.core.config import settings


class Redis:
    def __init__(self, url):
        self.url = url

    def __getattr__(self, item):
        return getattr(self._redis, item)

    async def connect(self):
        self._redis = await aioredis.create_redis(self.url)

    async def disconnect(self):
        self._redis.close()
        await self._redis.wait_closed()


redis = Redis(url=settings.REDIS_URL)


async def connect_redis():
    await redis.connect()


async def disconnect_redis():
    await redis.disconnect()
