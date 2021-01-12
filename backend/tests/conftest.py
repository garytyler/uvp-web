import contextlib
import os
import random
import socket
import uuid
from random import randint
from typing import Callable, List, Optional

import pytest
from asgi_lifespan import LifespanManager
from docker import DockerClient
from docker.models.containers import Container
from httpx import AsyncClient
from randstr_plus import randstr
from tortoise.contrib.test import finalizer as tortoise_test_finalizer
from tortoise.contrib.test import initializer as tortoise_test_initializer

from app.api.dependencies.users import authenticate_user
from app.core import config
from app.core.db import get_tortoise_config

#     return _login_user
from app.core.security import create_access_token, get_password_hash
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
    return DockerClient(base_url="unix:///var/run/docker.sock")


@pytest.fixture(autouse=True)
def initialize_db(request):
    os.environ["DB_SUFFIX"] = f"_test_{uuid.uuid4()}"
    tortoise_config: dict = get_tortoise_config()
    tortoise_test_initializer(
        modules=tortoise_config["apps"]["models"]["models"],
        db_url=tortoise_config["connections"]["default"],
        app_label="models",
    )
    yield
    tortoise_test_finalizer()


@pytest.fixture
@pytest.mark.asyncio
async def app(initialize_db):
    app = get_app()
    async with LifespanManager(app):
        yield app


@pytest.fixture
def create_random_session_key() -> Callable:
    def _create_random_session_key():
        return randstr(
            min_length=32,
            max_length=32,
            min_tokens=1,
            max_tokens=1,
            uppercase_letters=True,
            lowercase_letters=True,
            numbers=True,
        )

    return _create_random_session_key


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
def create_random_feature_obj_title() -> Callable:
    def _create_random_feature_obj_title() -> str:
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

    return _create_random_feature_obj_title


@pytest.fixture
def create_random_feature_obj_slug() -> Callable:
    def _create_random_feature_obj_slug() -> str:
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

    return _create_random_feature_obj_slug


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
async def create_random_user_obj(faker, create_random_password):
    async def _create_random_user_obj(email=None, password=None, name=None):
        user_create_db = UserDbCreate(
            name=name or faker.name(),
            hashed_password=get_password_hash(password or create_random_password()),
            email=email or faker.safe_email(),
        )
        return await User.create(**user_create_db.dict())

    return _create_random_user_obj


@pytest.fixture
@pytest.mark.asyncio
async def get_auth_headers(app, create_random_user_obj, create_random_password):
    async def _get_auth_headers(
        user: Optional[User] = None, password: Optional[str] = None
    ):
        if user and password:
            user_password = password
            user_obj = user
        elif user or password:
            raise RuntimeError("Accepts both a user_obj and a password or neither.")
        else:
            user_password = create_random_password()
            user_obj = await create_random_user_obj(password=user_password)
        user_obj = await authenticate_user(email=user_obj.email, password=user_password)
        access_token = create_access_token(data={"sub": user_obj.email})
        return {"Authorization": f"Bearer {access_token}"}

    return _get_auth_headers


@pytest.fixture
@pytest.mark.asyncio
async def create_random_feature_obj(
    create_random_user_obj,
    create_random_feature_obj_title,
    create_random_feature_obj_slug,
):
    async def _create_random_feature_obj(
        title: str = None,
        slug: str = None,
        user_id: User = None,
        turn_duration: int = None,
    ):
        return await Feature.create(
            title=title or create_random_feature_obj_title(),
            slug=slug or create_random_feature_obj_slug(),
            user_id=user_id or (await create_random_user_obj()).id,
            turn_duration=turn_duration or 30,
        )

    return _create_random_feature_obj


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
async def initial_user_objs(initialize_db, create_random_user_obj):
    return [await create_random_user_obj() for _ in range(randint(5, 9))]


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
async def initial_feature_objs(
    initialize_db, initial_user_objs, create_random_feature_obj
):
    feature_objs = []
    for user_obj in initial_user_objs:
        for _ in range(randint(1, 9)):
            feature_objs.append(await create_random_feature_obj(user_id=user_obj.id))
    return feature_objs


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
async def initial_guest_objs(
    initialize_db, initial_feature_objs, create_random_guest_obj
):
    guest_objs = []
    for feature_obj in initial_feature_objs:
        guest_objs = [
            await create_random_guest_obj(feature=feature_obj)
            for _ in range(randint(1, 9))
        ]
    return guest_objs


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
async def fetch_initial_relations(
    initialize_db, initial_user_objs, initial_feature_objs, initial_guest_objs
):
    for i in initial_user_objs:
        await i.fetch_related("features")
    for i in initial_feature_objs:
        await i.fetch_related("user", "guests", "presenters")
    for i in initial_guest_objs:
        await i.fetch_related("feature")
