import os
import uuid
from random import randint

import pytest
from asgi_lifespan import LifespanManager
from tortoise.contrib.test import finalizer as tortoise_test_finalizer
from tortoise.contrib.test import initializer as tortoise_test_initializer

from app.core.db import get_tortoise_config
from app.main import get_app


@pytest.fixture(autouse=True)
def db_suffix():
    suffix = f"_test_{uuid.uuid4()}"
    os.environ["DB_SUFFIX"] = suffix
    yield suffix
    del os.environ["DB_SUFFIX"]


@pytest.fixture()
def initialize_db():
    tortoise_config: dict = get_tortoise_config()
    tortoise_test_initializer(
        modules=tortoise_config["apps"]["models"]["models"],
        db_url=tortoise_config["connections"]["default"],
        app_label="models",
    )
    yield
    tortoise_test_finalizer()


@pytest.fixture()
@pytest.mark.asyncio
async def app():
    app = get_app()
    async with LifespanManager(app):
        yield app


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
