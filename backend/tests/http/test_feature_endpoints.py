from random import randint

import pytest
from app.models.features import Feature
from async_asgi_testclient import TestClient


@pytest.mark.asyncio
async def test_features_http_post_with_custom_slug(
    app, create_random_feature_slug, create_random_feature_title,
):
    path = "/api/features"
    async with TestClient(app) as client:
        data = {
            "title": create_random_feature_title(),
            "slug": create_random_feature_slug(),
            "turn_duration": randint(0, 99),
        }
        response = await client.post(path, json=data)
        assert response.status_code == 200
        content = response.json()
        assert content["title"] == data["title"]
        assert content["slug"] == data["slug"]
        assert content["turn_duration"] == data["turn_duration"]
        assert "id" in content
        feature = await Feature.get_or_none(pk=content["id"])
        assert feature
        assert feature.title == data["title"]
        assert feature.slug == data["slug"]
        assert feature.turn_duration == data["turn_duration"]


@pytest.mark.asyncio
async def test_features_http_post_without_custom_slug(app, create_random_feature_title):
    path = "/api/features"
    async with TestClient(app) as client:
        data = {"title": create_random_feature_title(), "turn_duration": randint(0, 99)}
        response = await client.post(path, json=data)
        assert response.status_code == 200
        content = response.json()
        assert content["slug"].strip()
        assert content["title"] == data["title"]
        assert content["turn_duration"] == data["turn_duration"]
        assert "id" in content
        feature = await Feature.get_or_none(pk=content["id"])
        assert feature
        assert feature.title == data["title"]
        assert feature.turn_duration == data["turn_duration"]


@pytest.mark.asyncio
async def test_features_http_get_by_id(
    app, create_random_feature_obj, create_random_guest_obj
):
    path = "/api/features/{id}"
    async with TestClient(app) as client:
        random_feature = await create_random_feature_obj()
        await create_random_guest_obj(random_feature)
        await create_random_guest_obj(random_feature)
        await create_random_guest_obj(random_feature)
        response = await client.get(path.format(id=random_feature.id))
        assert response.status_code == 200
        content = response.json()
        assert content["title"] == random_feature.title
        assert content["turn_duration"] == random_feature.turn_duration


@pytest.mark.asyncio
async def test_features_http_get_by_slug(
    app, create_random_feature_obj, create_random_guest_obj
):
    path = "/api/features/{slug}"
    async with TestClient(app) as client:
        random_feature = await create_random_feature_obj()
        await create_random_guest_obj(random_feature)
        await create_random_guest_obj(random_feature)
        await create_random_guest_obj(random_feature)
        response = await client.get(path.format(slug=random_feature.slug))
        assert response.status_code == 200
        content = response.json()
        assert content["title"] == random_feature.title
        assert content["turn_duration"] == random_feature.turn_duration


@pytest.mark.asyncio
async def test_features_http_get_all(app, create_random_feature_obj):
    path = "/api/features"
    async with TestClient(app) as client:
        features = [await create_random_feature_obj() for _ in range(5)]
        response = await client.get(path)
        assert response.status_code == 200
        content = response.json()
        assert [i["title"] for i in content] == [i.title for i in features]


@pytest.mark.asyncio
async def test_features_http_delete(app, create_random_feature_obj):
    path = "/api/features/{id}"
    async with TestClient(app) as client:
        features = [await create_random_feature_obj() for _ in range(5)]
        response = await client.delete(path.format(id=features[3].id))
        assert response.status_code == 200
        assert response.json() == 1
        response = await client.delete(path.format(id=features[3].id))
        assert response.status_code == 404
