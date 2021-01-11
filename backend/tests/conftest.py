import contextlib
import os
import random
import socket
import uuid
from typing import Callable, List

import docker
import pytest
from asgi_lifespan import LifespanManager
from docker import DockerClient
from docker.models.containers import Container
from randstr_plus import randstr
from tortoise.contrib.test import finalizer as tortoise_test_finalizer
from tortoise.contrib.test import initializer as tortoise_test_initializer

from app.core import config
from app.core.db import get_tortoise_config
from app.core.security import get_password_hash
from app.main import get_app
from app.models.features import Feature
from app.models.guests import Guest
from app.models.users import User
from app.schemas.users import UserDbCreate

pytest_plugins = ["pytest_asgi_server"]


def get_base_dir():
    return config.Settings().BASE_DIR


@pytest.fixture
def settings():
    return config.get_settings()


@pytest.fixture(scope="session")
def docker_client() -> DockerClient:
    # return docker.from_env()
    return DockerClient(base_url="unix:///var/run/docker.sock")


@pytest.fixture(autouse=True)
def initialize_tortoise_orm(request):
    os.environ["DB_SUFFIX"] = "_test"
    tortoise_config: dict = get_tortoise_config()
    tortoise_test_initializer(
        modules=tortoise_config["apps"]["models"]["models"],
        db_url=tortoise_config["connections"]["default"],
        app_label="models",
    )
    request.addfinalizer(tortoise_test_finalizer)


@pytest.fixture(autouse=True)
def pg_container(docker_client) -> Container:
    pg_main_container = docker_client.containers.get("postgres")
    try:
        pg_test_container = docker_client.containers.run(
            image=pg_main_container.attrs["Config"]["Image"],
            environment=dict(
                POSTGRES_HOST_AUTH_METHOD="trust",
            ),
            detach=True,
        )
        yield pg_test_container
    finally:
        try:
            pg_test_container.remove(v=True, force=True)
        except Exception:
            pass


@pytest.fixture
@pytest.mark.asyncio
async def app():
    app = get_app()
    async with LifespanManager(app):
        yield app


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
            min_length=2,
            max_length=15,
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
    async def _create_random_user(email=None, password=None, name=None):
        user_create_db = UserDbCreate(
            name=name or faker.name(),
            hashed_password=get_password_hash(password or create_random_password()),
            email=email or faker.safe_email(),
        )
        return await User.create(**user_create_db.dict())

    return _create_random_user


@pytest.fixture
@pytest.mark.asyncio
async def create_random_feature(
    create_random_user,
    create_random_feature_title,
    create_random_feature_slug,
):
    async def _create_random_feature(
        title: str = None,
        slug: str = None,
        user_id: User = None,
        turn_duration: int = None,
    ):
        return await Feature.create(
            title=title or create_random_feature_title(),
            slug=slug or create_random_feature_slug(),
            user_id=user_id or (await create_random_user()).id,
            turn_duration=turn_duration or 30,
        )

    return _create_random_feature
