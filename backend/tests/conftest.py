import contextlib
import os
import random
import socket
from functools import lru_cache
from typing import Callable, List

import pytest
from asgi_lifespan import LifespanManager
from randstr_plus import randstr

from app.core import config
from app.core.security import get_password_hash
from app.models.features import Feature
from app.models.guests import Guest
from app.models.users import User
from app.schemas.users import UserDbCreate

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DB_FILE_PATH = os.path.join(BASE_DIR, "test_db.sqlite3")
TEST_DB_URL = f"sqlite://{TEST_DB_FILE_PATH}"


@lru_cache
def get_settings_override():
    return config.Settings(DATABASE_URL=TEST_DB_URL)


config.get_settings = get_settings_override  # noqa


def pytest_runtest_teardown(item, nextitem):
    if os.path.exists(TEST_DB_FILE_PATH):
        os.remove(TEST_DB_FILE_PATH)


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
async def app(request):
    from app.main import app

    async with LifespanManager(app):
        yield app


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
def create_random_fake_session_key() -> Callable:
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
    def _create_random_euler_rotation() -> List[float]:
        return [random.uniform(0, 360) for i in range(3)]

    return _create_random_euler_rotation


@pytest.fixture
def create_random_guest_obj(faker):
    async def _create_random_guest_obj(feature: Feature) -> Guest:
        return await Guest.create(name=faker.name(), feature_id=feature.id)

    return _create_random_guest_obj


@pytest.fixture
def create_random_feature_title() -> Callable:
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
def create_random_feature_slug() -> Callable:
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
) -> Callable:
    async def _create_random_feature_obj() -> Feature:
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


@pytest.fixture
def create_random_password():
    def _create_random_password():
        return randstr(
            min_length=7,
            max_length=20,
            min_tokens=1,
            max_tokens=1,
            uppercase_letters=True,
            lowercase_letters=True,
            punctuation=False,
            numbers=True,
        )

    return _create_random_password


@pytest.fixture
@pytest.mark.asyncio
async def create_random_user(faker, create_random_password):
    async def _create_random_user(password=None):
        user_create_db = UserDbCreate(
            hashed_password=get_password_hash(password or create_random_password()),
            email=faker.safe_email(),
        )
        return await User.create(**user_create_db.dict())

    return _create_random_user
