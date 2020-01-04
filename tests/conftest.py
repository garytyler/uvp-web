import logging
import random
from collections import OrderedDict
from string import ascii_lowercase
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


@pytest.fixture(autouse=True, scope="function")
def flush_redis_cache_at_session_start():
    get_redis_connection("default").flushall()


@pytest.fixture(autouse=True, scope="function")
def flush_redis_cache_at_function_finish():
    yield
    get_redis_connection("default").flushall()


@pytest.fixture
async def fake_guest_factory(guest_name_factory) -> AsyncGenerator:
    communicators = []

    async def _fake_guest_factory(feature_slug: str) -> OrderedDict:
        guest_name = guest_name_factory()
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
async def connected_presenter_feature_factory(
    fake_guest_factory, feature_factory, fake_presenter_factory, transactional_db
):
    async def _connected_presenter_feature_factory():
        # Create objects
        feature = await db_sync_to_async(feature_factory)()
        presenter = await fake_presenter_factory(feature_slug=feature.slug)

        # Connect guest & presenter
        connected, subprotocol = await presenter["communicator"].connect()
        assert connected

        # Get latest feature state after connecting
        feature = await db_sync_to_async(
            lambda: Feature.objects.get(slug=feature.slug)
        )()

        return presenter, feature

    return _connected_presenter_feature_factory


@pytest.fixture
async def connected_presenter_feature_objs(connected_presenter_feature_factory,):
    return await connected_presenter_feature_factory()


@pytest.fixture
async def connected_guest_presenter_feature_factory(
    fake_guest_factory, feature_factory, fake_presenter_factory, transactional_db
):
    async def _connected_guest_presenter_feature_factory():
        # Create objects
        feature = await db_sync_to_async(feature_factory)()
        guest = await fake_guest_factory(feature_slug=feature.slug)
        presenter = await fake_presenter_factory(feature_slug=feature.slug)

        # Connect guest & presenter
        connected, subprotocol = await presenter["communicator"].connect()
        assert connected
        connected, subprotocol = await guest["communicator"].connect()
        assert connected

        # Get latest feature state after connecting
        feature = await db_sync_to_async(
            lambda: Feature.objects.get(slug=feature.slug)
        )()

        return guest, presenter, feature

    return _connected_guest_presenter_feature_factory


@pytest.fixture
async def connected_guest_presenter_feature_objs(
    connected_guest_presenter_feature_factory,
):
    return await connected_guest_presenter_feature_factory()


@pytest.fixture
def random_string_factory() -> Callable:
    """Create a new random string. Will not return the same string twice. All letters
    are lowercase."""
    _used: list = []

    def _random_string_factory(
        letters: bool = True,
        numbers: bool = True,
        num_words_min: int = 1,
        num_words_max: int = 1,
        word_length_min: int = 3,
        word_length_max: int = 9,
    ) -> str:

        word_length_min = word_length_min or 1
        word_length_max = word_length_max or 1
        num_words_min = num_words_min or 1
        num_words_max = num_words_max or 1

        options: list = list()
        if letters:
            options += ascii_lowercase
        if numbers:
            options += "".join([str(n) for n in range(9)])

        while True:
            words = []
            for n in range(random.randint(num_words_min, num_words_max)):
                word_length = random.randint(word_length_min, word_length_max)
                words.append("".join(random.choices(options, k=word_length)))
            result = " ".join(words)
            if result not in _used:
                _used.append(result)
                return result

    return _random_string_factory


@pytest.fixture
def guest_name_factory(random_string_factory) -> Callable:
    """Create a new random guest name"""

    def _guest_name_factory() -> str:
        return random_string_factory(
            letters=True,
            numbers=False,
            num_words_min=1,
            num_words_max=3,
            word_length_min=3,
            word_length_max=9,
        ).title()

    return _guest_name_factory


@pytest.fixture
def feature_title_factory(random_string_factory) -> Callable:
    """Create a new random guest name"""

    def _feature_title_factory() -> str:
        return random_string_factory(
            letters=True,
            numbers=False,
            num_words_min=2,
            num_words_max=3,
            word_length_min=2,
            word_length_max=9,
        ).title()

    return _feature_title_factory


@pytest.fixture
def session_key_factory(random_string_factory) -> Callable[[], str]:
    """Create a new random 32-character integer that imitates a session key"""

    def _create_session_key() -> str:
        while True:
            return random_string_factory(
                letters=True,
                numbers=True,
                num_words_min=1,
                num_words_max=1,
                word_length_min=32,
                word_length_max=32,
            )

    return _create_session_key


@pytest.fixture
def feature_factory(feature_title_factory):
    def _feature_factory(title=None):
        feature_title = title or feature_title_factory()
        feature = Feature.objects.create(title=feature_title)
        return feature

    return _feature_factory


@pytest.fixture
def SessionStore():
    yield Session.get_session_store_class()


@pytest.fixture
def random_orientation():
    return [random.uniform(0, 360) for i in range(3)]
