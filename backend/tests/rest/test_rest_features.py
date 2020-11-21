import uuid
from random import randint

import pytest
from httpx import AsyncClient

from app.models.features import Feature
from app.schemas.features import FeatureOut


@pytest.mark.asyncio
async def test_rest_features_post_with_custom_slug(
    app,
    create_random_feature_slug,
    create_random_feature_title,
):
    path = "/api/features"
    async with AsyncClient(app=app, base_url="http://test") as client:
        data = {
            "title": create_random_feature_title(),
            "slug": create_random_feature_slug(),
            "turn_duration": randint(0, 99),
        }
        r = await client.post(path, json=data)
        assert r.status_code == 200
        content = r.json()
        assert content["title"] == data["title"]
        assert content["slug"] == data["slug"]
        assert content["turn_duration"] == data["turn_duration"]
        assert "id" in content
        feature = await Feature.get_or_none(pk=content["id"])
        assert feature
        assert feature.title == data["title"]
        assert feature.slug == data["slug"]
        assert feature.turn_duration == data["turn_duration"]
        assert FeatureOut(**content)


@pytest.mark.asyncio
async def test_rest_features_post_without_custom_slug(app, create_random_feature_title):
    path = "/api/features"
    async with AsyncClient(app=app, base_url="http://test") as client:
        data = {"title": create_random_feature_title(), "turn_duration": randint(0, 99)}
        r = await client.post(path, json=data)
        assert r.status_code == 200
        content = r.json()
        assert content["slug"].strip()
        assert content["title"] == data["title"]
        assert content["turn_duration"] == data["turn_duration"]
        assert "id" in content
        feature = await Feature.get_or_none(pk=content["id"])
        assert feature
        assert feature.title == data["title"]
        assert feature.turn_duration == data["turn_duration"]
        assert FeatureOut(**content)


@pytest.mark.asyncio
async def test_rest_features_get_by_id(
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
async def test_rest_features_get_by_slug(
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
async def test_features_http_get_all(app, create_random_feature_obj):
    path = "/api/features"
    async with AsyncClient(app=app, base_url="http://test") as client:
        features = [await create_random_feature_obj() for _ in range(5)]
        r = await client.get(path)
        assert r.status_code == 200
        content = r.json()

        print(content[0])
        assert [FeatureOut(**i) for i in content]
        assert [i["title"] for i in content] == [i.title for i in features]


@pytest.mark.asyncio
async def test_features_http_delete_existing_succeeds(app, create_random_feature_obj):
    path = "/api/features/{id}"
    async with AsyncClient(app=app, base_url="http://test") as client:
        features = [await create_random_feature_obj() for _ in range(5)]
        r = await client.delete(path.format(id=features[3].id))
        assert r.status_code == 200


@pytest.mark.asyncio
async def test_features_http_delete_nonexisting_raises(app, create_random_feature_obj):
    path = "/api/features/{id}"
    async with AsyncClient(app=app, base_url="http://test") as client:
        r = await client.delete(path.format(id=uuid.uuid4()))
        assert r.status_code == 404
