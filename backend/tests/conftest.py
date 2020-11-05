import contextlib
import os
import random
import socket
from typing import List

import async_asgi_testclient
import pytest
from randstr_plus import randstr

from app.models.features import Feature
from app.models.guests import Guest

# from tortoise.contrib.test import finalizer, initializer


# pytest_plugins = "pytest_asgi_server"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DB_FILE_PATH = os.path.join(BASE_DIR, "test_db.sqlite3")
TEST_DB_URL = f"sqlite://{TEST_DB_FILE_PATH}"


def pytest_runtest_teardown(item, nextitem):
    if os.path.exists(TEST_DB_FILE_PATH):
        os.remove(TEST_DB_FILE_PATH)


@pytest.fixture(autouse=True)
def use_sqlite_memory_db(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", TEST_DB_URL)


def pytest_addoption(parser):
    # Set host/port for multiprocessing test server with command line options
    parser.addoption("--server-port", action="store", type=int)
    parser.addoption("--server-host", action="store", type=int)


def pytest_generate_tests(metafunc):
    """https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_generate_tests"""
    if "server_port" in metafunc.fixturenames:
        metafunc.parametrize("server_port", [metafunc.config.getoption("server_port")])
        metafunc.parametrize("server_host", [metafunc.config.getoption("server_host")])


@pytest.fixture
def app():
    from app.main import app

    yield app


@pytest.fixture
@pytest.mark.asyncio
async def async_client(app):
    def _client(*args, **kwargs):
        return async_asgi_testclient.TestClient(app, *args, **kwargs)

    yield _client


@pytest.fixture
async def xclient(xclient, app, request):
    yield await xclient(
        app,
        appstr="app.main:app",
        env={
            **os.environ,
            "PYTHONPATH": os.path.abspath(request.config.rootdir.strpath),
            "PYTHONDONTWRITEBYTECODE": "1",
        },
    )


@pytest.fixture
def create_random_fake_session_key() -> str:
    def _create_random_fake_session_key():
        return randstr(
            min_length=32,
            max_length=32,
            min_tokens=1,
            max_tokens=1,
            uppercase_letters=True,
            lowercase_letters=True,
            numbers=True,
        )

    return _create_random_fake_session_key


@pytest.fixture
def create_random_euler_rotation():
    def _create_random_euler_rotation() -> List[int]:
        return [random.uniform(0, 360) for i in range(3)]

    return _create_random_euler_rotation


@pytest.fixture
def create_random_guest_obj(faker):
    async def _create_random_guest_obj(feature: Feature) -> Guest:
        return await Guest.create(name=faker.name(), feature_id=feature.id)

    return _create_random_guest_obj


@pytest.fixture
def create_random_feature_title():
    def _create_random_feature_title() -> str:
        return randstr(
            min_length=10,
            max_length=25,
            min_tokens=2,
            max_tokens=6,
            uppercase_letters=True,
            lowercase_letters=True,
            punctuation=True,
            numbers=True,
        )

    return _create_random_feature_title


@pytest.fixture
def create_random_feature_slug():
    def _create_random_feature_slug() -> str:
        string = randstr(
            min_length=10,
            max_length=50,
            min_tokens=3,
            max_tokens=6,
            uppercase_letters=True,
            lowercase_letters=True,
            punctuation=False,
            numbers=True,
        )
        return "-".join(string.split()).lower()

    return _create_random_feature_slug


@pytest.fixture
def create_random_feature_obj(
    create_random_feature_title, create_random_feature_slug
) -> Feature:
    async def _create_random_feature_obj():
        return await Feature.create(
            title=create_random_feature_title(),
            slug=create_random_feature_slug(),
            turn_duration=random.randint(1, 99),
        )

    return _create_random_feature_obj


def _get_unused_tcp_port():
    """Find an unused localhost TCP port from 1024-65535 and return it."""
    with contextlib.closing(socket.socket()) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture
def get_unused_tcp_port():
    return _get_unused_tcp_port
