import asyncio
from weakref import WeakKeyDictionary, WeakSet

import aioredis
from aioredis import Channel
from app.core.config import settings


class Redis:
    def __init__(self, address, **kwargs):
        self.pool = None
        self._address = address
        self._kwargs = kwargs

    async def connect(self):
        self.pool = await aioredis.create_redis_pool(self._address, **self._kwargs)

    async def disconnect(self):
        self.pool.close()
        await self.pool.wait_closed()

    def __getattr__(self, name):
        return getattr(self.pool, name)


redis = Redis(settings.REDIS_URL)


async def connect_redis():
    await redis.connect()


async def disconnect_redis():
    await redis.disconnect()


class ChannelReader:
    """
    Wrapper against aioredis.Channel used to allow multiple readers
    on the same subscription

    Example::

        channels = await redis_pool.subscribe('subscribeme')
        reader = ChannelReader(channels[0])

        for message in reader:
            print(message)

    """

    loops: WeakKeyDictionary = WeakKeyDictionary()

    # time to wait before failing when readers get stuck
    ack_wait_time = 1.0

    def __init__(self, channel: Channel):
        self.channel: Channel = channel

        # if channel was not previously seen, create a new reader task
        if channel not in self.loops:
            weakset: WeakSet = WeakSet()

            self.loops[channel] = weakset
            asyncio.ensure_future(self._main_loop())

        self.subscribers = self.loops[channel]

    async def __aiter__(self):
        """
        Iterate over subscription messages
        """
        future = asyncio.Future()
        self.subscribers.add(future)

        while True:
            value = await future

            # NOTICE: previous future object is removed from the weakset
            # when this new reference is created
            future = asyncio.Future()
            self.subscribers.add(future)

            yield value

    async def _main_loop(self):
        """
        Task reading the actual channel messages and re-dispatching them
        to the different readers

        """
        time = asyncio.get_running_loop().time

        async for message in self.channel.iter():
            subscriber = None
            for subscriber in list(self.subscribers):
                subscriber.set_result(message)

            # Deleting reference to the last weakset entry
            # so it is correctly removed from the set when consumed
            del subscriber

            start = time()
            while True:
                # Wait for all done tasks to be acknowledged
                if not any(fut.done() for fut in self.subscribers):
                    break
                await asyncio.sleep(0)

                # … but don't wait too long (should not happen ©)
                if start + 1 < self.ack_wait_time:
                    raise RuntimeError("Task result not consumed")
