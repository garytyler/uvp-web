from typing import Callable

from ..services.broadcasting import connect_broadcaster, disconnect_broadcaster


def create_startup_event_handler() -> Callable:
    async def on_startup() -> None:
        await connect_broadcaster()

    return on_startup


def create_shutdown_event_handler() -> Callable:
    async def on_shutdown() -> None:
        await disconnect_broadcaster()

    return on_shutdown
