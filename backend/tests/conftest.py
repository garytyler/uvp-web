import contextlib
import random
import socket
from typing import Callable, List, Optional

import pytest
from docker import DockerClient
from docker.models.containers import Container
from pydantic import PostgresDsn
from randstr_plus import randstr

from app.api.dependencies.users import authenticate_user
from app.core import config, db
from app.core.security import create_access_token, get_password_hash
from app.models.features import Feature
from app.models.guests import Guest
from app.models.users import User
from app.schemas.users import UserDbCreate

pytest_plugins = ["pytest_asgi_server"]


def get_base_dir():
    return config.Settings().BASE_DIR


@pytest.fixture(scope="session")
def settings():
    return config.get_settings()


@pytest.fixture(scope="session")
def docker_client() -> DockerClient:
    return DockerClient(base_url="unix:///var/run/docker.sock")


# Database setup


@pytest.fixture
def pg_test_container_name(settings, worker_id):
    return f"{settings.POSTGRES_DB}-test-{worker_id}"


@pytest.fixture
def pg_test_db_url(settings, pg_test_container_name) -> PostgresDsn:
    return PostgresDsn.build(
        scheme="postgres",
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=pg_test_container_name,
        path=f"/{settings.POSTGRES_DB.lstrip('/')}",
    )


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
async def pg_container(
    monkeypatch,
    docker_client,
    settings,
    pg_test_db_url,
    pg_test_container_name,
) -> Container:

    _tortoise_config = db.get_tortoise_config()

    def get_test_tortoise_config():
        nonlocal _tortoise_config
        _tortoise_config["connections"]["default"] = pg_test_db_url
        return _tortoise_config

    monkeypatch.setattr(db, "get_tortoise_config", get_test_tortoise_config)

    pg_prod_container = docker_client.containers.get("postgres")
    pg_test_container = docker_client.containers.run(
        name=pg_test_container_name,
        image=pg_prod_container.image,
        command=["postgres", "-c", "log_statement=all"],
        environment=dict(
            POSTGRES_HOST=pg_test_container_name,
            POSTGRES_USER=settings.POSTGRES_USER,
            POSTGRES_DB=settings.POSTGRES_DB,
            POSTGRES_HOST_AUTH_METHOD="trust",
        ),
        network=pg_prod_container.attrs["HostConfig"]["NetworkMode"],
        publish_all_ports=True,
        detach=True,
        remove=True,
        auto_remove=True,
    )
    try:
        while True:
            response = pg_test_container.exec_run(
                [
                    "pg_isready",
                    f"--host={pg_test_container_name}",
                    f"--dbname={settings.POSTGRES_DB}",
                    f"--username={settings.POSTGRES_USER}",
                ]
            )
            if response.exit_code == 0:
                break
        yield pg_test_container
    finally:
        pg_test_container.remove(v=True, force=True)


# Factory fixtures


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
