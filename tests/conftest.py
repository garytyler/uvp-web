import logging
import random
from collections import OrderedDict
from string import ascii_letters, ascii_lowercase
from typing import AsyncGenerator, Callable

import pytest
from channels.db import database_sync_to_async as db_sync_to_async
from channels.testing import WebsocketCommunicator
from django.contrib.sessions.models import Session
from django.core.management import call_command
from django.test import Client
from django_redis import get_redis_connection

from live.models import Feature
from seevr.routing import application


@pytest.fixture(autouse=True)
def suppress_application_log_capture(caplog):
    caplog.set_level(logging.CRITICAL, logger="")
    caplog.set_level(logging.CRITICAL, logger="live")


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("flush", "--noinput")


@pytest.fixture(autouse=True, scope="session")
def flush_redis_cache_at_session_start():
    get_redis_connection("default").flushall()


@pytest.fixture(autouse=True, scope="function")
def flush_redis_cache_at_function_finish():
    yield
    get_redis_connection("default").flushall()


@pytest.fixture
async def fake_guest_factory(random_string_factory) -> AsyncGenerator:
    communicators = []

    async def _fake_guest_factory(feature_slug: str) -> OrderedDict:
        guest_name = random_string_factory()
        client = Client()
        await db_sync_to_async(
            lambda: client.post(f"/{feature_slug}/", {"guest_name": guest_name})
        )()
        communicator = WebsocketCommunicator(
            application=application,
            path=f"/ws/guest/{feature_slug}/",
            headers=[
                (b"cookie", f"sessionid={client.session.session_key}".encode("ascii"),)
            ],
        )
        communicators.append(communicator)
        return OrderedDict([("client", client), ("communicator", communicator)])

    yield _fake_guest_factory
    for communicator in communicators:
        await communicator.disconnect()


@pytest.fixture
async def fake_presenter_factory() -> AsyncGenerator:
    communicators = []

    async def _fake_presenter_factory(feature_slug: str) -> OrderedDict:
        client = Client()
        communicator = WebsocketCommunicator(
            application=application,
            path=f"/ws/presenter/{feature_slug}/",
            headers=[
                (b"cookie", f"sessionid={client.session.session_key}".encode("ascii"),)
            ],
        )
        communicators.append(communicator)
        return OrderedDict([("client", client), ("communicator", communicator)])

    yield _fake_presenter_factory
    for communicator in communicators:
        await communicator.disconnect()


@pytest.fixture
def random_string_factory() -> Callable:
    """Return a random string"""

    def _create_random_string(minimum: int = 5, maximum: int = 9) -> str:
        length = random.randint(minimum, maximum)
        return "".join(random.choices(ascii_letters, k=length))

    return _create_random_string


@pytest.fixture
def session_key_factory() -> Callable[[], str]:
    """Return a random 32-character integer that imitates a session key"""

    def _create_session_key() -> str:
        letters = ascii_lowercase
        numbers = "".join([str(n) for n in range(9)])
        return "".join([random.choice(numbers + letters) for n in range(32)])

    return _create_session_key


@pytest.fixture
def feature_factory(random_string_factory):
    def _feature_factory(title=None):
        title = title if not None else random_string_factory(10, 20).capitalize()
        feature_title = random_string_factory(11, 14).upper()
        feature = Feature.objects.create(title=feature_title)
        return feature

    return _feature_factory


@pytest.fixture
def SessionStore():
    yield Session.get_session_store_class()
