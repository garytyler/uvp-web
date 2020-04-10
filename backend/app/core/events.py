from typing import Callable

from ..services.broadcasting import connect_broadcaster, disconnect_broadcaster

# from ..services.caching import connect_redis, disconnect_redis


def create_startup_event_handler() -> Callable:
    async def on_startup() -> None:
        await connect_broadcaster()
        # await connect_redis()

    return on_startup


def create_shutdown_event_handler() -> Callable:
    async def on_shutdown() -> None:
        await disconnect_broadcaster()
        # await disconnect_redis()

    return on_shutdown
