from app.core.config import settings
from broadcaster import Broadcast

broadcast = Broadcast(settings.REDIS_URL)


async def connect_broadcaster():
    await broadcast.connect()


async def disconnect_broadcaster():
    await broadcast.disconnect()
