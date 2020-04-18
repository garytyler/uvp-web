import aioredis
from app.core.config import settings


class Redis:
    def __init__(self, url):
        self.url = url

    def __getattr__(self, item):
        return getattr(self._redis, item)

    async def connect(self):
        self.pub = await aioredis.create_redis("redis://localhost")
        self.sub = await aioredis.create_redis("redis://localhost")

    async def disconnect(self):
        self.pub.close()
        self.sub.close()
        await self.pub.wait_closed()
        await self.sub.wait_closed()


redis = Redis(url=settings.REDIS_URL)


async def connect_redis():
    await redis.connect()


async def disconnect_redis():
    await redis.disconnect()
