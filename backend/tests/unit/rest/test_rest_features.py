import uuid
from random import randint

import pytest
from httpx import AsyncClient

from app.models.features import Feature
from app.schemas.features import FeatureOut


@pytest.mark.asyncio
async def test_create_with_custom_slug(
    app,
    create_random_feature_obj_slug,
    create_random_feature_obj_title,
    create_random_user_obj,
    get_auth_headers,
):
    user_obj = await create_random_user_obj()
    path = "/api/features"
    async with AsyncClient(app=app, base_url="http://test") as client:
        data = {
            "title": create_random_feature_obj_title(),
            "slug": create_random_feature_obj_slug(),
            "turn_duration": randint(0, 99),
            "user_id": str(user_obj.id),
        }
        r = await client.post(path, json=data, headers=await get_auth_headers())
        assert r.status_code == 200
        content = r.json()
        assert content["title"] == data["title"]
        assert content["slug"] == data["slug"]
        assert content["turn_duration"] == data["turn_duration"]
        assert content["user_id"] == data["user_id"]
        assert "id" in content
        feature = await Feature.get_or_none(pk=content["id"])
        assert feature
        assert feature.title == data["title"]
        assert feature.slug == data["slug"]
        assert feature.turn_duration == data["turn_duration"]
        assert str(feature.user_id) == data["user_id"]
        assert FeatureOut(**content)


@pytest.mark.asyncio
async def test_create_without_custom_slug(
    app, create_random_user_obj, create_random_feature_obj_title, get_auth_headers
):
    user_obj = await create_random_user_obj()
    path = "/api/features"
    async with AsyncClient(app=app, base_url="http://test") as client:
        data = {
            "title": create_random_feature_obj_title(),
            "turn_duration": randint(0, 99),
            "user_id": str(user_obj.id),
        }
        r = await client.post(path, json=data, headers=await get_auth_headers())
        assert r.status_code == 200
        content = r.json()
        assert content["slug"].strip()
        assert content["title"] == data["title"]
        assert content["turn_duration"] == data["turn_duration"]
        assert content["user_id"] == data["user_id"]
        assert "id" in content
        feature = await Feature.get_or_none(pk=content["id"])
        assert feature
        assert feature.title == data["title"]
        assert feature.turn_duration == data["turn_duration"]
        assert str(feature.user_id) == data["user_id"]
        assert FeatureOut(**content)


@pytest.mark.asyncio
async def test_get_single_by_id(
    app, create_random_feature_obj, create_random_guest_obj
):
    path = "/api/features/{id}"
    async with AsyncClient(app=app, base_url="http://test") as client:
        random_feature = await create_random_feature_obj()
        await create_random_guest_obj(random_feature)
        await create_random_guest_obj(random_feature)
        await create_random_guest_obj(random_feature)
        r = await client.get(path.format(id=random_feature.id))
        assert r.status_code == 200
        content = r.json()
        assert content["title"] == random_feature.title
        assert content["turn_duration"] == random_feature.turn_duration
        assert FeatureOut(**content)


@pytest.mark.asyncio
async def test_get_single_by_slug(
    app, create_random_feature_obj, create_random_guest_obj
):
    path = "/api/features/{slug}"
    async with AsyncClient(app=app, base_url="http://test") as client:
        random_feature = await create_random_feature_obj()
        await create_random_guest_obj(random_feature)
        await create_random_guest_obj(random_feature)
        await create_random_guest_obj(random_feature)
        r = await client.get(path.format(slug=random_feature.slug))
        assert r.status_code == 200
        content = r.json()
        assert content["title"] == random_feature.title
        assert content["turn_duration"] == random_feature.turn_duration
        assert FeatureOut(**content)


@pytest.mark.asyncio
async def test_get_list_by_user_id_query(app, initial_user_objs, get_auth_headers):
    path = "/api/features"
    async with AsyncClient(app=app, base_url="http://test") as client:
        user_obj = initial_user_objs[randint(0, len(initial_user_objs) - 1)]
        r = await client.get(
            path, params=dict(user_id=user_obj.id), headers=await get_auth_headers()
        )
        assert r.status_code == 200
        content = r.json()
        assert content
        assert len(content) == len(user_obj.features)
        for n, feature_obj in enumerate(user_obj.features):
            assert content[n]["title"] == feature_obj.title
            assert content[n]["turn_duration"] == feature_obj.turn_duration


@pytest.mark.asyncio
async def test_get_list_all(app, initial_feature_objs, get_auth_headers):
    path = "/api/features"
    async with AsyncClient(app=app, base_url="http://test") as client:
        r = await client.get(path, headers=await get_auth_headers())
        assert r.status_code == 200
        content = r.json()
        assert content
        assert len(content) == len(initial_feature_objs)
        assert [i["title"] for i in content] == [i.title for i in initial_feature_objs]


@pytest.mark.asyncio
async def test_delete_existing_succeeds(
    app, create_random_feature_obj, get_auth_headers
):
    path = "/api/features/{id}"
    async with AsyncClient(app=app, base_url="http://test") as client:
        features = [await create_random_feature_obj() for _ in range(5)]
        r = await client.delete(
            path.format(id=features[3].id), headers=await get_auth_headers()
        )
        assert r.status_code == 200


@pytest.mark.asyncio
async def test_delete_nonexisting_raises(app, get_auth_headers):
    path = "/api/features/{id}"
    async with AsyncClient(app=app, base_url="http://test") as client:
        r = await client.delete(
            path.format(id=uuid.uuid4()), headers=await get_auth_headers()
        )
        assert r.status_code == 404
