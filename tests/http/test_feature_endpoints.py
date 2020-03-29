from random import randint

import pytest
from async_asgi_testclient import TestClient

from app.models.features import Feature
from tests._utils.features import create_random_feature, create_random_feature_title
from tests._utils.guests import create_random_guest


@pytest.mark.asyncio
async def test_feature_http_post(app):
    path = "/api/features"
    async with TestClient(app) as client:
        data = {
            "title": create_random_feature_title(),
            "turn_duration": randint(0, 99),
        }
        response = await client.post(path, json=data)
        assert response.status_code == 200
        content = response.json()
        assert content["title"] == data["title"]
        assert content["turn_duration"] == data["turn_duration"]
        assert "id" in content
        feature = await Feature.get_or_none(pk=content["id"])
        assert feature
        assert feature.title == data["title"]
        assert feature.turn_duration == data["turn_duration"]


@pytest.mark.asyncio
async def test_feature_http_get(app):
    path = "/api/features/{feature_id}"
    async with TestClient(app) as client:
        random_feature = await create_random_feature()
        await create_random_guest(random_feature)
        await create_random_guest(random_feature)
        await create_random_guest(random_feature)
        response = await client.get(path.format(feature_id=random_feature.id))
        assert response.status_code == 200
        content = response.json()
        assert content["title"] == random_feature.title
        assert content["turn_duration"] == random_feature.turn_duration
