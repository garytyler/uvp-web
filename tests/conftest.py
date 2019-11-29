import asyncio
import logging
import random
from collections import OrderedDict
from string import ascii_letters
from typing import AsyncGenerator, Awaitable, Callable, Optional, Tuple

import pytest
from channels.testing import WebsocketCommunicator
from django.test import Client
from django_redis import get_redis_connection

from seevr.routing import application


@pytest.fixture(autouse=True)
def suppress_application_log_capture(caplog):
    caplog.set_level(logging.CRITICAL, logger="")
    caplog.set_level(logging.CRITICAL, logger="live")


@pytest.fixture(autouse=True, scope="function")
def flush_redis_cache():
    get_redis_connection("default").flushall()


@pytest.fixture
def communicator_factory() -> Callable:
    def _create_communicator(path, client):
        communicator = WebsocketCommunicator(
            application=application,
            path=path,
            headers=[
                (b"cookie", f"sessionid={client.session.session_key}".encode("ascii"))
            ],
        )
        return communicator

    return _create_communicator


@pytest.fixture
async def client_communicator_factory(communicator_factory) -> AsyncGenerator:
    communicators = []

    async def _create_communicator(
        path: str, client: Client = None, connect: bool = False
    ) -> Tuple[Client, WebsocketCommunicator]:
        client = client if client else Client()
        communicator = communicator_factory(path=path, client=client)
        communicators.append(communicator)

        if connect:
            connected, subprotocol = await communicator.connect()
            assert connected is True
            await asyncio.sleep(0.5)
        return client, communicator

    yield _create_communicator

    for communicator in communicators:
        communicator.disconnect()


@pytest.fixture
async def connection_factory(
    client_communicator_factory,
) -> Callable[[str, Optional[bool]], Awaitable]:
    async def _create_connection(path, connect=False) -> OrderedDict:
        client, communicator = await client_communicator_factory(
            path=path, connect=connect
        )
        return OrderedDict([("client", client), ("communicator", communicator)])

    return _create_connection


@pytest.fixture
async def guest_factory(connection_factory) -> Callable[[Optional[bool]], Awaitable]:
    async def _create_guest(connect=False) -> OrderedDict:
        return await connection_factory(path="/ws/guest/", connect=connect)

    return _create_guest


@pytest.fixture
async def feature_factory(connection_factory) -> Callable[[Optional[bool]], Awaitable]:
    async def _create_feature(connect=False) -> OrderedDict:
        return await connection_factory(path="/ws/mediaplayer/", connect=connect)

    return _create_feature


@pytest.fixture
def random_string_factory() -> Callable:
    """Return a random string"""

    def _create_random_string(minimum: int = 5, maximum: int = 9) -> str:
        length = random.randint(minimum, maximum)
        return "".join(random.choices(ascii_letters, k=length))

    return _create_random_string


@pytest.fixture
def session_key_factory() -> Callable[[], int]:
    """Return a random 32-character integer that imitates a session key"""

    def _create_session_key() -> int:
        return int("".join([str(random.choice(range(9))) for n in range(32)]))

    return _create_session_key
